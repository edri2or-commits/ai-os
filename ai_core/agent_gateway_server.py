"""
Agent Gateway HTTP API Server

FastAPI server that exposes Agent Gateway via HTTP endpoints.
This allows external agents (Custom GPT, Telegram, etc) to interact with AI-OS.

Run with:
    python -m ai_core.agent_gateway_server

Or:
    uvicorn ai_core.agent_gateway_server:app --reload
"""

import sys
from pathlib import Path
from typing import Optional

# Ensure project root is in path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ai_core.agent_gateway import plan_and_optionally_execute


# Pydantic models for request/response validation

class IntentRequest(BaseModel):
    """Request body for /api/v1/intent endpoint"""
    intent: str = Field(
        ...,
        description="User intent in natural language (Hebrew/English)",
        min_length=1,
        examples=["צור workflow חדש לניהול טוקנים"]
    )
    auto_execute: bool = Field(
        default=False,
        description="Execute actions automatically if validation passes"
    )
    dry_run: bool = Field(
        default=False,
        description="Simulate execution without making real changes (not fully implemented)"
    )


class IntentResponse(BaseModel):
    """Response from /api/v1/intent endpoint"""
    status: str = Field(
        ...,
        description="Status: plan_ready, success, validation_failed, etc"
    )
    intent: str = Field(
        ...,
        description="Original intent"
    )
    plan: Optional[dict] = Field(
        None,
        description="Full plan from GPT Planner"
    )
    validation: Optional[dict] = Field(
        None,
        description="Validation results"
    )
    execution: Optional[dict] = Field(
        None,
        description="Execution results (if auto_execute=True)"
    )
    message: str = Field(
        ...,
        description="Human-readable status message"
    )
    error: Optional[str] = Field(
        None,
        description="Error message if status indicates failure"
    )


# FastAPI app

app = FastAPI(
    title="AI-OS Agent Gateway API",
    description="HTTP API for interacting with AI-OS through natural language intents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (allow all origins for now - tighten in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "service": "AI-OS Agent Gateway API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "intent": "/api/v1/intent",
            "docs": "/docs",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "agent-gateway-api",
        "version": "1.0.0"
    }


@app.post(
    "/api/v1/intent",
    response_model=IntentResponse,
    summary="Process user intent",
    description="""
    Main endpoint for processing user intents.
    
    Takes a natural language intent, plans actions via GPT Planner,
    validates them, and optionally executes them.
    
    **Flow:**
    1. Intent → GPT Planner (structured plan)
    2. Intent Router (validation)
    3. Action Executor (if auto_execute=True)
    4. Return full results
    
    **Example:**
    ```json
    {
        "intent": "צור workflow חדש",
        "auto_execute": false
    }
    ```
    """
)
async def process_intent(request: IntentRequest) -> IntentResponse:
    """
    Process user intent through Agent Gateway.
    
    Args:
        request: IntentRequest with intent text and options
    
    Returns:
        IntentResponse with plan, validation, and execution results
    
    Raises:
        HTTPException: If an unexpected error occurs
    """
    try:
        # Call Agent Gateway
        result = plan_and_optionally_execute(
            intent=request.intent,
            auto_execute=request.auto_execute,
            dry_run=request.dry_run
        )
        
        # Return result as-is (already matches IntentResponse structure)
        return IntentResponse(**result)
    
    except Exception as e:
        # Unexpected error - return 500
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": str(e),
                "intent": request.intent
            }
        )


# Run server if called directly
if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("AI-OS Agent Gateway HTTP API Server")
    print("=" * 70)
    print("\n🚀 Starting server...")
    print("\n📍 Endpoints:")
    print("   - Root:        http://localhost:8000/")
    print("   - API:         http://localhost:8000/api/v1/intent")
    print("   - Docs:        http://localhost:8000/docs")
    print("   - Health:      http://localhost:8000/health")
    print("\n📖 API Documentation: http://localhost:8000/docs")
    print("\n⏸️  Press CTRL+C to stop")
    print("=" * 70)
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
