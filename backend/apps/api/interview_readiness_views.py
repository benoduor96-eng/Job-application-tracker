from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.interview_readiness import InterviewReadinessService


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def interview_readiness(request, application_id):
    result = InterviewReadinessService(request.user).analyze(application_id)
    if result is None:
        return Response({"detail": "Application not found."}, status=404)
    return Response(result.to_dict())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def interview_readiness_summary(request):
    try:
        limit = int(request.query_params.get("limit", 50))
    except ValueError:
        return Response({"detail": "limit must be an integer."}, status=400)
    if not 1 <= limit <= 100:
        return Response({"detail": "limit must be between 1 and 100."}, status=400)
    return Response(InterviewReadinessService(request.user).summary(limit=limit))
