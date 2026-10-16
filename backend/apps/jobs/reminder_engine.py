"""Reminder planning for job applications, interviews, and career tasks.

The engine is pure: it creates reminder candidates but never sends email, SMS, or
push notifications. Delivery providers can consume the stable idempotency keys.
"""
from datetime import date, datetime, timedelta, timezone
from hashlib import sha256
from typing import Any, Iterable, Mapping

DEFAULT_HORIZON_DAYS = 14
MAX_HORIZON_DAYS = 90
MAX_REMINDERS = 500
TERMINAL_APPLICATION_STATES = {"rejected", "withdrawn"}


class ReminderInputError(ValueError):
    pass


def _parse_date(value: Any) -> date | None:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        raise ReminderInputError("Reminder dates must be ISO date strings.")
    try:
        return date.fromisoformat(value[:10])
    except ValueError as exc:
        raise ReminderInputError(f"Invalid ISO date: {value!r}.") from exc


def _key(kind: str, owner_id: Any, object_id: Any, due: date) -> str:
    raw = f"{kind}:{owner_id}:{object_id}:{due.isoformat()}".encode("utf-8")
    return sha256(raw).hexdigest()


def _candidate(kind: str, owner_id: Any, object_id: Any, title: str,
               due: date, today: date, details: Mapping | None = None) -> dict:
    delta = (due - today).days
    return {
        "idempotency_key": _key(kind, owner_id, object_id, due),
        "kind": kind,
        "object_id": object_id,
        "title": title[:200],
        "due_date": due.isoformat(),
        "days_from_today": delta,
        "urgency": "overdue" if delta < 0 else "today" if delta == 0 else "soon" if delta <= 3 else "upcoming",
        "details": dict(details or {}),
    }


def plan_application_reminders(
    applications: Iterable[Mapping],
    *,
    owner_id: Any,
    today: date | None = None,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
    include_overdue: bool = True,
) -> list[dict]:
    if isinstance(horizon_days, bool) or not isinstance(horizon_days, int) or not 0 <= horizon_days <= MAX_HORIZON_DAYS:
        raise ReminderInputError(f"horizon_days must be between 0 and {MAX_HORIZON_DAYS}.")
    today = today or date.today()
    reminders = []
    for app in applications:
        status = app.get("status", "saved")
        if status in TERMINAL_APPLICATION_STATES:
            continue
        due = _parse_date(app.get("next_action_date"))
        if due is None:
            continue
        delta = (due - today).days
        if delta > horizon_days or (delta < 0 and not include_overdue):
            continue
        title = app.get("next_action") or f"Follow up with {app.get('company') or 'employer'}"
        reminders.append(_candidate(
            "application_follow_up", owner_id, app.get("id"), title, due, today,
            {"company": app.get("company", ""), "role": app.get("role", ""),
             "status": status},
        ))
    return reminders


def plan_interview_reminders(
    interviews: Iterable[Mapping],
    *,
    owner_id: Any,
    today: date | None = None,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
) -> list[dict]:
    if not 0 <= horizon_days <= MAX_HORIZON_DAYS:
        raise ReminderInputError(f"horizon_days must be between 0 and {MAX_HORIZON_DAYS}.")
    today = today or date.today()
    reminders = []
    for interview in interviews:
        outcome = interview.get("outcome", "scheduled")
        if outcome in {"passed", "failed", "completed", "cancelled"}:
            continue
        due = _parse_date(interview.get("scheduled_date"))
        if due is None:
            continue
        delta = (due - today).days
        if delta < 0 or delta > horizon_days:
            continue
        kind = interview.get("interview_type", "interview").replace("_", " ").title()
        reminders.append(_candidate(
            "interview", owner_id, interview.get("id"),
            f"Prepare for {kind}", due, today,
            {"interview_type": interview.get("interview_type", ""),
             "company": interview.get("company", ""),
             "role": interview.get("role", "")},
        ))
    return reminders


def plan_task_reminders(
    tasks: Iterable[Mapping],
    *,
    owner_id: Any,
    today: date | None = None,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
) -> list[dict]:
    today = today or date.today()
    reminders = []
    for task in tasks:
        if task.get("completed") or task.get("status") in {"done", "completed", "cancelled"}:
            continue
        due = _parse_date(task.get("due_date") or task.get("due_at"))
        if due is None:
            continue
        delta = (due - today).days
        if delta > horizon_days:
            continue
        reminders.append(_candidate(
            "career_task", owner_id, task.get("id"),
            task.get("title") or task.get("name") or "Complete career task",
            due, today, {"priority": task.get("priority", "normal")},
        ))
    return reminders


def combine_reminders(*groups: Iterable[Mapping], limit: int = MAX_REMINDERS) -> list[dict]:
    """Merge candidates, deduplicate by key, and sort most urgent first."""
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= MAX_REMINDERS:
        raise ReminderInputError(f"limit must be between 1 and {MAX_REMINDERS}.")
    unique = {}
    for group in groups:
        for reminder in group:
            key = reminder.get("idempotency_key")
            if not key:
                continue
            previous = unique.get(key)
            if previous is None or reminder.get("days_from_today", 0) < previous.get("days_from_today", 0):
                unique[key] = dict(reminder)
    ordered = sorted(unique.values(), key=lambda item: (
        item.get("days_from_today", 0),
        item.get("due_date", ""),
        item.get("kind", ""),
        str(item.get("object_id", "")),
    ))
    return ordered[:limit]


def reminder_summary(reminders: Iterable[Mapping]) -> dict:
    items = list(reminders)
    return {
        "total": len(items),
        "overdue": sum(1 for item in items if item.get("urgency") == "overdue"),
        "today": sum(1 for item in items if item.get("urgency") == "today"),
        "soon": sum(1 for item in items if item.get("urgency") == "soon"),
        "upcoming": sum(1 for item in items if item.get("urgency") == "upcoming"),
        "by_kind": {
            kind: sum(1 for item in items if item.get("kind") == kind)
            for kind in sorted({item.get("kind", "unknown") for item in items})
        },
    }
