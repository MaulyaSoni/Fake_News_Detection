import pickle
import numpy as np
import os
import torch
from typing import Dict, Any

class NewsPredictor:
    def __init__(self):
        self.embedder = None
        self.classifier = None
        self._load_models()
    
    def _load_models(self):
        """Load the pre-trained models from disk"""
        try:
            # Load sentence embedder
            embedder_path = os.path.join("models", "sentence_embedder.pkl")
            with open(embedder_path, "rb") as f:
                self.embedder = pickle.load(f)
            
            # Load classifier with CPU mapping for PyTorch models
            classifier_path = os.path.join("models", "final_fake_news_model.pkl")
            try:
                # Try loading with torch for PyTorch models
                self.classifier = torch.load(classifier_path, map_location=torch.device('cpu'), weights_only=False)
            except:
                # Fallback to regular pickle for scikit-learn models
                with open(classifier_path, "rb") as f:
                    self.classifier = pickle.load(f)
                
            # Handle PyTorch models that might still have CUDA references
            if hasattr(self.classifier, 'cpu'):
                self.classifier = self.classifier.cpu()
                
            print("Models loaded successfully!")
            
        except Exception as e:
            print(f"Error loading models: {e}")
            raise
    
    def predict_news(self, news_text: str) -> Dict[str, Any]:
        """
        Predict whether news is fake or real
        
        Args:
            news_text: The news article text to analyze
            
        Returns:
            Dictionary containing prediction label and confidence
        """
        try:
            # Generate embeddings
            embedding = self.embedder.encode([news_text])
            
            # Make prediction
            prediction = self.classifier.predict(embedding)[0]
            
            # Calculate confidence
            if hasattr(self.classifier, "predict_proba"):
                probs = self.classifier.predict_proba(embedding)[0]
                confidence = max(probs)
            else:
                # For deep learning models that don't have predict_proba
                confidence = 0.85  # Default confidence
            
            # Convert prediction to label
            label = "FAKE" if prediction == 0 else "REAL"
            
            return {
                "label": label,
                "confidence": round(confidence * 100, 2),
                "raw_prediction": int(prediction)
            }
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            return {
                "label": "ERROR",
                "confidence": 0.0,
                "raw_prediction": -1,
                "error": str(e)
            }

# Create a global instance for easy import
predictor = NewsPredictor()

def predict_news(news_text: str) -> Dict[str, Any]:
    """Convenience function for direct prediction"""
    return predictor.predict_news(news_text)
