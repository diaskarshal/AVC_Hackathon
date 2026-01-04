from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.project import Project
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectSummary,
)
from app.services.project_service import ProjectService
from app.auth.dependencies import get_current_user, require_role

router = APIRouter()


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))],
)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    service = ProjectService(db)
    return service.create_project(project)


@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = ProjectService(db)
    
    if current_user["role"] == "manager":
        managed_project_ids = current_user.get("managed_projects", [])
        projects = service.get_projects(skip=skip, limit=limit)
        return [p for p in projects if p.id in managed_project_ids]
    
    return service.get_projects(skip=skip, limit=limit)


@router.get("/summary", response_model=List[ProjectSummary])
async def get_projects_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = ProjectService(db)
    summaries = service.get_projects_summary()
    
    if current_user["role"] == "manager":
        managed_project_ids = current_user.get("managed_projects", [])
        return [s for s in summaries if s["id"] in managed_project_ids]
    
    return summaries


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = ProjectService(db)
    project = service.get_project_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )
    
    if current_user["role"] == "manager":
        managed_project_ids = current_user.get("managed_projects", [])
        if project_id not in managed_project_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )
    
    return project


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] == "manager":
        managed_project_ids = current_user.get("managed_projects", [])
        if project_id not in managed_project_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )
    
    service = ProjectService(db)
    project = service.update_project(project_id, project_update)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )
    
    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin"))],  # Admin only
)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    service = ProjectService(db)
    success = service.delete_project(project_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )
    
    return None