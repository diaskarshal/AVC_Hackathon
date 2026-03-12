import os
import json
import httpx
import asyncio
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

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

"""

class LLMError(Exception):
    """Raised when both LLM providers fail after retries."""
    pass


class LLMService:

    MAX_RETRIES = 2
    RETRY_DELAY = 1.5  # seconds

    def _clean_json(self, text: str) -> str:
        """Strip markdown fences and whitespace from LLM JSON response."""
        clean = text.strip()
        if clean.startswith("```"):
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
        if clean.endswith("```"):
            clean = clean[:-3]
        return clean.strip()

    async def extract_tender_scope(self, tender_text: str) -> Dict:
        """
        Extract lot data from a Samruk-Kazyna / Goszakup tender document.
        The document is bilingual (Kazakh + Russian) — use only Russian content.
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
- Место поставки товара/выполнения работ  (delivery/work location — extract ONLY the city name, e.g. "Атырау")
- Требуемый срок                          (required deadline)

The document header also contains the ordering organization (Заказчик / Наименование заказчика).
Extract its full name for the "customer" field.

The procurement name appears at the very TOP of the text, labelled:
  НАИМЕНОВАНИЕ ЗАКУПКИ: <actual project name here>

⚠️ Use that labelled value for "title".
The column "Наименование и краткая характеристика" in the lot table contains
a GENERIC CATEGORY CODE (e.g. "Работы по ремонту/модернизации нефтеперерабатывающих
установок...") — do NOT use it for "title". Use ONLY the НАИМЕНОВАНИЕ ЗАКУПКИ line.

Return ONLY a valid JSON:
{{
  "title": "Value from 'НАИМЕНОВАНИЕ ЗАКУПКИ:' header line (e.g. 'Работы по ремонту печи П-1')",
  "work_type": "Short work category in Russian (e.g. 'Капитальный ремонт резервуара')",
  "equipment_list": ["list of equipment or facilities mentioned"],
  "customer": "Full name of the ordering organization (Заказчик) from the document header",
  "location": "ONLY the city name from Место поставки (e.g. 'Атырау', 'Павлодар', 'Шымкент')",
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

        response = await self._call_with_fallback(prompt)
        if not response:
            logger.warning("Both LLM providers failed for scope extraction")
            return {
                "title": "Тендер на ремонт оборудования",
                "work_type": "Ремонт оборудования",
                "equipment_list": [],
                "location": "Не указано",
                "volume_description": tender_text[:200],
                "deadline_days": 90,
                "estimated_budget_kzt": 0,
                "lots": [],
                "_llm_error": "Не удалось подключиться к AI-сервису. Проверьте API-ключи и сетевое подключение."
            }

        try:
            return json.loads(self._clean_json(response))
        except (json.JSONDecodeError, IndexError) as e:
            logger.error(f"Failed to parse scope JSON: {e}, raw={response[:200]}")
            return {
                "title": "Тендер на ремонт оборудования",
                "work_type": "Ремонт оборудования",
                "equipment_list": [],
                "location": "Не указано",
                "volume_description": tender_text[:200],
                "deadline_days": 90,
                "estimated_budget_kzt": 0,
                "lots": [],
                "_llm_error": "AI-сервис вернул некорректный ответ. Повторите попытку."
            }

    async def generate_resource_plan(
        self,
        parsed_scope: Dict[str, Any],
        similar_projects: list,
        company_context: str = ""
    ) -> Dict[str, Any]:
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

        budget: float = float(parsed_scope.get("estimated_budget_kzt") or 0)
        deadline: int = int(parsed_scope.get("deadline_days") or 90)

        ctx = company_context or AVC_COMPANY_CONTEXT
        labor_share = int(budget * 0.50)
        material_share = int(budget * 0.30)
        equipment_share = int(budget * 0.20)

        # Pre-compute realistic headcounts from the actual budget so the LLM
        # can't drift to unrealistic numbers. These are HINTS, not hard caps.
        avg_labor_rate: int = 45_000   # KZT/day (mid-range skilled worker)
        avg_equip_rate: int = 150_000  # KZT/shift
        implied_workers = max(1, round(labor_share / (avg_labor_rate * deadline))) if deadline > 0 else 10
        implied_equip   = max(1, round(equipment_share / (avg_equip_rate * deadline))) if deadline > 0 else 2

        prompt = f"""You are a senior cost estimator at AVC Group — an EPC company specialising in oil refinery repairs in Kazakhstan.

COMPANY PROFILE (AVC GROUP):
{ctx}

TENDER SCOPE:
- Title: {parsed_scope.get('title', parsed_scope.get('work_type', ''))}
- Work type: {parsed_scope.get('work_type', '')}
- Equipment: {', '.join(parsed_scope.get('equipment_list', []))}
- Location: {parsed_scope.get('location', '')}
- Volume: {parsed_scope.get('volume_description', '')}
- Duration: {deadline} calendar days
- Tender budget (ПЛАНИРУЕМАЯ СУММА БЕЗ НДС): {budget:,.0f} KZT
{lots_text}
SIMILAR COMPLETED PROJECTS (use for calibration):
{similar_text if similar_text else "No historical data — use industry norms for Kazakhstan 2024-2025."}

══════════════════════════════════════════════════════════════
BUDGET = {budget:,.0f} KZT  |  DURATION = {deadline} days
══════════════════════════════════════════════════════════════

BUDGET BREAKDOWN (mandatory targets):
  Labor    ~{labor_share:,.0f} KZT  (50%)  → ~{implied_workers} workers
  Materials~{material_share:,.0f} KZT  (30%)
  Equipment~{equipment_share:,.0f} KZT  (20%)  → ~{implied_equip} machines

⚠️ CRITICAL — HOW TO COMPUTE total_cost FOR EACH RESOURCE:
  • LABOR:     total_cost = quantity (number of workers) × unit_cost (KZT/day) × {deadline} days
               Example: 10 workers × 45 000 KZT/day × {deadline} days = {10*45_000*deadline:,.0f} KZT
  • EQUIPMENT: total_cost = quantity (shifts over whole project) × unit_cost (KZT/shift)
               OR:  daily_machines × unit_cost × {deadline} days
  • MATERIAL:  total_cost = quantity × unit_cost (one-time purchase price)

  The labor budget alone is {labor_share:,.0f} KZT.
  At 45 000 KZT/day per worker × {deadline} days, that covers ≈{implied_workers} workers.
  DO NOT compute labor as workers × rate × 1 day — use the FULL {deadline}-day duration.

Kazakhstan petroleum-industry daily rates:
  - Сварщик, монтажник (skilled): 35 000–55 000 KZT/day
  - ИТР, мастер (engineer):       45 000–70 000 KZT/day
  - Подсобный рабочий:            20 000–30 000 KZT/day
  - Machine-shift (маш/см):       80 000–250 000 KZT/shift

Return ONLY valid JSON (no fences):
{{
  "resources": [
    {{
      "resource_type": "labor|material|equipment",
      "name": "Name in Russian",
      "quantity": number  (for labor = headcount; for equipment = daily machines or total shifts; for material = units),
      "unit": "чел | маш/см | шт | м | кг | комплект",
      "unit_cost": number  (KZT — daily rate for labor, per-shift for equipment, per-unit for material),
      "total_cost": number  (KZT — MUST follow the formula above; labor = qty × rate × {deadline}),
      "notes": "brief justification with the calculation"
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
  "estimated_total_cost": number  (KZT — MUST be within ±10% of {budget:,.0f}),
  "estimated_duration_days": {deadline},
  "specialists_count": integer  (sum of quantity for all labor resources),
  "equipment_count":   integer  (sum of quantity for all equipment resources),
  "total_manhours":    integer  (specialists_count × {deadline} × 8),
  "reasoning": "Detailed reasoning in Russian (6-8 sentences): (1) analogue project used and why; (2) how {budget:,.0f} KZT splits across labor/materials/equipment; (3) headcount justification vs AVC GROUP benchmarks and budget; (4) why {deadline} days is sufficient; (5) key risks/assumptions; (6) how unit costs match Kazakhstan petroleum-industry norms."
}}

Validation rules:
- 6–12 resource rows, 4–8 task rows
- SINGLE OBJECT scope — not a full plant turnaround
- Sum of all resource total_cost ≈ {budget:,.0f} KZT (±10%)
- specialists_count = integer sum of labor quantities
- equipment_count   = integer sum of equipment quantities
- total_manhours    = specialists_count × {deadline} × 8"""

        response = await self._call_with_fallback(prompt)
        if not response:
            logger.error("Both LLM providers failed for resource plan generation")
            return {
                "resources": [], "tasks": [],
                "estimated_total_cost": 0,
                "estimated_duration_days": deadline,
                "specialists_count": 0,
                "equipment_count": 0,
                "total_manhours": 0,
                "reasoning": "Ошибка: не удалось получить ответ от AI-сервиса. Проверьте API-ключи (GEMINI_API_KEY / GROQ_API_KEY) и сетевое подключение.",
                "_llm_error": "Оба AI-провайдера недоступны."
            }

        try:
            result = json.loads(self._clean_json(response))

            resources = result.get("resources", [])
            duration = int(result.get("estimated_duration_days") or deadline)

            # ── Enforce correct labor cost server-side ──────────────────────
            # LLMs often compute total_cost = workers × rate × 1 day instead of
            # workers × rate × duration_days. We correct this unconditionally.
            for r in resources:
                qty = float(r.get("quantity") or 0)
                rate = float(r.get("unit_cost") or 0)
                if r.get("resource_type") == "labor" and qty > 0 and rate > 0:
                    r["total_cost"] = round(qty * rate * duration)
                elif r.get("resource_type") in ("material", "equipment") and qty > 0 and rate > 0:
                    # Keep LLM value for materials/equipment; only recompute if
                    # total_cost is suspiciously small (less than qty × rate)
                    llm_tc = float(r.get("total_cost") or 0)
                    expected_min = qty * rate
                    if llm_tc < expected_min * 0.5:
                        r["total_cost"] = round(qty * rate)

            # ── Workforce summary numbers ───────────────────────────────────
            specialists = int(sum(
                float(r.get("quantity") or 0)
                for r in resources if r.get("resource_type") == "labor"
            ))
            equipment_count = int(sum(
                float(r.get("quantity") or 0)
                for r in resources if r.get("resource_type") == "equipment"
            ))
            manhours = specialists * duration * 8

            result["specialists_count"] = specialists
            result["equipment_count"] = equipment_count
            result["total_manhours"] = manhours

            # ── Budget normalization ────────────────────────────────────────
            # After fixing labor costs the total should be close to budget.
            # If still off by >30%, scale all resource costs proportionally.
            if budget > 0 and resources:
                llm_total = sum(float(r.get("total_cost") or 0) for r in resources)
                if llm_total > 0:
                    ratio = budget / llm_total
                    if ratio > 1.3 or ratio < 0.7:
                        for r in resources:
                            r["unit_cost"] = round(float(r.get("unit_cost") or 0) * ratio)
                            r["total_cost"] = round(float(r.get("total_cost") or 0) * ratio)
                        result["estimated_total_cost"] = budget
                    else:
                        result["estimated_total_cost"] = round(llm_total)

            return result
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            logger.error(f"Failed to parse resource plan JSON: {e}, raw={response[:300]}")
            return {
                "resources": [], "tasks": [],
                "estimated_total_cost": 0,
                "estimated_duration_days": deadline,
                "specialists_count": 0,
                "equipment_count": 0,
                "total_manhours": 0,
                "reasoning": f"Ошибка разбора ответа AI: {str(e)[:100]}. Попробуйте повторить анализ.",
                "_llm_error": "AI вернул некорректный JSON. Повторите попытку."
            }

    async def _call_with_fallback(self, prompt: str) -> Optional[str]:
        """Try Gemini first (with retries), then Groq (with retries)."""
        response = await self._call_gemini(prompt)
        if response:
            return response
        logger.info("Gemini unavailable, falling back to Groq")
        return await self._call_groq(prompt)

    async def _call_gemini(self, prompt: str) -> Optional[str]:
        if not GEMINI_API_KEY:
            return None
        for attempt in range(self.MAX_RETRIES):
            try:
                async with httpx.AsyncClient(timeout=60) as client:
                    resp = await client.post(
                        f"{GEMINI_URL}?key={GEMINI_API_KEY}",
                        json={
                            "contents": [{"parts": [{"text": prompt}]}],
                            "generationConfig": {
                                "responseMimeType": "application/json"
                            }
                        }
                    )
                    if resp.status_code == 429:
                        logger.warning(f"Gemini rate limited, attempt {attempt+1}/{self.MAX_RETRIES}")
                        await asyncio.sleep(self.RETRY_DELAY * (attempt + 1))
                        continue
                    data = resp.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"]
            except (httpx.TimeoutException, httpx.ConnectError) as e:
                logger.warning(f"Gemini network error attempt {attempt+1}: {e}")
                if attempt < self.MAX_RETRIES - 1:
                    await asyncio.sleep(self.RETRY_DELAY * (attempt + 1))
            except Exception as e:
                logger.error(f"Gemini unexpected error: {e}")
                return None
        return None

    async def _call_groq(self, prompt: str) -> Optional[str]:
        if not GROQ_API_KEY:
            return None
        for attempt in range(self.MAX_RETRIES):
            try:
                async with httpx.AsyncClient(timeout=60) as client:
                    resp = await client.post(
                        GROQ_URL,
                        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                        json={
                            "model": "llama-3.3-70b-versatile",
                            "messages": [{"role": "user", "content": prompt}],
                            "max_tokens": 4000,
                            "response_format": {"type": "json_object"}
                        }
                    )
                    if resp.status_code == 429:
                        logger.warning(f"Groq rate limited, attempt {attempt+1}/{self.MAX_RETRIES}")
                        await asyncio.sleep(self.RETRY_DELAY * (attempt + 1))
                        continue
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
            except (httpx.TimeoutException, httpx.ConnectError) as e:
                logger.warning(f"Groq network error attempt {attempt+1}: {e}")
                if attempt < self.MAX_RETRIES - 1:
                    await asyncio.sleep(self.RETRY_DELAY * (attempt + 1))
            except Exception as e:
                logger.error(f"Groq unexpected error: {e}")
                return None
        return None
