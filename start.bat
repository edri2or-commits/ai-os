@echo off
REM AI-OS One-Command Startup - Windows Batch File
REM Double-click this file to start AI-OS

echo ======================================================================
echo AI-OS - Starting...
echo ======================================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Run start.py
python start.py

REM If error, pause so user can see message
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ======================================================================
    echo Error starting AI-OS
    echo ======================================================================
    pause
)
