@echo off
REM AI Employee Bronze Tier - Startup Script
REM This script starts both the Filesystem Watcher and Orchestrator

echo ============================================================
echo AI Employee Bronze Tier - Starting...
echo ============================================================
echo.

cd /d "%~dp0"

echo Starting Filesystem Watcher...
start "AI Employee - Filesystem Watcher" cmd /k "python scripts/filesystem_watcher.py AI_Employee_Vault"

timeout /t 2 /nobreak >nul

echo Starting Orchestrator...
start "AI Employee - Orchestrator" cmd /k "python scripts/orchestrator.py AI_Employee_Vault"

echo.
echo ============================================================
echo Both services started!
echo.
echo Windows opened:
echo   1. AI Employee - Filesystem Watcher
echo   2. AI Employee - Orchestrator
echo.
echo To stop: Close both windows or press Ctrl+C in each
echo ============================================================
echo.
echo To test: Drop a file in AI_Employee_Vault\Inbox\
echo.
