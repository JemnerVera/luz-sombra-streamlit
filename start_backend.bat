@echo off
echo ========================================
echo    BACKEND API - LUZ-SOMBRA
echo ========================================
echo.

echo Iniciando Backend (FastAPI)...
echo.
echo API disponible en: http://localhost:8000
echo Documentacion:     http://localhost:8000/docs
echo.

cd /d %~dp0
.\venv\Scripts\python.exe api.py

pause
