"""Explainable job-application prioritization; scores are configurable decision aids."""
from datetime import date, datetime
from typing import Iterable, Mapping

DEFAULT_WEIGHTS = {"role_fit": 30, "interest": 20, "readiness": 20, "deadline": 10, "growth": 10, "effort": 10}
RATINGS = tuple(DEFAULT_WEIGHTS)

def _date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None

def validate_ratings(record: Mapping) -> dict:
    output = {"id": record.get("id"), "company": str(record.get("company") or "").strip()[:200],
              "role": str(record.get("role") or "").strip()[:200]}
    for key in RATINGS:
        value = record.get(key)
        if value in (None, ""):
            output[key] = None
            continue
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"{key} must be an integer from 1 to 5")
        if not 1 <= value <= 5:
            raise ValueError(f"{key} must be an integer from 1 to 5")
        output[key] = value
    output["deadline"] = _date(record.get("deadline"))
    output["estimated_minutes"] = max(0, min(100000, int(record.get("estimated_minutes") or 0)))
    output["status"] = str(record.get("status") or "saved").lower()
    return output

def score_application(record: Mapping, weights: Mapping | None = None, today=None) -> dict:
    row = validate_ratings(record)
    weights = dict(DEFAULT_WEIGHTS if weights is None else weights)
    if set(weights) - set(RATINGS):
        raise ValueError("Unknown scoring weight")
    if any(not isinstance(weight, (int, float)) or weight < 0 for weight in weights.values()):
        raise ValueError("Weights must be non-negative numbers")
    if sum(weights.values()) <= 0:
        raise ValueError("At least one weight must be positive")
    numerator = denominator = 0.0
    missing = []
    for key in RATINGS:
        weight = float(weights.get(key, 0))
        rating = row.get(key)
        if rating is None:
            if weight:
                missing.append(key)
        else:
            numerator += (rating / 5) * weight
            denominator += weight
    deadline = row["deadline"]
    current = _date(today) or date.today()
    days = (deadline - current).days if deadline else None
    urgency = 0
    if days is not None:
        urgency = 5 if days < 0 else 4 if days <= 1 else 3 if days <= 3 else 2 if days <= 7 else 1
    return {"id": row["id"], "company": row["company"], "role": row["role"],
            "priority_score": round(100 * numerator / denominator, 2) if denominator else None,
            "rated_weight_percent": round(100 * denominator / sum(weights.values()), 2),
            "missing_ratings": missing, "deadline_days": days, "deadline_urgency": urgency,
            "estimated_minutes": row["estimated_minutes"],
            "status": row["status"],
            "interpretation": "Use this score to support reflection, not as an objective prediction of hiring success."}

def rank_applications(records: Iterable[Mapping], weights: Mapping | None = None, today=None) -> list[dict]:
    rows = [score_application(record, weights, today) for record in records]
    rows.sort(key=lambda row: (row["priority_score"] is not None, row["priority_score"] or -1,
                               row["deadline_urgency"], -row["estimated_minutes"]), reverse=True)
    for rank, row in enumerate(rows, 1):
        row["rank"] = rank
    return rows

def compare_priority_scenarios(records: Iterable[Mapping], scenarios: Mapping, today=None) -> dict:
    rows = list(records)
    if not scenarios:
        raise ValueError("At least one named scenario is required")
    output = {}
    for name, weights in scenarios.items():
        if not str(name).strip():
            raise ValueError("Scenario names cannot be blank")
        output[str(name)[:80]] = rank_applications(rows, weights, today)
    positions = {}
    for name, ranked in output.items():
        for row in ranked:
            positions.setdefault(str(row["id"]), {})[name] = row["rank"]
    return {"scenarios": output, "rank_positions_by_application": positions,
            "warning": "Scenario ranking changes with weights and missing ratings; it is not a recommendation to apply or decline."}

def decision_review_template(application: Mapping) -> dict:
    row = validate_ratings(application)
    return {"application_id": row["id"], "company": row["company"], "role": row["role"],
            "questions": [
                {"id": "fit", "prompt": "Which role requirements can you evidence with real examples?"},
                {"id": "motivation", "prompt": "What genuinely interests you about this work?"},
                {"id": "constraints", "prompt": "Are location, schedule, compensation, and authorization requirements clear?"},
                {"id": "effort", "prompt": "What is the smallest useful next step, and how much time will it take?"},
                {"id": "uncertainty", "prompt": "What important information is missing, and how can you verify it?"},
            ], "reviewed": False,
            "note": "This template does not infer eligibility, work authorization, or employer legitimacy."}

def effort_budget_report(applications: Iterable[Mapping], weekly_minutes: int = 600) -> dict:
    if not isinstance(weekly_minutes, int) or not 0 <= weekly_minutes <= 10080:
        raise ValueError("weekly_minutes must be an integer from 0 to 10080")
    rows = [validate_ratings(row) for row in applications]
    active = [row for row in rows if row["status"] not in {"rejected", "withdrawn"}]
    total = sum(row["estimated_minutes"] for row in active)
    return {"active_applications": len(active), "estimated_minutes": total,
            "weekly_budget_minutes": weekly_minutes,
            "budget_hours": round(weekly_minutes / 60, 2),
            "weeks_at_budget": round(total / weekly_minutes, 2) if weekly_minutes else None,
            "within_one_week": total <= weekly_minutes,
            "recommendation": "Prioritize quality and sustainable effort; reduce scope if the plan is unrealistic."}

def decision_log_entry(application_id, decision, rationale, reviewed_on=None) -> dict:
    decision = str(decision or "").strip().lower()
    if decision not in {"continue", "pause", "withdraw", "apply", "research"}:
        raise ValueError("Unsupported decision")
    rationale = str(rationale or "").strip()
    if len(rationale) < 8:
        raise ValueError("Provide a meaningful rationale of at least 8 characters")
    day = _date(reviewed_on) or date.today()
    return {"application_id": application_id, "decision": decision, "rationale": rationale[:2000],
            "reviewed_on": day.isoformat(), "saved": False,
            "note": "The caller must authorize and persist this entry separately."}

def rating_scale() -> dict:
    return {"scale": {1: "Weak fit or major unknowns", 2: "Some fit but meaningful gaps",
                      3: "Reasonable fit with evidence", 4: "Strong fit with supporting evidence",
                      5: "Excellent fit with clear evidence"},
            "criteria": {key: f"Rate {key.replace('_', ' ')} from 1 to 5 based on your own evidence."
                         for key in RATINGS},
            "caution": "Ratings are subjective and should be revised when new information arrives."}
