from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta
from app.auth.demo_users import authenticate_user
from app.auth.jwt_handler import create_access_token
from app.auth.dependencies import get_current_user
from app.config import settings

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """Login endpoint - authenticate user and return JWT token"""
    user = authenticate_user(credentials.username, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires,
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user information"""
    return current_user


@router.get("/demo-users")
async def get_demo_users():
    """Get list of demo users for login page (for presentation purposes)"""
    from app.auth.demo_users import DEMO_USERS
    
    demo_info = []
    for username, user_data in DEMO_USERS.items():
        demo_info.append({
            "username": username,
            "role": user_data["role"],
            "name": user_data["name"],
            "hint": f"Password: {username.split('worker')[0] if 'worker' in username else username}123"
        })
    
    return demo_info