"""Networking workflow helpers focused on consent, relevance, and respectful follow-up."""
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping

RELATIONSHIPS = {"recruiter", "hiring_manager", "peer", "mentor", "alumni", "community", "other"}
TOUCHPOINTS = {"research", "connection_request", "message", "conversation", "thank_you", "follow_up"}
DEFAULT_WAIT_DAYS = {"connection_request": 7, "message": 7, "conversation": 2, "thank_you": 5, "follow_up": 10}

def _date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None
    return None

def validate_contact(contact: Mapping) -> dict:
    name = str(contact.get("name") or "").strip()
    if not name:
        raise ValueError("Contact name is required")
    relationship = str(contact.get("relationship") or "other").lower()
    if relationship not in RELATIONSHIPS:
        raise ValueError("Unsupported relationship category")
    return {"id": contact.get("id"), "name": name[:160],
            "company": str(contact.get("company") or "").strip()[:200],
            "role": str(contact.get("role") or "").strip()[:200],
            "relationship": relationship, "last_contact_date": _date(contact.get("last_contact_date")),
            "next_follow_up_date": _date(contact.get("next_follow_up_date")),
            "consent_status": str(contact.get("consent_status") or "unknown").lower(),
            "notes": str(contact.get("notes") or "")[:2000],
            "touchpoint_count": max(0, min(100000, int(contact.get("touchpoint_count") or 0)))}

def contact_health(contact: Mapping, today=None) -> dict:
    row = validate_contact(contact)
    current = _date(today) or date.today()
    due = row["next_follow_up_date"]
    consent = row["consent_status"]
    overdue = bool(due and due < current)
    if consent in {"opted_out", "do_not_contact"}:
        state = "do_not_contact"
    elif overdue:
        state = "follow_up_overdue"
    elif due == current:
        state = "follow_up_today"
    elif consent == "unknown":
        state = "consent_unclear"
    else:
        state = "up_to_date"
    return {"id": row["id"], "name": row["name"], "state": state, "overdue": overdue,
            "days_until_follow_up": (due - current).days if due else None,
            "touchpoint_count": row["touchpoint_count"],
            "recommended_action": "Do not contact this person" if state == "do_not_contact" else
                "Clarify whether contact is welcome" if state == "consent_unclear" else
                "Send one concise, relevant follow-up" if overdue or due == current else
                "Wait until the planned date or a meaningful update"}

def rank_networking_contacts(contacts: Iterable[Mapping], today=None) -> list[dict]:
    current = _date(today) or date.today()
    output = []
    for contact in contacts:
        row = validate_contact(contact)
        if row["consent_status"] in {"opted_out", "do_not_contact"}:
            continue
        due = row["next_follow_up_date"]
        days = (due - current).days if due else None
        score = 0
        if days is not None and days < 0:
            score += min(50, abs(days) * 2)
        elif days == 0:
            score += 25
        elif days is not None and days <= 3:
            score += 10
        score += {"recruiter": 8, "hiring_manager": 7, "mentor": 5, "alumni": 4,
                  "peer": 3, "community": 2, "other": 1}[row["relationship"]]
        if row["consent_status"] == "unknown":
            score -= 5
        output.append({"id": row["id"], "name": row["name"], "company": row["company"],
                       "relationship": row["relationship"], "priority_score": score,
                       "days_until_follow_up": days, "consent_status": row["consent_status"]})
    return sorted(output, key=lambda item: (-item["priority_score"], item["name"].casefold()))

def plan_touchpoint(contact: Mapping, touchpoint_type: str, occurred_on=None,
                    wait_days: int | None = None) -> dict:
    row = validate_contact(contact)
    if touchpoint_type not in TOUCHPOINTS:
        raise ValueError("Unsupported touchpoint type")
    if row["consent_status"] in {"opted_out", "do_not_contact"}:
        raise ValueError("Contact has opted out; do not schedule a touchpoint")
    day = _date(occurred_on) or date.today()
    wait = DEFAULT_WAIT_DAYS.get(touchpoint_type, 7) if wait_days is None else int(wait_days)
    if not 0 <= wait <= 180:
        raise ValueError("wait_days must be between 0 and 180")
    next_date = day + timedelta(days=wait)
    return {"contact_id": row["id"], "touchpoint_type": touchpoint_type,
            "occurred_on": day.isoformat(), "suggested_follow_up": next_date.isoformat(),
            "wait_days": wait, "persistence_performed": False,
            "note": "Respect any reply, opt-out, or indication that further contact is unwelcome."}

def networking_week_summary(contacts: Iterable[Mapping], start_date=None) -> dict:
    start = _date(start_date) or date.today()
    monday = start - timedelta(days=start.weekday())
    sunday = monday + timedelta(days=6)
    rows = [validate_contact(contact) for contact in contacts]
    due = [row for row in rows if row["next_follow_up_date"] and monday <= row["next_follow_up_date"] <= sunday]
    blocked = [row for row in due if row["consent_status"] in {"opted_out", "do_not_contact"}]
    actionable = [row for row in due if row not in blocked]
    return {"week_start": monday.isoformat(), "week_end": sunday.isoformat(),
            "contacts": len(rows), "follow_ups_due": len(due), "actionable_follow_ups": len(actionable),
            "blocked_by_opt_out": len(blocked),
            "by_relationship": {relationship: sum(row["relationship"] == relationship for row in actionable)
                                for relationship in sorted(RELATIONSHIPS)},
            "note": "A follow-up date is a reminder, not an obligation; respect the person's response."}

def contact_deduplication_key(contact: Mapping) -> tuple:
    row = validate_contact(contact)
    return (row["name"].casefold(), row["company"].casefold(), row["role"].casefold())

def find_contact_duplicates(contacts: Iterable[Mapping]) -> list[dict]:
    groups = {}
    for contact in contacts:
        row = validate_contact(contact)
        groups.setdefault(contact_deduplication_key(contact), []).append(row)
    results = []
    for key, group in groups.items():
        if len(group) < 2:
            continue
        results.append({"key": list(key), "contact_ids": [row["id"] for row in group],
                        "count": len(group), "requires_manual_review": True,
                        "warning": "Do not merge contact records automatically; verify identity and consent."})
    return sorted(results, key=lambda item: (-item["count"], str(item["key"])))

def outreach_message_outline(contact: Mapping, reason: str, context: str = "") -> dict:
    row = validate_contact(contact)
    reason = str(reason or "").strip()
    context = str(context or "").strip()
    if not reason:
        raise ValueError("A genuine reason for reaching out is required")
    if row["consent_status"] in {"opted_out", "do_not_contact"}:
        raise ValueError("Contact has opted out; do not create outreach")
    return {"recipient_name": row["name"], "subject_hint": "Brief question about " + (row["company"] or "your work"),
            "outline": ["Introduce yourself briefly and truthfully.",
                        "Explain why this person's experience is relevant.",
                        "Ask one specific, easy-to-answer question.",
                        "Thank them and make it easy to decline."],
            "reason": reason[:500], "context": context[:1000],
            "privacy_note": "Use only contact details obtained appropriately; avoid repeated unsolicited messages."}

def relationship_maintenance_report(contacts: Iterable[Mapping], today=None) -> dict:
    current = _date(today) or date.today()
    rows = [validate_contact(contact) for contact in contacts]
    active = [row for row in rows if row["consent_status"] not in {"opted_out", "do_not_contact"}]
    by_type = {name: sum(row["relationship"] == name for row in active) for name in sorted(RELATIONSHIPS)}
    unknown = sum(row["consent_status"] == "unknown" for row in active)
    overdue = sum(bool(row["next_follow_up_date"] and row["next_follow_up_date"] < current) for row in active)
    no_history = sum(row["last_contact_date"] is None for row in active)
    return {"total_contacts": len(rows), "active_contacts": len(active),
            "opted_out_contacts": len(rows) - len(active), "consent_unknown": unknown,
            "overdue_follow_ups": overdue, "without_contact_history": no_history,
            "by_relationship": by_type,
            "recommendations": [
                {"code": "clarify_consent", "count": unknown} if unknown else None,
                {"code": "review_overdue", "count": overdue} if overdue else None,
                {"code": "add_context", "count": no_history} if no_history else None,
            ]}
