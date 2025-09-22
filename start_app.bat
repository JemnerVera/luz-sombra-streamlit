@echo off
echo ========================================
echo    AGRICOLA LUZ-SOMBRA SUPERVISADO
echo ========================================
echo.

echo Iniciando aplicacion...
echo.

echo [1/3] Iniciando Backend (FastAPI)...
start "Backend API" cmd /k "cd /d %~dp0 && .\venv\Scripts\python.exe api.py"
timeout /t 3 /nobreak >nul

echo [2/3] Iniciando Frontend (React)...
start "Frontend React" cmd /k "cd /d %~dp0\frontend-react && npm install && npm start"
timeout /t 3 /nobreak >nul

echo [3/3] Abriendo navegador...
timeout /t 5 /nobreak >nul
start http://localhost:3000

echo.
echo ========================================
echo    APLICACION INICIADA CORRECTAMENTE
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend:    http://localhost:3000
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul
