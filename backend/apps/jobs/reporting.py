from __future__ import annotations

from collections import defaultdict
from datetime import timedelta
from typing import Any

from django.db.models import Avg, Count, Max, Min, Q
from django.utils import timezone

from .models import JobApplication, Task


class ReportingService:
    """Application reporting and pipeline health for the current user."""

    def __init__(self, user):
        self.user = user

    def dashboard_summary(self) -> dict[str, Any]:
        apps = JobApplication.objects.filter(user=self.user)
        total = apps.count()
        active = apps.exclude(status__in=["rejected", "withdrawn"]).count()
        today = timezone.localdate()
        overdue = Task.objects.filter(user=self.user, is_completed=False, due_date__lt=today).count()
        upcoming = Task.objects.filter(user=self.user, is_completed=False, due_date__gte=today).count()
        offers = apps.filter(status="offer").count()
        return {
            "total_applications": total,
            "active_applications": active,
            "interviews": apps.filter(status="interview").count(),
            "offers": offers,
            "rejected": apps.filter(status="rejected").count(),
            "saved": apps.filter(status="saved").count(),
            "applied": apps.filter(status="applied").count(),
            "screening": apps.filter(status="screening").count(),
            "overdue_tasks": overdue,
            "upcoming_tasks": upcoming,
            "conversion_rate": round(offers / total * 100, 2) if total else 0.0,
            "by_status": list(apps.values("status").annotate(total=Count("id")).order_by("-total")),
        }

    def pipeline_health(self) -> dict[str, Any]:
        apps = JobApplication.objects.filter(user=self.user)
        total = apps.count()
        if not total:
            return {"total": 0, "screening_rate": 0.0, "interview_rate": 0.0, "offer_rate": 0.0, "response_rate": 0.0}
        screening = apps.filter(status__in=["screening", "interview", "offer"]).count()
        interviews = apps.filter(status__in=["interview", "offer"]).count()
        offers = apps.filter(status="offer").count()
        return {
            "total": total,
            "screening_rate": round(screening / total * 100, 2),
            "interview_rate": round(interviews / total * 100, 2),
            "offer_rate": round(offers / total * 100, 2),
            "response_rate": round(screening / total * 100, 2),
        }

    def salary_statistics(self) -> dict[str, Any]:
        apps = JobApplication.objects.filter(user=self.user, salary_min__isnull=False)
        if not apps.exists():
            return {"count": 0, "avg_min": None, "avg_max": None, "highest_min": None, "lowest_max": None}
        mins = apps.aggregate(avg=Avg("salary_min"), highest=Max("salary_min"))
        maxes = apps.aggregate(avg=Avg("salary_max"), lowest=Min("salary_max"))
        return {
            "count": apps.count(),
            "avg_min": round(float(mins["avg"])) if mins["avg"] is not None else None,
            "avg_max": round(float(maxes["avg"])) if maxes["avg"] is not None else None,
            "highest_min": round(float(mins["highest"])) if mins["highest"] is not None else None,
            "lowest_max": round(float(maxes["lowest"])) if maxes["lowest"] is not None else None,
        }

    def application_timeline(self, days_back: int = 90) -> list[dict[str, Any]]:
        cutoff = timezone.localdate() - timedelta(days=days_back)
        rows = JobApplication.objects.filter(user=self.user, created_at__date__gte=cutoff).order_by("created_at")
        return [{"application_id": a.id, "company": a.company, "role": a.role, "status": a.status,
                 "created_at": a.created_at.isoformat(), "next_action": a.next_action,
                 "next_action_date": a.next_action_date.isoformat() if a.next_action_date else None} for a in rows]

    def attention_queue(self, limit: int = 10) -> list[dict[str, Any]]:
        today = timezone.localdate()
        apps = JobApplication.objects.filter(user=self.user).exclude(status__in=["rejected", "withdrawn"])
        qs = apps.filter(Q(next_action_date__lt=today) | Q(status__in=["screening", "interview"]))
        return list(qs.values("id", "company", "role", "status", "next_action_date").order_by("next_action_date")[:limit])

    def weekly_summary(self, days: int = 30) -> dict[str, Any]:
        cutoff = timezone.localdate() - timedelta(days=days)
        rows = JobApplication.objects.filter(user=self.user, created_at__date__gte=cutoff)
        daily = defaultdict(int)
        for row in rows:
            daily[row.created_at.date().isoformat()] += 1
        return {"days": days, "new_applications": rows.count(), "daily_counts": dict(sorted(daily.items()))}
