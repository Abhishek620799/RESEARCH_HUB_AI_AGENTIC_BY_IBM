# ResearchHub AI - Configuration Settings
# Milestone 2: Activity 2.2 - Configure API credentials
# Responsible: Chetan Galphat

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Groq API Configuration
    groq_api_key: str = "your_groq_api_key_here"
    
    # JWT Security Configuration
    secret_key: str = "your_super_secret_jwt_key_here_min_32_chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database Configuration
    database_url: str = "sqlite:///./researchhub.db"
    
    # CORS Configuration
    backend_url: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    """Cache and return application settings."""
    return Settings()


settings = get_settings()
