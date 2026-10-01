from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.application_health import ApplicationHealthService


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def application_health(request, application_id):
    result = ApplicationHealthService(request.user).analyze(application_id)
    if result is None:
        return Response({"detail": "Application not found."}, status=404)
    return Response(result.to_dict())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def application_health_summary(request):
    try:
        limit = int(request.query_params.get("limit", 25))
    except ValueError:
        return Response({"detail": "limit must be an integer."}, status=400)
    if not 1 <= limit <= 100:
        return Response({"detail": "limit must be between 1 and 100."}, status=400)
    return Response(ApplicationHealthService(request.user).summary(limit=limit))
