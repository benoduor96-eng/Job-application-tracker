"""Evidence mapping for resume claims, designed to discourage unsupported exaggeration."""
from typing import Iterable, Mapping

CLAIM_TYPES = {"skill", "achievement", "responsibility", "qualification", "metric", "project"}
EVIDENCE_STRENGTH = {"none": 0, "personal_note": 1, "artifact": 2, "independent_confirmation": 3}

def validate_claim(claim: Mapping) -> dict:
    text = str(claim.get("claim") or "").strip()
    if not text:
        raise ValueError("Claim text is required")
    kind = str(claim.get("claim_type") or "achievement").lower()
    if kind not in CLAIM_TYPES:
        raise ValueError("Unsupported claim type")
    strength = str(claim.get("evidence_strength") or "none").lower()
    if strength not in EVIDENCE_STRENGTH:
        raise ValueError("Unsupported evidence strength")
    return {"id": claim.get("id"), "claim": text[:1500], "claim_type": kind,
            "evidence_strength": strength, "evidence_reference": str(claim.get("evidence_reference") or "")[:1000],
            "context": str(claim.get("context") or "")[:1000],
            "quantified": bool(claim.get("quantified", False)),
            "confidentiality_reviewed": bool(claim.get("confidentiality_reviewed", False))}

def claim_readiness(claim: Mapping) -> dict:
    row = validate_claim(claim)
    issues = []
    if row["evidence_strength"] == "none":
        issues.append("No evidence reference has been recorded.")
    if row["quantified"] and not any(char.isdigit() for char in row["claim"]):
        issues.append("Claim is marked quantified but contains no visible number.")
    if row["evidence_strength"] in {"artifact", "independent_confirmation"} and not row["evidence_reference"]:
        issues.append("Evidence strength is recorded without an evidence reference.")
    if not row["confidentiality_reviewed"]:
        issues.append("Review confidentiality and permission before sharing.")
    score = EVIDENCE_STRENGTH[row["evidence_strength"]]
    return {"id": row["id"], "claim": row["claim"], "evidence_score": score,
            "evidence_level": row["evidence_strength"], "issues": issues,
            "ready_for_review": not issues,
            "warning": "This checks documentation only; it cannot independently verify whether a claim is true."}

def claim_audit(claims: Iterable[Mapping]) -> dict:
    rows = [claim_readiness(claim) for claim in claims]
    issue_counts = {}
    for row in rows:
        for issue in row["issues"]:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
    return {"claim_count": len(rows), "ready_count": sum(row["ready_for_review"] for row in rows),
            "average_evidence_score": round(sum(row["evidence_score"] for row in rows)/len(rows), 2) if rows else 0,
            "issues": dict(sorted(issue_counts.items())), "claims": rows}

def match_claims_to_role(claims: Iterable[Mapping], required_skills: Iterable[str]) -> dict:
    normalized = []
    for claim in claims:
        row = validate_claim(claim)
        normalized.append(row)
    requirements = sorted({str(skill).strip().lower() for skill in required_skills if str(skill).strip()})
    matched, unmatched = [], []
    for skill in requirements:
        related = [row for row in normalized if skill in row["claim"].lower() or skill in row["context"].lower()]
        target = matched if related else unmatched
        target.append({"skill": skill, "claims": [{"id": row["id"], "claim": row["claim"],
                       "evidence_strength": row["evidence_strength"]} for row in related]})
    return {"required_skills": len(requirements), "matched_skills": len(matched),
            "unmatched_skills": unmatched, "matches": matched,
            "warning": "Text matches are suggestions; verify that each claim accurately represents your experience."}

def claim_revision_prompt(claim: Mapping) -> dict:
    row = validate_claim(claim)
    return {"claim_id": row["id"], "current_claim": row["claim"],
            "questions": ["What did you personally do?", "What was the context or constraint?",
                          "What evidence supports the claim?", "What changed as a result?",
                          "Can you share the evidence without exposing confidential information?"],
            "suggested_structure": "Action + context + result, only where the facts support it.",
            "do_not_invent_metrics": True}
