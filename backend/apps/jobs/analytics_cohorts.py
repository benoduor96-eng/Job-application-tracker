"""Pure analytics for application outcomes, response lag, and weekly cohorts."""
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from statistics import median
from typing import Iterable, Mapping

PIPELINE_ORDER = ("saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn")
ACTIVE = frozenset({"saved", "applied", "screening", "interview", "offer"})

def _as_date(value):
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

def _percent(numerator, denominator):
    return round(100 * numerator / denominator, 2) if denominator else 0.0

def _number(value):
    try:
        return float(value) if value not in (None, "") else None
    except (ValueError, TypeError):
        return None

def normalize_application(row: Mapping) -> dict:
    return {"id": row.get("id"), "company": str(row.get("company") or "").strip(),
            "role": str(row.get("role") or "").strip(), "status": str(row.get("status") or "unknown"),
            "created_date": _as_date(row.get("created_at")), "applied_date": _as_date(row.get("applied_date")),
            "updated_date": _as_date(row.get("updated_at")), "salary_min": _number(row.get("salary_min")),
            "salary_max": _number(row.get("salary_max")), "source": str(row.get("source") or "unknown")}

def funnel_summary(rows: Iterable[Mapping]) -> dict:
    applications = [normalize_application(row) for row in rows]
    counts = Counter(item["status"] for item in applications)
    applied = sum(counts.get(s, 0) for s in ("applied", "screening", "interview", "offer", "rejected"))
    screening = sum(counts.get(s, 0) for s in ("screening", "interview", "offer"))
    interviews = sum(counts.get(s, 0) for s in ("interview", "offer"))
    return {"total": len(applications),
            "by_status": {status: counts.get(status, 0) for status in PIPELINE_ORDER},
            "unknown_status_count": sum(count for status, count in counts.items() if status not in PIPELINE_ORDER),
            "screening_conversion_percent": _percent(screening, applied),
            "interview_conversion_percent": _percent(interviews, applied),
            "offer_conversion_percent": _percent(counts.get("offer", 0), applied),
            "active_count": sum(item["status"] in ACTIVE for item in applications),
            "interpretation": "Stage counts are snapshots, not unique stage-entry events; rates are directional."}

def weekly_application_counts(rows: Iterable[Mapping], weeks: int = 12,
                              today: date | None = None) -> list[dict]:
    if not 1 <= weeks <= 104:
        raise ValueError("weeks must be between 1 and 104")
    today = today or date.today()
    start = today - timedelta(days=today.weekday(), weeks=weeks - 1)
    buckets = {start + timedelta(weeks=index): 0 for index in range(weeks)}
    for row in rows:
        item = normalize_application(row)
        applied = item["applied_date"] or item["created_date"]
        if applied is not None:
            monday = applied - timedelta(days=applied.weekday())
            if monday in buckets:
                buckets[monday] += 1
    return [{"week_start": monday.isoformat(), "count": buckets[monday]} for monday in buckets]

def response_lag_summary(rows: Iterable[Mapping]) -> dict:
    lags, missing = [], 0
    for row in rows:
        applied = _as_date(row.get("applied_date"))
        response = _as_date(row.get("first_response_date") or row.get("updated_at"))
        if applied is None or response is None:
            missing += 1
            continue
        days = (response - applied).days
        if days >= 0:
            lags.append(days)
        else:
            missing += 1
    if not lags:
        return {"sample_size": 0, "missing_or_invalid": missing, "mean_days": None,
                "median_days": None, "minimum_days": None, "maximum_days": None}
    return {"sample_size": len(lags), "missing_or_invalid": missing,
            "mean_days": round(sum(lags) / len(lags), 2), "median_days": median(lags),
            "minimum_days": min(lags), "maximum_days": max(lags)}

def source_performance(rows: Iterable[Mapping], minimum_sample: int = 3) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[normalize_application(row)["source"]].append(normalize_application(row))
    result = []
    for source, applications in grouped.items():
        count = len(applications)
        interviews = sum(item["status"] == "interview" for item in applications)
        offers = sum(item["status"] == "offer" for item in applications)
        result.append({"source": source, "applications": count, "interviews": interviews, "offers": offers,
                       "interview_rate_percent": _percent(interviews, count),
                       "offer_rate_percent": _percent(offers, count), "sample_warning": count < minimum_sample})
    return sorted(result, key=lambda row: (-row["offers"], -row["interviews"], row["source"]))

def salary_band_summary(rows: Iterable[Mapping]) -> dict:
    ranges = []
    for row in rows:
        item = normalize_application(row)
        low, high = item["salary_min"], item["salary_max"]
        if low is None and high is None:
            continue
        if low is not None and high is not None and low > high:
            continue
        ranges.append({"min": low, "max": high})
    lows = [item["min"] for item in ranges if item["min"] is not None]
    highs = [item["max"] for item in ranges if item["max"] is not None]
    return {"range_count": len(ranges), "min_values_count": len(lows), "max_values_count": len(highs),
            "lowest_min": min(lows) if lows else None, "median_min": median(lows) if lows else None,
            "highest_max": max(highs) if highs else None, "median_max": median(highs) if highs else None,
            "currency_warning": "Values are comparable only when currency and pay period match."}

def company_rollup(rows: Iterable[Mapping], limit: int = 20) -> list[dict]:
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    grouped = defaultdict(list)
    for row in rows:
        item = normalize_application(row)
        grouped[item["company"] or "Unknown company"].append(item)
    output = []
    for company, applications in grouped.items():
        statuses = Counter(item["status"] for item in applications)
        output.append({"company": company, "total": len(applications),
                       "active": sum(count for status, count in statuses.items() if status in ACTIVE),
                       "interviews": statuses.get("interview", 0), "offers": statuses.get("offer", 0),
                       "rejected": statuses.get("rejected", 0)})
    output.sort(key=lambda row: (-row["offers"], -row["interviews"], -row["total"], row["company"].casefold()))
    return output[:limit]

def outcome_summary(rows: Iterable[Mapping]) -> dict:
    applications = [normalize_application(row) for row in rows]
    terminal = [item for item in applications if item["status"] in {"offer", "rejected", "withdrawn"}]
    offers = sum(item["status"] == "offer" for item in applications)
    rejected = sum(item["status"] == "rejected" for item in terminal)
    return {"total": len(applications), "resolved": len(terminal),
            "offer_rate_of_all_percent": _percent(offers, len(applications)),
            "offer_rate_of_resolved_percent": _percent(offers, len(terminal)),
            "rejection_rate_of_resolved_percent": _percent(rejected, len(terminal)),
            "warning": "Rates are descriptive and should not be interpreted as causal or predictive."}

def weekly_cohort_retention(rows: Iterable[Mapping], periods: int = 8,
                            today: date | None = None) -> list[dict]:
    if not 1 <= periods <= 52:
        raise ValueError("periods must be between 1 and 52")
    today = today or date.today()
    current_monday = today - timedelta(days=today.weekday())
    cohorts = defaultdict(list)
    for row in rows:
        item = normalize_application(row)
        started = item["applied_date"] or item["created_date"]
        if started is None:
            continue
        monday = started - timedelta(days=started.weekday())
        age = (current_monday - monday).days // 7
        if 0 <= age < periods:
            cohorts[monday].append(item)
    output = []
    for monday in sorted(cohorts):
        items = cohorts[monday]
        active = sum(item["status"] in ACTIVE for item in items)
        output.append({"cohort_week": monday.isoformat(), "applications": len(items),
                       "currently_active": active, "active_percent": _percent(active, len(items)),
                       "age_weeks": (current_monday - monday).days // 7})
    return output

def analytics_quality_report(rows: Iterable[Mapping]) -> dict:
    rows, issues, ids = list(rows), Counter(), set()
    for row in rows:
        identifier = row.get("id")
        if identifier is None:
            issues["missing_id"] += 1
        elif identifier in ids:
            issues["duplicate_id"] += 1
        else:
            ids.add(identifier)
        if not str(row.get("company") or "").strip():
            issues["missing_company"] += 1
        if not str(row.get("role") or "").strip():
            issues["missing_role"] += 1
        if row.get("status") not in PIPELINE_ORDER:
            issues["unknown_status"] += 1
        low, high = _number(row.get("salary_min")), _number(row.get("salary_max"))
        if low is not None and high is not None and low > high:
            issues["invalid_salary_range"] += 1
        if row.get("applied_date") and _as_date(row.get("applied_date")) is None:
            issues["invalid_applied_date"] += 1
    return {"records": len(rows), "issue_count": sum(issues.values()), "issues": dict(sorted(issues.items())),
            "quality_percent": round(100 * (1 - sum(issues.values()) / max(1, len(rows) * 5)), 2)}
