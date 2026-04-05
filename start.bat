@echo off
echo ========================================
echo   MediScan AI Pro - Starting Server
echo ========================================
echo.

cd /d "%~dp0backend"
call venv\Scripts\activate

echo Starting MediScan AI Pro...
echo Open http://localhost:8000 in your browser
echo.

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
