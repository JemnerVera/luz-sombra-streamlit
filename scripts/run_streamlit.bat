@echo off
echo ========================================
echo    AGRICOLA LUZ-SOMBRA - STREAMLIT
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado. Instala Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python encontrado

echo.
echo [1/2] Instalando dependencias Streamlit...
pip install -r requirements_streamlit.txt
if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)
echo ✅ Dependencias instaladas

echo.
echo [2/2] Iniciando aplicación Streamlit...
echo.
echo 🌱 La aplicación se abrirá en tu navegador
echo 📱 URL: http://localhost:8501
echo.
echo Presiona Ctrl+C para detener la aplicación
echo.

streamlit run streamlit_app.py

