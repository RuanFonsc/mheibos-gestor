@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0instalar_mheibos_gestor_cliente.ps1" %*
echo.
pause
