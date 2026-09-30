from collections import Counter
from datetime import timedelta
from django.db.models import Avg, Count, Q
from django.utils import timezone


FUNNEL_ORDER = ["saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn"]


def application_funnel(queryset):
    counts = queryset.values("status").annotate(total=Count("id"))
    by_status = {row["status"]: row["total"] for row in counts}
    total = queryset.count()
    return {
        "total": total,
        "stages": [
            {
                "status": status,
                "count": by_status.get(status, 0),
                "share": round((by_status.get(status, 0) / total) * 100, 2) if total else 0,
            }
            for status in FUNNEL_ORDER
        ],
    }


def response_metrics(queryset):
    total = queryset.count()
    active = queryset.exclude(status__in=["rejected", "withdrawn"]).count()
    offers = queryset.filter(status="offer").count()
    interviews = queryset.filter(status="interview").count()
    return {
        "total": total,
        "active": active,
        "interviews": interviews,
        "offers": offers,
        "interview_rate": round(interviews / total * 100, 2) if total else 0,
        "offer_rate": round(offers / total * 100, 2) if total else 0,
    }


def salary_metrics(queryset):
    values = queryset.filter(salary_min__isnull=False).aggregate(
        average=Avg("salary_min"),
        highest=Avg("salary_max"),
    )
    return values


def stale_applications(queryset, days=14):
    cutoff = timezone.now() - timedelta(days=days)
    return queryset.filter(
        updated_at__lt=cutoff,
    ).exclude(status__in=["rejected", "withdrawn", "offer"])


def company_breakdown(queryset):
    rows = queryset.values("company").annotate(
        total=Count("id"),
        interviews=Count("id", filter=Q(status="interview")),
        offers=Count("id", filter=Q(status="offer")),
    ).order_by("-total", "company")
    return list(rows)
