@echo off
REM AI Employee Bronze Tier - Stop Script
REM This script stops both the Filesystem Watcher and Orchestrator

echo ============================================================
echo AI Employee Bronze Tier - Stopping...
echo ============================================================
echo.

taskkill /F /FI "WINDOWTITLE eq AI Employee*" 2>nul

echo.
echo ============================================================
echo Both services stopped!
echo ============================================================
