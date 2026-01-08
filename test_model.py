"""Test script to verify the fake news model works with sample text."""

import sys
from pathlib import Path

# Add the project root to path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from server.main import model, vectorizer

def test_prediction():
    """Test the model with sample text."""
    if model is None or vectorizer is None:
        print("ERROR: Model or vectorizer not loaded!")
        return
    
    test_texts = [
        "Breaking: New study shows coffee is good for health",
        "FAKE NEWS ALERT: The moon landing was a hoax",
        "Scientists discover new species in the Amazon rainforest",
        "Biden secretly moves to Mars according to conspiracy theorists",
    ]
    
    print("=" * 80)
    print("FAKE NEWS DETECTOR - TEST PREDICTIONS")
    print("=" * 80)
    
    for text in test_texts:
        print(f"\nText: {text[:70]}...")
        X = vectorizer.transform([text])
        
        try:
            probs = model.predict_proba(X)[0]
            classes = getattr(model, "classes_", None)
            
            if classes is not None:
                print(f"Classes: {classes}")
                print(f"Probabilities: {probs}")
                
                idx = int(probs.argmax())
                pred = str(classes[idx])
                confidence = float(probs[idx] * 100)
                
                pred_upper = pred.upper()
                if "FAKE" in pred_upper or pred_upper in ["1", "TRUE"]:
                    verdict = "FAKE"
                else:
                    verdict = "REAL"
                
                print(f"VERDICT: {verdict} (Confidence: {confidence:.2f}%)")
            else:
                print("Could not extract classes from model")
                
        except Exception as e:
            print(f"Error during prediction: {e}")
    
    print("\n" + "=" * 80)
    print("Test complete!")
    print("=" * 80)

if __name__ == "__main__":
    # Load model and vectorizer
    import joblib
    
    MODEL_PATH = ROOT / "model" / "fake_news_model.pkl"
    VECT_PATH = ROOT / "model" / "fake_news_vectorizer.pkl"
    
    print("Loading model artifacts...")
    vectorizer = joblib.load(VECT_PATH)
    model = joblib.load(MODEL_PATH)
    print("✓ Model and vectorizer loaded\n")
    
    test_prediction()
