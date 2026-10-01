from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.jobs.application_timeline import ApplicationTimeline


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def timeline_dashboard(request):
    return Response(ApplicationTimeline(request.user).dashboard())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def application_timeline(request, application_id):
    try:
        limit = min(max(int(request.query_params.get("limit", 100)), 1), 250)
    except (TypeError, ValueError):
        limit = 100
    events = ApplicationTimeline(request.user).events_for_application(application_id, limit=limit)
    if events is None:
        return Response({"detail": "Application not found."}, status=404)
    return Response({"events": events})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def timeline_events(request):
    try:
        limit = min(max(int(request.query_params.get("limit", 100)), 1), 250)
    except (TypeError, ValueError):
        limit = 100
    service = ApplicationTimeline(request.user)
    return Response({"events": service.filter_events(
        kind=request.query_params.get("kind") or None,
        source=request.query_params.get("source") or None,
        application_id=request.query_params.get("application_id") or None,
        limit=limit,
    )})
