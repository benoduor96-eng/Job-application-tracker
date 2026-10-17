"""Milestone planning for application preparation, interviews, and follow-through."""
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping

MILESTONE_TYPES = {"research", "resume", "application", "follow_up", "interview", "decision", "learning"}
def _date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None

def validate_milestone(item: Mapping) -> dict:
    title = str(item.get("title") or "").strip()
    if not title:
        raise ValueError("Milestone title is required")
    kind = str(item.get("milestone_type") or "application").lower()
    if kind not in MILESTONE_TYPES:
        raise ValueError("Unsupported milestone type")
    status = str(item.get("status") or "planned").lower()
    if status not in {"planned", "in_progress", "completed", "blocked", "cancelled"}:
        raise ValueError("Unsupported milestone status")
    due = _date(item.get("due_date"))
    created = _date(item.get("created_date"))
    return {"id": item.get("id"), "application_id": item.get("application_id"),
            "title": title[:180], "milestone_type": kind, "status": status,
            "due_date": due, "created_date": created,
            "priority": str(item.get("priority") or "normal").lower(),
            "dependencies": list(item.get("dependencies") or []),
            "notes": str(item.get("notes") or "")[:2000]}

def milestone_progress(items: Iterable[Mapping], today=None) -> dict:
    current = _date(today) or date.today()
    rows = [validate_milestone(item) for item in items]
    counts = {status: sum(row["status"] == status for row in rows)
              for status in ("planned", "in_progress", "completed", "blocked", "cancelled")}
    overdue = [row for row in rows if row["due_date"] and row["due_date"] < current
               and row["status"] not in {"completed", "cancelled"}]
    applicable = len(rows) - counts["cancelled"]
    complete_percent = round(100 * counts["completed"] / applicable, 1) if applicable else 100
    return {"total": len(rows), "counts": counts, "completion_percent": complete_percent,
            "overdue_count": len(overdue), "overdue_ids": [row["id"] for row in overdue],
            "overdue_titles": [row["title"] for row in overdue]}

def dependency_report(items: Iterable[Mapping]) -> dict:
    rows = [validate_milestone(item) for item in items]
    identifiers = {str(row["id"]) for row in rows if row["id"] is not None}
    errors, dependencies = [], {}
    for row in rows:
        key = str(row["id"])
        deps = [str(dep) for dep in row["dependencies"]]
        dependencies[key] = deps
        for dep in deps:
            if dep not in identifiers:
                errors.append({"milestone_id": row["id"], "code": "missing_dependency", "dependency": dep})
            if dep == key:
                errors.append({"milestone_id": row["id"], "code": "self_dependency"})
    visiting, visited = set(), set()
    def visit(node, stack):
        if node in visiting:
            errors.append({"milestone_id": node, "code": "dependency_cycle", "path": stack + [node]})
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in dependencies.get(node, []):
            if dependency in dependencies:
                visit(dependency, stack + [node])
        visiting.remove(node)
        visited.add(node)
    for node in dependencies:
        visit(node, [])
    return {"valid": not errors, "errors": errors, "milestone_count": len(rows)}

def propose_milestones(application_id, company: str, role: str, applied_date=None) -> list[dict]:
    company, role = str(company or "").strip(), str(role or "").strip()
    if not company or not role:
        raise ValueError("Company and role are required")
    start = _date(applied_date) or date.today()
    definitions = [
        ("Review role and employer", "research", 0),
        ("Tailor resume and verify evidence", "resume", 1),
        ("Submit or confirm application", "application", 2),
        ("Review follow-up timing", "follow_up", 7),
        ("Review outcome and record learning", "decision", 21),
    ]
    return [{"application_id": application_id, "title": title + " — " + role,
             "milestone_type": kind, "due_date": (start + timedelta(days=offset)).isoformat(),
             "status": "planned", "dependencies": [],
             "notes": "Suggested milestone for " + company + "; edit to fit the actual process.",
             "persisted": False} for title, kind, offset in definitions]

def milestone_review(items: Iterable[Mapping], today=None) -> dict:
    rows = [validate_milestone(item) for item in items]
    progress = milestone_progress(items, today)
    blocked = [row for row in rows if row["status"] == "blocked"]
    upcoming = [row for row in rows if row["due_date"] and row["due_date"] >= (_date(today) or date.today())
                and row["status"] not in {"completed", "cancelled"}]
    upcoming.sort(key=lambda row: (row["due_date"], row["title"].casefold()))
    return {"progress": progress, "blocked": [{"id": row["id"], "title": row["title"]} for row in blocked],
            "upcoming": [{"id": row["id"], "title": row["title"], "due_date": row["due_date"].isoformat()}
                         for row in upcoming[:20]],
            "actions": (["Review blockers and adjust commitments."] if blocked else []) +
                       (["Review overdue milestones."] if progress["overdue_count"] else []),
            "automatic_updates_performed": False}
