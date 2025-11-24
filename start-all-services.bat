@echo off
echo ====================================
echo    AI-OS Services Launcher
echo ====================================
echo.
echo Starting all services...
echo.

REM Get the directory of this script
cd /d "%~dp0"

echo [1/3] Starting GitHub Client (port 8081)...
start "AI-OS GitHub Client" cmd /k "python start_github_client.py"
timeout /t 3 /nobreak >nul

echo [2/3] Starting Google Workspace Client (port 8082)...
start "AI-OS Google Workspace" cmd /k "python -m uvicorn services.google_workspace_client.main:app --port 8082 --reload"
timeout /t 3 /nobreak >nul

echo [3/3] Starting ngrok tunnel...
start "AI-OS ngrok" cmd /k "ngrok http 8082"
timeout /t 3 /nobreak >nul

echo.
echo ====================================
echo    All services started!
echo ====================================
echo.
echo GitHub Client:     http://localhost:8081
echo Google Workspace:  http://localhost:8082
echo ngrok:             Check the ngrok window
echo.
echo Press any key to exit this window...
echo (Services will keep running)
pause >nul
