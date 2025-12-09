@echo off
REM H3 Telegram Approval Bot - Run Script

echo ========================================
echo H3 Telegram Approval Bot - Starting
echo ========================================
echo.

cd /d "%~dp0"

REM Check if dependencies are installed
python -c "import telegram" 2>nul
if errorlevel 1 (
    echo ERROR: Dependencies not installed!
    echo Please run: install.bat
    pause
    exit /b 1
)

REM Check .env
if not exist "..\..\..\.env" (
    echo ERROR: .env file not found!
    echo Please create .env with:
    echo   TELEGRAM_BOT_TOKEN=your_token
    echo   TELEGRAM_CHAT_ID=your_chat_id
    pause
    exit /b 1
)

echo Starting backend...
echo.
echo 📁 Watching: truth-layer\drift\approvals\pending
echo 📱 Telegram: Your configured bot
echo 💾 Database: approvals.db
echo.
echo Press CTRL+C to stop
echo ========================================
echo.

venv-py311-clean\Scripts\python.exe backend.py

pause
