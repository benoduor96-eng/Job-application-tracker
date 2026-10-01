from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.jobs.dashboard_snapshot import DashboardSnapshot


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_snapshot(request):
    return Response(DashboardSnapshot(request.user).dashboard())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_focus(request):
    return Response({"focus": DashboardSnapshot(request.user).focus_items()})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_companies(request):
    try:
        limit = min(max(int(request.query_params.get("limit", 10)), 1), 50)
    except (TypeError, ValueError):
        limit = 10
    return Response({"companies": DashboardSnapshot(request.user).company_leaderboard(limit=limit)})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_activity(request):
    try:
        days = min(max(int(request.query_params.get("days", 30)), 1), 90)
    except (TypeError, ValueError):
        days = 30
    return Response(DashboardSnapshot(request.user).activity_window(days=days))
