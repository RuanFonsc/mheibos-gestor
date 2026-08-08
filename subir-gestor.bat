@echo off
setlocal

cd /d "%~dp0"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\open-mheibos-gestor\scripts\start-gestor.ps1"

echo.
pause
