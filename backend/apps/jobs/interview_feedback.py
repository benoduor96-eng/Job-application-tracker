"""Structured interview debriefs that turn reflections into reviewable next steps."""
from datetime import date, datetime
from typing import Iterable, Mapping

DIMENSIONS = {"role_understanding", "communication", "technical_reasoning", "examples", "questions", "logistics"}
def _date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None

def validate_debrief(debrief: Mapping) -> dict:
    company = str(debrief.get("company") or "").strip()
    role = str(debrief.get("role") or "").strip()
    if not company or not role:
        raise ValueError("Company and role are required")
    scores = {}
    for dimension in DIMENSIONS:
        value = debrief.get(dimension)
        if value in (None, ""):
            scores[dimension] = None
            continue
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValueError(f"{dimension} must be an integer from 1 to 5")
        if not 1 <= value <= 5:
            raise ValueError(f"{dimension} must be between 1 and 5")
        scores[dimension] = value
    outcome = str(debrief.get("outcome") or "pending").lower()
    if outcome not in {"pending", "next_round", "offer", "rejected", "withdrawn"}:
        raise ValueError("Unsupported interview outcome")
    return {"id": debrief.get("id"), "company": company[:200], "role": role[:200],
            "interview_date": _date(debrief.get("interview_date")),
            "outcome": outcome, "scores": scores,
            "went_well": str(debrief.get("went_well") or "")[:2000],
            "improve_next_time": str(debrief.get("improve_next_time") or "")[:2000],
            "questions_to_follow_up": [str(item).strip()[:300] for item in debrief.get("questions_to_follow_up", []) if str(item).strip()][:20]}

def debrief_summary(debriefs: Iterable[Mapping]) -> dict:
    rows = [validate_debrief(item) for item in debriefs]
    averages, samples = {}, {}
    for dimension in sorted(DIMENSIONS):
        values = [row["scores"][dimension] for row in rows if row["scores"][dimension] is not None]
        averages[dimension] = round(sum(values)/len(values), 2) if values else None
        samples[dimension] = len(values)
    return {"interviews": len(rows), "score_averages": averages, "score_sample_sizes": samples,
            "outcomes": {key: sum(row["outcome"] == key for row in rows)
                         for key in ("pending", "next_round", "offer", "rejected", "withdrawn")},
            "note": "Self-ratings are subjective reflections, not an objective assessment of ability."}

def improvement_plan(debriefs: Iterable[Mapping], threshold: float = 3.0) -> list[dict]:
    if not 1 <= threshold <= 5:
        raise ValueError("threshold must be between 1 and 5")
    rows = [validate_debrief(item) for item in debriefs]
    result = []
    for dimension in sorted(DIMENSIONS):
        values = [row["scores"][dimension] for row in rows if row["scores"][dimension] is not None]
        if not values:
            result.append({"dimension": dimension, "status": "no_data",
                           "action": "Choose one practice exercise and collect a reflection."})
        elif sum(values)/len(values) < threshold:
            result.append({"dimension": dimension, "status": "practice_opportunity",
                           "average": round(sum(values)/len(values), 2),
                           "action": "Choose a concrete practice exercise and review the next interview."})
    return result

def debrief_action_queue(debriefs: Iterable[Mapping]) -> list[dict]:
    output = []
    for row in (validate_debrief(item) for item in debriefs):
        for index, question in enumerate(row["questions_to_follow_up"]):
            output.append({"interview_id": row["id"], "company": row["company"],
                           "role": row["role"], "question": question, "sequence": index+1,
                           "completed": False})
        if row["improve_next_time"]:
            output.append({"interview_id": row["id"], "company": row["company"], "role": row["role"],
                           "question": "Practice: " + row["improve_next_time"][:250],
                           "sequence": len(row["questions_to_follow_up"])+1, "completed": False})
    return output

def compare_debriefs(first: Mapping, second: Mapping) -> dict:
    left, right = validate_debrief(first), validate_debrief(second)
    changes = {}
    for dimension in sorted(DIMENSIONS):
        a, b = left["scores"][dimension], right["scores"][dimension]
        changes[dimension] = {"before": a, "after": b, "delta": b-a if a is not None and b is not None else None}
    return {"before_id": left["id"], "after_id": right["id"], "score_changes": changes,
            "warning": "Differences are self-reported and may reflect different interview difficulty or conditions."}
