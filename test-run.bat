@echo off
REM Test script - Run watcher and orchestrator together
cd /d "%~dp0"

echo Starting Filesystem Watcher in background...
start /B python scripts/filesystem_watcher.py AI_Employee_Vault

timeout /t 2 /nobreak >nul

echo Starting Orchestrator (will run for 30 seconds)...
python scripts/orchestrator.py AI_Employee_Vault
