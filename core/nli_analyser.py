from core.nli_model import run_nli

def analyze_claim_with_evidence(claim: str, evidence: list):
    support = 0
    refute = 0
    neutral = 0

    detailed = []

    for ev in evidence:
        relation, score = run_nli(ev["title"], claim)

        if relation == "ENTAILMENT" and score > 0.55:
            support += 1
        elif relation == "CONTRADICTION" and score > 0.55:
            refute += 1
        else:
            neutral += 1

        detailed.append({
            "title": ev["title"],
            "relation": relation,
            "score": round(score * 100, 2)
        })

    return {
        "support": support,
        "refute": refute,
        "neutral": neutral,
        "details": detailed
    }
