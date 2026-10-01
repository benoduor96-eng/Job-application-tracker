from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.jobs.review_workspace import ReviewWorkspace


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def review_workspace(request):
    return Response(ReviewWorkspace(request.user).full_review())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def review_actions(request):
    try:
        limit = min(max(int(request.query_params.get("limit", 30)), 1), 100)
    except (TypeError, ValueError):
        limit = 30
    return Response({"actions": ReviewWorkspace(request.user).action_queue(limit=limit)})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def review_companies(request):
    return Response({"companies": ReviewWorkspace(request.user).company_summary()})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def review_funnel(request):
    return Response(ReviewWorkspace(request.user).funnel())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def review_interviews(request):
    try:
        days = min(max(int(request.query_params.get("days", 30)), 1), 90)
    except (TypeError, ValueError):
        days = 30
    return Response({"interviews": ReviewWorkspace(request.user).interview_calendar(days=days)})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def review_health(request):
    service = ReviewWorkspace(request.user)
    return Response({
        "contact_health": service.contact_health(),
        "task_health": service.task_health(),
        "risk": service.risk_summary(),
    })
