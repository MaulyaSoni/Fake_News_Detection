# core/heuristic.py
import re

HIGH_RISK_PATTERNS = [
    "miracle cure", "secret study", "leaked report",
    "government hides", "they don’t want you to know",
    "100% effective", "instantly kills", "confirmed secretly"
]

NUMERIC_CLAIM = re.compile(r"\b\d{2,}%|\b\d{4,}\b")

def detect_red_flags(text: str) -> list:
    text = text.lower()
    flags = []

    for p in HIGH_RISK_PATTERNS:
        if p in text:
            flags.append(f"High-risk phrase detected: '{p}'")

    if NUMERIC_CLAIM.search(text):
        flags.append("Suspicious numeric claim without citation")

    if text.count("!") >= 3:
        flags.append("Emotional exaggeration")

    if len(text.split()) < 20:
        flags.append("Very short unverifiable claim")

    return flags
