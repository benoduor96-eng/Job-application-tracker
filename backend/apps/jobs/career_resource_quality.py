"""Learning-resource quality checks that preserve user-provided entries."""
from typing import Iterable, Mapping

def normalize_resource_key(resource: Mapping) -> tuple:
    title = " ".join(str(resource.get("title") or "").lower().split())
    url = str(resource.get("url") or "").strip().rstrip("/").lower()
    provider = " ".join(str(resource.get("provider") or "").lower().split())
    return title, url, provider

def resource_quality(resource: Mapping) -> dict:
    title = str(resource.get("title") or "").strip()
    url = str(resource.get("url") or "").strip()
    skills = [str(value).strip() for value in resource.get("skills", []) if str(value).strip()]
    issues = []
    if not title:
        issues.append("missing_title")
    if not url:
        issues.append("missing_url")
    elif not url.lower().startswith(("https://", "http://")):
        issues.append("unusual_url_scheme")
    if not skills:
        issues.append("missing_skill_tags")
    if not str(resource.get("provider") or "").strip():
        issues.append("missing_provider")
    if not str(resource.get("notes") or "").strip():
        issues.append("missing_personal_context")
    return {"id": resource.get("id"), "title": title, "issues": issues,
            "quality_percent": round(100*(5-len(issues))/5, 1),
            "review_recommended": bool(issues)}

def duplicate_resource_groups(resources: Iterable[Mapping]) -> list[dict]:
    groups = {}
    for index, resource in enumerate(resources):
        key = normalize_resource_key(resource)
        if not any(key):
            continue
        groups.setdefault(key, []).append({"id": resource.get("id", index),
                                           "title": str(resource.get("title") or "")[:200]})
    duplicates = []
    for key, rows in groups.items():
        if len(rows) > 1:
            duplicates.append({"key": list(key), "resources": rows, "count": len(rows),
                               "manual_review_required": True})
    return sorted(duplicates, key=lambda row: (-row["count"], str(row["key"])))

def resource_review_queue(resources: Iterable[Mapping]) -> dict:
    rows = [resource_quality(resource) for resource in resources]
    duplicates = duplicate_resource_groups(resources)
    return {"resource_count": len(rows), "clean_count": sum(not row["issues"] for row in rows),
            "review_count": sum(row["review_recommended"] for row in rows),
            "average_quality_percent": round(sum(row["quality_percent"] for row in rows)/len(rows), 1) if rows else 100,
            "items": rows, "duplicate_groups": duplicates,
            "automatic_deletions_performed": False,
            "note": "Duplicate candidates are suggestions; verify records before editing or removing them."}
