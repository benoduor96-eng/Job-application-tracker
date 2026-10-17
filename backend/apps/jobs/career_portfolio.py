"""Portfolio planning helpers that separate claims from verifiable evidence."""
from datetime import date, datetime
from typing import Iterable, Mapping

EVIDENCE_TYPES = {"repository", "demo", "case_study", "certificate", "writing_sample", "reference", "other"}
def _date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None

def validate_portfolio_item(item: Mapping) -> dict:
    title = str(item.get("title") or "").strip()
    if not title:
        raise ValueError("Portfolio item title is required")
    kind = str(item.get("evidence_type") or "other").lower()
    if kind not in EVIDENCE_TYPES:
        raise ValueError("Unsupported evidence type")
    url = str(item.get("url") or "").strip()
    if url and not url.lower().startswith(("https://", "http://")):
        raise ValueError("Portfolio URLs must use HTTP or HTTPS")
    status = str(item.get("status") or "draft").lower()
    if status not in {"draft", "ready_for_review", "published", "archived"}:
        raise ValueError("Unsupported portfolio status")
    return {"id": item.get("id"), "title": title[:180], "evidence_type": kind,
            "url": url[:1000], "status": status, "role": str(item.get("role") or "")[:180],
            "skills": sorted({str(skill).strip().lower()[:80] for skill in item.get("skills", []) if str(skill).strip()}),
            "created_date": _date(item.get("created_date")), "updated_date": _date(item.get("updated_date")),
            "description": str(item.get("description") or "")[:3000],
            "contribution": str(item.get("contribution") or "")[:2000],
            "confidentiality_checked": bool(item.get("confidentiality_checked", False))}

def portfolio_readiness(item: Mapping) -> dict:
    row = validate_portfolio_item(item)
    checks = {
        "has_description": bool(row["description"]),
        "has_contribution": bool(row["contribution"]),
        "has_skills": bool(row["skills"]),
        "has_public_evidence": bool(row["url"]),
        "confidentiality_checked": row["confidentiality_checked"],
    }
    blockers = [key for key, value in checks.items() if not value]
    return {"id": row["id"], "title": row["title"], "checks": checks,
            "readiness_percent": round(100 * sum(checks.values()) / len(checks)),
            "blockers": blockers, "ready_for_review": not blockers,
            "warning": "Never publish confidential employer or client material without permission."}

def portfolio_skill_coverage(items: Iterable[Mapping], target_skills: Iterable[str] = ()) -> dict:
    rows = [validate_portfolio_item(item) for item in items]
    coverage = {}
    for row in rows:
        if row["status"] not in {"ready_for_review", "published"}:
            continue
        for skill in row["skills"]:
            coverage.setdefault(skill, []).append(row["title"])
    targets = sorted({str(skill).strip().lower() for skill in target_skills if str(skill).strip()})
    missing = [skill for skill in targets if skill not in coverage]
    return {"item_count": len(rows), "reviewable_item_count": sum(row["status"] in {"ready_for_review", "published"} for row in rows),
            "skills_covered": {skill: sorted(titles) for skill, titles in sorted(coverage.items())},
            "target_skills": targets, "uncovered_target_skills": missing,
            "note": "Coverage means a skill is tagged to an item, not that the item proves proficiency."}

def accomplishment_entry(title: str, context: str, action: str, result: str,
                         evidence: str = "", metric: str = "") -> dict:
    values = {"title": title, "context": context, "action": action, "result": result}
    cleaned = {key: str(value or "").strip()[:1500] for key, value in values.items()}
    missing = [key for key, value in cleaned.items() if not value]
    if missing:
        raise ValueError("Missing accomplishment fields: " + ", ".join(missing))
    return {**cleaned, "evidence": str(evidence or "").strip()[:1000],
            "metric": str(metric or "").strip()[:300], "verified": False,
            "guidance": "Use accurate facts; do not invent metrics or overstate personal contribution."}

def convert_accomplishment_to_bullet(entry: Mapping, maximum_chars: int = 280) -> dict:
    if not 80 <= maximum_chars <= 600:
        raise ValueError("maximum_chars must be between 80 and 600")
    title = str(entry.get("title") or "").strip()
    action = str(entry.get("action") or "").strip()
    result = str(entry.get("result") or "").strip()
    if not title or not action or not result:
        raise ValueError("Title, action, and result are required")
    pieces = [action.rstrip(".")]
    if result:
        pieces.append(result.rstrip("."))
    bullet = "; ".join(pieces) + "."
    if len(bullet) > maximum_chars:
        bullet = bullet[:maximum_chars-1].rsplit(" ", 1)[0] + "…"
    return {"bullet": bullet, "source_title": title,
            "evidence_present": bool(entry.get("evidence") or entry.get("metric")),
            "warning": "Review for accuracy and context before using in a resume."}

def portfolio_audit(items: Iterable[Mapping]) -> dict:
    rows = [portfolio_readiness(item) for item in items]
    blockers = {}
    for row in rows:
        for blocker in row["blockers"]:
            blockers[blocker] = blockers.get(blocker, 0) + 1
    return {"item_count": len(rows), "ready_count": sum(row["ready_for_review"] for row in rows),
            "average_readiness_percent": round(sum(row["readiness_percent"] for row in rows)/len(rows), 1) if rows else 100,
            "blockers": dict(sorted(blockers.items())), "items": rows,
            "automatic_publication_performed": False}
