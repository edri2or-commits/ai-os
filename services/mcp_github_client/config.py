"""Configuration for MCP GitHub Client service"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Service configuration loaded from environment variables"""
    
    # GitHub API Configuration
    github_api_base_url: str = "https://api.github.com"
    github_pat: Optional[str] = None
    github_owner: str = "edri2or-commits"
    github_repo: str = "ai-os"
    
    # OpenAI Configuration (for AI-powered PR content generation)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    
    # Service Configuration
    log_level: str = "INFO"
    service_port: int = 8081
    
    # MCP Server Configuration (if needed for local MCP calls)
    mcp_server_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
