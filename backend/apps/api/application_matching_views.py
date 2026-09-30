from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.jobs.application_matching import find_possible_duplicates
from apps.jobs.models import JobApplication


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def possible_duplicates(request, application_id):
    try:
        application = JobApplication.objects.get(
            id=application_id,
            user=request.user,
        )
    except JobApplication.DoesNotExist:
        return Response({"detail": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

    threshold_raw = request.query_params.get("threshold", "0.45")
    try:
        threshold = min(max(float(threshold_raw), 0.0), 1.0)
    except ValueError:
        return Response({"detail": "threshold must be a number between 0 and 1"}, status=400)

    candidates = JobApplication.objects.filter(user=request.user).only(
        "id", "company", "role", "job_url"
    )
    matches = find_possible_duplicates(application, candidates, threshold)
    return Response({
        "application_id": application.id,
        "threshold": threshold,
        "matches": [
            {
                "application_id": item.application_id,
                "company": item.company,
                "role": item.role,
                "score": item.score,
                "reasons": list(item.reasons),
            }
            for item in matches
        ],
    })
