import pdfplumber
import pandas as pd
import io
from typing import Optional, List


class TenderParserService:

    def parse_pdf(self, file_bytes: bytes) -> str:
        """
        Extract text from a PDF tender document.

        Strategy for Samruk-Kazyna PDFs (which have Kazakh + Russian pages):
        1. Try structured table extraction (most precise)
        2. If tables not found, locate the Russian section in raw text
           ("Номер лота" marks the start of the Russian lot table)
        3. Always put the relevant content FIRST so it lands within the LLM's
           character window.
        """
        all_page_texts: List[str] = []
        all_table_sections: List[str] = []

        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                # Structured table extraction
                for table in (page.extract_tables() or []):
                    fmt = self._format_table(table)
                    if fmt:
                        all_table_sections.append(fmt)

                # Raw text
                raw = page.extract_text() or ""
                if raw.strip():
                    all_page_texts.append(raw)

        full_raw = "\n\n".join(all_page_texts)

        # ── Case 1: structured Samruk table found ─────────────────────────
        samruk = [t for t in all_table_sections if "ТЕНДЕРНЫЕ ЛОТЫ" in t]
        if samruk:
            # Prepend procurement title extracted from raw text (first ~300 chars)
            preamble = full_raw[:300]
            return preamble + "\n\n" + "\n\n".join(samruk)

        # ── Case 2: no structured table — find the Russian section in raw text
        # The Russian version contains "Номер лота" (Kazakh has "Лот нөмірі")
        russian_start = full_raw.find("Номер лота")
        if russian_start == -1:
            # Try alternate Russian marker
            russian_start = full_raw.find("Наименование и краткая")
        if russian_start > 0:
            preamble = full_raw[:400]
            russian_section = full_raw[russian_start:]
            return preamble + "\n\n" + russian_section

        # ── Case 3: plain fallback
        return full_raw

    def _format_table(self, table: list) -> str:
        """
        Format a pdfplumber table into labeled key-value text.
        Searches the first 4 rows for Samruk-Kazyna column headers.
        """
        if not table or len(table) < 2:
            return ""

        # Find the row that contains recognizable Samruk column headers
        header_idx = -1
        for i, row in enumerate(table[:4]):
            row_text = " ".join(
                str(c or "").replace("\n", " ").lower() for c in row
            )
            if any(kw in row_text for kw in [
                "номер лота", "наименование", "планируемая сумма",
                "место поставки", "требуемый срок"
            ]):
                header_idx = i
                break

        if header_idx == -1:
            # Generic table — pipe-separated
            lines = []
            for row in table:
                row_str = " | ".join(
                    str(c or "").replace("\n", " ").strip() for c in row if c
                )
                if row_str.strip():
                    lines.append(row_str)
            return "\n".join(lines)

        # Samruk-format table
        header = [
            str(c or "").replace("\n", " ").strip()
            for c in table[header_idx]
        ]
        lines = ["=== ТЕНДЕРНЫЕ ЛОТЫ (Самрук-Казына / Госзакупки) ==="]

        for row in table[header_idx + 1:]:
            cells = [str(c or "").replace("\n", " ").strip() for c in row]
            if not any(cells):
                continue
            entry = []
            for h, v in zip(header, cells):
                if h and v:
                    entry.append(f"  {h}: {v}")
            if entry:
                lines.append("\n".join(entry))
                lines.append("")  # blank line between lots

        return "\n".join(lines)

    def parse_excel(self, file_bytes: bytes, filename: str) -> str:
        xls = pd.ExcelFile(io.BytesIO(file_bytes))
        parts = []
        for sheet_name in xls.sheet_names:
            df = xls.parse(sheet_name)
            parts.append(f"Sheet: {sheet_name}")
            parts.append(df.to_string(index=False, max_rows=100))
        return "\n\n".join(parts)

    def parse(self, file_bytes: bytes, filename: str) -> str:
        if filename.lower().endswith(".pdf"):
            return self.parse_pdf(file_bytes)
        elif filename.lower().endswith((".xlsx", ".xls")):
            return self.parse_excel(file_bytes, filename)
        else:
            return file_bytes.decode("utf-8", errors="replace")
