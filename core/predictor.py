import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_DIR = r"D:\Fake_news_Detection\models"

# -------------------- LOAD TOKENIZER (FIXED) --------------------
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_DIR,  
    fix_mistral_regex=True
)

# -------------------- LOAD MODEL --------------------
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

# -------------------- LOCK LABEL SEMANTICS --------------------
# IMPORTANT: adjust ONLY if your training used opposite order
ID2LABEL = {
    0: "REAL",
    1: "FAKE"
}

# -------------------- PREDICT FUNCTION --------------------
def predict_news(text: str) -> dict:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)[0]

    real_prob = probs[0].item()
    fake_prob = probs[1].item()

    pred_id = int(torch.argmax(probs))
    label = ID2LABEL[pred_id]

    confidence = max(real_prob, fake_prob) * 100

    return {
        "label": label,
        "confidence": round(confidence, 2),
        "real_prob": round(real_prob * 100, 2),
        "fake_prob": round(fake_prob * 100, 2)
    }


# DEBUG (run once if needed)
if __name__ == "__main__":
    print("Model labels:", model.config.id2label)
