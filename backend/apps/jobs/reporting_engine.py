"""Composable reporting primitives for job-search progress and funnel health."""
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from statistics import median
from typing import Iterable, Mapping

STATUS_ORDER = ("saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn")
ACTIVE_STATUSES = frozenset({"saved", "applied", "screening", "interview", "offer"})


def _date(value):
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


def _money(value):
    if value is None or value == "":
        return None
    try:
        amount = Decimal(str(value))
        return amount if amount.is_finite() and amount >= 0 else None
    except (InvalidOperation, ValueError, TypeError):
        return None


def safe_percent(numerator: int | float, denominator: int | float) -> float:
    return round(float(numerator) * 100 / float(denominator), 2) if denominator else 0.0


def status_distribution(applications: Iterable[Mapping]) -> dict:
    counts = Counter({status: 0 for status in STATUS_ORDER})
    for application in applications:
        status = application.get("status")
        if status in counts:
            counts[status] += 1
    total = sum(counts.values())
    return {
        "total": total,
        "counts": dict(counts),
        "percentages": {key: safe_percent(value, total) for key, value in counts.items()},
    }


def funnel_metrics(applications: Iterable[Mapping]) -> dict:
    items = list(applications)
    counts = Counter(item.get("status") for item in items)
    applied = sum(1 for item in items if item.get("applied_date") or item.get("status") != "saved")
    interviews = counts["interview"] + sum(
        1 for item in items if item.get("status") == "offer"
    )
    offers = counts["offer"]
    rejected = counts["rejected"]
    return {
        "applications": len(items),
        "applied_or_later": applied,
        "interview_stage_or_beyond": interviews,
        "offers": offers,
        "rejected": rejected,
        "application_to_interview_percent": safe_percent(interviews, applied),
        "application_to_offer_percent": safe_percent(offers, applied),
        "interview_to_offer_percent": safe_percent(offers, interviews),
        "active_pipeline": sum(1 for item in items if item.get("status") in ACTIVE_STATUSES),
    }


def weekly_activity(applications: Iterable[Mapping], *, today: date | None = None,
                    weeks: int = 12) -> list[dict]:
    if isinstance(weeks, bool) or not isinstance(weeks, int) or not 1 <= weeks <= 104:
        raise ValueError("weeks must be between 1 and 104.")
    today = today or date.today()
    current_monday = today - timedelta(days=today.weekday())
    buckets = []
    for offset in reversed(range(weeks)):
        start = current_monday - timedelta(days=7 * offset)
        buckets.append({"week_start": start.isoformat(), "applications_created": 0,
                        "applications_submitted": 0, "offers": 0, "interviews": 0})
    index = {item["week_start"]: item for item in buckets}
    for item in applications:
        created = _date(item.get("created_at"))
        applied = _date(item.get("applied_date"))
        status = item.get("status")
        if created:
            monday = (created - timedelta(days=created.weekday())).isoformat()
            if monday in index:
                index[monday]["applications_created"] += 1
        if applied:
            monday = (applied - timedelta(days=applied.weekday())).isoformat()
            if monday in index:
                index[monday]["applications_submitted"] += 1
        if status == "offer" and created:
            monday = (created - timedelta(days=created.weekday())).isoformat()
            if monday in index:
                index[monday]["offers"] += 1
        if status == "interview" and created:
            monday = (created - timedelta(days=created.weekday())).isoformat()
            if monday in index:
                index[monday]["interviews"] += 1
    return buckets


def company_breakdown(applications: Iterable[Mapping], *, limit: int = 20) -> list[dict]:
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100.")
    groups = defaultdict(list)
    for item in applications:
        company = str(item.get("company") or "").strip()
        if company:
            groups[company.casefold()].append(item)
    results = []
    for normalized, rows in groups.items():
        company_name = next((str(row.get("company")).strip() for row in rows if row.get("company")), normalized)
        counts = Counter(row.get("status") for row in rows)
        results.append({
            "company": company_name,
            "application_count": len(rows),
            "interview_count": counts["interview"],
            "offer_count": counts["offer"],
            "rejection_count": counts["rejected"],
            "active_count": sum(count for status, count in counts.items() if status in ACTIVE_STATUSES),
            "offer_rate_percent": safe_percent(counts["offer"], len(rows)),
        })
    return sorted(results, key=lambda row: (-row["application_count"], row["company"].casefold()))[:limit]


def salary_summary(applications: Iterable[Mapping]) -> dict:
    lows, highs, midpoints = [], [], []
    for item in applications:
        low, high = _money(item.get("salary_min")), _money(item.get("salary_max"))
        if low is not None:
            lows.append(low)
        if high is not None:
            highs.append(high)
        if low is not None and high is not None and low <= high:
            midpoints.append((low + high) / 2)
    def serial(value):
        return round(float(value), 2) if value is not None else None
    return {
        "records_with_minimum": len(lows),
        "records_with_maximum": len(highs),
        "records_with_valid_ranges": len(midpoints),
        "average_minimum": serial(sum(lows) / len(lows)) if lows else None,
        "average_maximum": serial(sum(highs) / len(highs)) if highs else None,
        "median_range_midpoint": serial(median(midpoints)) if midpoints else None,
        "lowest_minimum": serial(min(lows)) if lows else None,
        "highest_maximum": serial(max(highs)) if highs else None,
    }


def time_to_apply(applications: Iterable[Mapping]) -> dict:
    durations = []
    invalid = 0
    for item in applications:
        created, applied = _date(item.get("created_at")), _date(item.get("applied_date"))
        if created is None or applied is None:
            continue
        days = (applied - created).days
        if days < 0:
            invalid += 1
            continue
        durations.append(days)
    return {
        "sample_size": len(durations),
        "average_days": round(sum(durations) / len(durations), 2) if durations else None,
        "median_days": median(durations) if durations else None,
        "min_days": min(durations) if durations else None,
        "max_days": max(durations) if durations else None,
        "invalid_date_order_count": invalid,
    }


def build_report(applications: Iterable[Mapping], *, today: date | None = None,
                 weeks: int = 12) -> dict:
    items = list(applications)
    return {
        "generated_for_date": (today or date.today()).isoformat(),
        "status_distribution": status_distribution(items),
        "funnel": funnel_metrics(items),
        "weekly_activity": weekly_activity(items, today=today, weeks=weeks),
        "companies": company_breakdown(items),
        "salary": salary_summary(items),
        "time_to_apply": time_to_apply(items),
    }
