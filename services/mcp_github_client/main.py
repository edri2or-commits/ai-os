"""MCP GitHub Client - Main FastAPI application"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api import github_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI-OS MCP GitHub Client",
    description="HTTP service for GitHub operations via MCP - The heart of AI-OS",
    version="0.1.0"
)

# Add CORS middleware (for GPT Custom Actions)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(github_router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "ok": True,
        "service": "AI-OS MCP GitHub Client",
        "version": "0.1.0",
        "message": "Service is running"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "ok": True,
        "service": "AI-OS MCP GitHub Client",
        "github_configured": settings.github_pat is not None,
        "openai_configured": settings.openai_api_key is not None,
        "repository": f"{settings.github_owner}/{settings.github_repo}"
    }


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting MCP GitHub Client on port {settings.service_port}")
    uvicorn.run(app, host="0.0.0.0", port=settings.service_port)
