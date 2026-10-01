from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
from typing import Any

from django.db.models import Count

from .models import Interview, JobApplication, Task


class HealthMetricsService:
    """Measures operational health of a user's job-search pipeline."""

    def __init__(self, user):
        self.user = user

    def task_load(self) -> dict[str, Any]:
        tasks = Task.objects.filter(user=self.user, is_completed=False)
        today = date.today()
        return {
            "total_open": tasks.count(),
            "overdue": tasks.filter(due_date__lt=today).count(),
            "due_today": tasks.filter(due_date=today).count(),
            "due_next_7_days": tasks.filter(due_date__range=[today, today + timedelta(days=7)]).count(),
            "unscheduled": tasks.filter(due_date__isnull=True).count(),
        }

    def interview_velocity(self) -> dict[str, Any]:
        interviews = Interview.objects.filter(application__user=self.user)
        total = interviews.count()
        if not total:
            return {"total": 0, "by_type": {}, "feedback_rate": 0.0}
        by_type = {row["interview_type"]: row["total"] for row in interviews.values("interview_type").annotate(total=Count("id"))}
        feedback = interviews.exclude(feedback="").count()
        return {"total": total, "by_type": by_type, "feedback_rate": round(feedback / total * 100, 2)}

    def application_trend(self, days: int = 30) -> dict[str, Any]:
        start = date.today() - timedelta(days=days)
        rows = JobApplication.objects.filter(user=self.user, created_at__date__gte=start)
        daily = Counter(row.created_at.date().isoformat() for row in rows)
        return {"days": days, "total": rows.count(), "daily": dict(sorted(daily.items()))}

    def health_score(self) -> dict[str, Any]:
        task_data = self.task_load()
        active = JobApplication.objects.filter(user=self.user).exclude(status__in=["rejected", "withdrawn"]).count()
        offers = JobApplication.objects.filter(user=self.user, status="offer").count()
        score = min(100, max(0, round((max(0, 100 - task_data["overdue"] * 15) + min(100, active * 3) + offers * 20) / 5, 2)))
        return {"score": score, "task_load": task_data, "application_trend": self.application_trend(),
                "active_applications": active, "offers": offers}
