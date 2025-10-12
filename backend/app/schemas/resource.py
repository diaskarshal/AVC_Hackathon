from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.resource import ResourceType, ResourceStatus


class ResourceBase(BaseModel):
    project_id: int
    name: str = Field(..., min_length=1, max_length=255)
    resource_type: ResourceType
    status: ResourceStatus = ResourceStatus.AVAILABLE
    quantity: float = Field(default=0.0, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    unit_cost: float = Field(default=0.0, ge=0)
    supplier: Optional[str] = None


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    resource_type: Optional[ResourceType] = None
    status: Optional[ResourceStatus] = None
    quantity: Optional[float] = Field(None, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    unit_cost: Optional[float] = Field(None, ge=0)
    supplier: Optional[str] = None


class ResourceResponse(ResourceBase):
    id: int
    total_cost: float
    allocated_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True