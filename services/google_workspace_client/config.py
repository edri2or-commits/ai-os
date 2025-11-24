"""Configuration for Google Workspace Client service"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Service configuration loaded from environment variables"""
    
    # Service Configuration
    service_port: int = 8082
    log_level: str = "INFO"
    
    # Google OAuth Configuration
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_token_file: str = "token.json"
    google_credentials_file: str = "credentials.json"
    
    # Google API Scopes
    google_scopes: list = [
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/documents",
        "https://www.googleapis.com/auth/tasks",
    ]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra env vars from other services


# Global settings instance
settings = Settings()
