"""API endpoint for application data-quality auditing."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.application_audit import ApplicationAuditService


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def application_audit(request):
    try:
        limit = int(request.query_params.get("limit", 50))
    except (TypeError, ValueError):
        return Response({"detail": "limit must be an integer."}, status=400)
    if not 1 <= limit <= 200:
        return Response({"detail": "limit must be between 1 and 200."}, status=400)
    return Response(ApplicationAuditService(request.user).dashboard(limit=limit))
