@echo off
cd /d "%~dp0"
echo ========================================
echo  FPS++ System Optimizer
echo ========================================
echo.
echo Iniciando o aplicativo via Python...
echo.

python src\main.py

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo  ERRO ao iniciar o aplicativo.
    echo  Verifique se o Python esta instalado e
    echo  as dependencias estao configuradas:
    echo    python -m pip install -r requirements.txt
    echo ========================================
    pause
    exit /b 1
)