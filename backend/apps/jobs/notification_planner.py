from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable

from django.utils import timezone

from .models import CareerTask, JobApplication


@dataclass(frozen=True)
class NotificationPlan:
    application_id: int
    action: str
    due_at: datetime
    priority: str
    reason: str


STATUS_DELAYS = {
    "applied": (5, "Follow up after application"),
    "screening": (3, "Check screening progress"),
    "interview": (1, "Prepare for the next interview step"),
    "offer": (2, "Review offer and response timeline"),
}


def plan_application_notifications(
    applications: Iterable[JobApplication],
    now: datetime | None = None,
) -> list[NotificationPlan]:
    current = now or timezone.now()
    plans: list[NotificationPlan] = []

    for application in applications:
        if application.status not in STATUS_DELAYS:
            continue

        days, reason = STATUS_DELAYS[application.status]
        base = application.updated_at or current
        due_at = base + timedelta(days=days)
        if due_at < current:
            due_at = current

        priority = "high" if application.status in {"interview", "offer"} else "medium"
        plans.append(
            NotificationPlan(
                application_id=application.id,
                action=reason,
                due_at=due_at,
                priority=priority,
                reason=f"Application is currently in {application.get_status_display()} status.",
            )
        )

    return sorted(plans, key=lambda item: (item.due_at, -{"urgent": 4, "high": 3, "medium": 2, "low": 1}[item.priority]))


def create_notification_tasks(
    user,
    applications: Iterable[JobApplication],
    now: datetime | None = None,
) -> list[CareerTask]:
    plans = plan_application_notifications(applications, now)
    created: list[CareerTask] = []

    for plan in plans:
        title = f"{plan.action}: {next((a.company for a in applications if a.id == plan.application_id), 'application')}"
        existing = CareerTask.objects.filter(
            user=user,
            application_id=plan.application_id,
            title=title,
            status__in=["todo", "in_progress"],
        ).first()
        if existing:
            created.append(existing)
            continue

        task = CareerTask.objects.create(
            user=user,
            application_id=plan.application_id,
            title=title,
            description=plan.reason,
            priority=plan.priority,
            due_date=plan.due_at,
            tags=["notification", "follow-up"],
        )
        created.append(task)

    return created


def summarize_notification_plan(plans: Iterable[NotificationPlan]) -> dict:
    items = list(plans)
    by_priority = {}
    for item in items:
        by_priority[item.priority] = by_priority.get(item.priority, 0) + 1

    return {
        "count": len(items),
        "by_priority": by_priority,
        "next_due": min((item.due_at for item in items), default=None),
        "application_ids": [item.application_id for item in items],
    }
