@echo off
setlocal
cd /d "%~dp0"

set DJANGO_DEBUG=True
set DJANGO_ALLOWED_HOSTS=*
set PYTHONUNBUFFERED=1

echo.
echo Mheibos Gestor - servidor de rede
echo.
echo Este computador sera o servidor central.
echo Deixe esta janela aberta enquanto outros computadores usam o sistema.
echo.
echo Enderecos provaveis para os clientes:
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr /C:"IPv4"') do (
  echo   http://%%A:8001/
)
echo.

if not exist ".venv\Scripts\python.exe" (
  echo Python da .venv nao encontrado.
  echo Rode a instalacao das dependencias neste computador antes de iniciar.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" manage.py migrate
if errorlevel 1 (
  echo.
  echo Nao foi possivel aplicar/verificar as migracoes.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" manage.py runserver 0.0.0.0:8001 --noreload
pause
