from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any, Dict, List

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from .models import JobApplication, Task, CareerProfile


@dataclass
class NotificationMessage:
    subject: str
    body: str
    channel: str = "email"
    metadata: Dict[str, Any] = field(default_factory=dict)


class NotificationService:
    """
    Job-search reminders and status notifications for active applications.
    """

    def __init__(self, user):
        self.user = user

    def build_overdue_task_notice(self) -> NotificationMessage:
        overdue = Task.objects.filter(
            user=self.user,
            is_completed=False,
            due_date__lt=timezone.localdate(),
        ).order_by("due_date")[:10]

        if not overdue.exists():
            return NotificationMessage(
                subject="No overdue tasks",
                body="You are all caught up.",
                channel="email",
                metadata={"count": 0},
            )

        items = [f"- {task.title} (due {task.due_date})" for task in overdue]
        body = "You have overdue tasks:

" + "
".join(items)
        return NotificationMessage(
            subject="Job search follow-up reminder",
            body=body,
            channel="email",
            metadata={"count": overdue.count()},
        )

    def build_application_status_digest(self) -> NotificationMessage:
        active = JobApplication.objects.filter(user=self.user).exclude(status__in=["rejected", "withdrawn"])
        summary = []
        for app in active.order_by("-updated_at")[:5]:
            summary.append(f"- {app.company}: {app.role} ({app.status})")

        body = "Your active applications:

" + ("
".join(summary) if summary else "No active applications.")
        return NotificationMessage(
            subject="Application status digest",
            body=body,
            channel="email",
            metadata={"count": active.count()},
        )

    def build_profile_gap_notice(self) -> NotificationMessage:
        profile = CareerProfile.objects.filter(user=self.user).first()
        if not profile:
            return NotificationMessage(
                subject="Profile setup reminder",
                body="You have not completed your profile yet. Add your headline, skills, and role preferences.",
                channel="email",
                metadata={"profile_complete": False},
            )

        missing = []
        if not profile.headline:
            missing.append("headline")
        if not profile.professional_summary:
            missing.append("summary")
        if not profile.skills:
            missing.append("skills")
        if not profile.preferred_roles:
            missing.append("preferred roles")

        if not missing:
            return NotificationMessage(
                subject="Profile is complete",
                body="Your profile is complete and ready for role targeting.",
                channel="email",
                metadata={"profile_complete": True},
            )

        return NotificationMessage(
            subject="Profile improvement reminder",
            body=f"Your profile is missing: {', '.join(missing)}.",
            channel="email",
            metadata={"profile_complete": False, "missing_fields": missing},
        )

    def send_digest(self) -> Dict[str, Any]:
        notices = [
            self.build_overdue_task_notice(),
            self.build_application_status_digest(),
            self.build_profile_gap_notice(),
        ]

        sent = []
        for item in notices:
            if self.user.email:
                send_mail(
                    item.subject,
                    item.body,
                    "noreply@example.com",
                    [self.user.email],
                    fail_silently=True,
                )
            sent.append({
                "subject": item.subject,
                "channel": item.channel,
                "metadata": item.metadata,
            })
        return {"sent": sent, "count": len(sent)}

    def reminder_candidates(self, days_ahead: int = 3) -> List[Dict[str, Any]]:
        deadline = timezone.localdate() + timedelta(days=days_ahead)
        tasks = Task.objects.filter(
            user=self.user,
            is_completed=False,
            due_date__lte=deadline,
        ).order_by("due_date")

        result = []
        for task in tasks:
            result.append({
                "task_id": task.id,
                "title": task.title,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "priority": task.priority,
                "application_id": task.application_id,
            })
        return result
