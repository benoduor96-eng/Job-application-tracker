"""Measurable career goal tracking with reviewable milestones and no automatic edits."""
from datetime import date, datetime
from typing import Iterable, Mapping

GOAL_TYPES = {"applications", "networking", "learning_hours", "portfolio_items", "interviews", "custom"}
def _date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None

def validate_goal(goal: Mapping) -> dict:
    title = str(goal.get("title") or "").strip()
    if not title:
        raise ValueError("Goal title is required")
    kind = str(goal.get("goal_type") or "custom").lower()
    if kind not in GOAL_TYPES:
        raise ValueError("Unsupported goal type")
    try:
        target = float(goal.get("target", 0))
        current = float(goal.get("current", 0))
    except (TypeError, ValueError):
        raise ValueError("Goal target and current progress must be numeric")
    if target <= 0 or target > 1e9 or current < 0 or current > 1e9:
        raise ValueError("Target must be positive and progress non-negative")
    if kind == "learning_hours" and (target > 100000 or current > 100000):
        raise ValueError("Learning-hour values exceed supported limits")
    status = str(goal.get("status") or "active").lower()
    if status not in {"active", "paused", "completed", "cancelled"}:
        raise ValueError("Unsupported goal status")
    return {"id": goal.get("id"), "title": title[:180], "goal_type": kind, "target": target,
            "current": current, "start_date": _date(goal.get("start_date")),
            "due_date": _date(goal.get("due_date")), "status": status,
            "unit": str(goal.get("unit") or _default_unit(kind))[:40],
            "notes": str(goal.get("notes") or "")[:2000]}

def _default_unit(kind):
    return {"applications": "applications", "networking": "contacts", "learning_hours": "hours",
            "portfolio_items": "items", "interviews": "interviews"}.get(kind, "units")

def goal_progress(goal: Mapping, today=None) -> dict:
    row = validate_goal(goal)
    current = _date(today) or date.today()
    percent = min(100.0, round(100 * row["current"] / row["target"], 1))
    due = row["due_date"]
    days_left = (due-current).days if due else None
    days_total = (due-row["start_date"]).days if due and row["start_date"] else None
    elapsed = (current-row["start_date"]).days if row["start_date"] else None
    remaining = max(0.0, row["target"]-row["current"])
    daily_pace = round(remaining / days_left, 2) if days_left and days_left > 0 else None
    if row["status"] == "completed" or percent >= 100:
        state = "complete"
    elif row["status"] != "active":
        state = row["status"]
    elif due and due < current:
        state = "overdue"
    elif days_total and elapsed is not None and days_total > 0 and percent < min(100, 100*elapsed/days_total):
        state = "behind_pace"
    else:
        state = "on_track_or_insufficient_data"
    return {"id": row["id"], "title": row["title"], "goal_type": row["goal_type"],
            "current": row["current"], "target": row["target"], "unit": row["unit"],
            "progress_percent": percent, "remaining": remaining, "days_left": days_left,
            "suggested_daily_pace": daily_pace, "state": state,
            "note": "Pace estimates are approximate; adjust targets to available time and wellbeing."}

def goals_dashboard(goals: Iterable[Mapping], today=None) -> dict:
    rows = [goal_progress(goal, today) for goal in goals]
    counts = {state: sum(row["state"] == state for row in rows)
              for state in ("complete", "active", "paused", "cancelled", "overdue", "behind_pace", "on_track_or_insufficient_data")}
    return {"goal_count": len(rows), "completed_count": counts["complete"],
            "average_progress_percent": round(sum(row["progress_percent"] for row in rows)/len(rows), 1) if rows else 0,
            "states": counts, "goals": sorted(rows, key=lambda row: (row["state"] == "complete", row["days_left"] is None,
                                                                       row["days_left"] if row["days_left"] is not None else 99999,
                                                                       row["title"].casefold()))}

def goal_check_in(goal: Mapping, progress_note: str, new_current=None, checked_on=None) -> dict:
    row = validate_goal(goal)
    note = str(progress_note or "").strip()
    if len(note) < 5:
        raise ValueError("A useful check-in note is required")
    if new_current is None:
        current = row["current"]
    else:
        try:
            current = float(new_current)
        except (TypeError, ValueError):
            raise ValueError("Progress must be numeric")
        if current < 0 or current > 1e9:
            raise ValueError("Progress must be non-negative")
    return {"goal_id": row["id"], "checked_on": (_date(checked_on) or date.today()).isoformat(),
            "previous_value": row["current"], "reported_value": current, "progress_note": note[:2000],
            "persisted": False, "goal_complete": current >= row["target"]}

def compare_goal_snapshots(first: Iterable[Mapping], second: Iterable[Mapping]) -> dict:
    left = {str(row.get("id")): validate_goal(row) for row in first}
    right = {str(row.get("id")): validate_goal(row) for row in second}
    keys = sorted(set(left) | set(right))
    changes = []
    for key in keys:
        old, new = left.get(key), right.get(key)
        changes.append({"id": (new or old)["id"], "title": (new or old)["title"],
                        "change": "added" if old is None else "removed" if new is None else "updated" if old != new else "unchanged",
                        "previous_current": old["current"] if old else None,
                        "current": new["current"] if new else None})
    return {"count": len(changes), "changes": changes,
            "warning": "Snapshot differences are descriptive and do not independently verify progress."}
