# 🚀 How to Run the Fake News Detection System

## ✅ Prerequisites Verified
- ✅ Python 3.8+ with virtual environment configured
- ✅ Node.js dependencies installed (pnpm install completed)
- ✅ Model files present: `model/fake_news_model.pkl` and `model/fake_news_vectorizer.pkl`
- ✅ All required Python packages installed

---

## 📋 Quick Start (3 Steps)

### Step 1: Start the AI Model Server (Python Backend)
**In Terminal 1:**
```powershell
cd D:\Fake_news_Detection
.\.venv\Scripts\python.exe -m uvicorn server.main:app --host 127.0.0.1 --port 8000
```

**Expected Output:**
```
INFO:     Loaded vectorizer and model successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

✅ **Server is ready when you see this message!**

---

### Step 2: Start the Web Application (Next.js Frontend)
**In Terminal 2 (while Terminal 1 runs):**
```powershell
cd D:\Fake_news_Detection
pnpm dev
```

**Expected Output:**
```
  ▲ Next.js 16.0.10
  - Local:        http://localhost:3000
```

✅ **Frontend is ready when you see this message!**

---

### Step 3: Open Browser & Test
**Open your browser to:** `http://localhost:3000`

You should see the Fake News Detector interface with a text input box.

---

## 🧪 Manual Testing Steps

### Test in Web UI:
1. **Paste test news text** in the text area
2. **Click "Analyze with AI"** button
3. **Wait 2-3 seconds** for the model to process
4. **View result** showing: Verdict (REAL/FAKE) + Confidence %

### Test Samples to Try:

**Sample 1: Real News** ✓
```
New study shows coffee consumption correlates with better health outcomes
```
Expected: REAL (high confidence)

**Sample 2: Fake News** ✗
```
BREAKING: Scientists discover aliens living inside the moon - NASA confirms
```
Expected: FAKE (high confidence)

**Sample 3: Real News** ✓
```
Stock market reaches record highs as inflation decreases
```
Expected: REAL (high confidence)

---

## 🔧 Alternative: Direct API Testing (Without Web UI)

### Using PowerShell:

**Test 1 - Real News:**
```powershell
$json = @{text="New breakthrough in renewable energy technology"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://127.0.0.1:8000/predict" -Method POST -Body $json -ContentType "application/json" | Select-Object -ExpandProperty Content | ConvertFrom-Json | Format-Table
```

**Test 2 - Suspicious Article:**
```powershell
$json = @{text="Aliens spotted over White House - government cover-up exposed"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://127.0.0.1:8000/predict" -Method POST -Body $json -ContentType "application/json" | Select-Object -ExpandProperty Content | ConvertFrom-Json | Format-Table
```

**Expected Response:**
```
verdict confidence modelName
------- ---------- ---------
REAL         84.19 Sklearn TF-IDF + Classifier
```

### Using cURL (if available):
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Breaking news about economic growth\"}"
```

---

## 🔍 Health Check

**Verify the AI server is running:**
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -Method GET
```

**Expected Response:**
```
status        : ok
model_loaded  : True
```

---

## 📝 What's Happening Behind the Scenes

1. **Frontend** (Next.js at port 3000)
   - User pastes news text
   - Clicks "Analyze with AI"
   - Component sends POST request to backend

2. **Backend** (FastAPI at port 8000)
   - Receives text
   - Vectorizes it using TF-IDF
   - Runs through ML classifier
   - Returns verdict + confidence

3. **ML Model**
   - Trained classifier using Logistic Regression
   - TF-IDF vectorizer for text feature extraction
   - Binary classification: REAL (0) or FAKE (1)

---

## ⚠️ Troubleshooting

### Issue: "Connection refused" at port 8000
**Solution:** 
- Make sure Terminal 1 is still running and shows "Uvicorn running"
- Check if port 8000 is blocked by firewall
- Try a different port: `--port 8001`

### Issue: "Cannot find module 'react'"
**Solution:**
```powershell
cd D:\Fake_news_Detection
pnpm install
```

### Issue: Python module not found (e.g., "No module named uvicorn")
**Solution:**
```powershell
cd D:\Fake_news_Detection
.\.venv\Scripts\python.exe -m pip install fastapi uvicorn scikit-learn joblib numpy pydantic
```

### Issue: Model file not found
**Solution:**
- Verify these files exist in `D:\Fake_news_Detection\model\`:
  - `fake_news_model.pkl` ✓
  - `fake_news_vectorizer.pkl` ✓

---

## 📊 Test Results Recap

✅ Model loads successfully
✅ Vectorizer loads successfully
✅ API endpoint `/predict` working
✅ Web UI connects to backend
✅ Predictions return verdict + confidence
✅ All dependencies installed

---

## 🎯 Terminal Commands Summary

| Task | Command |
|------|---------|
| Start AI Server | `.\.venv\Scripts\python.exe -m uvicorn server.main:app --host 127.0.0.1 --port 8000` |
| Start Web App | `pnpm dev` |
| Install Dependencies | `pnpm install` |
| Install Python Packages | `.\.venv\Scripts\python.exe -m pip install -r server/requirements.txt` |
| Test API | `Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -Method GET` |

---

## 🎉 System Status

✅ **Backend (AI Server)**: Ready to run  
✅ **Frontend (Web UI)**: Ready to run  
✅ **Model Files**: Present and validated  
✅ **Dependencies**: Installed  
✅ **Configuration**: Complete  

**You are ready to test the full system!**

---

## 📱 Web Interface Features

- **Real-time predictions** with AI model
- **Confidence percentages** for each prediction
- **Risk level indicators** (LOW/MEDIUM/HIGH)
- **Model name display** (Sklearn TF-IDF + Classifier)
- **Beautiful UI** with animated effects
- **Responsive design** for all devices
- **Graceful fallback** if API is unreachable

---

## 🔗 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check if API server and model are ready |
| `/predict` | POST | Send text for fake news detection |

**Request body for `/predict`:**
```json
{
  "text": "Your news headline or article here"
}
```

**Response:**
```json
{
  "verdict": "REAL",
  "confidence": 84.19,
  "modelName": "Sklearn TF-IDF + Classifier"
}
```

---

Start with **Step 1**, then **Step 2**, then open your browser - that's it! 🚀
