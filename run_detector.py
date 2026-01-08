#!/usr/bin/env python
"""Standalone fake news detection server with integrated model loading and testing."""

import sys
import os
from pathlib import Path
from typing import Tuple

# Ensure we can import from project
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def load_model_and_vectorizer() -> Tuple:
    """Load the model and vectorizer pickle files."""
    import joblib
    import warnings
    
    MODEL_DIR = PROJECT_ROOT / "model"
    MODEL_PATH = MODEL_DIR / "fake_news_model.pkl"
    VECT_PATH = MODEL_DIR / "fake_news_vectorizer.pkl"
    
    # Suppress sklearn version warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        
        print(f"📂 Loading vectorizer from {VECT_PATH}...")
        if not VECT_PATH.exists():
            print(f"❌ ERROR: Vectorizer not found at {VECT_PATH}")
            return None, None
        
        vectorizer = joblib.load(str(VECT_PATH))
        print("✅ Vectorizer loaded successfully")
        
        print(f"📂 Loading model from {MODEL_PATH}...")
        if not MODEL_PATH.exists():
            print(f"❌ ERROR: Model not found at {MODEL_PATH}")
            return None, None
        
        model = joblib.load(str(MODEL_PATH))
        print("✅ Model loaded successfully")
    
    return model, vectorizer

def predict_news(text: str, model, vectorizer) -> dict:
    """Make a prediction on the given text."""
    if model is None or vectorizer is None:
        return {"error": "Model or vectorizer not loaded"}
    
    try:
        X = vectorizer.transform([text])
        probs = model.predict_proba(X)[0]
        classes = model.classes_
        
        idx = int(probs.argmax())
        pred = str(classes[idx])
        confidence = float(probs[idx] * 100)
        
        # Normalize verdict
        pred_upper = pred.upper()
        if "FAKE" in pred_upper or pred_upper in ["1", "TRUE"]:
            verdict = "FAKE"
        else:
            verdict = "REAL"
        
        return {
            "text": text[:100] + ("..." if len(text) > 100 else ""),
            "verdict": verdict,
            "confidence": round(confidence, 2),
            "raw_class": pred,
            "all_probs": {str(c): round(float(p * 100), 2) for c, p in zip(classes, probs)}
        }
    except Exception as e:
        return {"error": str(e)}

def run_tests(model, vectorizer):
    """Run test predictions."""
    print("\n" + "="*80)
    print("🧪 FAKE NEWS DETECTOR - TEST PREDICTIONS")
    print("="*80)
    
    test_cases = [
        ("Breaking: New study shows coffee is good for health and wellness", "expected: REAL"),
        ("FAKE NEWS ALERT: The moon landing was a complete hoax by NASA", "expected: FAKE"),
        ("Scientists discover new species in the Amazon rainforest today", "expected: REAL"),
        ("Biden secretly moves to Mars according to secret government files", "expected: FAKE"),
        ("Stock market rallies as unemployment drops to historic lows", "expected: REAL"),
    ]
    
    for i, (text, note) in enumerate(test_cases, 1):
        print(f"\n📰 Test {i}: {note}")
        print(f"   Text: {text[:70]}...")
        
        result = predict_news(text, model, vectorizer)
        
        if "error" in result:
            print(f"   ❌ Error: {result['error']}")
        else:
            print(f"   ✓ Verdict: {result['verdict']}")
            print(f"   ✓ Confidence: {result['confidence']}%")
            print(f"   ✓ All probabilities: {result['all_probs']}")
    
    print("\n" + "="*80)
    print("✅ Test suite complete!")
    print("="*80)

def run_fastapi_server():
    """Start the FastAPI server."""
    print("\n" + "="*80)
    print("🚀 STARTING FASTAPI MODEL SERVER")
    print("="*80)
    print("\n💡 Server will be available at: http://localhost:8000")
    print("   Health check: http://localhost:8000/health")
    print("   Prediction API: POST http://localhost:8000/predict")
    print("\n⏸️  Press CTRL+C to stop the server\n")
    
    try:
        import uvicorn
        uvicorn.run(
            "server.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🤖 FAKE NEWS DETECTION SYSTEM")
    print("="*80)
    
    # Load model and vectorizer
    model, vectorizer = load_model_and_vectorizer()
    
    if model is None or vectorizer is None:
        print("\n❌ Failed to load model files. Exiting.")
        sys.exit(1)
    
    # Run tests
    run_tests(model, vectorizer)
    
    # Ask user what to do
    print("\n📋 Options:")
    print("   1. Start FastAPI server (default)")
    print("   2. Exit")
    
    try:
        choice = input("\nEnter choice [1]: ").strip() or "1"
        
        if choice == "1":
            run_fastapi_server()
        else:
            print("Goodbye!")
            sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
