"""Pipeline board API endpoints."""
from django.utils import timezone
from rest_framework import decorators, permissions, response
from apps.jobs.models import JobApplication
from apps.jobs.pipeline_board import build_board, parse_move_request
from apps.jobs.pipeline_moves import move_applications

@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def pipeline_board(request):
    try:
        stale_days = int(request.query_params.get("stale_days", 14))
    except ValueError:
        return response.Response({"detail": "stale_days must be an integer."}, status=400)
    if stale_days < 1:
        return response.Response({"detail": "stale_days must be at least 1."}, status=400)
    board = build_board(
        JobApplication.objects.filter(user=request.user),
        today=timezone.localdate(), stale_days=stale_days,
        query=request.query_params.get("q", ""),
    )
    return response.Response(board)

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.IsAuthenticated])
def pipeline_move(request):
    try:
        ids, target = parse_move_request(request.data)
    except ValueError as exc:
        return response.Response({"detail": str(exc)}, status=400)
    return response.Response(move_applications(request.user, ids, target))
