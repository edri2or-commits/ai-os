@echo off
REM MCP GitHub Client - Service Launcher
REM AI-OS v2 - Infrastructure Layer

echo ================================================
echo   AI-OS MCP GitHub Client
echo   Starting service on port 8081...
echo ================================================
echo.

REM Check if .env file exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo.
    echo Please create .env from .env.example:
    echo   1. Copy .env.example to .env
    echo   2. Add your GitHub Personal Access Token
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist main.py (
    echo [ERROR] main.py not found!
    echo.
    echo Please run this script from services/mcp_github_client/
    echo.
    pause
    exit /b 1
)

echo [INFO] Starting FastAPI service...
echo [INFO] Service URL: http://localhost:8081
echo [INFO] Health check: http://localhost:8081/health
echo [INFO] Press Ctrl+C to stop the service
echo.

REM Change to project root to support relative imports
cd ..\..
python -m uvicorn services.mcp_github_client.main:app --host 0.0.0.0 --port 8081 --reload

if errorlevel 1 (
    echo.
    echo [ERROR] Service failed to start!
    echo.
    echo Common issues:
    echo   - Missing dependencies: pip install -r requirements.txt
    echo   - Port 8081 already in use
    echo   - Invalid .env configuration
    echo.
    pause
)
