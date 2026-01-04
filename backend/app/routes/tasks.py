from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.auth.dependencies import get_current_user, require_role

router = APIRouter()


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.get("/project/{project_id}/overdue", response_model=List[TaskResponse])
async def get_overdue_tasks(
    project_id: int,
    db: Session = Depends(get_db)
):
    from datetime import datetime
    tasks = db.query(Task).filter(
        Task.project_id == project_id,
        Task.status != TaskStatus.COMPLETED,
        Task.planned_end_date < datetime.utcnow()
    ).all()
    return tasks

def check_task_access(current_user: dict, task: Task) -> bool:
    if current_user["role"] == "admin":
        return True
    elif current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        return task.project_id in managed_projects
    elif current_user["role"] == "worker":
        return task.assigned_to == current_user.get("worker_name")
    return False


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    project_id: Optional[int] = Query(None),
    status: Optional[TaskStatus] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    query = db.query(Task)
    
    if current_user["role"] == "worker":
        worker_name = current_user.get("worker_name")
        query = query.filter(Task.assigned_to == worker_name)
    elif current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        query = query.filter(Task.project_id.in_(managed_projects))
    
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if status:
        query = query.filter(Task.status == status)
    
    return query.offset(skip).limit(limit).all()


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if task.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create tasks for your managed projects",
            )
    
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    
    if not check_task_access(current_user, db_task):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this task",
        )
    
    if current_user["role"] == "worker":
        allowed_fields = {"status", "progress_percentage", "actual_end_date"}
        update_data = task_update.model_dump(
            exclude_unset=True, include=allowed_fields
        )
    else:
        update_data = task_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if db_task.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete tasks from your managed projects",
            )
    
    db.delete(db_task)
    db.commit()
    return None