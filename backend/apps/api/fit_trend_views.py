"""Authenticated API for application-fit trend analytics."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.jobs.fit_trends import FitTrendService

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fit_trends(request):
    try:
        limit = int(request.query_params.get("limit", 100))
    except (TypeError, ValueError):
        return Response({"detail": "limit must be an integer."}, status=400)
    if not 1 <= limit <= 100:
        return Response({"detail": "limit must be between 1 and 100."}, status=400)
    return Response(FitTrendService(request.user).summary(limit))
