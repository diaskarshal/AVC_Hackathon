from typing import Dict, Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

_DEMO_USER_PASSWORDS = {
    "admin": "admin123",
    "manager1": "manager123",
    "worker1": "worker123",
    "worker2": "worker123",
    "worker3": "worker123",
}

DEMO_USERS = {
    "admin": {
        "username": "admin",
        "role": "admin",
        "name": "Arman",
        "email": "admin@buildflow.com",
        "worker_name": None,
        "managed_projects": [],
    },
    "manager1": {
        "username": "manager1",
        "role": "manager",
        "name": "Aruzhan",
        "email": "aruzhan@buildflow.com",
        "worker_name": None,
        "managed_projects": [1, 2],
    },
    "worker1": {
        "username": "worker1",
        "role": "worker",
        "name": "Mike",
        "email": "mike@buildflow.com",
        "worker_name": "Mike Construction",
        "managed_projects": [],
    },
    "worker2": {
        "username": "worker2",
        "role": "worker",
        "name": "Alisa Field",
        "email": "alisa@buildflow.com",
        "worker_name": "Alisa Field",
        "managed_projects": [],
    },
    "worker3": {
        "username": "worker3",
        "role": "worker",
        "name": "Construction Team A",
        "email": "teama@buildflow.com",
        "worker_name": "Construction Team A",
        "managed_projects": [],
    },
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user_by_username(username: str) -> Optional[Dict]:
    return DEMO_USERS.get(username)


def authenticate_user(username: str, password: str) -> Optional[Dict]:
    user = get_user_by_username(username)
    if not user:
        return None
    
    demo_password = _DEMO_USER_PASSWORDS.get(username)
    if not demo_password:
        return None
    
    if password != demo_password:
        return None
    
    return user.copy()