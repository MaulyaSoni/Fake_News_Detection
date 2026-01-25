import os
import joblib
from sentence_transformers import SentenceTransformer  # ✅ MISSING IMPORT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = r"D:\Fake_news_Detection\models"

# Load embedder (384-dim)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load trained classifier
model = joblib.load(os.path.join(MODEL_DIR, "fake_news_embedding_model.pkl"))

def predict_news(text: str) -> dict:
    embedding = embedder.encode(text).reshape(1, -1)

    probs = model.predict_proba(embedding)[0]
    fake_prob = float(probs[0])
    real_prob = float(probs[1])

    verdict = "FAKE" if fake_prob >= real_prob else "REAL"

    return {
        "verdict": verdict,
        "fake_prob": round(fake_prob * 100, 2),
        "real_prob": round(real_prob * 100, 2),
        "confidence": round(max(fake_prob, real_prob) * 100, 2)
    }
