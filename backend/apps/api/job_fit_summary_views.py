"""Batch application-fit insights for the authenticated user's pipeline."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.jobs.models import JobApplication
from apps.jobs.job_fit import JobFitAnalyzer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def application_fit_summary(request):
    limit = min(max(int(request.query_params.get("limit", 25)), 1), 100)
    minimum = min(max(int(request.query_params.get("min_score", 0)), 0), 100)
    applications = JobApplication.objects.filter(user=request.user).order_by("-updated_at", "-id")[:limit]
    analyzer = JobFitAnalyzer(request.user)
    items = []
    for application in applications:
        result = analyzer.analyze(application).to_dict()
        if result["score"] >= minimum:
            items.append({
                "application_id": application.id,
                "role": application.role,
                "company": application.company,
                "status": application.status,
                **result,
            })
    items.sort(key=lambda item: (-item["score"], item["company"].lower(), item["role"].lower()))
    scores = [item["score"] for item in items]
    return Response({
        "count": len(items),
        "average_score": round(sum(scores) / len(scores), 1) if scores else 0,
        "strong_matches": sum(score >= 80 for score in scores),
        "needs_review": sum(score < 60 for score in scores),
        "applications": items,
    })
