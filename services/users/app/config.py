from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # MongoDB
    MONGODB_URI: str = "mongodb://localhost:27017/platform_db"
    MONGODB_DB_NAME: str = "platform_db"
    
    # Service
    SERVICE_NAME: str = "users"
    LOG_LEVEL: str = "INFO"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3001", "http://localhost:5173"]
    
    # JWT
    JWT_SECRET: str = "change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24 * 7  # 7 days
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
