from core.predictor import predict_news
from core.evidence_fetcher import fetch_evidence
from core.claim_verifier import verify_claim_with_evidence
from core.heuristics import detect_red_flags

TRUSTED_SOURCES = [
    "the hindu", "ndtv", "reuters", "bbc",
    "times of india", "hindustan times",
    "indian express"
]
def has_trusted_source(evidence):
    for e in evidence:
        # Handle dict: check all string values case-insensitively
        if isinstance(e, dict):
            for value in e.values():
                if isinstance(value, str) and any(src in value.lower() for src in TRUSTED_SOURCES):
                    return True
        # Fallback for strings
        elif isinstance(e, str) and any(src in e.lower() for src in TRUSTED_SOURCES):
            return True
    return False

def evaluate_news(text: str) -> dict:
    ml = predict_news(text)
    evidence = fetch_evidence(text)
    relation = verify_claim_with_evidence(text, evidence)
    flags = detect_red_flags(text)

    contains_number = any(char.isdigit() for char in text)
    trusted = has_trusted_source(evidence)

    # 🚨 DEFINITIVE FAKE
    if relation["refutes"] >= 1:
        verdict = "FAKE"

    # ✅ STRONG REAL
    elif relation["supports"] >= 2:
        verdict = "REAL"

    # 🔥 TRUSTED SOURCE OVERRIDE (THIS FIXES YOUR ISSUE)
    elif trusted and ml["confidence"] >= 90:
        verdict = "LIKELY REAL"

    # ⚠️ NUMERIC CLAIM WITHOUT CONFIRMATION
    elif contains_number:
        verdict = "UNVERIFIED News without Confirmation"

    # 🟡 HIGH ML CONFIDENCE, SOME EVIDENCE
    elif relation["supports"] == 1 and ml["confidence"] >= 90:
        verdict = "LIKELY REAL"

    else:
        verdict = "UNVERIFIED"

    return {
        "final_verdict": verdict,
        "ml_confidence": ml["confidence"],
        "evidence": evidence,
        "flags": flags,
        "relation": relation
    }
