from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BudgetBase(BaseModel):
    project_id: int
    category: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    planned_amount: float = Field(default=0.0, ge=0)
    actual_amount: float = Field(default=0.0, ge=0)


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    category: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    planned_amount: Optional[float] = Field(None, ge=0)
    actual_amount: Optional[float] = Field(None, ge=0)


class BudgetResponse(BudgetBase):
    id: int
    variance: float
    variance_percentage: float
    budget_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True