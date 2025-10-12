from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.project import ProjectStatus


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    total_budget: float = Field(default=0.0, ge=0)
    location: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    total_budget: Optional[float] = Field(None, ge=0)
    spent_amount: Optional[float] = Field(None, ge=0)
    location: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    spent_amount: float
    actual_end_date: Optional[datetime] = None
    budget_utilization: float
    remaining_budget: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectSummary(BaseModel):
    id: int
    name: str
    status: ProjectStatus
    budget_utilization: float
    progress: float = 0.0
    
    class Config:
        from_attributes = True