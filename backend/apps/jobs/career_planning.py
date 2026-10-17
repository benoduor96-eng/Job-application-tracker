"""Deterministic planning helpers for a sustainable job-search routine."""
from collections import defaultdict
from datetime import date, datetime, timedelta
from math import ceil
from typing import Iterable, Mapping

TASK_TYPES = {"research", "tailor_resume", "write_cover_letter", "apply", "follow_up",
              "network", "interview_prep", "skill_practice", "review"}
DEFAULT_MINUTES = {"research": 20, "tailor_resume": 35, "write_cover_letter": 25,
                   "apply": 20, "follow_up": 10, "network": 15, "interview_prep": 30,
                   "skill_practice": 30, "review": 15}
PRIORITY_WEIGHT = {"urgent": 4, "high": 3, "normal": 2, "low": 1}

def _day(value):
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

def _int(value, default=0, minimum=0, maximum=100000):
    try:
        return max(minimum, min(maximum, int(value)))
    except (TypeError, ValueError):
        return default

def _priority(value):
    return value if value in PRIORITY_WEIGHT else "normal"

def validate_task(task: Mapping) -> dict:
    kind = str(task.get("type") or "apply").strip().lower()
    if kind not in TASK_TYPES:
        raise ValueError(f"Unsupported task type: {kind}")
    title = str(task.get("title") or kind.replace("_", " ").title()).strip()
    if not title:
        raise ValueError("Task title cannot be empty")
    due = _day(task.get("due_date"))
    minutes = _int(task.get("estimated_minutes"), DEFAULT_MINUTES[kind], 1, 1440)
    return {"id": task.get("id"), "title": title[:180], "type": kind, "priority": _priority(task.get("priority")),
            "due_date": due, "estimated_minutes": minutes, "completed": bool(task.get("completed", False)),
            "application_id": task.get("application_id"), "notes": str(task.get("notes") or "")[:2000]}

def capacity_for_day(tasks: Iterable[Mapping], daily_minutes: int = 120, target_date=None) -> dict:
    day = _day(target_date) or date.today()
    normalized = [validate_task(task) for task in tasks]
    due_today = [task for task in normalized if task["due_date"] == day and not task["completed"]]
    estimated = sum(task["estimated_minutes"] for task in due_today)
    capacity = _int(daily_minutes, 120, 0, 1440)
    return {"date": day.isoformat(), "task_count": len(due_today), "estimated_minutes": estimated,
            "capacity_minutes": capacity, "remaining_minutes": max(0, capacity - estimated),
            "over_capacity_minutes": max(0, estimated - capacity),
            "is_over_capacity": estimated > capacity,
            "tasks": [{**task, "due_date": task["due_date"].isoformat()} for task in due_today]}

def prioritize_tasks(tasks: Iterable[Mapping], today=None) -> list[dict]:
    current = _day(today) or date.today()
    normalized = [validate_task(task) for task in tasks if not task.get("completed", False)]
    def key(task):
        due = task["due_date"]
        overdue = due is not None and due < current
        days = (due - current).days if due else 9999
        return (0 if overdue else 1, days, -PRIORITY_WEIGHT[task["priority"]],
                task["estimated_minutes"], task["title"].casefold(), str(task["id"] or ""))
    normalized.sort(key=key)
    output = []
    for index, task in enumerate(normalized, 1):
        due = task["due_date"]
        output.append({**task, "rank": index, "overdue": bool(due and due < current),
                       "days_until_due": (due - current).days if due else None,
                       "due_date": due.isoformat() if due else None})
    return output

def build_week_plan(tasks: Iterable[Mapping], daily_capacity: Mapping | None = None,
                    start_date=None, days: int = 7) -> dict:
    if not 1 <= days <= 31:
        raise ValueError("days must be between 1 and 31")
    start = _day(start_date) or date.today()
    capacity = daily_capacity or {}
    normalized = prioritize_tasks(tasks, today=start)
    schedule = []
    for offset in range(days):
        current = start + timedelta(days=offset)
        cap = _int(capacity.get(current.isoformat(), 120), 120, 0, 1440)
        schedule.append({"date": current, "capacity": cap, "minutes": 0, "tasks": []})
    unscheduled = []
    for task in normalized:
        duration = task["estimated_minutes"]
        due = _day(task["due_date"])
        candidates = schedule
        if due is not None:
            candidates = [day for day in schedule if day["date"] <= due]
            if not candidates:
                unscheduled.append({**task, "reason": "Due date precedes plan window"})
                continue
        fit = next((day for day in candidates if day["minutes"] + duration <= day["capacity"]), None)
        if fit is None:
            unscheduled.append({**task, "reason": "No available capacity before deadline"})
            continue
        fit["tasks"].append(task)
        fit["minutes"] += duration
    for day in schedule:
        day["date"] = day["date"].isoformat()
        day["remaining_minutes"] = day["capacity"] - day["minutes"]
        day["utilization_percent"] = round(100 * day["minutes"] / day["capacity"], 1) if day["capacity"] else 0
    return {"start_date": start.isoformat(), "days": days, "schedule": schedule,
            "scheduled_count": sum(len(day["tasks"]) for day in schedule),
            "unscheduled_count": len(unscheduled), "unscheduled": unscheduled,
            "disclaimer": "This is a suggested plan. Reassess priorities and rest time as circumstances change."}

def weekly_goal_progress(tasks: Iterable[Mapping], goals: Mapping | None = None, start_date=None) -> dict:
    start = _day(start_date) or date.today()
    monday = start - timedelta(days=start.weekday())
    sunday = monday + timedelta(days=6)
    targets = {"applications": 5, "networking": 3, "practice_minutes": 90, "follow_ups": 5}
    if goals:
        for key in targets:
            if key in goals:
                targets[key] = _int(goals[key], targets[key], 0, 10000)
    counts = defaultdict(int)
    for raw in tasks:
        task = validate_task(raw)
        due = task["due_date"]
        if not task["completed"] or due is None or not monday <= due <= sunday:
            continue
        if task["type"] == "apply":
            counts["applications"] += 1
        elif task["type"] == "network":
            counts["networking"] += 1
        elif task["type"] == "skill_practice":
            counts["practice_minutes"] += task["estimated_minutes"]
        elif task["type"] == "follow_up":
            counts["follow_ups"] += 1
    items = {key: {"target": target, "actual": counts[key],
                   "percent": round(100 * counts[key] / target, 1) if target else 100,
                   "complete": counts[key] >= target} for key, target in targets.items()}
    return {"week_start": monday.isoformat(), "week_end": sunday.isoformat(), "goals": items,
            "completed_goals": sum(item["complete"] for item in items.values()),
            "total_goals": len(items)}

def effort_estimate(application_count: int, minutes_per_application: int = 30,
                    networking_events: int = 3, interview_count: int = 1) -> dict:
    count = _int(application_count, 0, 0, 10000)
    minutes = _int(minutes_per_application, 30, 1, 1440)
    networking = _int(networking_events, 3, 0, 10000)
    interviews = _int(interview_count, 1, 0, 10000)
    application_minutes = count * minutes
    networking_minutes = networking * DEFAULT_MINUTES["network"]
    interview_minutes = interviews * DEFAULT_MINUTES["interview_prep"]
    total = application_minutes + networking_minutes + interview_minutes
    return {"application_count": count, "application_minutes": application_minutes,
            "networking_minutes": networking_minutes, "interview_prep_minutes": interview_minutes,
            "total_minutes": total, "total_hours": round(total / 60, 2),
            "suggested_days_at_120_minutes": ceil(total / 120) if total else 0,
            "note": "Planning estimate only; quality and recovery time matter more than raw volume."}

def task_backlog_report(tasks: Iterable[Mapping], today=None) -> dict:
    current = _day(today) or date.today()
    rows = [validate_task(task) for task in tasks]
    incomplete = [row for row in rows if not row["completed"]]
    overdue = [row for row in incomplete if row["due_date"] and row["due_date"] < current]
    by_type = defaultdict(int)
    by_priority = defaultdict(int)
    for row in incomplete:
        by_type[row["type"]] += 1
        by_priority[row["priority"]] += 1
    return {"total": len(rows), "completed": len(rows) - len(incomplete), "open": len(incomplete),
            "overdue": len(overdue), "overdue_minutes": sum(row["estimated_minutes"] for row in overdue),
            "open_minutes": sum(row["estimated_minutes"] for row in incomplete),
            "by_type": dict(sorted(by_type.items())), "by_priority": dict(sorted(by_priority.items())),
            "oldest_due_date": min((row["due_date"] for row in overdue), default=None).isoformat()
                if overdue else None,
            "overdue_task_ids": [row["id"] for row in overdue]}

def workload_recommendations(backlog: Mapping, capacity_minutes: int = 120) -> list[dict]:
    recommendations = []
    open_minutes = _int(backlog.get("open_minutes"), 0, 0, 10**9)
    overdue = _int(backlog.get("overdue"), 0, 0, 10**6)
    capacity = _int(capacity_minutes, 120, 1, 1440)
    if overdue:
        recommendations.append({"code": "review_overdue", "severity": "high",
                                 "message": f"Review {overdue} overdue task(s) and remove obsolete commitments."})
    days = ceil(open_minutes / capacity) if open_minutes else 0
    if days > 5:
        recommendations.append({"code": "reduce_scope", "severity": "medium",
                                 "message": f"The current backlog represents about {days} full-capacity days."})
    if not recommendations:
        recommendations.append({"code": "maintain_rhythm", "severity": "info",
                                 "message": "Backlog is manageable; keep a realistic pace and protect rest time."})
    return recommendations

def compare_week_plans(first: Mapping, second: Mapping) -> dict:
    def totals(plan):
        schedule = plan.get("schedule") or []
        return {"scheduled": sum(len(day.get("tasks") or []) for day in schedule),
                "minutes": sum(_int(day.get("minutes"), 0) for day in schedule),
                "capacity": sum(_int(day.get("capacity"), 0) for day in schedule),
                "unscheduled": _int(plan.get("unscheduled_count"), 0)}
    left, right = totals(first), totals(second)
    return {"first": left, "second": right,
            "delta": {key: right[key] - left[key] for key in left},
            "better_capacity_fit": right["unscheduled"] < left["unscheduled"],
            "warning": "A plan comparison measures scheduling fit, not job-search quality."}

def normalize_goal_payload(payload: Mapping) -> dict:
    allowed = {"applications", "networking", "practice_minutes", "follow_ups"}
    unknown = set(payload) - allowed
    if unknown:
        raise ValueError("Unknown goal fields: " + ", ".join(sorted(unknown)))
    result = {}
    for key, value in payload.items():
        try:
            numeric = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"{key} must be an integer")
        if numeric < 0 or numeric > 10000:
            raise ValueError(f"{key} must be between 0 and 10000")
        result[key] = numeric
    return result
