from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.auth.dependencies import get_current_user, require_role
from app.models.tender import Tender, TenderResourcePlan, TenderStatus
from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskPriority, TaskStatus
from app.models.resource import Resource, ResourceType, ResourceStatus
from app.models.budget import Budget
from app.services.tender_parser import TenderParserService, shorten_company, extract_city
from app.services.llm_service import LLMService
from app.services.similarity_service import SimilarityService
from app.services.embedding_service import embed_text
from datetime import datetime, timedelta

router = APIRouter()


class AcceptPlanBody(BaseModel):
    plan_id: int
    project_name: Optional[str] = None
    resources: Optional[list] = None
    tasks: Optional[list] = None


@router.post("/upload", dependencies=[Depends(require_role("admin", "manager"))])
async def upload_tender(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Step 1: Upload a tender document"""
    contents = await file.read()

    parser = TenderParserService()
    raw_text = parser.parse(contents, file.filename)

    tender = Tender(
        title=file.filename.replace(".pdf", "").replace(".xlsx", ""),
        raw_text=raw_text[:50000],
        file_name=file.filename,
        uploaded_by=current_user["username"],
        status=TenderStatus.UPLOADED
    )
    db.add(tender)
    db.commit()
    db.refresh(tender)

    return {"tender_id": tender.id, "message": "Upload successful. Call /analyze to process."}


@router.post("/{tender_id}/analyze")
async def analyze_tender(
    tender_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Step 2: Parse scope with LLM + find similar projects + generate resource plan."""
    tender = db.query(Tender).filter(Tender.id == tender_id).first()
    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")

    llm = LLMService()
    similarity = SimilarityService(db)

    parsed_scope = await llm.extract_tender_scope(tender.raw_text or "")

    if parsed_scope.get("location"):
        parsed_scope["location"] = extract_city(parsed_scope["location"])
    if parsed_scope.get("customer"):
        parsed_scope["customer"] = shorten_company(parsed_scope["customer"])
    for lot in parsed_scope.get("lots", []):
        if lot.get("location"):
            lot["location"] = extract_city(lot["location"])

    tender.parsed_scope = parsed_scope
    tender.status = TenderStatus.PARSED

    parsed_title = parsed_scope.get("title") or parsed_scope.get("work_type", "")
    if parsed_title:
        tender.title = parsed_title

    title = parsed_scope.get("title") or parsed_scope.get("work_type", "")
    equipment_str = " ".join(parsed_scope.get("equipment_list", []))
    lots_names = " ".join(lot.get("name", "") for lot in parsed_scope.get("lots", []))
    query_text = f"{title} {equipment_str} {lots_names} {parsed_scope.get('location', '')}".strip()
    tender.embedding = embed_text(query_text)

    similar = similarity.find_similar_projects(query_text, top_k=3)

    plan_data = await llm.generate_resource_plan(parsed_scope, similar)

    total_cost = sum(r.get("total_cost", 0) for r in plan_data.get("resources", []))

    # Components:
    #   1. Similarity quality (40%) - best match cosine score
    #   2. Budget alignment (30%) - how close LLM estimate is to tender budget
    #   3. Plan completeness (30%) - did the LLM return enough resources + tasks
    sim_score = similar[0]["similarity_score"] if similar else 0.0
    tender_budget = parsed_scope.get("estimated_budget_kzt", 0)
    llm_total = plan_data.get("estimated_total_cost", 0) or total_cost
    if tender_budget > 0 and llm_total > 0:
        budget_ratio = min(llm_total, tender_budget) / max(llm_total, tender_budget)
    else:
        budget_ratio = 0.3  # no budget data = low confidence
    n_resources = len(plan_data.get("resources", []))
    n_tasks = len(plan_data.get("tasks", []))
    completeness = min(1.0, (n_resources / 6) * 0.5 + (n_tasks / 4) * 0.5)
    confidence = round(sim_score * 0.4 + budget_ratio * 0.3 + completeness * 0.3, 3)

    resource_plan = TenderResourcePlan(
        tender_id=tender.id,
        plan_data=plan_data,
        estimated_total_cost=total_cost or plan_data.get("estimated_total_cost", 0),
        estimated_duration_days=plan_data.get("estimated_duration_days", 90),
        similar_project_ids=[sp["project"].id for sp in similar],
        confidence_score=confidence,
        llm_reasoning=plan_data.get("reasoning", "")
    )
    db.add(resource_plan)
    tender.status = TenderStatus.PLAN_GENERATED
    db.commit()
    db.refresh(resource_plan)

    warnings = []
    if parsed_scope.get("_llm_error"):
        warnings.append(f"Извлечение данных: {parsed_scope['_llm_error']}")
    if plan_data.get("_llm_error"):
        warnings.append(f"Ресурсный план: {plan_data['_llm_error']}")

    return {
        "tender_id": tender.id,
        "parsed_scope": parsed_scope,
        "plan_id": resource_plan.id,
        "estimated_total_cost": resource_plan.estimated_total_cost,
        "estimated_duration_days": resource_plan.estimated_duration_days,
        "resources": plan_data.get("resources", []),
        "tasks": plan_data.get("tasks", []),
        "similar_projects": [
            {"id": sp["project"].id, "name": sp["project"].name, "score": sp["similarity_score"]}
            for sp in similar
        ],
        "reasoning": plan_data.get("reasoning", ""),
        "confidence_score": resource_plan.confidence_score,
        "specialists_count": plan_data.get("specialists_count", 0),
        "equipment_count": plan_data.get("equipment_count", 0),
        "total_manhours": plan_data.get("total_manhours", 0),
        "warnings": warnings if warnings else None,
    }


@router.post("/{tender_id}/accept")
async def accept_tender_plan(
    tender_id: int,
    body: AcceptPlanBody,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Step 3: Accept the plan - creates a real Project with Tasks and Resources in the ERP."""
    tender = db.query(Tender).filter(Tender.id == tender_id).first()
    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")

    plan = db.query(TenderResourcePlan).filter(TenderResourcePlan.id == body.plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    scope = tender.parsed_scope or {}
    full_plan = plan.plan_data or {}

    project = Project(
        name=body.project_name or tender.title,
        description=f"Тендер: {scope.get('work_type', '')}. {scope.get('volume_description', '')}",
        status=ProjectStatus.PLANNING,
        start_date=datetime.utcnow(),
        planned_end_date=datetime.utcnow() + timedelta(days=plan.estimated_duration_days or 90),
        total_budget=plan.estimated_total_cost,
        location=scope.get("location", ""),
        customer=scope.get("customer", "") or None,
    )
    db.add(project)
    db.flush()

    resources_list = body.resources if body.resources is not None else (
        full_plan.get("resources", []) if isinstance(full_plan, dict) else full_plan
    )
    tasks_list_override = body.tasks if body.tasks is not None else None

    rtype_map = {"labor": ResourceType.LABOR, "equipment": ResourceType.EQUIPMENT, "material": ResourceType.MATERIAL}
    for item in (resources_list or []):
        resource = Resource(
            project_id=project.id,
            name=item.get("name", "Resource"),
            resource_type=rtype_map.get(item.get("resource_type", "material"), ResourceType.MATERIAL),
            quantity=float(item.get("quantity", 1)),
            unit=item.get("unit", "шт"),
            unit_cost=float(item.get("unit_cost", 0)),
            status=ResourceStatus.AVAILABLE
        )
        resource.calculate_total_cost()
        db.add(resource)

    tasks_list = tasks_list_override if tasks_list_override is not None else (
        full_plan.get("tasks", []) if isinstance(full_plan, dict) else []
    )
    priority_map = {"high": TaskPriority.HIGH, "medium": TaskPriority.MEDIUM, "low": TaskPriority.LOW}
    start = datetime.utcnow()
    for task_item in (tasks_list or []):
        duration = task_item.get("duration_days", 14)
        task = Task(
            project_id=project.id,
            name=task_item.get("name", "Task"),
            description=task_item.get("description", ""),
            priority=priority_map.get(task_item.get("priority", "medium"), TaskPriority.MEDIUM),
            start_date=start,
            planned_end_date=start + timedelta(days=duration),
            status=TaskStatus.NOT_STARTED,
            progress_percentage=0.0
        )
        db.add(task)
        start = start + timedelta(days=duration)

    confidence_str = f"{plan.confidence_score:.0%}" if plan.confidence_score else "N/A"
    budget = Budget(
        project_id=project.id,
        category="Tender Estimate",
        description=f"Auto-generated from tender analysis. Confidence: {confidence_str}",
        planned_amount=plan.estimated_total_cost,
        actual_amount=0.0
    )
    db.add(budget)

    tender.status = TenderStatus.ACCEPTED
    tender.created_project_id = project.id
    db.commit()
    db.refresh(project)

    similarity = SimilarityService(db)
    similarity.index_project(project)

    return {
        "project_id": project.id,
        "message": f"Project '{project.name}' created successfully",
        "resources_count": len(resources_list or []),
        "tasks_count": len(tasks_list or [])
    }


@router.get("/hot-deals", dependencies=[Depends(get_current_user)])
async def get_hot_deals():
    import httpx, asyncio

    TARGET_COMPANIES = [
        "КАЗАХСТАН ПЕТРОКЕМИКАЛ ИНДАСТРИЗ",
        "АТЫРАУСКИЙ НЕФТЕПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД",
        "ПАВЛОДАРСКИЙ НЕФТЕХИМИЧЕСКИЙ ЗАВОД",
        "АНПЗ",
        "ПНХЗ",
    ]

    # Goszakup public API
    live_deals = []
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                "https://goszakup.gov.kz/v3/announces",
                params={"limit": 50, "status": 1},
                headers={"Accept": "application/json"},
            )
            if resp.status_code == 200:
                data = resp.json()
                for item in data.get("items", []):
                    org = (item.get("organizer_biin") or item.get("org_name") or "").upper()
                    if any(kw in org for kw in TARGET_COMPANIES):
                        item_id = item.get("id")
                        live_deals.append({
                            "id": item_id,
                            "number": item.get("number", ""),
                            "title": item.get("name_ru") or item.get("name_kz") or "—",
                            "company": item.get("org_name", ""),
                            "amount_kzt": item.get("total_sum", 0),
                            "deadline": item.get("end_date", ""),
                            "status": "open",
                            "source": "goszakup",
                            "url": f"https://goszakup.gov.kz/ru/announce/index/{item_id}" if item_id else "https://goszakup.gov.kz/ru/announce",
                        })
    except Exception:
        pass

    if live_deals:
        return {"deals": live_deals, "is_demo": False}

    #demo tenders if Goszakup API unavailable
    import random
    from datetime import date, timedelta
    today = date.today()

    def gz_url(number: str) -> str:
        from urllib.parse import quote
        return f"https://goszakup.gov.kz/ru/announces/index?filter[name]={quote(number)}"

    def sk_url(number: str) -> str:
        from urllib.parse import quote
        return f"https://zakup.sk.kz/Searching?query={quote(number)}"

    pool = [
        {
            "id": "mock-1",
            "number": "КРТ-АНПЗ-2025-0412",
            "title": "Капитальный ремонт резервуаров РВС-10000 №7, №9 на АНПЗ",
            "company": "ТОО «АТЫРАУСКИЙ НЕФТЕПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД»",
            "amount_kzt": 245_000_000,
            "deadline": str(today + timedelta(days=18)),
            "status": "open",
            "source": "samruk",
            "url": sk_url("КРТ-АНПЗ-2025-0412"),
        },
        {
            "id": "mock-2",
            "number": "ТО-ПНХЗ-2025-0089",
            "title": "Техническое обслуживание теплообменного оборудования установки АВТ-3 ПНХЗ",
            "company": "ТОО «ПАВЛОДАРСКИЙ НЕФТЕХИМИЧЕСКИЙ ЗАВОД»",
            "amount_kzt": 87_500_000,
            "deadline": str(today + timedelta(days=12)),
            "status": "open",
            "source": "samruk",
            "url": sk_url("ТО-ПНХЗ-2025-0089"),
        },
        {
            "id": "mock-3",
            "number": "КР-KPI-2025-0156",
            "title": "Ремонт трубопроводов межцеховой обвязки Д=300 мм, протяжённость 450 м",
            "company": "ТОО «KAZAKHSTAN PETROCHEMICAL INDUSTRIES INC.»",
            "amount_kzt": 132_000_000,
            "deadline": str(today + timedelta(days=25)),
            "status": "open",
            "source": "goszakup",
            "url": gz_url("КР-KPI-2025-0156"),
        },
        {
            "id": "mock-4",
            "number": "ППР-АНПЗ-2025-0201",
            "title": "ППР технологической установки ГО-1 АНПЗ — замена катализатора, ревизия оборудования",
            "company": "ТОО «АТЫРАУСКИЙ НЕФТЕПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД»",
            "amount_kzt": 580_000_000,
            "deadline": str(today + timedelta(days=35)),
            "status": "open",
            "source": "samruk",
            "url": sk_url("ППР-АНПЗ-2025-0201"),
        },
        {
            "id": "mock-5",
            "number": "МНТ-ПНХЗ-2025-0034",
            "title": "Монтаж насосного агрегата ЦНА-180/95 с обвязкой трубопроводами на установке ЛК-6У",
            "company": "ТОО «ПАВЛОДАРСКИЙ НЕФТЕХИМИЧЕСКИЙ ЗАВОД»",
            "amount_kzt": 45_200_000,
            "deadline": str(today + timedelta(days=9)),
            "status": "open",
            "source": "goszakup",
            "url": gz_url("МНТ-ПНХЗ-2025-0034"),
        },
        {
            "id": "mock-6",
            "number": "ТР-KPI-2025-0078",
            "title": "Текущий ремонт компрессора ПК-101 установки пиролиза KPI — ревизия и замена уплотнений",
            "company": "ТОО «KAZAKHSTAN PETROCHEMICAL INDUSTRIES INC.»",
            "amount_kzt": 54_300_000,
            "deadline": str(today + timedelta(days=14)),
            "status": "open",
            "source": "goszakup",
            "url": gz_url("ТР-KPI-2025-0078"),
        },
        {
            "id": "mock-7",
            "number": "ЭЛ-АНПЗ-2025-0330",
            "title": "Ремонт электрооборудования и КИПиА установки первичной переработки нефти АТ-2 АНПЗ",
            "company": "ТОО «АТЫРАУСКИЙ НЕФТЕПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД»",
            "amount_kzt": 98_700_000,
            "deadline": str(today + timedelta(days=22)),
            "status": "open",
            "source": "samruk",
            "url": sk_url("ЭЛ-АНПЗ-2025-0330"),
        },
        {
            "id": "mock-8",
            "number": "ИЗ-ПНХЗ-2025-0112",
            "title": "Восстановление антикоррозийной изоляции надземных трубопроводов ПНХЗ, 1-я очередь",
            "company": "ТОО «ПАВЛОДАРСКИЙ НЕФТЕХИМИЧЕСКИЙ ЗАВОД»",
            "amount_kzt": 36_800_000,
            "deadline": str(today + timedelta(days=7)),
            "status": "open",
            "source": "goszakup",
            "url": gz_url("ИЗ-ПНХЗ-2025-0112"),
        },
        {
            "id": "mock-9",
            "number": "СВ-АНПЗ-2025-0415",
            "title": "Сварочные работы при замене змеевиков печи П-101 установки ЭЛОУ-АВТ-6 АНПЗ",
            "company": "ТОО «АТЫРАУСКИЙ НЕФТЕПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД»",
            "amount_kzt": 73_500_000,
            "deadline": str(today + timedelta(days=30)),
            "status": "open",
            "source": "samruk",
            "url": sk_url("СВ-АНПЗ-2025-0415"),
        },
        {
            "id": "mock-10",
            "number": "НС-KPI-2025-0099",
            "title": "Капитальный ремонт насосных агрегатов ЦН-800/100 (6 ед.) установки этилена KPI",
            "company": "ТОО «KAZAKHSTAN PETROCHEMICAL INDUSTRIES INC.»",
            "amount_kzt": 164_000_000,
            "deadline": str(today + timedelta(days=41)),
            "status": "open",
            "source": "goszakup",
            "url": gz_url("НС-KPI-2025-0099"),
        },
    ]

    return {"deals": random.sample(pool, min(5, len(pool))), "is_demo": True}


@router.get("/", dependencies=[Depends(get_current_user)])
async def list_tenders(db: Session = Depends(get_db)):
    tenders = db.query(Tender).order_by(Tender.created_at.desc()).all()
    return [
        {
            "id": t.id, "title": t.title, "status": t.status.value if t.status else None,
            "file_name": t.file_name, "created_at": str(t.created_at),
            "parsed_scope": t.parsed_scope,
            "created_project_id": t.created_project_id
        }
        for t in tenders
    ]


@router.delete("/{tender_id}", dependencies=[Depends(require_role("admin", "manager"))])
async def delete_tender(tender_id: int, db: Session = Depends(get_db)):
    tender = db.query(Tender).filter(Tender.id == tender_id).first()
    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")

    db.query(TenderResourcePlan).filter(TenderResourcePlan.tender_id == tender_id).delete()
    db.delete(tender)
    db.commit()
    return {"message": "Tender deleted"}


@router.get("/{tender_id}")
async def get_tender(tender_id: int, db: Session = Depends(get_db)):
    tender = db.query(Tender).filter(Tender.id == tender_id).first()
    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")

    plans = db.query(TenderResourcePlan).filter(TenderResourcePlan.tender_id == tender_id).all()

    return {
        "id": tender.id,
        "title": tender.title,
        "status": tender.status.value if tender.status else None,
        "file_name": tender.file_name,
        "raw_text": tender.raw_text[:2000] if tender.raw_text else None,
        "parsed_scope": tender.parsed_scope,
        "created_at": str(tender.created_at),
        "created_project_id": tender.created_project_id,
        "plans": [
            {
                "id": p.id,
                "plan_data": p.plan_data,
                "estimated_total_cost": p.estimated_total_cost,
                "estimated_duration_days": p.estimated_duration_days,
                "similar_project_ids": p.similar_project_ids,
                "confidence_score": p.confidence_score,
                "llm_reasoning": p.llm_reasoning,
                "created_at": str(p.created_at)
            }
            for p in plans
        ]
    }
