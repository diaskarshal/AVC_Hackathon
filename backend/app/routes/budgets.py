from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse
from app.auth.dependencies import get_current_user, require_role

router = APIRouter()


@router.post(
    "/",
    response_model=BudgetResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def create_budget(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if budget.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create budgets for your managed projects",
            )
    
    db_budget = Budget(**budget.model_dump())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


@router.get("/", response_model=List[BudgetResponse])
async def get_budgets(
    project_id: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    query = db.query(Budget)
    
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        query = query.filter(Budget.project_id.in_(managed_projects))
    elif current_user["role"] == "worker":
        return []
    
    if project_id:
        query = query.filter(Budget.project_id == project_id)
    if category:
        query = query.filter(Budget.category.ilike(f"%{category}%"))
    
    return query.offset(skip).limit(limit).all()


@router.get("/{budget_id}", response_model=BudgetResponse)
async def get_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Budget with id {budget_id} not found",
        )
    
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if budget.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this budget",
            )
    elif current_user["role"] == "worker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workers cannot access budget details",
        )
    
    return budget


@router.put(
    "/{budget_id}",
    response_model=BudgetResponse,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def update_budget(
    budget_id: int,
    budget_update: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    
    if not db_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Budget with id {budget_id} not found",
        )
    
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if db_budget.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update budgets in your managed projects",
            )
    
    update_data = budget_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_budget, field, value)
    
    db.commit()
    db.refresh(db_budget)
    return db_budget


@router.delete(
    "/{budget_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin", "manager"))],
)
async def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    
    if not db_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Budget with id {budget_id} not found",
        )
    
    if current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        if db_budget.project_id not in managed_projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete budgets from your managed projects",
            )
    
    db.delete(db_budget)
    db.commit()
    return None