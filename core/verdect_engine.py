def generate_verdict(nli_result: dict, evidence_count: int):
    support = nli_result["support"]
    refute = nli_result["refute"]
    neutral = nli_result["neutral"]
# HARD CONTRADICTION RULE
    if nli_result.get("contradict", 0) > 0:
        return {
            "verdict": "FAKE",
            "reason": "Trusted sources contradict the claim"
        }
    if support >= 2:
        return "REAL"

    if support == 0:
        return "FAKE"
    
    if evidence_count >= 1:
        return "LIKELY_REAL (as one article found)"

    if refute >= 2:
        return "FAKE"

    if evidence_count == 0:
        return "LIKELY_FAKE (NO_VERIFIED_EVIDENCE)"

    return "UNVERIFIED"
