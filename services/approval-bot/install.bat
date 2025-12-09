@echo off
REM H3 Telegram Approval Bot - Installation Script
REM Run this once to install dependencies

echo ========================================
echo H3 Telegram Approval Bot - Installation
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.9+ and add to PATH
    pause
    exit /b 1
)
echo.

echo [2/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: pip install failed!
    pause
    exit /b 1
)
echo.

echo [3/3] Verifying installation...
python -c "import telegram; import watchdog; import aiosqlite; print('✅ All modules installed')"
if errorlevel 1 (
    echo ERROR: Module verification failed!
    pause
    exit /b 1
)
echo.

echo ========================================
echo ✅ Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Ensure .env has TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
echo 2. Run: run.bat
echo.
pause
