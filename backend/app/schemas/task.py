from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    project_id: int
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.NOT_STARTED
    priority: TaskPriority = TaskPriority.MEDIUM
    start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    progress_percentage: float = Field(default=0.0, ge=0, le=100)
    assigned_to: Optional[str] = None
    depends_on_task_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    progress_percentage: Optional[float] = Field(None, ge=0, le=100)
    assigned_to: Optional[str] = None
    depends_on_task_id: Optional[int] = None


class TaskResponse(TaskBase):
    id: int
    actual_end_date: Optional[datetime] = None
    is_overdue: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True