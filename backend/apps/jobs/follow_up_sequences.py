"""Follow-up sequence planning for applications."""
from dataclasses import dataclass
from datetime import date, timedelta

from django.utils import timezone

from apps.jobs.models import CareerTask, JobApplication


@dataclass(frozen=True)
class FollowUpStep:
    offset_days: int
    title: str
    priority: str
    reason: str


SEQUENCES = {
    "applied": (
        FollowUpStep(5, "Check application status", "medium", "Application has been submitted."),
        FollowUpStep(10, "Send a concise follow-up", "medium", "Allow reasonable time before contacting the employer."),
        FollowUpStep(18, "Review application and update pipeline", "low", "Keep stale applications visible."),
    ),
    "screening": (
        FollowUpStep(3, "Follow up after screening", "high", "Screening is an active pipeline stage."),
        FollowUpStep(7, "Review screening notes", "medium", "Capture lessons while the conversation is recent."),
    ),
    "interview": (
        FollowUpStep(2, "Send interview follow-up", "high", "Interview activity should receive prompt follow-up."),
        FollowUpStep(7, "Check interview status", "medium", "Keep an unanswered interview visible."),
    ),
}


def build_sequence(application: JobApplication, start: date | None = None) -> list[dict]:
    start = start or timezone.localdate()
    steps = SEQUENCES.get(application.status, ())
    return [
        {
            "application_id": application.id,
            "title": step.title,
            "priority": step.priority,
            "reason": step.reason,
            "due_date": start + timedelta(days=step.offset_days),
        }
        for step in steps
    ]


def create_sequence(application: JobApplication, start: date | None = None) -> list[CareerTask]:
    created = []
    for plan in build_sequence(application, start):
        exists = CareerTask.objects.filter(
            application=application,
            title=plan["title"],
            status__in=["todo", "in_progress"],
        ).exists()
        if exists:
            continue
        created.append(CareerTask.objects.create(
            application=application,
            title=plan["title"],
            description=plan["reason"],
            priority=plan["priority"],
            status="todo",
            due_date=plan["due_date"],
            tags=["follow-up", application.status],
        ))
    return created


def cancel_open_sequence(application: JobApplication) -> int:
    return CareerTask.objects.filter(
        application=application,
        status__in=["todo", "in_progress"],
        tags__contains=["follow-up"],
    ).update(status="cancelled")


def sequence_summary(application: JobApplication) -> dict:
    tasks = CareerTask.objects.filter(application=application, tags__contains=["follow-up"])
    return {
        "total": tasks.count(),
        "open": tasks.filter(status__in=["todo", "in_progress"]).count(),
        "completed": tasks.filter(status="done").count(),
        "cancelled": tasks.filter(status="cancelled").count(),
    }
