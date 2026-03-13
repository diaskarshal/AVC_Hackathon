from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import AnalyticsService
from app.auth.dependencies import get_current_user

router = APIRouter()


def _check_manager_access(current_user: dict, project_id: int):
    if current_user["role"] == "manager":
        managed = current_user.get("managed_projects", [])
        if project_id not in managed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )


def _deny_worker(current_user: dict, detail: str = "Access denied"):
    if current_user["role"] == "worker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=detail
        )


@router.get("/dashboard")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = AnalyticsService(db)

    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        return service.get_manager_dashboard_stats(managed_projects)
    elif current_user["role"] == "worker":
        worker_name = current_user.get("worker_name")
        return service.get_worker_dashboard_stats(worker_name)
    else:
        return service.get_dashboard_stats()


@router.get("/charts")
async def get_charts_data(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _deny_worker(current_user)
    service = AnalyticsService(db)
    return service.get_charts_data()


@router.get("/workforce-utilization")
async def get_workforce_utilization(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _deny_worker(current_user)
    service = AnalyticsService(db)
    return service.get_workforce_utilization()


@router.get("/budget-trend")
async def get_budget_trend(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _deny_worker(current_user)
    service = AnalyticsService(db)
    return service.get_budget_trend()


@router.get("/team-performance")
async def get_team_performance(
    project_id: int = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _deny_worker(current_user, "Workers cannot access team performance data")
    if project_id:
        _check_manager_access(current_user, project_id)
    service = AnalyticsService(db)
    return service.get_team_performance(project_id)


@router.get("/project/{project_id}/kpi")
async def get_project_kpi(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _check_manager_access(current_user, project_id)
    service = AnalyticsService(db)
    return service.get_project_kpi(project_id)


@router.get("/project/{project_id}/budget-breakdown")
async def get_budget_breakdown(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _deny_worker(current_user, "Workers cannot access budget information")
    _check_manager_access(current_user, project_id)
    service = AnalyticsService(db)
    return service.get_budget_breakdown(project_id)


@router.get("/project/{project_id}/resource-distribution")
async def get_resource_distribution(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _deny_worker(current_user, "Workers cannot access resource information")
    _check_manager_access(current_user, project_id)
    service = AnalyticsService(db)
    return service.get_resource_distribution(project_id)


@router.get("/project/{project_id}/timeline")
async def get_project_timeline(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _check_manager_access(current_user, project_id)
    service = AnalyticsService(db)
    return service.get_project_timeline(project_id)


@router.get("/project/{project_id}/predict-completion")
async def predict_completion(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _check_manager_access(current_user, project_id)
    service = AnalyticsService(db)
    return service.predict_completion(project_id)
