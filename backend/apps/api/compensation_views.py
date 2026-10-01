from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.compensation_analysis import CompensationAnalysisService


def _limit(request):
    try:
        value = int(request.query_params.get("limit", 50))
    except ValueError:
        return None
    return value if 1 <= value <= 100 else None


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def compensation_analysis(request, application_id):
    result = CompensationAnalysisService(request.user).analyze(application_id)
    if result is None:
        return Response({"detail": "Application not found."}, status=404)
    return Response(result.to_dict())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def compensation_summary(request):
    limit = _limit(request)
    if limit is None:
        return Response({"detail": "limit must be an integer between 1 and 100."}, status=400)
    return Response(CompensationAnalysisService(request.user).summary(limit=limit))
