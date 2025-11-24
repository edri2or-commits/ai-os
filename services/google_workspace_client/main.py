"""Google Workspace Client - Main FastAPI application"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI-OS Google Workspace Client",
    description="HTTP service for Google Workspace operations (Gmail, Calendar, Drive, etc.)",
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

# Import routers
from .api.routes_gmail import router as gmail_router
from .api.routes_calendar import router as calendar_router
from .api.routes_drive import router as drive_router
from .api.routes_sheets import router as sheets_router
from .api.routes_docs import router as docs_router
from .api.routes_tasks import router as tasks_router

# Include routers
app.include_router(gmail_router)
app.include_router(calendar_router)
app.include_router(drive_router)
app.include_router(sheets_router)
app.include_router(docs_router)
app.include_router(tasks_router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "ok": True,
        "service": "AI-OS Google Workspace Client",
        "version": "0.1.0",
        "message": "Service is running"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    from .core.google_client import google_client
    
    return {
        "ok": True,
        "service": "AI-OS Google Workspace Client",
        "google_configured": google_client.is_authenticated(),
        "available_services": ["gmail", "calendar", "drive", "sheets", "docs", "tasks"]
    }


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting Google Workspace Client on port {settings.service_port}")
    uvicorn.run(app, host="0.0.0.0", port=settings.service_port)
