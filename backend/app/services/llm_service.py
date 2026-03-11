import os
import json
import httpx
from typing import Dict, Optional

# Config keys as fallback (in case env var is empty)
try:
    from app.config import settings as _cfg
    _GEMINI_FALLBACK = _cfg.GEMINI_API_KEY
    _GROQ_FALLBACK = _cfg.GROQ_API_KEY
except Exception:
    _GEMINI_FALLBACK = ""
    _GROQ_FALLBACK = ""

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or _GEMINI_FALLBACK
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or _GROQ_FALLBACK

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Real AVC GROUP company profile for LLM context calibration
AVC_COMPANY_CONTEXT = """
AVC GROUP — EPC-подрядчик по ремонту нефтеперерабатывающих заводов в Казахстане.

КАДРОВЫЙ ПОТЕНЦИАЛ:
- Квалифицированный ИТР: 150+ человек
- Рабочий персонал в штате: 1000+ человек

РЕАЛИЗОВАННЫЕ ПРОЕКТЫ (для калибровки расчётов):

1. Капитальный ремонт МНПЗ (23 установки, 8 производств):
   - Задействовано: 1400 специалистов (ИТР 83 + рабочие 1292), 50 ед. техники
   - Трудозатраты: 381 308 чел/часов
   - Выполнено: замена пароперегревателя, ёмкостей, сепараторов, 95 теплообменников,
     166 ед. колонного оборудования, 30 технологических печей, 1400+ ТРО, 46 ПКУ

2. ППР АНПЗ — 24 установки (1-й цикл):
   - Задействовано: 1695 специалистов, 69 ед. техники
   - Трудозатраты: 985 322 чел/часов
   - Выполнено: CCR, ФКК (реакторы R-104, R-105), АВТ-2 (теплообменники Т-6,Т-23,Т-26,Т-28),
     компрессоры K-0251, K-1302, K-0101, 20-C-001 — одновременный ремонт

3. ППР АНПЗ — 24 установки (2-й цикл, 31 рабочий день):
   - Задействовано: 2220 специалистов, 95 ед. техники (26 кранов + 12 ДВС/длинномеры + 8 экскаваторов)
   - Трудозатраты: 505 153 чел/часов
   - Сварных стыков: 2717; прокладок/фланцев: 20 286 шт; КИП и ЗРА: 3 070 комплектов

4. Модернизация КС КТ-1 АНПЗ (июнь 2023 — июль 2025):
   - Замена компрессоров Hitachi, АСУ ТП, антипомпажная защита
   - Прогнозируемая экономия > 120 млн тенге/год

ОРИЕНТИРЫ ДЛЯ РАСЧЁТА (единичный объект, не весь завод):
- Ремонт одного резервуара РВС 10 000 м³: ~28 специалистов, ~8 ед. техники, ~90 дней
- Ремонт теплообменника: ~10 специалистов, ~2 ед. техники, ~45 дней
- Ремонт насоса: ~3–5 специалистов, ~1 ед. техники, ~30 дней
- Замена участка трубопровода 100–200 м: ~13 специалистов, ~1 ед. техники, ~60 дней
"""


class LLMService:

    async def extract_tender_scope(self, tender_text: str) -> Dict:
        """
        Extract lot data from a Samruk-Kazyna / Goszakup tender document.
        The document is bilingual (Kazakh + Russian) — use only Russian content.

        The table columns are:
          Номер лота | Наименование и краткая характеристика |
          Дополнительная характеристика | Кол-во | Ед. изм. |
          Планируемая сумма без НДС | Место поставки | Требуемый срок
        """
        prompt = f"""You are parsing a Kazakhstani procurement tender (Самрук-Казына / Госзакупки).
The document is bilingual. Use ONLY the Russian text (not Kazakh).

The document contains a table with these columns:
- Номер лота
- Наименование и краткая характеристика  (main lot description)
- Дополнительная характеристика           (additional description / technical spec)
- Кол-во                                  (quantity)
- Ед. изм.                                (unit of measure)
- Планируемая сумма без НДС               (planned amount excl. VAT, in KZT)
- Место поставки товара/выполнения работ  (delivery/work location)
- Требуемый срок                          (required deadline)

The procurement title (наименование закупки) appears above the table.

Return ONLY a valid JSON:
{{
  "title": "Full project name — use Наименование и краткая характеристика of the first lot",
  "work_type": "Short work category in Russian (e.g. 'Капитальный ремонт резервуара')",
  "equipment_list": ["list of equipment or facilities mentioned"],
  "location": "Location from Место поставки field",
  "volume_description": "Short Russian summary of scope",
  "deadline_days": integer (from Требуемый срок — convert calendar days to integer; default 90),
  "estimated_budget_kzt": number (sum of Планируемая сумма без НДС across all lots),
  "lots": [
    {{
      "lot_number": "lot number string",
      "name": "Наименование и краткая характеристика (full text)",
      "description": "Дополнительная характеристика (full text)",
      "quantity": number,
      "unit": "Ед. изм. string",
      "planned_amount_kzt": number,
      "location": "Место поставки full text",
      "deadline": "Требуемый срок full text as written"
    }}
  ]
}}

TENDER TEXT:
{tender_text[:8000]}

Respond with ONLY the JSON object. No markdown fences. No explanation."""

        response = await self._call_gemini(prompt)
        if not response:
            response = await self._call_groq(prompt)

        try:
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except Exception:
            return {
                "title": "Тендер на ремонт оборудования",
                "work_type": "Ремонт оборудования",
                "equipment_list": [],
                "location": "Не указано",
                "volume_description": tender_text[:200],
                "deadline_days": 90,
                "estimated_budget_kzt": 0,
                "lots": []
            }

    async def generate_resource_plan(
        self,
        parsed_scope: Dict,
        similar_projects: list,
        company_context: str = ""
    ) -> Dict:
        """
        Generate a resource plan and calculate workforce summary numbers.
        Returns specialists_count, equipment_count, total_manhours as calculated integers.
        """
        similar_text = ""
        for i, sp in enumerate(similar_projects, 1):
            proj = sp["project"]
            duration = "N/A"
            if proj.start_date and proj.planned_end_date:
                duration = (proj.planned_end_date - proj.start_date).days
            resources_sample = ", ".join([r.name for r in proj.resources[:6]])
            similar_text += (
                f"\nReference Project {i} (similarity {sp['similarity_score']:.0%}):\n"
                f"  Name: {proj.name}\n"
                f"  Budget: {proj.total_budget:,.0f} KZT  |  Spent: {proj.spent_amount:,.0f} KZT\n"
                f"  Duration: {duration} days\n"
                f"  Resources: {resources_sample}\n"
            )

        lots_text = ""
        for lot in parsed_scope.get("lots", []):
            lots_text += (
                f"  Лот {lot.get('lot_number','')}: {lot.get('name','')}\n"
                f"    Доп. характ.: {lot.get('description','')}\n"
                f"    Сумма: {lot.get('planned_amount_kzt', 0):,.0f} KZT  |  "
                f"Срок: {lot.get('deadline','')}\n"
            )

        budget = parsed_scope.get("estimated_budget_kzt", 0)
        deadline = parsed_scope.get("deadline_days", 90)

        ctx = company_context or AVC_COMPANY_CONTEXT
        prompt = f"""You are a senior estimator at AVC Group — an EPC company specialising in oil refinery repairs in Kazakhstan.

COMPANY PROFILE (AVC GROUP):
{ctx}

TENDER SCOPE:
- Title: {parsed_scope.get('title', parsed_scope.get('work_type', ''))}
- Work type: {parsed_scope.get('work_type', '')}
- Equipment: {', '.join(parsed_scope.get('equipment_list', []))}
- Location: {parsed_scope.get('location', '')}
- Volume: {parsed_scope.get('volume_description', '')}
- Deadline: {deadline} calendar days
- Tender budget: {budget:,.0f} KZT
{lots_text}
SIMILAR COMPLETED PROJECTS (use for calibration):
{similar_text if similar_text else "No historical data — use industry norms for Kazakhstan 2024-2025."}

Return ONLY valid JSON (no fences):
{{
  "resources": [
    {{
      "resource_type": "labor|material|equipment",
      "name": "Name in Russian",
      "quantity": number,
      "unit": "чел/дн | шт | м | кг | маш/см | комплект",
      "unit_cost": number (KZT),
      "total_cost": number (KZT),
      "notes": "brief justification"
    }}
  ],
  "tasks": [
    {{
      "name": "Task name in Russian",
      "description": "brief description in Russian",
      "duration_days": number,
      "priority": "high|medium|low",
      "assigned_role": "role in Russian"
    }}
  ],
  "estimated_total_cost": number (KZT, should be close to tender budget {budget:,.0f}),
  "estimated_duration_days": {deadline},
  "specialists_count": integer (REQUIRED: total number of workers = sum of all labor resource quantities),
  "equipment_count": integer (REQUIRED: total machinery units = sum of all equipment resource quantities),
  "total_manhours": integer (REQUIRED: specialists_count × {deadline} days × 8 hours/day),
  "reasoning": "2 sentences in Russian"
}}

Rules:
- 6-12 resources, 4-8 tasks
- Scale workforce to this SINGLE OBJECT tender (not full plant turnaround)
- Use the "ОРИЕНТИРЫ ДЛЯ РАСЧЁТА" benchmarks from company profile to set realistic headcount
- For labor: unit=чел/дн, unit_cost = daily rate 10 000–25 000 KZT
- specialists_count MUST equal the INTEGER sum of quantity for all labor resources
- equipment_count MUST equal the INTEGER sum of quantity for all equipment resources
- total_manhours = specialists_count × {deadline} × 8"""

        response = await self._call_gemini(prompt)
        if not response:
            response = await self._call_groq(prompt)

        try:
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            result = json.loads(clean.strip())

            # Recalculate workforce numbers server-side to ensure correctness
            resources = result.get("resources", [])
            specialists = int(sum(
                r.get("quantity", 0)
                for r in resources if r.get("resource_type") == "labor"
            ))
            equipment = int(sum(
                r.get("quantity", 0)
                for r in resources if r.get("resource_type") == "equipment"
            ))
            duration = result.get("estimated_duration_days", deadline)
            manhours = specialists * duration * 8

            result["specialists_count"] = specialists
            result["equipment_count"] = equipment
            result["total_manhours"] = manhours

            return result
        except Exception:
            return {
                "resources": [], "tasks": [],
                "estimated_total_cost": 0,
                "estimated_duration_days": deadline,
                "specialists_count": 0,
                "equipment_count": 0,
                "total_manhours": 0,
                "reasoning": "Parse error — check API keys and network connectivity"
            }

    async def _call_gemini(self, prompt: str) -> Optional[str]:
        if not GEMINI_API_KEY:
            return None
        try:
            async with httpx.AsyncClient(timeout=45) as client:
                resp = await client.post(
                    f"{GEMINI_URL}?key={GEMINI_API_KEY}",
                    json={"contents": [{"parts": [{"text": prompt}]}]}
                )
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return None

    async def _call_groq(self, prompt: str) -> Optional[str]:
        if not GROQ_API_KEY:
            return None
        try:
            async with httpx.AsyncClient(timeout=45) as client:
                resp = await client.post(
                    GROQ_URL,
                    headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 3000
                    }
                )
                data = resp.json()
                return data["choices"][0]["message"]["content"]
        except Exception:
            return None
