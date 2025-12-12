"""
AI-OS Agent Kernel
==================
FastAPI service that receives automation triggers from n8n.
This is the core orchestration layer that coordinates between:
- n8n workflows (automation triggers)
- OS Core (ADHD-aware task processing)
- External services (via MCP)

Port: 8084
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI-OS Agent Kernel",
    description="Core orchestration service for AI-OS automation",
    version="0.1.0"
)

# ============================================================================
# Data Models
# ============================================================================

class SyncRequest(BaseModel):
    """Request model for context sync trigger"""
    triggered_by: Optional[str] = "manual"
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class SyncResponse(BaseModel):
    """Response model for context sync"""
    status: str
    message: str
    timestamp: str
    execution_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

# ============================================================================
# Health Check Endpoint
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "service": "AI-OS Agent Kernel",
        "status": "online",
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "agent_kernel",
        "uptime": "active",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "daily_sync": "/daily-context-sync/run",
            "health": "/health"
        }
    }

# ============================================================================
# Core Endpoint: Daily Context Sync
# ============================================================================

@app.post("/daily-context-sync/run", response_model=SyncResponse)
async def trigger_daily_context_sync(request: SyncRequest):
    """
    Receives daily context sync trigger from n8n.
    
    This endpoint is called by n8n's cron workflow to initiate
    the daily context synchronization process.
    
    Current Implementation (Slice 2C):
    - Mock response for integration testing
    - Validates incoming request
    - Returns success confirmation
    
    Future Implementation (Slice 2D+):
    - Trigger OS Core context loading
    - Coordinate with MCP services
    - Return detailed execution status
    """
    try:
        # Log incoming trigger
        logger.info(f"Daily context sync triggered by: {request.triggered_by}")
        logger.info(f"Request timestamp: {request.timestamp}")
        
        # Generate execution ID
        execution_id = f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Prepare response
        response = SyncResponse(
            status="success",
            message="Context Sync Initiated",
            timestamp=datetime.now().isoformat(),
            execution_id=execution_id,
            details={
                "triggered_by": request.triggered_by,
                "received_at": datetime.now().isoformat(),
                "phase": "mock_response",
                "note": "Full logic will be implemented in Slice 2D+"
            }
        )
        
        logger.info(f"Context sync response prepared: {execution_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing context sync: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# ============================================================================
# Additional Endpoints (Future)
# ============================================================================

@app.post("/task/submit")
async def submit_task():
    """
    Future endpoint for submitting tasks to OS Core.
    To be implemented in later slices.
    """
    return {
        "status": "not_implemented",
        "message": "This endpoint will be implemented in future slices"
    }

# ============================================================================
# Startup Event
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Execute on service startup"""
    logger.info("=" * 60)
    logger.info("AI-OS Agent Kernel Starting...")
    logger.info(f"Service: Agent Kernel v0.1.0")
    logger.info(f"Port: 8084")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Execute on service shutdown"""
    logger.info("AI-OS Agent Kernel Shutting Down...")
