"""Explainable prioritization for a personal job-search queue."""
from datetime import date, datetime
from typing import Any, Mapping, Sequence

WEIGHTS = {
    "fit": 0.30, "deadline": 0.20, "stage": 0.15,
    "freshness": 0.10, "salary": 0.10, "preparation": 0.10,
    "relationship": 0.05,
}
STAGE_SCORES = {
    "saved": 45, "applied": 58, "screening": 68, "interview": 88,
    "offer": 96, "rejected": 0, "withdrawn": 0,
}


def _clamp(value: Any, low=0.0, high=100.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = low
    return max(low, min(high, number))


def _parse_day(value: Any) -> date | None:
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


def deadline_score(due_date: Any, *, today: date | None = None) -> float:
    due = _parse_day(due_date)
    if due is None:
        return 35.0
    delta = (due - (today or date.today())).days
    if delta < 0:
        return 100.0
    if delta == 0:
        return 98.0
    if delta <= 2:
        return 90.0
    if delta <= 7:
        return 78.0
    if delta <= 14:
        return 62.0
    if delta <= 30:
        return 48.0
    return 30.0


def freshness_score(updated_at: Any, *, today: date | None = None) -> float:
    updated = _parse_day(updated_at)
    if updated is None:
        return 25.0
    age = ((today or date.today()) - updated).days
    if age <= 1:
        return 100.0
    if age <= 3:
        return 85.0
    if age <= 7:
        return 65.0
    if age <= 14:
        return 45.0
    if age <= 30:
        return 30.0
    return 15.0


def salary_alignment(application: Mapping, profile: Mapping | None) -> float:
    if not profile:
        return 50.0
    target = profile.get("target_salary") or profile.get("minimum_salary")
    offered = application.get("salary_max") or application.get("salary_min")
    if target in (None, "") or offered in (None, ""):
        return 50.0
    try:
        target_value, offered_value = float(target), float(offered)
    except (TypeError, ValueError):
        return 50.0
    if target_value <= 0:
        return 50.0
    ratio = offered_value / target_value
    return _clamp(50 + (ratio - 1) * 50)


def relationship_score(application: Mapping, contact_count: int = 0) -> float:
    if contact_count > 0:
        return _clamp(65 + min(contact_count, 5) * 7)
    if application.get("referral") or application.get("has_referral"):
        return 90.0
    return 35.0


def explain_priority(
    application: Mapping,
    *,
    fit_score: Any = None,
    profile: Mapping | None = None,
    contact_count: int = 0,
    preparation_score: Any = None,
    today: date | None = None,
) -> dict:
    """Return weighted score plus human-readable factors; never predict hiring outcomes."""
    status = application.get("status", "saved")
    if status in {"rejected", "withdrawn"}:
        return {
            "application_id": application.get("id"),
            "score": 0.0,
            "priority": "inactive",
            "factors": [],
            "explanation": "This application is in a terminal state and is excluded from active prioritization.",
            "model": "transparent-weighted-rules-v1",
        }
    factors = {
        "fit": _clamp(fit_score, 50, 100) if fit_score is not None else 50.0,
        "deadline": deadline_score(application.get("next_action_date"), today=today),
        "stage": STAGE_SCORES.get(status, 40),
        "freshness": freshness_score(application.get("updated_at"), today=today),
        "salary": salary_alignment(application, profile),
        "preparation": _clamp(preparation_score) if preparation_score is not None else 50.0,
        "relationship": relationship_score(application, contact_count),
    }
    score = round(sum(factors[name] * weight for name, weight in WEIGHTS.items()), 2)
    explanations = []
    best = max(factors, key=factors.get)
    worst = min(factors, key=factors.get)
    labels = {
        "fit": "role fit", "deadline": "follow-up timing", "stage": "pipeline stage",
        "freshness": "recent activity", "salary": "salary alignment",
        "preparation": "interview preparation", "relationship": "relationship context",
    }
    explanations.append(f"Strongest signal: {labels[best]} ({factors[best]:.0f}/100).")
    explanations.append(f"Improvement opportunity: {labels[worst]} ({factors[worst]:.0f}/100).")
    if factors["deadline"] >= 90:
        explanations.append("Review the due or overdue follow-up before starting lower-priority work.")
    if factors["preparation"] < 50 and status == "interview":
        explanations.append("Prepare examples and questions before the scheduled interview.")
    priority = "high" if score >= 75 else "medium" if score >= 50 else "low"
    return {
        "application_id": application.get("id"),
        "score": score,
        "priority": priority,
        "factors": [{"name": key, "score": value, "weight": WEIGHTS[key]}
                    for key, value in factors.items()],
        "explanation": " ".join(explanations),
        "model": "transparent-weighted-rules-v1",
        "disclaimer": "This score organizes your work; it does not estimate hiring probability.",
    }


def rank_applications(
    applications: Sequence[Mapping],
    *,
    profile: Mapping | None = None,
    fit_scores: Mapping[Any, Any] | None = None,
    contact_counts: Mapping[Any, int] | None = None,
    preparation_scores: Mapping[Any, Any] | None = None,
    today: date | None = None,
    limit: int = 50,
) -> list[dict]:
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 200:
        raise ValueError("limit must be between 1 and 200.")
    fit_scores, contact_counts, preparation_scores = fit_scores or {}, contact_counts or {}, preparation_scores or {}
    ranked = []
    for application in applications:
        app_id = application.get("id")
        ranked.append(explain_priority(
            application, fit_score=fit_scores.get(app_id), profile=profile,
            contact_count=contact_counts.get(app_id, 0),
            preparation_score=preparation_scores.get(app_id), today=today,
        ))
    return sorted(ranked, key=lambda row: (-row["score"], str(row.get("application_id"))))[:limit]
