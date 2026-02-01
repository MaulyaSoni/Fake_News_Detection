
from core.evidence_fetcher import fetch_evidence
from core.heuristics import detect_red_flags
from core.nli_analyser import analyze_claim_with_evidence
from core.verdect_engine import generate_verdict

def evaluate_news(claim: str):
    if not claim or len(claim.strip()) == 0:
        return {"error": "EMPTY_CLAIM"}

    flags = detect_red_flags(claim)

    evidence = fetch_evidence(claim)
    trusted_evidence = [e for e in evidence if e["trusted"]]

    nli_result = analyze_claim_with_evidence(claim, trusted_evidence)

    verdict = generate_verdict(nli_result, len(trusted_evidence))

    return {
        "claim": claim,
        "verdict": verdict,
        "flags": flags,
        "evidence": trusted_evidence,
        "nli": nli_result
    }
VERDICT_UI = {
    "LIKELY_REAL": {"color": "green", "emoji": "✅"},
    "UNVERIFIED_BUT_REPORTED": {"color": "orange", "emoji": "🟡"},
    "UNVERIFIED": {"color": "yellow", "emoji": "⚠️"},
    "NO_VERIFIED_EVIDENCE": {"color": "grey", "emoji": "❓"},
    "FAKE": {"color": "red", "emoji": "❌"}
}
