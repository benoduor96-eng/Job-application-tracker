"""Sustainable job-search budgeting helpers."""
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping

ACTIVITY_MINUTES = {"research": 20, "resume": 35, "cover_letter": 25, "application": 20,
                    "follow_up": 10, "networking": 15, "interview_prep": 30, "learning": 30, "review": 15}
def _date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None

def validate_activity(activity: Mapping) -> dict:
    kind = str(activity.get("type") or "").lower()
    if kind not in ACTIVITY_MINUTES:
        raise ValueError("Unsupported activity type")
    try:
        minutes = int(activity.get("minutes", ACTIVITY_MINUTES[kind]))
    except (ValueError, TypeError):
        raise ValueError("minutes must be an integer")
    if not 0 <= minutes <= 1440:
        raise ValueError("minutes must be between 0 and 1440")
    day = _date(activity.get("date"))
    if day is None:
        raise ValueError("A valid activity date is required")
    return {"id": activity.get("id"), "type": kind, "minutes": minutes, "date": day,
            "completed": bool(activity.get("completed", True)), "quality_note": str(activity.get("quality_note") or "")[:500]}

def summarize_effort(activities: Iterable[Mapping], start_date=None, end_date=None) -> dict:
    rows = [validate_activity(row) for row in activities]
    start, end = _date(start_date), _date(end_date)
    if start and end and end < start:
        raise ValueError("end_date must not precede start_date")
    filtered = [row for row in rows if (start is None or row["date"] >= start)
                and (end is None or row["date"] <= end)]
    completed = [row for row in filtered if row["completed"]]
    by_type = {kind: sum(row["minutes"] for row in completed if row["type"] == kind)
               for kind in sorted(ACTIVITY_MINUTES)}
    by_day = {}
    for row in completed:
        key = row["date"].isoformat()
        by_day[key] = by_day.get(key, 0) + row["minutes"]
    return {"activity_count": len(filtered), "completed_count": len(completed),
            "total_minutes": sum(row["minutes"] for row in completed),
            "total_hours": round(sum(row["minutes"] for row in completed)/60, 2),
            "by_activity_type_minutes": by_type,
            "by_day_minutes": dict(sorted(by_day.items())),
            "average_minutes_per_active_day": round(sum(by_day.values())/len(by_day), 1) if by_day else 0}

def weekly_effort_report(activities: Iterable[Mapping], week_start=None, weekly_budget_minutes: int = 600) -> dict:
    start = _date(week_start) or date.today()
    start = start - timedelta(days=start.weekday())
    end = start + timedelta(days=6)
    if not isinstance(weekly_budget_minutes, int) or not 0 <= weekly_budget_minutes <= 10080:
        raise ValueError("weekly_budget_minutes must be between 0 and 10080")
    summary = summarize_effort(activities, start, end)
    total = summary["total_minutes"]
    return {"week_start": start.isoformat(), "week_end": end.isoformat(), **summary,
            "budget_minutes": weekly_budget_minutes, "remaining_minutes": max(0, weekly_budget_minutes-total),
            "over_budget_minutes": max(0, total-weekly_budget_minutes),
            "budget_used_percent": round(100*total/weekly_budget_minutes, 1) if weekly_budget_minutes else 0,
            "wellbeing_note": "A budget is a planning aid, not a requirement to work beyond your capacity."}

def compare_effort_periods(first: Iterable[Mapping], second: Iterable[Mapping]) -> dict:
    left, right = summarize_effort(first), summarize_effort(second)
    return {"first": left, "second": right,
            "delta_minutes": right["total_minutes"]-left["total_minutes"],
            "delta_by_activity": {key: right["by_activity_type_minutes"][key]-left["by_activity_type_minutes"][key]
                                  for key in ACTIVITY_MINUTES},
            "warning": "More time spent does not necessarily mean better outcomes; review quality and rest as well."}

def workload_balance(activities: Iterable[Mapping]) -> dict:
    summary = summarize_effort(activities)
    values = summary["by_activity_type_minutes"]
    applications = values["application"] + values["resume"] + values["cover_letter"]
    preparation = values["research"] + values["interview_prep"] + values["learning"]
    relationships = values["networking"] + values["follow_up"]
    total = applications + preparation + relationships + values["review"]
    components = {"applications_and_materials": applications, "preparation_and_learning": preparation,
                  "relationships": relationships, "review": values["review"]}
    return {"total_minutes": total, "components": components,
            "shares_percent": {key: round(100*value/total, 1) if total else 0 for key, value in components.items()},
            "note": "There is no universal ideal allocation; adapt to deadlines, goals, and available energy."}

def estimate_activity_plan(targets: Mapping, available_minutes: int = 600) -> dict:
    if not isinstance(available_minutes, int) or not 0 <= available_minutes <= 10080:
        raise ValueError("available_minutes must be between 0 and 10080")
    unknown = set(targets) - set(ACTIVITY_MINUTES)
    if unknown:
        raise ValueError("Unknown activity types: " + ", ".join(sorted(unknown)))
    plan, total = [], 0
    for kind, count in targets.items():
        try:
            count = int(count)
        except (ValueError, TypeError):
            raise ValueError(f"{kind} count must be an integer")
        if not 0 <= count <= 10000:
            raise ValueError(f"{kind} count must be between 0 and 10000")
        minutes = count * ACTIVITY_MINUTES[kind]
        total += minutes
        plan.append({"type": kind, "count": count, "estimated_minutes": minutes})
    return {"activities": plan, "estimated_minutes": total, "available_minutes": available_minutes,
            "within_budget": total <= available_minutes, "over_budget_minutes": max(0, total-available_minutes),
            "suggestion": "Adjust the plan to fit your actual time; do not optimize for volume alone."}
