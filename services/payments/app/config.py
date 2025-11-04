from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # MongoDB
    MONGODB_URI: str = "mongodb://localhost:27017/platform_db"
    MONGODB_DB_NAME: str = "platform_db"
    
    # Service
    SERVICE_NAME: str = "payments"
    LOG_LEVEL: str = "INFO"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3001", "http://localhost:5173"]
    
    # Payment Provider (stub)
    STRIPE_API_KEY: str = "sk_test_dummy"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()