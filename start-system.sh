#!/bin/bash
# Fake News Detection System - Startup Script (macOS/Linux)

echo ""
echo "========================================"
echo "  FAKE NEWS DETECTION SYSTEM"
echo "  Automated Startup Script"
echo "========================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "[1/2] Starting AI Model Server (port 8000)..."
echo "      Loading TF-IDF vectorizer and classifier..."
cd "$SCRIPT_DIR"

# Start AI server in background
./venv/bin/python -m uvicorn server.main:app --host 127.0.0.1 --port 8000 --reload &
AI_PID=$!
sleep 3

echo ""
echo "[2/2] Starting Web UI Server (port 3000)..."
echo "      Running Next.js React frontend..."

# Start web server in background
pnpm dev &
WEB_PID=$!
sleep 5

echo ""
echo "========================================"
echo "   ✅ SYSTEM STARTUP COMPLETE"
echo "========================================"
echo ""
echo "📊 SERVERS STATUS:"
echo "   • AI Model API:  http://127.0.0.1:8000"
echo "   • Web UI:        http://localhost:3000"
echo ""
echo "🌐 OPEN YOUR BROWSER:"
echo "   → http://localhost:3000"
echo ""
echo "💡 RUNNING PROCESSES:"
echo "   PID $AI_PID: Python FastAPI Server (port 8000)"
echo "   PID $WEB_PID: Next.js React App (port 3000)"
echo ""
echo "⏹️  To stop all servers:"
echo "   kill $AI_PID $WEB_PID"
echo "   or press CTRL+C"
echo ""
echo "========================================"
echo ""

# Open browser if available
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:3000
elif command -v open > /dev/null; then
    open http://localhost:3000
fi

# Wait for both processes
wait
