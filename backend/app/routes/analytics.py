from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.get_dashboard_stats()


@router.get("/project/{project_id}/kpi")
async def get_project_kpi(project_id: int, db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.get_project_kpi(project_id)


@router.get("/project/{project_id}/budget-breakdown")
async def get_budget_breakdown(project_id: int, db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.get_budget_breakdown(project_id)


@router.get("/project/{project_id}/resource-distribution")
async def get_resource_distribution(project_id: int, db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.get_resource_distribution(project_id)


@router.get("/project/{project_id}/timeline")
async def get_project_timeline(project_id: int, db: Session = Depends(get_db)):
    """Get project timeline with milestones"""
    service = AnalyticsService(db)
    return service.get_project_timeline(project_id)


@router.get("/project/{project_id}/predict-completion")
async def predict_completion(project_id: int, db: Session = Depends(get_db)):
    """Predict project completion date and cost using ML"""
    service = AnalyticsService(db)
    return service.predict_completion(project_id)