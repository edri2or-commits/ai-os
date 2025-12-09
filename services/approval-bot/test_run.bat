@echo off
cd /d "%~dp0"
echo Starting Telegram Bot...
.\venv-telegram\Scripts\python.exe backend.py
pause
