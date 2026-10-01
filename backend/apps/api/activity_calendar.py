from collections import defaultdict
from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.models import CareerTask, Interview, JobApplication


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def activity_calendar(request):
    today = timezone.localdate()
    start = today - timedelta(days=14)
    end = today + timedelta(days=45)

    applications = JobApplication.objects.filter(
        user=request.user,
        applied_date__range=(start, end),
    ).values("id", "company", "role", "status", "applied_date")

    tasks = CareerTask.objects.filter(
        user=request.user,
        due_date__date__range=(start, end),
    ).values("id", "title", "status", "priority", "due_date")

    interviews = Interview.objects.filter(
        application__user=request.user,
        scheduled_date__date__range=(start, end),
    ).select_related("application").values(
        "id", "scheduled_date", "interview_type", "outcome",
        "application__company", "application__role",
    )

    days = defaultdict(list)
    for item in applications:
        key = str(item["applied_date"])
        days[key].append({
            "type": "application",
            "id": item["id"],
            "title": f'{item["company"]} · {item["role"]}',
            "status": item["status"],
        })
    for item in tasks:
        key = str(item["due_date"].date())
        days[key].append({
            "type": "task",
            "id": item["id"],
            "title": item["title"],
            "status": item["status"],
            "priority": item["priority"],
        })
    for item in interviews:
        key = str(item["scheduled_date"].date())
        days[key].append({
            "type": "interview",
            "id": item["id"],
            "title": f'{item["application__company"]} · {item["application__role"]}',
            "status": item["outcome"],
            "interview_type": item["interview_type"],
        })

    return Response({
        "range": {"start": str(start), "end": str(end)},
        "today": str(today),
        "days": dict(days),
        "totals": {
            "applications": len(applications),
            "tasks": len(tasks),
            "interviews": len(interviews),
        },
    })
