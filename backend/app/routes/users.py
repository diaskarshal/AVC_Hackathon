from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth.dependencies import require_role, get_current_user
from app.auth.demo_users import DEMO_USERS, get_user_by_username
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", dependencies=[Depends(require_role("admin"))])
async def get_all_users(db: Session = Depends(get_db)):
    users = []
    for username, user_data in DEMO_USERS.items():
        user_copy = user_data.copy()
        user_copy.pop("password_hash", None)
        user_copy["username"] = username
        users.append(user_copy)
    return users


@router.get("/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    return current_user


@router.put("/profile")
async def update_user_profile(
    profile_data: dict,
    current_user: dict = Depends(get_current_user),
):
    updated_user = current_user.copy()
    
    allowed_fields = ["name", "email"]
    for field in allowed_fields:
        if field in profile_data:
            updated_user[field] = profile_data[field]
    
    return updated_user


@router.get("/team", dependencies=[Depends(require_role("admin", "manager"))])
async def get_team_members(
    current_user: dict = Depends(get_current_user),
):
    """Get team members based on role"""
    if current_user["role"] == "admin":
        team = []
        for username, user_data in DEMO_USERS.items():
            user_copy = user_data.copy()
            user_copy.pop("password_hash", None)
            user_copy["username"] = username
            team.append(user_copy)
        return team
    elif current_user["role"] == "manager":
        managed_projects = current_user.get("managed_projects", [])
        team = []
        for username, user_data in DEMO_USERS.items():
            if user_data["role"] == "worker":
                user_copy = user_data.copy()
                user_copy.pop("password_hash", None)
                user_copy["username"] = username
                team.append(user_copy)
        return team
    
    return []


@router.get("/activity-log", dependencies=[Depends(require_role("admin"))])
async def get_activity_log(
    limit: int = 50,
    db: Session = Depends(get_db),
):
    return {
        "message": "Activity logging not yet implemented",
        "activities": []
    }