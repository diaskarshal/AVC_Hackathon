from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "BuildFlow ERP"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    DATABASE_URL: str = "postgresql://buildflow:buildflow123@db:5432/buildflow_db"
    
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".xlsx", ".xls", ".csv"}
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()