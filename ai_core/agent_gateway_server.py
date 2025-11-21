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
from fastapi.responses import HTMLResponse
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


@app.get("/system/health")
async def system_health():
    """
    Comprehensive system health check.
    
    Checks all core components:
    - API Key configuration
    - GPT Planner
    - Intent Router
    - Action Executor
    - Git operations
    - File system access
    
    Returns detailed status for each component.
    """
    import os
    from pathlib import Path
    import subprocess
    from dotenv import load_dotenv
    
    # Reload .env to get latest values
    load_dotenv(override=True)
    
    health_status = {
        "overall_status": "healthy",
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "components": {}
    }
    
    # Check 1: API Key Configuration
    try:
        api_key = os.getenv('OPENAI_API_KEY', '')
        demo_mode = os.getenv('DEMO_MODE', 'false').lower() == 'true'
        
        if demo_mode:
            health_status["components"]["api_key"] = {
                "status": "warning",
                "mode": "demo",
                "message": "Running in Demo Mode (simulated GPT)"
            }
        elif api_key and api_key.startswith('sk-'):
            masked_key = f"{api_key[:7]}...{api_key[-4:]}"
            health_status["components"]["api_key"] = {
                "status": "healthy",
                "mode": "real",
                "message": f"API key configured: {masked_key}"
            }
        else:
            health_status["components"]["api_key"] = {
                "status": "error",
                "mode": "none",
                "message": "No valid API key found"
            }
            health_status["overall_status"] = "degraded"
    except Exception as e:
        health_status["components"]["api_key"] = {
            "status": "error",
            "message": f"Failed to check API key: {str(e)}"
        }
        health_status["overall_status"] = "degraded"
    
    # Check 2: GPT Planner
    try:
        from ai_core.gpt_orchestrator import REPO_ROOT
        
        # Check if SSOT files exist
        ssot_exists = (REPO_ROOT / "docs" / "CONSTITUTION.md").exists()
        
        if ssot_exists:
            health_status["components"]["gpt_planner"] = {
                "status": "healthy",
                "message": "GPT Planner module loaded, SSOT files present"
            }
        else:
            health_status["components"]["gpt_planner"] = {
                "status": "warning",
                "message": "GPT Planner loaded but SSOT files missing"
            }
    except Exception as e:
        health_status["components"]["gpt_planner"] = {
            "status": "error",
            "message": f"Failed to load GPT Planner: {str(e)}"
        }
        health_status["overall_status"] = "degraded"
    
    # Check 3: Intent Router
    try:
        from ai_core.intent_router import VALID_ACTION_TYPES
        
        if len(VALID_ACTION_TYPES) > 0:
            health_status["components"]["intent_router"] = {
                "status": "healthy",
                "message": f"Intent Router loaded, {len(VALID_ACTION_TYPES)} action types supported"
            }
        else:
            health_status["components"]["intent_router"] = {
                "status": "warning",
                "message": "Intent Router loaded but no action types defined"
            }
    except Exception as e:
        health_status["components"]["intent_router"] = {
            "status": "error",
            "message": f"Failed to load Intent Router: {str(e)}"
        }
        health_status["overall_status"] = "degraded"
    
    # Check 4: Action Executor
    try:
        from ai_core.action_executor import execute_actions
        
        health_status["components"]["action_executor"] = {
            "status": "healthy",
            "message": "Action Executor module loaded"
        }
    except Exception as e:
        health_status["components"]["action_executor"] = {
            "status": "error",
            "message": f"Failed to load Action Executor: {str(e)}"
        }
        health_status["overall_status"] = "degraded"
    
    # Check 5: Git Operations
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            git_version = result.stdout.strip()
            health_status["components"]["git"] = {
                "status": "healthy",
                "message": git_version
            }
        else:
            health_status["components"]["git"] = {
                "status": "error",
                "message": "Git command failed"
            }
            health_status["overall_status"] = "degraded"
    except Exception as e:
        health_status["components"]["git"] = {
            "status": "error",
            "message": f"Git not available: {str(e)}"
        }
        health_status["overall_status"] = "degraded"
    
    # Check 6: File System Access
    try:
        project_root = Path(__file__).parent.parent
        
        # Check read access
        readme = project_root / "README.md"
        read_ok = readme.exists() and readme.is_file()
        
        # Check write access (try to create temp file)
        test_file = project_root / ".health_check_test"
        try:
            test_file.write_text("test")
            write_ok = True
            test_file.unlink()  # Clean up
        except:
            write_ok = False
        
        if read_ok and write_ok:
            health_status["components"]["filesystem"] = {
                "status": "healthy",
                "message": "Read and write access OK"
            }
        elif read_ok:
            health_status["components"]["filesystem"] = {
                "status": "warning",
                "message": "Read OK, write failed"
            }
        else:
            health_status["components"]["filesystem"] = {
                "status": "error",
                "message": "File system access failed"
            }
            health_status["overall_status"] = "degraded"
    except Exception as e:
        health_status["components"]["filesystem"] = {
            "status": "error",
            "message": f"File system check failed: {str(e)}"
        }
        health_status["overall_status"] = "degraded"
    
    # Check 7: Agent Gateway
    try:
        from ai_core.agent_gateway import plan_and_optionally_execute
        
        health_status["components"]["agent_gateway"] = {
            "status": "healthy",
            "message": "Agent Gateway module loaded"
        }
    except Exception as e:
        health_status["components"]["agent_gateway"] = {
            "status": "error",
            "message": f"Failed to load Agent Gateway: {str(e)}"
        }
        health_status["overall_status"] = "degraded"
    
    return health_status


@app.get("/system/dashboard", response_class=HTMLResponse)
async def system_dashboard():
    """
    HTML Dashboard for system health visualization.
    
    Provides a visual representation of all component statuses.
    """
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI-OS System Health Dashboard</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .header {
                background: white;
                border-radius: 12px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            h1 {
                font-size: 32px;
                margin-bottom: 10px;
                color: #1a202c;
            }
            
            .status-badge {
                display: inline-block;
                padding: 6px 16px;
                border-radius: 20px;
                font-weight: 600;
                font-size: 14px;
                text-transform: uppercase;
            }
            
            .status-healthy {
                background: #48bb78;
                color: white;
            }
            
            .status-warning {
                background: #ed8936;
                color: white;
            }
            
            .status-degraded {
                background: #f56565;
                color: white;
            }
            
            .status-error {
                background: #c53030;
                color: white;
            }
            
            .components-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .component-card {
                background: white;
                border-radius: 12px;
                padding: 24px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            }
            
            .component-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 8px 12px rgba(0,0,0,0.15);
            }
            
            .component-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }
            
            .component-name {
                font-size: 18px;
                font-weight: 600;
                color: #2d3748;
            }
            
            .component-status {
                width: 12px;
                height: 12px;
                border-radius: 50%;
            }
            
            .status-dot-healthy {
                background: #48bb78;
            }
            
            .status-dot-warning {
                background: #ed8936;
            }
            
            .status-dot-error {
                background: #f56565;
            }
            
            .component-message {
                color: #718096;
                font-size: 14px;
                line-height: 1.5;
            }
            
            .footer {
                text-align: center;
                color: white;
                margin-top: 30px;
                font-size: 14px;
            }
            
            .refresh-info {
                color: #cbd5e0;
                margin-top: 10px;
            }
            
            .loading {
                text-align: center;
                padding: 40px;
            }
            
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥 AI-OS System Health Dashboard</h1>
                <p id="timestamp" style="color: #718096; margin-top: 8px;">Loading...</p>
                <div id="overall-status" style="margin-top: 16px;"></div>
            </div>
            
            <div id="components" class="components-grid">
                <div class="loading">
                    <div class="spinner"></div>
                    <p style="margin-top: 16px; color: white;">Loading system status...</p>
                </div>
            </div>
            
            <div class="footer">
                <p>AI-OS Agent Gateway v1.0</p>
                <p class="refresh-info">Auto-refreshes every 30 seconds</p>
            </div>
        </div>
        
        <script>
            async function loadHealth() {
                try {
                    const response = await fetch('/system/health');
                    const data = await response.json();
                    
                    // Update timestamp
                    const timestamp = new Date(data.timestamp).toLocaleString();
                    document.getElementById('timestamp').textContent = `Last updated: ${timestamp}`;
                    
                    // Update overall status
                    const overallStatus = data.overall_status;
                    const statusClass = `status-${overallStatus}`;
                    document.getElementById('overall-status').innerHTML = `
                        <span class="status-badge ${statusClass}">
                            Overall Status: ${overallStatus}
                        </span>
                    `;
                    
                    // Update components
                    const componentsDiv = document.getElementById('components');
                    componentsDiv.innerHTML = '';
                    
                    for (const [name, component] of Object.entries(data.components)) {
                        const statusDotClass = `status-dot-${component.status}`;
                        const componentName = name.replace(/_/g, ' ').toUpperCase();
                        
                        const card = document.createElement('div');
                        card.className = 'component-card';
                        card.innerHTML = `
                            <div class="component-header">
                                <div class="component-name">${componentName}</div>
                                <div class="component-status ${statusDotClass}"></div>
                            </div>
                            <div class="component-message">${component.message}</div>
                        `;
                        componentsDiv.appendChild(card);
                    }
                    
                } catch (error) {
                    console.error('Failed to load health status:', error);
                    document.getElementById('components').innerHTML = `
                        <div class="component-card">
                            <div class="component-name">Error</div>
                            <div class="component-message">Failed to load system status</div>
                        </div>
                    `;
                }
            }
            
            // Load immediately
            loadHealth();
            
            // Refresh every 30 seconds
            setInterval(loadHealth, 30000);
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


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
