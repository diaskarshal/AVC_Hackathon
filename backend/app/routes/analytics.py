from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import AnalyticsService
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = AnalyticsService(db)
    
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        stats = service.get_manager_dashboard_stats(managed_projects)
    elif current_user["role"] == "worker":
        worker_name = current_user.get("worker_name")
        stats = service.get_worker_dashboard_stats(worker_name)
    else:
        stats = service.get_dashboard_stats()
    
    return stats


@router.get("/team-performance")
async def get_team_performance(
    project_id: int = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] == "worker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workers cannot access team performance data"
        )
    
    if current_user["role"] == "manager" and project_id:
        managed_projects = current_user.get("managed_projects", [])
        if project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project"
            )
    
    service = AnalyticsService(db)
    return service.get_team_performance(project_id)


@router.get("/project/{project_id}/kpi")
async def get_project_kpi(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if project_id not in managed_projects:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )
    
    service = AnalyticsService(db)
    return service.get_project_kpi(project_id)


@router.get("/project/{project_id}/budget-breakdown")
async def get_budget_breakdown(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get budget breakdown - admin and manager only"""
    if current_user["role"] == "worker":
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workers cannot access budget information",
        )
    
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if project_id not in managed_projects:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )
    
    service = AnalyticsService(db)
    return service.get_budget_breakdown(project_id)


@router.get("/project/{project_id}/resource-distribution")
async def get_resource_distribution(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get resource distribution - admin and manager only"""
    if current_user["role"] == "worker":
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workers cannot access resource information",
        )
    
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if project_id not in managed_projects:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )
    
    service = AnalyticsService(db)
    return service.get_resource_distribution(project_id)


@router.get("/project/{project_id}/timeline")
async def get_project_timeline(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get project timeline with milestones"""
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if project_id not in managed_projects:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )
    
    service = AnalyticsService(db)
    return service.get_project_timeline(project_id)


@router.get("/project/{project_id}/predict-completion")
async def predict_completion(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Predict project completion date and cost using ML"""
    # Check manager permissions
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if project_id not in managed_projects:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )
    
    service = AnalyticsService(db)
    return service.predict_completion(project_id)