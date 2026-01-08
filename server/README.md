# Model server

This directory contains a small FastAPI server that loads the TF-IDF vectorizer and the trained classifier from `../model` and exposes a `/predict` endpoint.

Quick start:

1. Create and activate a Python virtual environment (Windows example):

   python -m venv .venv
   .\.venv\Scripts\activate

2. Install requirements:

   pip install -r requirements.txt

3. Run the server (or use the npm script `pnpm run model:serve`):

   uvicorn server.main:app --reload --port 8000

4. Health check:

   GET http://localhost:8000/health

5. Prediction:

   POST http://localhost:8000/predict
   Body: { "text": "Your news headline or article here" }

Notes:
- Ensure the `model` folder in the repo contains `fake_news_model.pkl` and `fake_news_vectorizer.pkl` (already present in the repository as provided).
- The frontend expects the server at `http://localhost:8000`.
