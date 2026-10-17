"""Weekly reflection helpers for turning activity into concrete, reviewable next steps."""
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping

REFLECTION_AREAS = {"progress", "learning", "wellbeing", "barriers", "relationships", "next_week"}
def _date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None

def validate_reflection(entry: Mapping) -> dict:
    week = _date(entry.get("week_start"))
    if week is None:
        raise ValueError("week_start must be a valid date")
    week = week - timedelta(days=week.weekday())
    responses = {}
    raw = entry.get("responses") or {}
    unknown = set(raw) - REFLECTION_AREAS
    if unknown:
        raise ValueError("Unknown reflection areas: " + ", ".join(sorted(unknown)))
    for area in REFLECTION_AREAS:
        responses[area] = str(raw.get(area) or "").strip()[:2000]
    energy = entry.get("energy_rating")
    if energy not in (None, ""):
        try:
            energy = int(energy)
        except (TypeError, ValueError):
            raise ValueError("energy_rating must be an integer from 1 to 5")
        if not 1 <= energy <= 5:
            raise ValueError("energy_rating must be between 1 and 5")
    return {"id": entry.get("id"), "week_start": week, "responses": responses,
            "energy_rating": energy, "completed": bool(entry.get("completed", False)),
            "private": bool(entry.get("private", True))}

def reflection_quality(entry: Mapping) -> dict:
    row = validate_reflection(entry)
    filled = [area for area, text in row["responses"].items() if text]
    return {"id": row["id"], "week_start": row["week_start"].isoformat(),
            "answered_areas": len(filled), "total_areas": len(REFLECTION_AREAS),
            "coverage_percent": round(100*len(filled)/len(REFLECTION_AREAS), 1),
            "missing_areas": sorted(REFLECTION_AREAS-set(filled)),
            "completed": row["completed"], "private": row["private"],
            "note": "Reflection quality is not measured by length; short, honest notes can be useful."}

def propose_next_steps(entry: Mapping, limit: int = 5) -> list[dict]:
    if not 1 <= limit <= 12:
        raise ValueError("limit must be between 1 and 12")
    row = validate_reflection(entry)
    prompts = {
        "barriers": ("Resolve one blocker", "Choose a small action that makes the main barrier easier to address."),
        "learning": ("Apply one lesson", "Use a recent lesson in a practical task or interview example."),
        "relationships": ("Maintain one relationship", "Send a relevant, respectful note only when contact is welcome."),
        "progress": ("Preserve what worked", "Repeat one useful habit without increasing workload unnecessarily."),
        "wellbeing": ("Protect sustainable effort", "Adjust the plan to leave room for rest and other responsibilities."),
        "next_week": ("Set a realistic priority", "Choose one outcome that matters most for the coming week."),
    }
    candidates = []
    for area, text in row["responses"].items():
        if text and area in prompts:
            title, guidance = prompts[area]
            candidates.append({"source_area": area, "title": title, "guidance": guidance,
                               "based_on_user_note": True})
    if not candidates:
        candidates = [{"source_area": "next_week", "title": "Choose one realistic priority",
                       "guidance": "Start with a small, concrete action and a realistic time estimate.",
                       "based_on_user_note": False}]
    return candidates[:limit]

def reflection_trends(entries: Iterable[Mapping]) -> dict:
    rows = sorted((validate_reflection(entry) for entry in entries), key=lambda row: row["week_start"])
    ratings = [row["energy_rating"] for row in rows if row["energy_rating"] is not None]
    answered = [len([text for text in row["responses"].values() if text]) for row in rows]
    return {"reflection_count": len(rows), "completed_count": sum(row["completed"] for row in rows),
            "average_energy_rating": round(sum(ratings)/len(ratings), 2) if ratings else None,
            "average_areas_answered": round(sum(answered)/len(answered), 2) if answered else 0,
            "weeks": [{"week_start": row["week_start"].isoformat(), "energy_rating": row["energy_rating"],
                       "areas_answered": sum(bool(text) for text in row["responses"].values())} for row in rows],
            "note": "Energy ratings are subjective self-reflections and are not health assessments."}
