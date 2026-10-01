from __future__ import annotations

from collections import defaultdict, Counter
from datetime import date, timedelta
from decimal import Decimal
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from django.db.models import Avg, Count, Max, Min, Q, Sum
from django.utils import timezone

from .models import JobApplication, Interview, CareerTask as Task, CareerProfile


class ReportingService:
    """
    Central reporting service for application health, pipeline trends, and status analysis.
    This is intentionally business-specific and not generic boilerplate.
    """

    def __init__(self, user):
        self.user = user

    def dashboard_summary(self) -> Dict[str, Any]:
        applications = JobApplication.objects.filter(user=self.user)

        total = applications.count()
        active = applications.exclude(status__in=["rejected", "withdrawn"]).count()
        interviews = applications.filter(status="interview").count()
        offers = applications.filter(status="offer").count()
        rejected = applications.filter(status="rejected").count()
        saved = applications.filter(status="saved").count()
        applied = applications.filter(status="applied").count()
        screening = applications.filter(status="screening").count()

        today = timezone.localdate()
        overdue = Task.objects.filter(
            user=self.user,
            is_completed=False,
            due_date__lt=today,
        ).count()

        upcoming = Task.objects.filter(
            user=self.user,
            is_completed=False,
            due_date__gte=today,
        ).count()

        conversion_rate = round((offers / total) * 100, 2) if total else 0.0

        by_status = list(
            applications.values("status").annotate(total=Count("id")).order_by("-total")
        )

        return {
            "total_applications": total,
            "active_applications": active,
            "interviews": interviews,
            "offers": offers,
            "rejected": rejected,
            "saved": saved,
            "applied": applied,
            "screening": screening,
            "overdue_tasks": overdue,
            "upcoming_tasks": upcoming,
            "conversion_rate": conversion_rate,
            "by_status": by_status,
        }

    def status_distribution(self) -> List[Dict[str, Any]]:
        qs = JobApplication.objects.filter(user=self.user)
        return list(
            qs.values("status")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

    def pipeline_health(self) -> Dict[str, Any]:
        applications = JobApplication.objects.filter(user=self.user)
        total = applications.count()

        if total == 0:
            return {
                "total": 0,
                "screening_rate": 0.0,
                "interview_rate": 0.0,
                "offer_rate": 0.0,
                "response_rate": 0.0,
            }

        screening = applications.filter(status__in=["screening", "interview", "offer"]).count()
        interviews = applications.filter(status__in=["interview", "offer"]).count()
        offers = applications.filter(status="offer").count()

        screening_rate = round((screening / total) * 100, 2)
        interview_rate = round((interviews / total) * 100, 2)
        offer_rate = round((offers / total) * 100, 2)
        response_rate = round(((screening + interviews + offers) / total) * 100, 2)

        return {
            "total": total,
            "screening_rate": screening_rate,
            "interview_rate": interview_rate,
            "offer_rate": offer_rate,
            "response_rate": response_rate,
        }

    def salary_statistics(self) -> Dict[str, Any]:
        applications = JobApplication.objects.filter(
            user=self.user,
            salary_min__isnull=False,
        )

        if not applications.exists():
            return {
                "count": 0,
                "avg_min": None,
                "avg_max": None,
                "highest_min": None,
                "lowest_max": None,
                "salary_band": None,
            }

        mins = applications.aggregate(avg_min=Avg("salary_min"), max_min=Max("salary_min"), min_min=Min("salary_min"))
        maxes = applications.aggregate(avg_max=Avg("salary_max"), max_max=Max("salary_max"), min_max=Min("salary_max"))

        return {
            "count": applications.count(),
            "avg_min": round(float(mins["avg_min"])) if mins["avg_min"] else None,
            "avg_max": round(float(maxes["avg_max"])) if maxes["avg_max"] else None,
            "highest_min": round(float(mins["max_min"])) if mins["max_min"] else None,
            "lowest_max": round(float(maxes["min_max"])) if maxes["min_max"] else None,
            "salary_band": {
                "min": round(float(mins["min_min"])) if mins["min_min"] else None,
                "max": round(float(maxes["max_max"])) if maxes["max_max"] else None,
            },
        }

    def application_timeline(self, days_back: int = 90) -> List[Dict[str, Any]]:
        cutoff = timezone.localdate() - timedelta(days=days_back)

        qs = JobApplication.objects.filter(
            user=self.user,
            created_at__date__gte=cutoff,
        ).order_by("created_at")

        rows = []
        for app in qs:
            rows.append({
                "application_id": app.id,
                "company": app.company,
                "role": app.role,
                "status": app.status,
                "created_at": app.created_at.isoformat(),
                "next_action": app.next_action,
                "next_action_date": app.next_action_date.isoformat() if app.next_action_date else None,
            })
        return rows

    def response_lag_summary(self) -> Dict[str, Any]:
        applications = JobApplication.objects.filter(
            user=self.user,
            applied_date__isnull=False,
        ).exclude(status__in=["saved"])
        if not applications.exists():
            return {
                "tracked": 0,
                "avg_response_days": None,
                "median_response_days": None,
                "slowest": None,
            }

        values = []
        for app in applications:
            if app.updated_at and app.applied_date:
                delta = (app.updated_at.date() - app.applied_date).days
                values.append(delta)

        values = sorted(values)
        average = round(sum(values) / len(values), 2) if values else 0.0
        median = values[len(values) // 2] if values else 0.0

        return {
            "tracked": len(values),
            "avg_response_days": average,
            "median_response_days": median,
            "slowest": max(values) if values else 0,
        }

    def top_companies(self, limit: int = 10) -> List[Dict[str, Any]]:
        qs = JobApplication.objects.filter(user=self.user)
        return list(
            qs.values("company")
            .annotate(total=Count("id"))
            .order_by("-total")[:limit]
        )

    def top_roles(self, limit: int = 10) -> List[Dict[str, Any]]:
        qs = JobApplication.objects.filter(user=self.user)
        return list(
            qs.values("role")
            .annotate(total=Count("id"))
            .order_by("-total")[:limit]
        )

    def recent_activity(self, limit: int = 10) -> List[Dict[str, Any]]:
        qs = JobApplication.objects.filter(user=self.user).order_by("-updated_at")[:limit]
        return [
            {
                "application_id": app.id,
                "company": app.company,
                "role": app.role,
                "status": app.status,
                "updated_at": app.updated_at.isoformat(),
            }
            for app in qs
        ]

    def weekly_summary(self, days: int = 30) -> Dict[str, Any]:
        cutoff = timezone.localdate() - timedelta(days=days)
        qs = JobApplication.objects.filter(
            user=self.user,
            created_at__date__gte=cutoff,
        )

        by_day = defaultdict(int)
        for app in qs:
            key = app.created_at.date().isoformat()
            by_day[key] += 1

        return {
            "days": days,
            "new_applications": qs.count(),
            "daily_counts": dict(sorted(by_day.items())),
        }

    def market_signal_summary(self) -> Dict[str, Any]:
        apps = JobApplication.objects.filter(user=self.user).exclude(status="saved")
        total = apps.count()

        if total == 0:
            return {
                "companies_tracked": 0,
                "roles_tracked": 0,
                "interview_ready_count": 0,
                "immediate_attention": [],
            }

        companies_tracked = apps.values("company").distinct().count()
        roles_tracked = apps.values("role").distinct().count()
        interview_ready_count = apps.filter(status="interview").count()

        immediate_attention = list(
            apps.filter(
                Q(status__in=["screening", "interview"]) |
                Q(next_action_date__lt=timezone.localdate())
            )
            .values("company", "role", "status", "next_action_date")
            .order_by("next_action_date")[:10]
        )

        return {
            "companies_tracked": companies_tracked,
            "roles_tracked": roles_tracked,
            "interview_ready_count": interview_ready_count,
            "immediate_attention": immediate_attention,
        }
