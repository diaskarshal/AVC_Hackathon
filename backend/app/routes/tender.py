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
from app.services.tender_parser import TenderParserService
from app.services.llm_service import LLMService
from app.services.similarity_service import SimilarityService
from app.services.embedding_service import embed_text
from datetime import datetime, timedelta

router = APIRouter()


class AcceptPlanBody(BaseModel):
    plan_id: int
    project_name: Optional[str] = None
    resources: Optional[list] = None  # edited overrides
    tasks: Optional[list] = None       # edited overrides


@router.post("/upload", dependencies=[Depends(require_role("admin", "manager"))])
async def upload_tender(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Step 1: Upload a tender document (PDF or Excel)."""
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

    # Extract structured scope
    parsed_scope = await llm.extract_tender_scope(tender.raw_text or "")
    tender.parsed_scope = parsed_scope
    tender.status = TenderStatus.PARSED
    # Update tender title with the parsed project name
    parsed_title = parsed_scope.get("title") or parsed_scope.get("work_type", "")
    if parsed_title:
        tender.title = parsed_title

    # Compute embedding for the tender — use title + equipment + location for best similarity match
    title = parsed_scope.get("title") or parsed_scope.get("work_type", "")
    equipment_str = " ".join(parsed_scope.get("equipment_list", []))
    lots_names = " ".join(lot.get("name", "") for lot in parsed_scope.get("lots", []))
    query_text = f"{title} {equipment_str} {lots_names} {parsed_scope.get('location', '')}".strip()
    tender.embedding = embed_text(query_text)

    # Find similar historical projects
    similar = similarity.find_similar_projects(query_text, top_k=3)

    # Generate resource plan
    plan_data = await llm.generate_resource_plan(parsed_scope, similar)

    # Calculate total cost from resources
    total_cost = sum(r.get("total_cost", 0) for r in plan_data.get("resources", []))

    # Store the FULL plan (resources + tasks + reasoning) in plan_data
    resource_plan = TenderResourcePlan(
        tender_id=tender.id,
        plan_data=plan_data,  # full dict: {resources, tasks, estimated_total_cost, ...}
        estimated_total_cost=total_cost or plan_data.get("estimated_total_cost", 0),
        estimated_duration_days=plan_data.get("estimated_duration_days", 90),
        similar_project_ids=[sp["project"].id for sp in similar],
        confidence_score=similar[0]["similarity_score"] if similar else 0.0,
        llm_reasoning=plan_data.get("reasoning", "")
    )
    db.add(resource_plan)
    tender.status = TenderStatus.PLAN_GENERATED
    db.commit()
    db.refresh(resource_plan)

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

    # Create project
    project = Project(
        name=body.project_name or tender.title,
        description=f"Тендер: {scope.get('work_type', '')}. {scope.get('volume_description', '')}",
        status=ProjectStatus.PLANNING,
        start_date=datetime.utcnow(),
        planned_end_date=datetime.utcnow() + timedelta(days=plan.estimated_duration_days or 90),
        total_budget=plan.estimated_total_cost,
        location=scope.get("location", "")
    )
    db.add(project)
    db.flush()

    # Use edited overrides if provided, otherwise fall back to stored plan
    resources_list = body.resources if body.resources is not None else (
        full_plan.get("resources", []) if isinstance(full_plan, dict) else full_plan
    )
    tasks_list_override = body.tasks if body.tasks is not None else None

    # Create resources from plan
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

    # Create tasks from plan
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

    # Create budget entry
    confidence_str = f"{plan.confidence_score:.0%}" if plan.confidence_score else "N/A"
    budget = Budget(
        project_id=project.id,
        category="Tender Estimate",
        description=f"Auto-generated from tender analysis. Confidence: {confidence_str}",
        planned_amount=plan.estimated_total_cost,
        actual_amount=0.0
    )
    db.add(budget)

    # Mark tender as accepted
    tender.status = TenderStatus.ACCEPTED
    tender.created_project_id = project.id
    db.commit()
    db.refresh(project)

    return {
        "project_id": project.id,
        "message": f"Project '{project.name}' created successfully",
        "resources_count": len(resources_list or []),
        "tasks_count": len(tasks_list or [])
    }


@router.get("/", dependencies=[Depends(get_current_user)])
async def list_tenders(db: Session = Depends(get_db)):
    """List all tenders."""
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
    """Delete a tender and all its associated plans."""
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
