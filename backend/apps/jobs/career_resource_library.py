"""Personal learning resource catalog helpers with bounded metadata and explicit review status."""
from typing import Iterable, Mapping

RESOURCE_TYPES = {"article", "course", "video", "book", "documentation", "project", "practice", "other"}
RESOURCE_STATUSES = {"saved", "in_progress", "completed", "skipped"}
def validate_resource(resource: Mapping) -> dict:
    title = str(resource.get("title") or "").strip()
    if not title:
        raise ValueError("Resource title is required")
    kind = str(resource.get("resource_type") or "other").lower()
    status = str(resource.get("status") or "saved").lower()
    if kind not in RESOURCE_TYPES:
        raise ValueError("Unsupported resource type")
    if status not in RESOURCE_STATUSES:
        raise ValueError("Unsupported resource status")
    url = str(resource.get("url") or "").strip()
    if url and not url.lower().startswith(("http://", "https://")):
        raise ValueError("Resource URL must use HTTP or HTTPS")
    try:
        minutes = int(resource.get("estimated_minutes") or 0)
    except (ValueError, TypeError):
        raise ValueError("estimated_minutes must be an integer")
    if not 0 <= minutes <= 100000:
        raise ValueError("estimated_minutes must be between 0 and 100000")
    return {"id": resource.get("id"), "title": title[:200], "resource_type": kind, "status": status,
            "url": url[:1500], "provider": str(resource.get("provider") or "")[:160],
            "skills": sorted({str(skill).strip().lower()[:80] for skill in resource.get("skills", []) if str(skill).strip()}),
            "estimated_minutes": minutes, "rating": _rating(resource.get("rating")),
            "notes": str(resource.get("notes") or "")[:2000]}

def _rating(value):
    if value in (None, ""):
        return None
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValueError("rating must be an integer from 1 to 5")
    if not 1 <= value <= 5:
        raise ValueError("rating must be between 1 and 5")
    return value

def rank_resources(resources: Iterable[Mapping], target_skills: Iterable[str] = (),
                   preferred_types: Iterable[str] = ()) -> list[dict]:
    targets = {str(skill).strip().lower() for skill in target_skills if str(skill).strip()}
    types = {str(kind).strip().lower() for kind in preferred_types if str(kind).strip()}
    invalid = types - RESOURCE_TYPES
    if invalid:
        raise ValueError("Unsupported preferred resource type")
    rows = []
    for resource in resources:
        item = validate_resource(resource)
        overlap = sorted(targets & set(item["skills"]))
        score = 10 * len(overlap) + (5 if item["resource_type"] in types else 0)
        score += item["rating"] or 0
        if item["status"] == "completed":
            score -= 100
        rows.append({"resource": item, "matched_skills": overlap, "relevance_score": score})
    rows.sort(key=lambda row: (-row["relevance_score"], row["resource"]["title"].casefold(), str(row["resource"]["id"])))
    return [{"rank": index, **row} for index, row in enumerate(rows, 1)]

def resource_learning_queue(resources: Iterable[Mapping], available_minutes: int = 120) -> dict:
    if not isinstance(available_minutes, int) or not 0 <= available_minutes <= 10080:
        raise ValueError("available_minutes must be between 0 and 10080")
    rows = [validate_resource(item) for item in resources if item.get("status", "saved") != "completed"]
    rows.sort(key=lambda row: (row["estimated_minutes"] == 0, row["estimated_minutes"], row["title"].casefold()))
    selected, deferred, spent = [], [], 0
    for row in rows:
        if spent + row["estimated_minutes"] <= available_minutes:
            selected.append(row)
            spent += row["estimated_minutes"]
        else:
            deferred.append({"id": row["id"], "title": row["title"], "reason": "outside_time_budget"})
    return {"available_minutes": available_minutes, "planned_minutes": spent, "selected": selected,
            "deferred": deferred, "completed_resources_excluded": True,
            "note": "Prioritize practice and evidence, not simply consuming more resources."}

def resource_progress(resources: Iterable[Mapping]) -> dict:
    rows = [validate_resource(item) for item in resources]
    counts = {status: sum(row["status"] == status for row in rows) for status in sorted(RESOURCE_STATUSES)}
    minutes = sum(row["estimated_minutes"] for row in rows if row["status"] == "completed")
    skills = sorted({skill for row in rows if row["status"] == "completed" for skill in row["skills"]})
    return {"total": len(rows), "counts": counts, "completed_minutes": minutes,
            "completed_hours": round(minutes / 60, 2), "skills_touched": skills,
            "completion_percent": round(100 * counts["completed"] / len(rows), 1) if rows else 0}
