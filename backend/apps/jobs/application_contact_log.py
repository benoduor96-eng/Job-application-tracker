"""Structured interaction logs for job contacts; no outreach is sent by these helpers."""
from datetime import date, datetime
from typing import Iterable, Mapping

INTERACTION_TYPES = {"email", "phone", "message", "meeting", "interview", "follow_up", "note"}
def _date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None

def validate_interaction(event: Mapping) -> dict:
    kind = str(event.get("interaction_type") or "note").lower()
    if kind not in INTERACTION_TYPES:
        raise ValueError("Unsupported interaction type")
    summary = str(event.get("summary") or "").strip()
    if not summary:
        raise ValueError("Interaction summary is required")
    happened = _date(event.get("occurred_on"))
    if happened is None:
        raise ValueError("A valid interaction date is required")
    outcome = str(event.get("outcome") or "unknown").lower()
    if outcome not in {"unknown", "no_response", "positive", "neutral", "negative", "action_required"}:
        raise ValueError("Unsupported interaction outcome")
    return {"id": event.get("id"), "application_id": event.get("application_id"),
            "contact_id": event.get("contact_id"), "interaction_type": kind,
            "summary": summary[:1500], "occurred_on": happened,
            "outcome": outcome, "next_step": str(event.get("next_step") or "")[:500],
            "private_notes": str(event.get("private_notes") or "")[:2000]}

def interaction_timeline(events: Iterable[Mapping]) -> list[dict]:
    rows = [validate_interaction(event) for event in events]
    rows.sort(key=lambda row: (row["occurred_on"], str(row["id"])))
    return [{**row, "occurred_on": row["occurred_on"].isoformat()} for row in rows]

def interaction_summary(events: Iterable[Mapping]) -> dict:
    rows = [validate_interaction(event) for event in events]
    types = {kind: sum(row["interaction_type"] == kind for row in rows) for kind in sorted(INTERACTION_TYPES)}
    outcomes = {outcome: sum(row["outcome"] == outcome for row in rows)
                for outcome in ("unknown", "no_response", "positive", "neutral", "negative", "action_required")}
    return {"total": len(rows), "by_type": types, "by_outcome": outcomes,
            "action_required_count": outcomes["action_required"],
            "latest_interaction": max((row["occurred_on"] for row in rows), default=None).isoformat()
                if rows else None}

def next_step_queue(events: Iterable[Mapping]) -> list[dict]:
    rows = [validate_interaction(event) for event in events]
    pending = [row for row in rows if row["outcome"] == "action_required" or row["next_step"]]
    pending.sort(key=lambda row: (row["occurred_on"], str(row["id"])))
    return [{"id": row["id"], "application_id": row["application_id"], "contact_id": row["contact_id"],
             "occurred_on": row["occurred_on"].isoformat(), "interaction_type": row["interaction_type"],
             "next_step": row["next_step"] or "Review the interaction and decide whether action is appropriate."}
            for row in pending]

def interaction_gaps(events: Iterable[Mapping], gap_days: int = 21) -> list[dict]:
    if not 1 <= gap_days <= 3650:
        raise ValueError("gap_days must be between 1 and 3650")
    rows = interaction_timeline(events)
    gaps = []
    for previous, current in zip(rows, rows[1:]):
        left, right = date.fromisoformat(previous["occurred_on"]), date.fromisoformat(current["occurred_on"])
        delta = (right-left).days
        if delta >= gap_days:
            gaps.append({"previous_id": previous["id"], "next_id": current["id"], "gap_days": delta,
                         "note": "A gap in the log is not proof that no communication occurred."})
    return gaps

def redact_interaction(event: Mapping, include_private_notes: bool = False) -> dict:
    row = validate_interaction(event)
    output = {**row, "occurred_on": row["occurred_on"].isoformat()}
    if not include_private_notes:
        output["private_notes"] = "[REDACTED]"
    return output
