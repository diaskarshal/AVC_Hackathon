from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.resource import Resource, ResourceType
from app.schemas.resource import (
    ResourceCreate,
    ResourceUpdate,
    ResourceResponse,
)
from app.auth.dependencies import get_current_user, require_role

router = APIRouter()


@router.post(
    "/",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if resource.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create resources for your managed projects",
            )
    
    db_resource = Resource(**resource.model_dump())
    db_resource.calculate_total_cost()
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


@router.get("/", response_model=List[ResourceResponse])
async def get_resources(
    project_id: Optional[int] = Query(None),
    resource_type: Optional[ResourceType] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    query = db.query(Resource)
    
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        query = query.filter(Resource.project_id.in_(managed_projects))
    elif current_user["role"] == "worker":
        return []
    
    if project_id:
        query = query.filter(Resource.project_id == project_id)
    if resource_type:
        query = query.filter(Resource.resource_type == resource_type)
    
    return query.offset(skip).limit(limit).all()


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found",
        )
    
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if resource.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this resource",
            )
    elif current_user["role"] == "worker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workers cannot access resource details",
        )
    
    return resource


@router.put(
    "/{resource_id}",
    response_model=ResourceResponse,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def update_resource(
    resource_id: int,
    resource_update: ResourceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_resource = (
        db.query(Resource).filter(Resource.id == resource_id).first()
    )
    
    if not db_resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found",
        )
    
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if db_resource.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update resources in your managed projects",
            )
    
    update_data = resource_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_resource, field, value)
    
    db_resource.calculate_total_cost()
    db.commit()
    db.refresh(db_resource)
    return db_resource


@router.delete(
    "/{resource_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_resource = (
        db.query(Resource).filter(Resource.id == resource_id).first()
    )
    
    if not db_resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found",
        )
    
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if db_resource.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete resources from your managed projects",
            )
    
    db.delete(db_resource)
    db.commit()
    return None