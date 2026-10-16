"""Follow-up planning rules with explicit limits and no automatic outreach."""
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping

DEFAULT_INTERVALS = {"applied": 7, "screening": 5, "interview": 2, "offer": 2, "saved": 14}
CLOSED = {"rejected", "withdrawn"}

def _date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None

def validate_follow_up(record: Mapping) -> dict:
    status = str(record.get("status") or "saved").lower()
    if status not in {*DEFAULT_INTERVALS, *CLOSED}:
        raise ValueError("Unsupported application status")
    applied = _date(record.get("applied_date"))
    due = _date(record.get("next_action_date"))
    interval = record.get("interval_days")
    if interval in (None, ""):
        interval = DEFAULT_INTERVALS.get(status)
    else:
        try:
            interval = int(interval)
        except (ValueError, TypeError):
            raise ValueError("interval_days must be an integer")
        if not 0 <= interval <= 365:
            raise ValueError("interval_days must be between 0 and 365")
    return {"id": record.get("id"), "company": str(record.get("company") or "")[:200],
            "role": str(record.get("role") or "")[:200], "status": status,
            "applied_date": applied, "due_date": due, "interval_days": interval,
            "next_action": str(record.get("next_action") or "")[:255],
            "last_contact_date": _date(record.get("last_contact_date")),
            "opted_out": bool(record.get("opted_out", False))}

def suggest_follow_up(record: Mapping, today=None) -> dict:
    row = validate_follow_up(record)
    current = _date(today) or date.today()
    if row["status"] in CLOSED:
        return {"id": row["id"], "eligible": False, "reason": "application_closed", "suggested_date": None}
    if row["opted_out"]:
        return {"id": row["id"], "eligible": False, "reason": "contact_opted_out", "suggested_date": None}
    base = row["last_contact_date"] or row["applied_date"]
    suggested = row["due_date"] or (base + timedelta(days=row["interval_days"]) if base else None)
    if suggested is None:
        return {"id": row["id"], "eligible": False, "reason": "missing_reference_date", "suggested_date": None}
    return {"id": row["id"], "eligible": True, "company": row["company"], "role": row["role"],
            "suggested_date": suggested.isoformat(), "days_from_today": (suggested-current).days,
            "overdue": suggested < current, "due_today": suggested == current,
            "message_guidance": "Send one concise, relevant follow-up only when appropriate; respect any response."}

def reminder_queue(records: Iterable[Mapping], today=None, include_future_days: int = 7) -> dict:
    if not 0 <= include_future_days <= 180:
        raise ValueError("include_future_days must be between 0 and 180")
    current = _date(today) or date.today()
    output = []
    excluded = {}
    for record in records:
        suggestion = suggest_follow_up(record, current)
        if not suggestion["eligible"]:
            reason = suggestion["reason"]
            excluded[reason] = excluded.get(reason, 0) + 1
            continue
        day = _date(suggestion["suggested_date"])
        if day is not None and day <= current + timedelta(days=include_future_days):
            output.append(suggestion)
    output.sort(key=lambda row: (not row["overdue"], row["days_from_today"], str(row["company"]).casefold(), str(row["id"])))
    return {"as_of": current.isoformat(), "window_days": include_future_days, "reminders": output,
            "reminder_count": len(output), "excluded_by_reason": excluded,
            "automated_messages_sent": False}

def rebalance_reminder_load(records: Iterable[Mapping], daily_capacity: int = 8, today=None) -> dict:
    if not 1 <= daily_capacity <= 100:
        raise ValueError("daily_capacity must be between 1 and 100")
    queue = reminder_queue(records, today=today, include_future_days=180)["reminders"]
    current = _date(today) or date.today()
    schedule = {}
    overflow = []
    for reminder in queue:
        original = _date(reminder["suggested_date"])
        candidate = max(current, original)
        placed = False
        for offset in range(181):
            day = candidate + timedelta(days=offset)
            bucket = schedule.setdefault(day.isoformat(), [])
            if len(bucket) < daily_capacity:
                bucket.append(reminder)
                placed = True
                break
        if not placed:
            overflow.append(reminder)
    return {"daily_capacity": daily_capacity, "days_scheduled": len(schedule),
            "schedule": [{"date": day, "count": len(items), "items": items} for day, items in sorted(schedule.items())],
            "overflow": overflow, "messages_sent": False,
            "note": "Rebalancing changes only this preview; it does not update stored due dates."}

def reminder_suppression_report(records: Iterable[Mapping]) -> dict:
    rows = [validate_follow_up(row) for row in records]
    return {"total": len(rows), "closed": sum(row["status"] in CLOSED for row in rows),
            "opted_out": sum(row["opted_out"] for row in rows),
            "missing_reference_date": sum(row["status"] not in CLOSED and row["applied_date"] is None
                                          and row["due_date"] is None and row["last_contact_date"] is None
                                          for row in rows),
            "suppression_policy": "Closed applications and opted-out contacts are excluded from reminders."}
