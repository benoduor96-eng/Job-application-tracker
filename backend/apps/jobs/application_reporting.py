"""Reporting and export helpers for the application pipeline."""
from collections import Counter, defaultdict
from datetime import timedelta
from decimal import Decimal

from django.db.models import Avg, Count, Max, Min
from django.utils import timezone

from apps.jobs.models import JobApplication


def status_report(user) -> dict:
    qs = JobApplication.objects.filter(user=user)
    counts = Counter(qs.values_list("status", flat=True))
    return {
        "total": qs.count(),
        "counts": dict(counts),
        "active": sum(value for key, value in counts.items()
                      if key not in {"rejected", "withdrawn", "offer"}),
        "terminal": sum(value for key, value in counts.items()
                        if key in {"rejected", "withdrawn", "offer"}),
    }


def company_report(user) -> list[dict]:
    rows = (
        JobApplication.objects.filter(user=user)
        .values("company")
        .annotate(
            applications=Count("id"),
            latest_update=Max("updated_at"),
            average_min=Avg("salary_min"),
            average_max=Avg("salary_max"),
        )
        .order_by("-applications", "company")
    )
    return list(rows)


def salary_report(user) -> dict:
    values = JobApplication.objects.filter(user=user).aggregate(
        minimum=Min("salary_min"),
        maximum=Max("salary_max"),
        average_min=Avg("salary_min"),
        average_max=Avg("salary_max"),
    )
    return {
        key: float(value) if isinstance(value, Decimal) else value
        for key, value in values.items()
    }


def stale_report(user, days: int = 14) -> list[dict]:
    cutoff = timezone.now() - timedelta(days=max(1, days))
    qs = JobApplication.objects.filter(
        user=user,
        updated_at__lt=cutoff,
    ).exclude(status__in=["rejected", "withdrawn", "offer"])
    return list(qs.values(
        "id", "company", "role", "status", "updated_at", "next_action", "next_action_date"
    ).order_by("updated_at"))


def funnel_report(user) -> dict:
    counts = Counter(
        JobApplication.objects.filter(user=user).values_list("status", flat=True)
    )
    applied = counts.get("applied", 0) + counts.get("screening", 0) + counts.get("interview", 0) + counts.get("offer", 0)
    interview = counts.get("interview", 0) + counts.get("offer", 0)
    offer = counts.get("offer", 0)
    return {
        "saved": counts.get("saved", 0),
        "applied": applied,
        "interview": interview,
        "offer": offer,
        "interview_rate": _rate(interview, applied),
        "offer_rate": _rate(offer, applied),
    }


def _rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator * 100, 2)


def dashboard_report(user) -> dict:
    return {
        "status": status_report(user),
        "companies": company_report(user),
        "salary": salary_report(user),
        "funnel": funnel_report(user),
        "stale": stale_report(user),
    }
