# 🚀 Complete Startup Guide - Fake News Detection System

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                             │
│                  http://localhost:3000                       │
│         (Paste news text → Click "Analyze with AI")         │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP Request (text)
                 ▼
┌─────────────────────────────────────────────────────────────┐
│         NEXT.JS REACT FRONTEND (Terminal 2)                 │
│              Port: 3000                                      │
│    • fake-news-detector.tsx component                       │
│    • Sends POST /predict to backend API                     │
│    • Displays results with confidence                       │
└────────────────┬────────────────────────────────────────────┘
                 │ POST /predict {text}
                 ▼
┌─────────────────────────────────────────────────────────────┐
│        FASTAPI PYTHON BACKEND (Terminal 1)                  │
│              Port: 8000                                      │
│    • server/main.py                                         │
│    • Loads model artifacts at startup                       │
│    • Vectorizes text with TF-IDF                            │
│    • Predicts with Logistic Regression                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│        MACHINE LEARNING MODEL (Loaded in Memory)            │
│                                                              │
│    📦 fake_news_vectorizer.pkl                              │
│       (TF-IDF Text Vectorization)                           │
│                                                              │
│    🤖 fake_news_model.pkl                                   │
│       (Logistic Regression Classifier)                      │
│       Input: TF-IDF vector                                  │
│       Output: "REAL" or "FAKE" + confidence %               │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚡ Quick Start (Recommended)

### For Windows Users:
**Double-click this file:**
```
D:\Fake_news_Detection\start-system.bat
```

This will:
1. ✅ Start AI Server on port 8000 (Terminal 1)
2. ✅ Start Web UI on port 3000 (Terminal 2)
3. ✅ Open http://localhost:3000 in your browser
4. ✅ Display system status

**Expected Result:**
- Two terminal windows appear
- Browser opens at http://localhost:3000
- You see the Fake News Detector interface

---

## 📋 Manual Startup (If Batch File Doesn't Work)

### Terminal 1: Start AI Server
```powershell
cd D:\Fake_news_Detection
.\.venv\Scripts\python.exe -m uvicorn server.main:app --host 127.0.0.1 --port 8000 --reload
```

**Wait for this message:**
```
INFO:     Loaded vectorizer and model successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

✅ **Server 1 Ready** - Don't close this terminal!

---

### Terminal 2: Start Web UI
**Open a NEW terminal window, then:**
```powershell
cd D:\Fake_news_Detection
pnpm dev
```

**Wait for this message:**
```
  ▲ Next.js 16.0.10
  - Local:        http://localhost:3000
```

✅ **Server 2 Ready** - Don't close this terminal!

---

### Terminal 3: Open Browser
**Open a web browser to:**
```
http://localhost:3000
```

✅ **You should see the Fake News Detector UI!**

---

## 🧪 Testing Once Everything is Running

### Web UI Testing (Easiest):

1. **In the browser at http://localhost:3000**
2. **Paste a news headline/article in the text box**
3. **Click "Analyze with AI"**
4. **View the result:**
   - ✅ Verdict: REAL or FAKE
   - ✅ Confidence: percentage (0-100%)
   - ✅ Model Name: Sklearn TF-IDF + Classifier

### Test Headlines:

| Text | Expected | Notes |
|------|----------|-------|
| "Scientists find cure for disease" | REAL | Legitimate news |
| "Aliens invade Earth - NASA coverup" | FAKE | Suspicious claim |
| "Stock market hits new record" | REAL | Financial news |
| "President secretly on Mars" | FAKE | Conspiracy |

---

## 🔧 Direct API Testing (PowerShell)

**If you want to test the API directly without the UI:**

### Test 1: Health Check
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -Method GET | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

**Expected Output:**
```
status       model_loaded
------       ------------
ok           True
```

### Test 2: Make Prediction
```powershell
$json = @{text="Breaking news about economic growth"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://127.0.0.1:8000/predict" -Method POST -Body $json -ContentType "application/json" | Select-Object -ExpandProperty Content | ConvertFrom-Json | Format-Table
```

**Expected Output:**
```
verdict confidence modelName
------- ---------- ---------
REAL         84.19 Sklearn TF-IDF + Classifier
```

---

## ✅ Verification Checklist

- [ ] Virtual environment exists at `.venv/`
- [ ] Python packages installed (uvicorn, fastapi, scikit-learn, etc.)
- [ ] Model files present:
  - [ ] `model/fake_news_model.pkl`
  - [ ] `model/fake_news_vectorizer.pkl`
- [ ] Node packages installed (pnpm install completed)
- [ ] Terminal 1 shows "Uvicorn running on http://127.0.0.1:8000"
- [ ] Terminal 2 shows "Local: http://localhost:3000"
- [ ] Browser loads http://localhost:3000 successfully
- [ ] Text input and button are visible in browser
- [ ] Can paste text and click analyze
- [ ] Prediction results appear with verdict + confidence

---

## 📊 What Each Component Does

### AI Server (server/main.py)
- **Runs**: FastAPI web framework
- **Port**: 8000
- **On Startup**: Loads both pickle files into memory
- **Endpoints**:
  - `GET /health` → Returns model status
  - `POST /predict` → Accepts text, returns verdict

### Web UI (components/fake-news-detector.tsx)
- **Framework**: React with Next.js
- **Port**: 3000
- **Features**:
  - Text input area
  - Analyze button
  - Real-time API calls
  - Displays results

### ML Model (model/ folder)
- **Vectorizer**: TF-IDF (Text Feature Extraction)
- **Classifier**: Logistic Regression (Binary Classification)
- **Classes**: 0 (REAL) or 1 (FAKE)
- **Output**: Probability scores

---

## 🚨 Troubleshooting

### Issue: "Port 8000 already in use"
```powershell
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: "Port 3000 already in use"
```powershell
# Find and kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Issue: "pnpm: command not found"
```powershell
npm install -g pnpm
```

### Issue: "Cannot find module 'react'"
```powershell
cd D:\Fake_news_Detection
pnpm install
```

### Issue: "Model files not found"
**Check these files exist:**
- `D:\Fake_news_Detection\model\fake_news_model.pkl`
- `D:\Fake_news_Detection\model\fake_news_vectorizer.pkl`

---

## 📝 File Structure

```
D:\Fake_news_Detection\
├── .venv/                          # Python virtual environment
├── node_modules/                   # Node.js dependencies (after pnpm install)
├── app/                            # Next.js app directory
├── components/
│   ├── fake-news-detector.tsx     # ✨ Main UI component
│   └── ...
├── model/
│   ├── fake_news_model.pkl        # ✅ ML classifier
│   ├── fake_news_vectorizer.pkl   # ✅ TF-IDF vectorizer
│   └── ...
├── server/
│   ├── main.py                    # ✨ FastAPI backend
│   └── requirements.txt
├── start-system.bat               # ✨ Windows startup script
├── start-system.sh                # ✨ Linux/Mac startup script
├── MANUAL_TESTING_GUIDE.md        # This file
└── package.json
```

---

## 🎯 Success Criteria

You'll know everything is working when:

1. ✅ Both terminal windows show "running" messages
2. ✅ Browser opens at http://localhost:3000
3. ✅ Text input box is visible and clickable
4. ✅ Can paste text into the input
5. ✅ "Analyze with AI" button is clickable
6. ✅ After clicking, a loading spinner appears
7. ✅ After 2-3 seconds, results appear showing:
   - Verdict (REAL or FAKE)
   - Confidence percentage
   - Model name

---

## 🎉 Next Steps

Once running:
1. **Try the test headlines** provided above
2. **Experiment with different news texts**
3. **Observe the confidence scores**
4. **Check the API directly** using the PowerShell tests
5. **Monitor the terminal windows** to see API calls logging

---

## 📞 Quick Reference

| Action | Command |
|--------|---------|
| Start All | Double-click `start-system.bat` |
| Start AI Server | `.\.venv\Scripts\python.exe -m uvicorn server.main:app --host 127.0.0.1 --port 8000` |
| Start Web UI | `pnpm dev` |
| Health Check | `Invoke-WebRequest -Uri http://127.0.0.1:8000/health` |
| Stop Servers | Close both terminal windows |
| View Logs | Check the terminal windows (don't close them) |

---

**You're all set! Open http://localhost:3000 and start detecting fake news!** 🚀
