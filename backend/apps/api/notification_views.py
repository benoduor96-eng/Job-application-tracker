from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.models import JobApplication
from apps.jobs.notification_planner import (
    create_notification_tasks,
    plan_application_notifications,
    summarize_notification_plan,
)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def notification_plan(request):
    applications = JobApplication.objects.filter(
        user=request.user,
        status__in=["applied", "screening", "interview", "offer"],
    )

    plans = plan_application_notifications(applications, timezone.now())
    if request.method == "POST":
        tasks = create_notification_tasks(request.user, applications, timezone.now())
        created = [task.id for task in tasks]
    else:
        created = []

    return Response({
        "summary": summarize_notification_plan(plans),
        "plans": [
            {
                "application_id": plan.application_id,
                "action": plan.action,
                "due_at": plan.due_at,
                "priority": plan.priority,
                "reason": plan.reason,
            }
            for plan in plans
        ],
        "task_ids": created,
    })
