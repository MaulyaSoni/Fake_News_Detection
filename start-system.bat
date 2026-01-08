@echo off
REM Fake News Detection System - Startup Script

echo.
echo ========================================
echo   FAKE NEWS DETECTION SYSTEM
echo   Automated Startup Script
echo ========================================
echo.

REM Get the script directory
set SCRIPT_DIR=%~dp0

echo [1/3] Checking Python environment...
if not exist "%SCRIPT_DIR%.venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found at .venv
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)
echo ✓ Python environment found

echo.
echo [2/3] Starting AI Model Server (port 8000)...
echo        This loads the TF-IDF vectorizer and classifier model...
start "Fake News AI Server" cmd /k "cd %SCRIPT_DIR% && .\.venv\Scripts\python.exe -m uvicorn server.main:app --host 127.0.0.1 --port 8000 --reload"
echo ✓ AI Server starting in new window...
echo   Waiting for startup...
timeout /t 5 /nobreak

echo.
echo [3/3] Starting Web UI Server (port 3000)...
echo        This runs the Next.js React frontend...
start "Fake News Web UI" cmd /k "cd %SCRIPT_DIR% && pnpm dev"
echo ✓ Web UI starting in new window...
echo   Waiting for startup...
timeout /t 8 /nobreak

echo.
echo ========================================
echo   ✅ SYSTEM STARTUP COMPLETE
echo ========================================
echo.
echo 📊 SERVERS STATUS:
echo    • AI Model API:  http://127.0.0.1:8000
echo    • Web UI:        http://localhost:3000
echo.
echo 🌐 OPEN YOUR BROWSER:
echo    → http://localhost:3000
echo.
echo 💡 WHAT'S RUNNING:
echo    Terminal 1: Python FastAPI Server (port 8000)
echo    Terminal 2: Next.js React App (port 3000)
echo.
echo ⏹️  To stop: Close both terminal windows or press CTRL+C
echo.
echo ========================================
echo.

REM Optional: Open browser automatically
timeout /t 2 /nobreak
echo Opening browser...
start http://localhost:3000

echo System is ready. Two terminal windows are running in the background.
pause
