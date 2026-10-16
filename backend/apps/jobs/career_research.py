"""Employer research checklist and evidence log helpers."""
from datetime import date, datetime
from typing import Iterable, Mapping

RESEARCH_AREAS = {
    "identity": "Verify the employer identity using independent sources.",
    "domain": "Check that recruiter email and application links match the employer domain.",
    "role": "Confirm the position appears on an official careers page or trusted recruiter channel.",
    "compensation": "Clarify currency, pay period, bonus conditions, and contract type in writing.",
    "interview": "Confirm interviewer identity, meeting details, and reasonable assessment expectations.",
    "privacy": "Check what personal information is requested and why it is needed.",
    "payment": "Be cautious of recruitment, training, equipment, or release fees.",
    "references": "Use more than one independent source and record dates and uncertainty.",
}
def _date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None

def research_checklist(company: str, role: str, country: str = "") -> dict:
    company, role = str(company or "").strip(), str(role or "").strip()
    if not company or not role:
        raise ValueError("Company and role are required")
    return {"company": company[:200], "role": role[:200], "country": str(country or "")[:100],
            "checks": [{"key": key, "guidance": value, "status": "not_checked", "evidence": []}
                       for key, value in RESEARCH_AREAS.items()],
            "warning": "A checklist cannot certify legitimacy; verify independently and never share passwords or PINs."}

def validate_evidence(item: Mapping) -> dict:
    source, claim = str(item.get("source") or "").strip(), str(item.get("claim") or "").strip()
    if not source or not claim:
        raise ValueError("Evidence needs both a source and a claim")
    status = str(item.get("status") or "unverified").lower()
    if status not in {"unverified", "supports", "contradicts", "inconclusive"}:
        raise ValueError("Unsupported evidence status")
    observed = _date(item.get("observed_on")) or date.today()
    return {"source": source[:500], "claim": claim[:1000], "status": status,
            "observed_on": observed.isoformat(), "notes": str(item.get("notes") or "")[:2000]}

def summarize_evidence(items: Iterable[Mapping]) -> dict:
    rows = [validate_evidence(item) for item in items]
    statuses = {key: sum(row["status"] == key for row in rows)
                for key in ("unverified", "supports", "contradicts", "inconclusive")}
    return {"evidence_count": len(rows), "by_status": statuses,
            "contradiction_count": statuses["contradicts"], "unverified_count": statuses["unverified"],
            "needs_follow_up": bool(statuses["contradicts"] or statuses["unverified"]),
            "note": "Evidence status is the user's assessment, not an automated verification result."}

def research_decision(evidence: Iterable[Mapping], unresolved_questions: Iterable[str] = ()) -> dict:
    summary = summarize_evidence(evidence)
    questions = [str(question).strip()[:500] for question in unresolved_questions if str(question).strip()]
    if summary["contradiction_count"]:
        recommendation = "pause_and_verify"
    elif summary["evidence_count"] == 0 or summary["unverified_count"] or questions:
        recommendation = "gather_more_information"
    else:
        recommendation = "review_evidence_before_deciding"
    return {"recommendation": recommendation, "evidence": summary, "unresolved_questions": questions,
            "not_a_verdict": True,
            "safety_note": "Do not pay to obtain a job or provide bank credentials, passwords, PINs, or recovery phrases."}

def research_log_entry(area: str, action: str, result: str, source: str = "", observed_on=None) -> dict:
    if area not in RESEARCH_AREAS:
        raise ValueError("Unknown research area")
    action, result = str(action or "").strip(), str(result or "").strip()
    if not action or not result:
        raise ValueError("Action and result are required")
    return {"area": area, "action": action[:500], "result": result[:1500],
            "source": str(source or "")[:500], "observed_on": (_date(observed_on) or date.today()).isoformat(),
            "persisted": False}

def checklist_progress(checks: Iterable[Mapping]) -> dict:
    rows = list(checks)
    allowed = {"not_checked", "in_progress", "checked", "blocked", "not_applicable"}
    if any(row.get("status") not in allowed for row in rows):
        raise ValueError("Unsupported checklist status")
    counts = {status: sum(row.get("status") == status for row in rows) for status in sorted(allowed)}
    applicable = len(rows) - counts["not_applicable"]
    done = counts["checked"] + counts["not_applicable"]
    return {"total": len(rows), "counts": counts,
            "progress_percent": round(100 * done / applicable, 1) if applicable else 100,
            "blocked": counts["blocked"]}

def prioritize_verification(evidence: Iterable[Mapping]) -> list[dict]:
    rows = [validate_evidence(item) for item in evidence]
    order = {"contradicts": 0, "unverified": 1, "inconclusive": 2, "supports": 3}
    rows.sort(key=lambda row: (order[row["status"]], row["observed_on"], row["source"].casefold()))
    return [{"rank": index, **row} for index, row in enumerate(rows, 1)]

def safe_information_request(topic: str) -> dict:
    prompts = {
        "identity": "Could you share the official company website and public careers page for this role?",
        "compensation": "Could you confirm salary range, currency, pay period, and employment type in writing?",
        "interview": "Could you confirm interviewer names, meeting link, duration, and interview format?",
        "privacy": "Could you explain why this information is required, how it is protected, and how long it is retained?",
        "payment": "Please clarify the purpose of this fee. I do not pay recruitment or job-release fees.",
        "role": "Could you share the official job description and explain the main responsibilities?",
    }
    if topic not in prompts:
        raise ValueError("Unsupported request topic")
    return {"topic": topic, "message": prompts[topic], "tone": "polite and direct",
            "note": "Do not include passwords, PINs, bank credentials, or unnecessary identity documents."}
