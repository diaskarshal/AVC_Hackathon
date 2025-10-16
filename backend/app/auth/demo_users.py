from typing import Dict, Optional, List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hardcoded demo users for MVP presentation
DEMO_USERS = {
    "admin": {
        "username": "admin",
        "password_hash": pwd_context.hash("admin123"),
        "role": "admin",
        "name": "John Admin",
        "email": "admin@buildflow.com",
        "worker_name": None,
        "managed_projects": [],
    },
    "manager1": {
        "username": "manager1",
        "password_hash": pwd_context.hash("manager123"),
        "role": "manager",
        "name": "Sarah Manager",
        "email": "sarah@buildflow.com",
        "worker_name": None,
        "managed_projects": [1, 2],  # Can manage these project IDs
    },
    "worker1": {
        "username": "worker1",
        "password_hash": pwd_context.hash("worker123"),
        "role": "worker",
        "name": "Mike Construction",
        "email": "mike@buildflow.com",
        "worker_name": "Mike Construction",  # Matches 'assigned_to' in tasks
        "managed_projects": [],
    },
    "worker2": {
        "username": "worker2",
        "password_hash": pwd_context.hash("worker123"),
        "role": "worker",
        "name": "Lisa Field",
        "email": "lisa@buildflow.com",
        "worker_name": "Lisa Field",
        "managed_projects": [],
    },
    "worker3": {
        "username": "worker3",
        "password_hash": pwd_context.hash("worker123"),
        "role": "worker",
        "name": "Construction Team A",
        "email": "teama@buildflow.com",
        "worker_name": "Construction Team A",
        "managed_projects": [],
    },
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_username(username: str) -> Optional[Dict]:
    """Get user by username"""
    return DEMO_USERS.get(username)


def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Authenticate a user"""
    user = get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    # Return user without password hash
    user_copy = user.copy()
    user_copy.pop("password_hash", None)
    return user_copy