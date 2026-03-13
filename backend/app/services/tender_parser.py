import re
import pdfplumber
import pandas as pd
import io
from typing import Optional, List

# Full name → abbreviation for Kazakh petroleum industry customers
COMPANY_SHORTCUTS: dict = {
    "АТЫРАУСКИЙ НЕФТЕПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД": "АНПЗ",
    "АТЫРАУСКИЙ НПЗ": "АНПЗ",
    "АТЫРАУ НПЗ": "АНПЗ",
    "ПАВЛОДАРСКИЙ НЕФТЕХИМИЧЕСКИЙ ЗАВОД": "ПНХЗ",
    "ПАВЛОДАРСКИЙ НХЗ": "ПНХЗ",
    "КАЗАХСТАН ПЕТРОКЕМИКАЛ ИНДАСТРИЗ": "KPI",
    "KAZAKHSTAN PETROCHEMICAL INDUSTRIES": "KPI",
    "МАНГИСТАУСКИЙ НЕФТЕПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД": "МНПЗ",
    "МАНГИСТАУСКИЙ НПЗ": "МНПЗ",
    "ШЫМКЕНТСКИЙ НЕФТЕПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД": "ПКОП",
    "PETRO KAZAKHSTAN OIL PRODUCTS": "ПКОП",
}


def shorten_company(name: str) -> str:
    if not name:
        return name
    upper = name.upper()
    for long_name, short in COMPANY_SHORTCUTS.items():
        if long_name in upper:
            return short
    return name


def extract_city(location_text: str) -> str:
    if not location_text or len(location_text.strip()) <= 30:
        return location_text.strip()

    text = location_text.replace("\n", " ")

    m = re.search(r'город\s+([А-ЯЁа-яёA-Za-z][А-ЯЁа-яё\-A-Za-z]*)', text, re.IGNORECASE)
    if m:
        return m.group(1).capitalize()

    m = re.search(r'г\.\s*([А-ЯЁа-яёA-Za-z][А-ЯЁа-яё\-A-Za-z]*)', text, re.IGNORECASE)
    if m:
        return m.group(1).capitalize()

    parts = [p.strip() for p in text.split(",") if p.strip()]
    for part in parts:
        if re.search(r'\bобласть\b|\bрайон\b|КАЗАХСТАН|KAZAKHSTAN', part, re.IGNORECASE):
            continue
        if re.match(r'^[А-ЯЁA-Z][а-яёa-z\-]{3,}$', part):
            return part

    return location_text.strip()


class TenderParserService:

    def _extract_procurement_title(self, raw_text: str) -> str:
        for marker in ["(наименование закупки)", "(сатып алу атауы)"]:
            idx = raw_text.lower().find(marker.lower())
            if idx == -1:
                continue
            before = raw_text[:idx].strip()
            lines = [ln.strip() for ln in before.split("\n") if ln.strip()]
            if lines:
                return lines[-1]
        return ""

    def parse_pdf(self, file_bytes: bytes) -> str:
        all_page_texts: List[str] = []
        all_table_sections: List[str] = []

        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                for table in (page.extract_tables() or []):
                    fmt = self._format_table(table)
                    if fmt:
                        all_table_sections.append(fmt)

                raw = page.extract_text() or ""
                if raw.strip():
                    all_page_texts.append(raw)

        full_raw = "\n\n".join(all_page_texts)

        procurement_title = self._extract_procurement_title(full_raw)
        title_header = (
            f"НАИМЕНОВАНИЕ ЗАКУПКИ: {procurement_title}\n\n"
            if procurement_title else ""
        )

        samruk = [t for t in all_table_sections if "ТЕНДЕРНЫЕ ЛОТЫ" in t]
        if samruk:
            preamble = full_raw[:300]
            return title_header + preamble + "\n\n" + "\n\n".join(samruk)

        russian_start = full_raw.find("Номер лота")
        if russian_start == -1:
            russian_start = full_raw.find("Наименование и краткая")
        if russian_start > 0:
            preamble = full_raw[:400]
            russian_section = full_raw[russian_start:]
            return title_header + preamble + "\n\n" + russian_section

        return title_header + full_raw

    def _format_table(self, table: list) -> str:
        if not table or len(table) < 2:
            return ""

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
            lines = []
            for row in table:
                row_str = " | ".join(
                    str(c or "").replace("\n", " ").strip() for c in row if c
                )
                if row_str.strip():
                    lines.append(row_str)
            return "\n".join(lines)

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
                lines.append("")

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
