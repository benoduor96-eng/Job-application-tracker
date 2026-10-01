"""Database operations for moving applications between pipeline stages."""
from django.db import transaction
from django.utils import timezone
from .models import ApplicationActivity, JobApplication
from .pipeline_board import STAGE_LABELS, plan_moves

@transaction.atomic
def move_applications(user, ids, target, now=None):
    now = now or timezone.now()
    applications = {a.id: a for a in JobApplication.objects.select_for_update().filter(user=user, id__in=ids)}
    plan = plan_moves({i: a.status for i, a in applications.items()}, ids, target)
    activities = []
    for application_id in plan["moved"]:
        application = applications[application_id]
        previous = application.status
        application.status = target
        fields = ["status", "updated_at"]
        if target == "applied" and application.applied_date is None:
            application.applied_date = now.date()
            fields.append("applied_date")
        application.save(update_fields=fields)
        activities.append(ApplicationActivity(
            application=application, user=user, activity_type="status_change",
            title=f"Moved from {STAGE_LABELS[previous]} to {STAGE_LABELS[target]}",
            metadata={"from": previous, "to": target, "source": "pipeline_board"},
            occurred_at=now,
        ))
    ApplicationActivity.objects.bulk_create(activities)
    return plan
