@echo off
setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════════════════
echo   🚀 FAKE NEWS DETECTION - COMPLETE SYSTEM STARTUP
echo ════════════════════════════════════════════════════════════════════════
echo.

REM Check if port 8000 is in use and kill it
echo [STEP 1/3] Checking for port conflicts...
netstat -ano | findstr :8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  Port 8000 is in use. Killing existing process...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
        taskkill /PID %%a /F >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
    echo ✅ Port cleared
) else (
    echo ✅ Port 8000 is free
)

echo.
echo [STEP 2/3] Starting AI Model Server (FastAPI)...
echo 📍 Activating Python virtual environment...
call .\.venv\Scripts\activate.bat

echo 🚀 Starting server on http://127.0.0.1:8000...
start "Fake News Detection API Server" cmd /k ".\.venv\Scripts\python.exe -m uvicorn server.main:app --host 127.0.0.1 --port 8000"

timeout /t 4 /nobreak >nul

echo.
echo [STEP 3/3] Starting Web Application (Next.js Frontend)...
echo 🌐 Starting frontend on http://localhost:3000...
start "Fake News Detection Web UI" cmd /k "pnpm dev"

echo.
echo ════════════════════════════════════════════════════════════════════════
echo   ✅ SYSTEM STARTUP COMPLETE!
echo ════════════════════════════════════════════════════════════════════════
echo.
echo 📍 API Server:  http://127.0.0.1:8000
echo 🌐 Web UI:      http://localhost:3000
echo.
echo 📖 Next steps:
echo    1. Wait 5-10 seconds for servers to fully start
echo    2. Open your browser to http://localhost:3000
echo    3. Paste news text and click "Analyze with AI"
echo.
echo ⏹️  To stop: Close both command windows
echo.
pause
