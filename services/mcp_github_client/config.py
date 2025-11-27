"""Configuration for MCP GitHub Client service"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

# Get the directory where this config file is located
CONFIG_DIR = Path(__file__).parent
ENV_FILE = CONFIG_DIR / ".env"


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
    github_client_port: Optional[int] = None  # Alias for service_port
    
    # MCP Server Configuration (if needed for local MCP calls)
    mcp_server_url: Optional[str] = None
    
    class Config:
        env_file = str(ENV_FILE)
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra env vars from other services


# Global settings instance
settings = Settings()
