"""
Agent Kernel Server - FastAPI HTTP Interface to LangGraph

Provides HTTP endpoints to trigger LangGraph workflows.
Currently supports: Daily Context Sync
"""

import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware

# Import graphs
from graphs.daily_context_sync_graph import run_daily_context_sync

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI-OS Agent Kernel",
    description="HTTP service for LangGraph-based AI-OS workflows",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- API Endpoints ---

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "ok": True,
        "service": "AI-OS Agent Kernel",
        "version": "0.1.0",
        "message": "Agent Kernel is running",
        "workflows": {
            "daily_context_sync": "/daily-context-sync/run"
        }
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "ok": True,
        "service": "AI-OS Agent Kernel",
        "version": "0.1.0",
        "workflows": {
            "daily_context_sync": {
                "endpoint": "/daily-context-sync/run",
                "method": "POST",
                "status": "available"
            }
        }
    }


@app.post("/daily-context-sync/run")
async def run_daily_context_sync_endpoint(
    x_trace_id: Optional[str] = Header(None, alias="X-Trace-ID")
) -> Dict[str, Any]:
    """
    Execute Daily Context Sync workflow
    
    Headers:
        X-Trace-ID (optional): Trace identifier for observability
    
    This workflow:
    1. Reads current state from OS Core MCP
    2. Computes patch with updated timestamp
    3. Applies patch and logs events
    
    Returns:
    {
        "status": "ok" | "error",
        "last_sync_time": "2025-11-27T15:30:00Z",
        "trace_id": "..." (if provided),
        "error": "error message" (if status == "error")
    }
    """
    trace_id = x_trace_id or "no-trace"
    logger.info(f"Executing Daily Context Sync workflow... [trace_id={trace_id}]")
    
    try:
        result = run_daily_context_sync(trace_id=trace_id)
        
        logger.info(f"Daily Context Sync completed: {result['status']} [trace_id={trace_id}]")
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
        
        # Include trace_id in response
        result["trace_id"] = trace_id
        
        return result
        
    except Exception as e:
        logger.error(f"Error executing Daily Context Sync: {e} [trace_id={trace_id}]")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8084)
