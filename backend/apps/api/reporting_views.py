"""Reporting API endpoints."""
from rest_framework import decorators, permissions, response, status

from apps.jobs.application_reporting import dashboard_report, stale_report
from apps.jobs.follow_up_sequences import build_sequence, create_sequence, sequence_summary
from apps.jobs.interview_prep import interview_readiness, questions_for_application
from apps.jobs.models import JobApplication


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def reporting_dashboard(request):
    return response.Response(dashboard_report(request.user))


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def stale_applications(request):
    try:
        days = int(request.query_params.get("days", 14))
    except ValueError:
        return response.Response({"detail": "days must be an integer"}, status=400)
    return response.Response({"items": stale_report(request.user, days)})


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def interview_preparation(request, application_id):
    application = JobApplication.objects.filter(
        id=application_id, user=request.user
    ).first()
    if not application:
        return response.Response({"detail": "Application not found."}, status=404)
    return response.Response({
        "readiness": interview_readiness(application),
        "questions": [item.__dict__ for item in questions_for_application(application)],
    })


@decorators.api_view(["GET", "POST"])
@decorators.permission_classes([permissions.IsAuthenticated])
def follow_up_sequence(request, application_id):
    application = JobApplication.objects.filter(
        id=application_id, user=request.user
    ).first()
    if not application:
        return response.Response({"detail": "Application not found."}, status=404)
    if request.method == "GET":
        return response.Response({
            "plan": build_sequence(application),
            "summary": sequence_summary(application),
        })
    tasks = create_sequence(application)
    return response.Response(
        {"created": [task.id for task in tasks], "summary": sequence_summary(application)},
        status=status.HTTP_201_CREATED,
    )
