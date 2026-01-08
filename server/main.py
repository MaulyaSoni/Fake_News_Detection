from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from pathlib import Path
import joblib
import logging
import numpy as np

app = FastAPI(title="Fake News ML API")

# Allow requests from the frontend dev server (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("uvicorn")

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "model"
MODEL_PATH = MODEL_DIR / "fake_news_model.pkl"
VECT_PATH = MODEL_DIR / "fake_news_vectorizer.pkl"

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    verdict: str
    confidence: float
    modelName: str

# Load model and vectorizer at startup
model = None
vectorizer = None

@app.on_event("startup")
def load_artifacts():
    global model, vectorizer
    if not MODEL_PATH.exists() or not VECT_PATH.exists():
        logger.error(f"Model files not found at {MODEL_PATH} or {VECT_PATH}")
        return
    try:
        vectorizer = joblib.load(VECT_PATH)
        model = joblib.load(MODEL_PATH)
        logger.info("Loaded vectorizer and model successfully")
    except Exception as e:
        logger.exception("Failed to load model artifacts: %s", e)

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None and vectorizer is not None}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if model is None or vectorizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    text = req.text
    X = vectorizer.transform([text])

    # Try predict_proba
    try:
        probs = model.predict_proba(X)[0]
        # Assume classes_ exists and index 1 corresponds to FAKE, but we make it robust
        classes = getattr(model, "classes_", None)
        if classes is not None and len(classes) == len(probs):
            # Determine which class string corresponds to fake/real
            # We'll pick class with higher prob as predicted class
            idx = int(probs.argmax())
            pred = str(classes[idx])
            confidence = float(probs[idx] * 100)
        else:
            idx = int(probs.argmax())
            pred = str(idx)
            confidence = float(probs[idx] * 100)
    except Exception:
        # Fallback to predict + decision_function
        pred = str(model.predict(X)[0])
        try:
            score = model.decision_function(X)[0]
            confidence = float(1 / (1 + np.exp(-score)) * 100)
        except Exception:
            confidence = 50.0

    # Normalize labels to FAKE/REAL strings if possible
    pred_upper = pred.upper()
    if "FAKE" in pred_upper or pred_upper in ["1", "TRUE"] and "REAL" not in pred_upper:
        verdict = "FAKE"
    elif "REAL" in pred_upper or pred_upper in ["0", "FALSE"]:
        verdict = "REAL"
    else:
        # If unknown, treat non-zero as FAKE
        verdict = "FAKE" if pred_upper not in ["REAL", "TRUE", "0"] else "REAL"

    return PredictResponse(verdict=verdict, confidence=round(confidence, 2), modelName="Sklearn TF-IDF + Classifier")
