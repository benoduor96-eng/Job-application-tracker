from datetime import timedelta
from collections import Counter, defaultdict
from django.db.models import Q, Count
from django.utils import timezone
from .models import JobApplication, Interview, CareerContact, CareerTask, ApplicationActivity

ACTIVE_STATUSES = {"saved", "applied", "screening", "interview", "offer"}
CLOSED_STATUSES = {"rejected", "withdrawn"}
STATUS_ORDER = ["saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn"]


class ReviewWorkspace:
    """Build a deterministic weekly review from the user's stored career data."""

    def __init__(self, user, today=None):
        self.user = user
        self.today = today or timezone.localdate()
        self.now = timezone.now()
        self.applications = JobApplication.objects.filter(user=user).prefetch_related(
            "interviews", "contacts", "activities"
        )
        self.contacts = CareerContact.objects.filter(user=user)
        self.tasks = CareerTask.objects.filter(user=user)
        self.interviews = Interview.objects.filter(application__user=user)
        self.activities = ApplicationActivity.objects.filter(user=user)

    def _days_since(self, value):
        if not value:
            return None
        if hasattr(value, "date"):
            value = value.date()
        return max(0, (self.today - value).days)

    def _application_age(self, application):
        return self._days_since(application.applied_date or application.created_at)

    def _active(self, applications=None):
        items = applications if applications is not None else self.applications
        return [a for a in items if a.status in ACTIVE_STATUSES]

    def _closed(self, applications=None):
        items = applications if applications is not None else self.applications
        return [a for a in items if a.status in CLOSED_STATUSES]

    def status_counts(self, applications=None):
        counts = Counter(a.status for a in (applications if applications is not None else self.applications))
        return {status: counts.get(status, 0) for status in STATUS_ORDER}

    @staticmethod
    def _rate(numerator, denominator):
        return round(numerator / denominator * 100, 1) if denominator else 0.0

    def momentum(self):
        current_start = self.today - timedelta(days=7)
        previous_start = self.today - timedelta(days=14)
        current = self.applications.filter(created_at__date__gte=current_start).count()
        previous = self.applications.filter(
            created_at__date__gte=previous_start, created_at__date__lt=current_start
        ).count()
        current_activities = self.activities.filter(occurred_at__date__gte=current_start).count()
        previous_activities = self.activities.filter(
            occurred_at__date__gte=previous_start, occurred_at__date__lt=current_start
        ).count()
        return {
            "applications_this_week": current,
            "applications_previous_week": previous,
            "application_change": current - previous,
            "activities_this_week": current_activities,
            "activities_previous_week": previous_activities,
            "activity_change": current_activities - previous_activities,
            "direction": "up" if current > previous else "down" if current < previous else "steady",
        }

    def risk_summary(self, applications=None):
        items = applications if applications is not None else self._active()
        buckets = Counter()
        for app in items:
            age = self._application_age(app)
            if app.next_action_date and app.next_action_date < self.today:
                buckets["overdue_follow_up"] += 1
            elif age is not None and age >= 7 and app.status in {"saved", "applied"}:
                buckets["aging_early_stage"] += 1
            elif not app.next_action_date:
                buckets["missing_next_action"] += 1
            elif app.status == "interview" and not app.interviews.filter(outcome="pending").exists():
                buckets["interview_needs_review"] += 1
            else:
                buckets["healthy"] += 1
        return dict(buckets)

    def overview(self):
        apps = list(self.applications)
        active = self._active(apps)
        closed = self._closed(apps)
        overdue = [a for a in active if a.next_action_date and a.next_action_date < self.today]
        due_today = [a for a in active if a.next_action_date == self.today]
        upcoming = [
            a for a in active
            if a.next_action_date and self.today < a.next_action_date <= self.today + timedelta(days=7)
        ]
        interviews = list(
            self.interviews.filter(
                scheduled_date__gte=self.now,
                scheduled_date__lte=self.now + timedelta(days=14),
            )
        )
        open_tasks = list(self.tasks.exclude(status__in=["done", "cancelled"]))
        return {
            "generated_at": self.now.isoformat(),
            "today": self.today.isoformat(),
            "totals": {
                "applications": len(apps),
                "active": len(active),
                "closed": len(closed),
                "interviews_next_14_days": len(interviews),
                "open_tasks": len(open_tasks),
                "contacts": self.contacts.count(),
            },
            "attention": {
                "overdue_followups": len(overdue),
                "due_today": len(due_today),
                "upcoming_7_days": len(upcoming),
                "applications_without_next_action": sum(1 for a in active if not a.next_action_date),
                "applications_without_notes": sum(1 for a in active if not a.notes.strip()),
            },
            "status_counts": self.status_counts(apps),
            "momentum": self.momentum(),
            "risk": self.risk_summary(active),
        }

    def action_queue(self, limit=30):
        actions = []
        for app in self._active():
            if app.next_action_date and app.next_action_date < self.today:
                actions.append(self._action("overdue", app, 100, f"Follow up on {app.company}"))
            elif app.next_action_date == self.today:
                actions.append(self._action("today", app, 90, app.next_action or f"Review {app.company}"))
            elif not app.next_action_date:
                actions.append(self._action("missing_plan", app, 70, f"Set a next action for {app.company}"))
            elif self._application_age(app) >= 21 and app.status in {"saved", "applied"}:
                actions.append(self._action("aging", app, 55, f"Refresh activity for {app.company}"))

        for task in self.tasks.filter(status__in=["todo", "in_progress"]).order_by("due_date")[:limit]:
            overdue = bool(task.due_date and task.due_date.date() < self.today)
            priority = {"urgent": 80, "high": 70, "medium": 50, "low": 30}.get(task.priority, 40)
            if overdue:
                priority = min(priority + 5, 85)
            actions.append({
                "kind": "task_overdue" if overdue else "task",
                "priority": priority,
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "status": task.status,
                "application_id": task.application_id,
            })

        actions.sort(key=lambda x: (-x["priority"], x.get("due_date") or "9999-12-31", x["title"]))
        return actions[:limit]

    def _action(self, kind, app, priority, title):
        return {
            "kind": kind,
            "priority": priority,
            "application_id": app.id,
            "company": app.company,
            "role": app.role,
            "status": app.status,
            "title": title,
            "due_date": app.next_action_date.isoformat() if app.next_action_date else None,
            "next_action": app.next_action,
        }

    def company_summary(self):
        groups = defaultdict(list)
        for app in self.applications:
            groups[app.company.strip().lower()].append(app)
        result = []
        for apps in groups.values():
            statuses = Counter(a.status for a in apps)
            active = [a for a in apps if a.status in ACTIVE_STATUSES]
            result.append({
                "company": apps[0].company,
                "applications": len(apps),
                "active": len(active),
                "roles": sorted({a.role for a in apps}),
                "statuses": dict(statuses),
                "last_updated": max(a.updated_at for a in apps).isoformat(),
                "has_offer": any(a.status == "offer" for a in apps),
                "follow_ups_due": sum(
                    1 for a in active if a.next_action_date and a.next_action_date <= self.today
                ),
            })
        return sorted(
            result,
            key=lambda x: (-x["active"], -x["applications"], x["company"].lower()),
        )

    def funnel(self):
        counts = self.status_counts()
        applied = sum(counts[s] for s in STATUS_ORDER if s not in {"saved"})
        screening_base = counts["screening"] + counts["interview"] + counts["offer"] + counts["rejected"]
        interview_base = counts["interview"] + counts["offer"] + counts["rejected"]
        return {
            "saved": counts["saved"],
            "applied": applied,
            "screening": screening_base,
            "interview": interview_base,
            "offer": counts["offer"],
            "conversion_rates": {
                "applied_to_screening": self._rate(screening_base, applied),
                "screening_to_interview": self._rate(interview_base, screening_base),
                "interview_to_offer": self._rate(counts["offer"], interview_base),
                "applied_to_offer": self._rate(counts["offer"], applied),
            },
        }

    def interview_calendar(self, days=30):
        end = self.now + timedelta(days=days)
        rows = []
        for interview in self.interviews.filter(
            scheduled_date__gte=self.now, scheduled_date__lte=end
        ).order_by("scheduled_date"):
            app = interview.application
            rows.append({
                "id": interview.id,
                "application_id": app.id,
                "company": app.company,
                "role": app.role,
                "type": interview.get_interview_type_display(),
                "scheduled_date": interview.scheduled_date.isoformat() if interview.scheduled_date else None,
                "outcome": interview.outcome,
                "interviewer": interview.interviewer_name,
            })
        return rows

    def contact_health(self):
        contacts = list(self.contacts)
        stale_cutoff = self.now - timedelta(days=30)
        return {
            "total": len(contacts),
            "never_contacted": sum(1 for c in contacts if not c.last_contacted_at and not c.application_id),
            "stale": sum(1 for c in contacts if c.last_contacted_at and c.last_contacted_at < stale_cutoff),
            "overdue_followups": sum(1 for c in contacts if c.next_follow_up and c.next_follow_up < self.now),
            "with_application": sum(1 for c in contacts if c.application_id),
            "by_type": dict(Counter(c.contact_type for c in contacts)),
        }

    def task_health(self):
        tasks = list(self.tasks)
        open_tasks = [t for t in tasks if t.status in {"todo", "in_progress"}]
        overdue = [t for t in open_tasks if t.due_date and t.due_date.date() < self.today]
        return {
            "total": len(tasks),
            "open": len(open_tasks),
            "overdue": len(overdue),
            "completed": sum(1 for t in tasks if t.status == "done"),
            "cancelled": sum(1 for t in tasks if t.status == "cancelled"),
            "by_priority": dict(Counter(t.priority for t in open_tasks)),
            "completion_rate": self._rate(sum(1 for t in tasks if t.status == "done"), len(tasks)),
        }

    def full_review(self):
        return {
            "overview": self.overview(),
            "action_queue": self.action_queue(),
            "companies": self.company_summary(),
            "funnel": self.funnel(),
            "interviews": self.interview_calendar(),
            "contact_health": self.contact_health(),
            "task_health": self.task_health(),
        }
