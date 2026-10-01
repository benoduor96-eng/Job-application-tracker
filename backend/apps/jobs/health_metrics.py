from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
from typing import Any, Dict, List

from django.db.models import Count, Q

from .models import CareerTask as Task, Interview, JobApplication


class HealthMetricsService:
    """
    Tracks operational health across task load, interview velocity, and application momentum.
    """

    def __init__(self, user):
        self.user = user

    def task_load(self) -> Dict[str, Any]:
        tasks = Task.objects.filter(user=self.user, status__in=["todo", "in_progress"])
        overdue = tasks.filter(due_date__lt=date.today()).count()
        today = tasks.filter(due_date__date=date.today()).count()
        next_7_days = tasks.filter(due_date__date__range=[date.today(), date.today() + timedelta(days=7)]).count()
        no_due_date = tasks.filter(due_date__isnull=True).count()

        return {
            "total_open": tasks.count(),
            "overdue": overdue,
            "due_today": today,
            "due_next_7_days": next_7_days,
            "unscheduled": no_due_date,
        }

    def interview_velocity(self) -> Dict[str, Any]:
        interviews = Interview.objects.filter(application__user=self.user)
        if not interviews.exists():
            return {
                "total": 0,
                "by_type": {},
                "avg_feedback_count": 0,
            }

        by_type = dict(
            interviews.values("interview_type")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        return {
            "total": interviews.count(),
            "by_type": by_type,
            "avg_feedback_count": round(interviews.filter(feedback__isnull=False).count() / interviews.count(), 2),
        }

    def application_trend(self, days: int = 30) -> Dict[str, Any]:
        start = date.today() - timedelta(days=days)
        rows = JobApplication.objects.filter(user=self.user, created_at__date__gte=start)
        counts = Counter(row.created_at.date().isoformat() for row in rows)
        return {
            "days": days,
            "total": rows.count(),
            "daily": dict(sorted(counts.items())),
        }

    def health_score(self) -> Dict[str, Any]:
        task_data = self.task_load()
        app_data = self.application_trend()
        pipeline = JobApplication.objects.filter(user=self.user)
        active = pipeline.exclude(status__in=["rejected", "withdrawn"]).count()
        offers = pipeline.filter(status="offer").count()

        weighted = 0
        weighted += max(0, 100 - (task_data["overdue"] * 15))
        weighted += min(100, active * 3)
        weighted += offers * 20

        score = min(100, max(0, round(weighted / 5, 2)))

        return {
            "score": score,
            "task_load": task_data,
            "application_trend": app_data,
            "active_applications": active,
            "offers": offers,
        }
