# 🚀 QUICK REFERENCE - Fake News Detection System

## ⚡ START THE SYSTEM IN 10 SECONDS

**Windows Users:**
```
Double-click: D:\Fake_news_Detection\start-system.bat
```

That's it! Everything starts automatically.

---

## 📖 START MANUALLY (If Needed)

**Terminal 1 - AI Server:**
```powershell
cd D:\Fake_news_Detection
.\.venv\Scripts\python.exe -m uvicorn server.main:app --host 127.0.0.1 --port 8000
```

Wait for:
```
INFO:     Loaded vectorizer and model successfully
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 - Web UI (NEW WINDOW):**
```powershell
cd D:\Fake_news_Detection
pnpm dev
```

Wait for:
```
Local:        http://localhost:3000
```

**Browser:**
```
http://localhost:3000
```

---

## 🎯 HOW TO USE (3 Steps)

1. **Paste** a news headline/article in the text box
2. **Click** "Analyze with AI" button
3. **See** the verdict (REAL or FAKE) with confidence %

---

## 📚 NEED HELP?

| Issue | File | Solution |
|-------|------|----------|
| How to start? | STARTUP_GUIDE.md | Read detailed instructions |
| How to test? | MANUAL_TESTING_GUIDE.md | Try the test examples |
| Technical details? | INTEGRATION_COMPLETE.md | Learn the architecture |
| Troubleshooting? | STARTUP_GUIDE.md | Common issues & fixes |
| System verified? | SETUP_CHECKLIST.md | See what's been tested |

---

## 🔗 URLS

| Service | URL | Purpose |
|---------|-----|---------|
| Web UI | http://localhost:3000 | Paste news & get predictions |
| Health Check | http://127.0.0.1:8000/health | Verify API is running |
| Predictions | http://127.0.0.1:8000/predict | API endpoint (POST) |

---

## 🧪 QUICK TEST

**Paste in the web UI:**
```
Scientists discover breakthrough in quantum computing
```

**Expected:**
```
Verdict: REAL
Confidence: ~85%
```

---

## ⚙️ WHAT'S INCLUDED

✅ Machine Learning Model (scikit-learn)  
✅ REST API Server (FastAPI)  
✅ Web Interface (React/Next.js)  
✅ Startup Scripts (Batch & Shell)  
✅ Complete Documentation  
✅ All Dependencies  

---

## 📦 WHAT GETS INSTALLED

- Python packages: fastapi, uvicorn, scikit-learn, numpy, joblib
- Node packages: react, next, typescript, tailwindcss, lucide-react, and 180+ more

---

## 🎬 WHAT HAPPENS WHEN YOU ANALYZE

1. Text sent to → AI Model API (port 8000)
2. Text converted to → TF-IDF vector
3. Vector processed by → Logistic Regression classifier
4. Result returned → "REAL" or "FAKE" + confidence %
5. UI displays → Verdict with visual styling

---

## ✅ VERIFICATION

Both servers must be running:

**Check AI Server:**
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -Method GET
```

**Check Web UI:**
```powershell
Invoke-WebRequest -Uri "http://localhost:3000" -Method GET
```

---

## 🔧 PORTS IN USE

- **8000** = AI Model API (FastAPI)
- **3000** = Web UI (Next.js)

If busy:
```powershell
netstat -ano | findstr :<port>
taskkill /PID <PID> /F
```

---

## 🚨 COMMON ERRORS

### "Port already in use"
```powershell
taskkill /PID <PID> /F
```

### "Module not found"
```powershell
cd D:\Fake_news_Detection
pnpm install
.\.venv\Scripts\python.exe -m pip install -r server/requirements.txt
```

### "Cannot load model"
Check files exist:
- `model/fake_news_model.pkl` ✓
- `model/fake_news_vectorizer.pkl` ✓

---

## 📊 SYSTEM INFO

- **Language:** Python (backend) + TypeScript/React (frontend)
- **ML Library:** scikit-learn
- **Model Type:** Logistic Regression + TF-IDF
- **Prediction Time:** <1 second
- **Confidence Range:** 0-100%
- **Accuracy:** ~85%

---

## 🎯 NEXT STEPS

1. Start the system (see above)
2. Open http://localhost:3000
3. Test with sample headlines
4. Experiment with different texts
5. Watch the confidence scores

---

## 📞 QUICK COMMANDS

| Task | Command |
|------|---------|
| Start everything | `start-system.bat` (double-click) |
| Start AI server | `.\.venv\Scripts\python.exe -m uvicorn server.main:app --port 8000` |
| Start web UI | `pnpm dev` |
| Check health | `Invoke-WebRequest -Uri http://127.0.0.1:8000/health` |
| Test prediction | See MANUAL_TESTING_GUIDE.md |
| Stop servers | Close both terminal windows |

---

**You're all set! Start the system now! 🚀**

Any questions? Check the documentation files (*.md) in the project folder.
