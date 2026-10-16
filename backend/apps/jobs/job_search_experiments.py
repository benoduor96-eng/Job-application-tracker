"""Track job-search experiments without presenting small samples as causal proof."""
from collections import defaultdict
from datetime import date, datetime
from typing import Iterable, Mapping

EXPERIMENT_STATUSES = {"planned", "running", "completed", "paused"}
def _date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None

def validate_experiment(experiment: Mapping) -> dict:
    title = str(experiment.get("title") or "").strip()
    hypothesis = str(experiment.get("hypothesis") or "").strip()
    if not title or not hypothesis:
        raise ValueError("Experiment title and hypothesis are required")
    status = str(experiment.get("status") or "planned").lower()
    if status not in EXPERIMENT_STATUSES:
        raise ValueError("Unsupported experiment status")
    return {"id": experiment.get("id"), "title": title[:180], "hypothesis": hypothesis[:1000],
            "status": status, "start_date": _date(experiment.get("start_date")),
            "end_date": _date(experiment.get("end_date")),
            "success_metric": str(experiment.get("success_metric") or "interviews per application")[:180],
            "notes": str(experiment.get("notes") or "")[:2000]}

def validate_observation(observation: Mapping) -> dict:
    try:
        applications = int(observation.get("applications", 0))
        interviews = int(observation.get("interviews", 0))
        offers = int(observation.get("offers", 0))
    except (ValueError, TypeError):
        raise ValueError("Counts must be integers")
    if min(applications, interviews, offers) < 0 or interviews > applications or offers > interviews:
        raise ValueError("Counts must be non-negative and offers <= interviews <= applications")
    return {"experiment_id": observation.get("experiment_id"), "segment": str(observation.get("segment") or "all")[:100],
            "applications": applications, "interviews": interviews, "offers": offers,
            "observed_on": (_date(observation.get("observed_on")) or date.today()).isoformat(),
            "notes": str(observation.get("notes") or "")[:1000]}

def summarize_observations(observations: Iterable[Mapping]) -> dict:
    rows = [validate_observation(row) for row in observations]
    applications = sum(row["applications"] for row in rows)
    interviews = sum(row["interviews"] for row in rows)
    offers = sum(row["offers"] for row in rows)
    return {"segments": len(rows), "applications": applications, "interviews": interviews, "offers": offers,
            "interview_rate_percent": round(100*interviews/applications, 2) if applications else None,
            "offer_rate_percent": round(100*offers/applications, 2) if applications else None,
            "interview_to_offer_percent": round(100*offers/interviews, 2) if interviews else None,
            "sample_warning": applications < 20,
            "interpretation": "Descriptive rates only; differences may reflect role mix, timing, selection bias, or chance."}

def compare_experiments(first: Iterable[Mapping], second: Iterable[Mapping]) -> dict:
    left, right = summarize_observations(first), summarize_observations(second)
    delta = {}
    for key in ("interview_rate_percent", "offer_rate_percent", "interview_to_offer_percent"):
        a, b = left[key], right[key]
        delta[key] = round(b-a, 2) if a is not None and b is not None else None
    return {"first": left, "second": right, "percentage_point_delta": delta,
            "causal_claim_supported": False,
            "warning": "Do not infer causation from this comparison; cohorts may not be comparable."}

def experiment_report(experiment: Mapping, observations: Iterable[Mapping]) -> dict:
    plan = validate_experiment(experiment)
    rows = [validate_observation(row) for row in observations]
    matching = [row for row in rows if row["experiment_id"] == plan["id"]]
    summary = summarize_observations(matching)
    return {"experiment": {**plan, "start_date": plan["start_date"].isoformat() if plan["start_date"] else None,
                           "end_date": plan["end_date"].isoformat() if plan["end_date"] else None},
            "summary": summary, "observation_count": len(matching),
            "next_steps": ["Check whether the groups were comparable.",
                           "Record the role types and time window.",
                           "Continue gathering observations before changing strategy based on small samples."],
            "report_is_predictive": False}

def group_observations(observations: Iterable[Mapping], group_field: str = "segment") -> list[dict]:
    if group_field not in {"segment", "experiment_id", "observed_on"}:
        raise ValueError("Unsupported group field")
    groups = defaultdict(list)
    for observation in observations:
        row = validate_observation(observation)
        groups[str(row[group_field])].append(row)
    output = []
    for key, rows in groups.items():
        summary = summarize_observations(rows)
        output.append({"group": key, **summary})
    return sorted(output, key=lambda row: row["group"])
