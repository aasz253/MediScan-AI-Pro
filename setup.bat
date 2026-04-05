@echo off
echo ========================================
echo   MediScan AI Pro - Setup Script
echo ========================================
echo.

cd /d "%~dp0backend"

echo [1/3] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo [2/3] Installing dependencies...
pip install -r requirements.txt

echo [3/3] Setup complete!
echo.
echo To start the application, run: start.bat
echo.
pause
