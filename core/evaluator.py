# core/evaluator.py
from core.heuristic import detect_red_flags
from core.realtime_fetcher import fetch_realtime_articles

def evaluate_news(text, ml_result):
    flags = detect_red_flags(text)
    articles = fetch_realtime_articles(text)

    ml_conf = ml_result["confidence"]
    risk_penalty = len(flags) * 10
    evidence_bonus = 20 if articles else 0

    score = ml_conf - risk_penalty + evidence_bonus
    score = max(0, min(100, score))

    # 🚨 FINAL DECISION RULES
    if ml_conf < 70:
        verdict = "UNVERIFIED"
    elif flags and not articles:
        verdict = "LIKELY FAKE"
    else:
        verdict = ml_result["ml_label"]

    return {
        "final_verdict": verdict,
        "truth_score": round(score, 2),
        "flags": flags,
        "realtime_articles": articles,
        "reason": {
            "ml_confidence": ml_conf,
            "heuristic_penalty": risk_penalty,
            "evidence_bonus": evidence_bonus
        }
    }
