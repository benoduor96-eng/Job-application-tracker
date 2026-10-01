from collections import Counter
from datetime import timedelta
from decimal import Decimal
from django.db.models import Avg, Count, Q
from django.utils import timezone
from .models import JobApplication, Interview, CareerContact, CareerTask, ApplicationActivity


class DashboardSnapshot:
    """Return a compact operational snapshot without mutating career records."""

    ACTIVE = {"saved", "applied", "screening", "interview", "offer"}
    CLOSED = {"rejected", "withdrawn"}

    def __init__(self, user, now=None):
        self.user = user
        self.now = now or timezone.now()
        self.today = self.now.date()
        self.apps = JobApplication.objects.filter(user=user)
        self.interviews = Interview.objects.filter(application__user=user)
        self.contacts = CareerContact.objects.filter(user=user)
        self.tasks = CareerTask.objects.filter(user=user)
        self.activities = ApplicationActivity.objects.filter(user=user)

    def counts(self):
        status_counts = Counter(self.apps.values_list("status", flat=True))
        return {
            "applications": self.apps.count(),
            "active": sum(status_counts[s] for s in self.ACTIVE),
            "closed": sum(status_counts[s] for s in self.CLOSED),
            "saved": status_counts["saved"],
            "applied": status_counts["applied"],
            "screening": status_counts["screening"],
            "interview": status_counts["interview"],
            "offer": status_counts["offer"],
            "rejected": status_counts["rejected"],
            "withdrawn": status_counts["withdrawn"],
            "contacts": self.contacts.count(),
            "open_tasks": self.tasks.filter(status__in=["todo", "in_progress"]).count(),
        }

    def activity_window(self, days=30):
        start = self.now - timedelta(days=days)
        queryset = self.activities.filter(occurred_at__gte=start)
        by_type = Counter(queryset.values_list("activity_type", flat=True))
        daily = Counter(item.occurred_at.date().isoformat() for item in queryset)
        return {
            "days": days,
            "total": queryset.count(),
            "by_type": dict(by_type),
            "daily": [
                {"date": day, "count": count}
                for day, count in sorted(daily.items())
            ],
        }

    def application_velocity(self, days=30):
        start = self.today - timedelta(days=days - 1)
        current = self.apps.filter(created_at__date__gte=start).count()
        previous_start = start - timedelta(days=days)
        previous = self.apps.filter(
            created_at__date__gte=previous_start,
            created_at__date__lt=start,
        ).count()
        average = round(current / days, 2) if days else 0
        change = current - previous
        return {
            "window_days": days,
            "applications": current,
            "previous_window": previous,
            "daily_average": average,
            "change": change,
            "direction": "up" if change > 0 else "down" if change < 0 else "steady",
        }

    def response_metrics(self):
        applied = list(self.apps.exclude(applied_date__isnull=True))
        interview_ids = set(
            self.interviews.filter(scheduled_date__isnull=False)
            .values_list("application_id", flat=True)
        )
        interviewed = [item for item in applied if item.id in interview_ids]
        days_to_interview = []
        for item in interviewed:
            first = self.interviews.filter(
                application=item,
                scheduled_date__isnull=False,
            ).order_by("scheduled_date").first()
            if first and item.applied_date:
                delta = (first.scheduled_date.date() - item.applied_date).days
                if delta >= 0:
                    days_to_interview.append(delta)
        return {
            "applied_with_date": len(applied),
            "applications_reaching_interview": len(interviewed),
            "interview_rate": round(len(interviewed) / len(applied) * 100, 1) if applied else 0,
            "average_days_to_interview": round(sum(days_to_interview) / len(days_to_interview), 1) if days_to_interview else None,
        }

    def salary_snapshot(self):
        rows = list(
            self.apps.exclude(salary_min__isnull=True, salary_max__isnull=True)
            .values_list("salary_min", "salary_max", "status")
        )
        midpoints = []
        for minimum, maximum, status in rows:
            if minimum is not None and maximum is not None:
                midpoints.append((Decimal(minimum) + Decimal(maximum)) / Decimal("2"))
            elif minimum is not None:
                midpoints.append(Decimal(minimum))
            elif maximum is not None:
                midpoints.append(Decimal(maximum))
        return {
            "applications_with_salary": len(rows),
            "average_midpoint": str(round(sum(midpoints) / len(midpoints), 2)) if midpoints else None,
            "minimum": str(min(midpoints)) if midpoints else None,
            "maximum": str(max(midpoints)) if midpoints else None,
            "active_with_salary": sum(1 for row in rows if row[2] in self.ACTIVE),
        }

    def deadlines(self):
        upcoming = self.apps.filter(
            user=self.user,
            next_action_date__isnull=False,
            next_action_date__gte=self.today,
            next_action_date__lte=self.today + timedelta(days=14),
        ).order_by("next_action_date")
        overdue = self.apps.filter(
            user=self.user,
            status__in=self.ACTIVE,
            next_action_date__lt=self.today,
        ).order_by("next_action_date")
        return {
            "due_today": upcoming.filter(next_action_date=self.today).count(),
            "next_14_days": upcoming.count(),
            "overdue": overdue.count(),
            "upcoming": [{
                "id": item.id,
                "company": item.company,
                "role": item.role,
                "date": item.next_action_date.isoformat(),
                "action": item.next_action,
            } for item in upcoming[:15]],
            "overdue_items": [{
                "id": item.id,
                "company": item.company,
                "role": item.role,
                "date": item.next_action_date.isoformat(),
                "action": item.next_action,
            } for item in overdue[:15]],
        }

    def interview_window(self, days=14):
        end = self.now + timedelta(days=days)
        rows = self.interviews.filter(
            scheduled_date__gte=self.now,
            scheduled_date__lte=end,
        ).select_related("application").order_by("scheduled_date")
        return [{
            "id": item.id,
            "application_id": item.application_id,
            "company": item.application.company,
            "role": item.application.role,
            "type": item.get_interview_type_display(),
            "scheduled": item.scheduled_date.isoformat() if item.scheduled_date else None,
            "outcome": item.outcome,
            "interviewer": item.interviewer_name,
        } for item in rows]

    def workload(self):
        open_tasks = self.tasks.filter(status__in=["todo", "in_progress"])
        overdue_tasks = open_tasks.filter(due_date__lt=self.now)
        overdue_contacts = self.contacts.filter(next_follow_up__lt=self.now)
        return {
            "open_tasks": open_tasks.count(),
            "overdue_tasks": overdue_tasks.count(),
            "urgent_tasks": open_tasks.filter(priority="urgent").count(),
            "high_priority_tasks": open_tasks.filter(priority="high").count(),
            "overdue_contact_followups": overdue_contacts.count(),
            "never_contacted": self.contacts.filter(last_contacted_at__isnull=True).count(),
        }

    def company_leaderboard(self, limit=10):
        rows = (
            self.apps.values("company")
            .annotate(
                applications_count=Count("id"),
                active_count=Count("id", filter=Q(status__in=self.ACTIVE)),
                offer_count=Count("id", filter=Q(status="offer")),
                interview_count=Count("id", filter=Q(status="interview")),
            )
            .order_by("-active_count", "-applications_count", "company")[:limit]
        )
        return [{
            "company": row["company"],
            "applications": row["applications_count"],
            "active": row["active_count"],
            "interviews": row["interview_count"],
            "offers": row["offer_count"],
        } for row in rows]

    def focus_items(self):
        items = []
        deadlines = self.deadlines()
        for row in deadlines["overdue_items"]:
            items.append({
                "priority": 100,
                "type": "overdue",
                "title": "Overdue follow-up",
                "company": row["company"],
                "role": row["role"],
                "application_id": row["id"],
                "detail": row["action"] or "No action recorded",
            })
        for row in deadlines["upcoming"][:8]:
            items.append({
                "priority": 80,
                "type": "upcoming",
                "title": "Upcoming follow-up",
                "company": row["company"],
                "role": row["role"],
                "application_id": row["id"],
                "detail": row["action"] or "Review application",
            })
        workload = self.workload()
        if workload["urgent_tasks"]:
            items.append({
                "priority": 95,
                "type": "task",
                "title": "Urgent career tasks",
                "company": None,
                "role": None,
                "application_id": None,
                "detail": f'{workload["urgent_tasks"]} urgent task(s) remain open',
            })
        for item in self.interview_window(7)[:5]:
            items.append({
                "priority": 90,
                "type": "interview",
                "title": "Interview scheduled",
                "company": item["company"],
                "role": item["role"],
                "application_id": item["application_id"],
                "detail": item["scheduled"],
            })
        return sorted(items, key=lambda row: (-row["priority"], row["title"], row.get("company") or ""))

    def dashboard(self):
        return {
            "generated_at": self.now.isoformat(),
            "counts": self.counts(),
            "velocity": self.application_velocity(),
            "activity": self.activity_window(),
            "response": self.response_metrics(),
            "salary": self.salary_snapshot(),
            "deadlines": self.deadlines(),
            "interviews": self.interview_window(),
            "workload": self.workload(),
            "companies": self.company_leaderboard(),
            "focus": self.focus_items(),
        }
