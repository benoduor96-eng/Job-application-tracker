"""Calendar export endpoint."""
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import decorators, permissions, response

from apps.jobs.calendar_export import build_ics, parse_bool, parse_duration
from apps.jobs.models import Interview, JobApplication

@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def calendar_export(request):
    """Download interviews and follow-up dates as an .ics calendar file."""
    try:
        duration = parse_duration(request.query_params.get("duration"))
        include_past = parse_bool(request.query_params.get("include_past"))
    except ValueError as exc:
        return response.Response({"detail": str(exc)}, status=400)

    interviews = Interview.objects.filter(application__user=request.user).select_related("application")
    applications = JobApplication.objects.filter(user=request.user)
    content = build_ics(interviews, applications, now=timezone.now(),
                        duration_minutes=duration, include_past=include_past)
    reply = HttpResponse(content, content_type="text/calendar; charset=utf-8")
    reply["Content-Disposition"] = 'attachment; filename="job-tracker.ics"'
    return reply
