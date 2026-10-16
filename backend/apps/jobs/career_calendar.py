"""Calendar aggregation for career activities; output is a preview and sends no invitations."""
from datetime import date, datetime
from typing import Iterable, Mapping

EVENT_TYPES = {"interview", "follow_up", "milestone", "learning", "networking", "deadline"}
def _date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None

def normalize_calendar_event(event: Mapping) -> dict:
    title = str(event.get("title") or "").strip()
    if not title:
        raise ValueError("Calendar event title is required")
    kind = str(event.get("event_type") or "milestone").lower()
    if kind not in EVENT_TYPES:
        raise ValueError("Unsupported calendar event type")
    day = _date(event.get("date") or event.get("due_date") or event.get("start_date"))
    if day is None:
        raise ValueError("A valid event date is required")
    try:
        duration = int(event.get("duration_minutes") or 0)
    except (TypeError, ValueError):
        raise ValueError("duration_minutes must be an integer")
    if not 0 <= duration <= 1440:
        raise ValueError("duration_minutes must be between 0 and 1440")
    return {"id": event.get("id"), "title": title[:200], "event_type": kind,
            "date": day, "duration_minutes": duration, "application_id": event.get("application_id"),
            "location": str(event.get("location") or "")[:300],
            "completed": bool(event.get("completed", False)),
            "notes": str(event.get("notes") or "")[:1000]}

def build_calendar(events: Iterable[Mapping], start_date=None, end_date=None) -> dict:
    start, end = _date(start_date), _date(end_date)
    if start and end and end < start:
        raise ValueError("end_date must not precede start_date")
    rows = [normalize_calendar_event(event) for event in events]
    filtered = [row for row in rows if (start is None or row["date"] >= start) and (end is None or row["date"] <= end)]
    filtered.sort(key=lambda row: (row["date"], row["event_type"], row["title"].casefold(), str(row["id"])))
    days = {}
    for row in filtered:
        key = row["date"].isoformat()
        days.setdefault(key, []).append({**row, "date": key})
    return {"start_date": start.isoformat() if start else None, "end_date": end.isoformat() if end else None,
            "event_count": len(filtered), "days": [{"date": key, "count": len(items), "events": items}
                                                   for key, items in sorted(days.items())],
            "by_type": {kind: sum(row["event_type"] == kind for row in filtered) for kind in sorted(EVENT_TYPES)},
            "calendar_invites_sent": False}

def daily_capacity_conflicts(events: Iterable[Mapping], available_minutes: int = 480) -> list[dict]:
    if not isinstance(available_minutes, int) or not 0 <= available_minutes <= 1440:
        raise ValueError("available_minutes must be between 0 and 1440")
    days = {}
    for event in events:
        row = normalize_calendar_event(event)
        if row["duration_minutes"]:
            days.setdefault(row["date"].isoformat(), []).append(row)
    result = []
    for day, rows in sorted(days.items()):
        total = sum(row["duration_minutes"] for row in rows)
        if total > available_minutes:
            result.append({"date": day, "scheduled_minutes": total, "available_minutes": available_minutes,
                           "over_capacity_minutes": total-available_minutes,
                           "event_titles": [row["title"] for row in rows],
                           "suggestion": "Review the schedule and preserve travel, breaks, and preparation time."})
    return result

def calendar_summary(events: Iterable[Mapping]) -> dict:
    rows = [normalize_calendar_event(event) for event in events]
    incomplete = [row for row in rows if not row["completed"]]
    return {"total": len(rows), "completed": len(rows)-len(incomplete), "upcoming_or_open": len(incomplete),
            "duration_minutes": sum(row["duration_minutes"] for row in rows),
            "by_type": {kind: sum(row["event_type"] == kind for row in rows) for kind in sorted(EVENT_TYPES)},
            "note": "The summary does not connect to external calendars or send invitations."}
