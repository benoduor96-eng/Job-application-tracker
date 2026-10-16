"""Career decision journaling helpers that keep choices explainable and revisitable."""
from datetime import date, datetime
from typing import Iterable, Mapping

DECISIONS = {"apply", "continue", "pause", "withdraw", "accept", "decline", "research"}
def _date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None

def validate_decision(entry: Mapping) -> dict:
    choice = str(entry.get("decision") or "").lower()
    if choice not in DECISIONS:
        raise ValueError("Unsupported career decision")
    rationale = str(entry.get("rationale") or "").strip()
    if len(rationale) < 8:
        raise ValueError("Rationale must contain at least 8 characters")
    certainty = entry.get("certainty")
    if certainty not in (None, ""):
        try:
            certainty = int(certainty)
        except (ValueError, TypeError):
            raise ValueError("certainty must be an integer from 1 to 5")
        if not 1 <= certainty <= 5:
            raise ValueError("certainty must be between 1 and 5")
    return {"id": entry.get("id"), "application_id": entry.get("application_id"),
            "decision": choice, "rationale": rationale[:3000], "certainty": certainty,
            "review_date": _date(entry.get("review_date")),
            "assumptions": [str(value).strip()[:300] for value in entry.get("assumptions", []) if str(value).strip()][:15],
            "evidence": [str(value).strip()[:500] for value in entry.get("evidence", []) if str(value).strip()][:20],
            "revisit": bool(entry.get("revisit", False))}

def decision_review_queue(entries: Iterable[Mapping], today=None) -> list[dict]:
    current = _date(today) or date.today()
    rows = [validate_decision(entry) for entry in entries]
    output = []
    for row in rows:
        if row["revisit"] or (row["review_date"] and row["review_date"] <= current):
            output.append({"id": row["id"], "application_id": row["application_id"],
                           "decision": row["decision"], "rationale": row["rationale"],
                           "review_date": row["review_date"].isoformat() if row["review_date"] else None,
                           "questions": ["Has any important information changed?",
                                         "Are the assumptions still supported by evidence?",
                                         "Does this choice fit current constraints and priorities?"]})
    return sorted(output, key=lambda row: (row["review_date"] or "9999-12-31", str(row["id"])))

def decision_patterns(entries: Iterable[Mapping]) -> dict:
    rows = [validate_decision(entry) for entry in entries]
    counts = {decision: sum(row["decision"] == decision for row in rows) for decision in sorted(DECISIONS)}
    certainty = [row["certainty"] for row in rows if row["certainty"] is not None]
    return {"count": len(rows), "by_decision": counts,
            "average_certainty": round(sum(certainty)/len(certainty), 2) if certainty else None,
            "with_assumptions": sum(bool(row["assumptions"]) for row in rows),
            "with_evidence": sum(bool(row["evidence"]) for row in rows),
            "revisit_requested": sum(row["revisit"] for row in rows),
            "warning": "Patterns summarize self-reported notes and do not establish that decisions were right or wrong."}

def decision_template(application_id=None) -> dict:
    return {"application_id": application_id,
            "prompts": [
                "What choice am I making and what alternatives exist?",
                "What evidence supports this choice?",
                "Which assumptions remain uncertain?",
                "What constraints or deadlines matter?",
                "What information would change my mind?",
                "When should I revisit the decision?",
            ], "saved": False}
