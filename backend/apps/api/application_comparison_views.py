from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.jobs.application_comparison import ApplicationComparison


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def application_comparison_summary(request):
    return Response(ApplicationComparison(request.user).summary())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def application_comparison(request):
    left = request.query_params.get("left")
    right = request.query_params.get("right")
    if not left or not right:
        return Response({"detail": "left and right application ids are required."}, status=400)
    result = ApplicationComparison(request.user).compare(left, right)
    if result is None:
        return Response({"detail": "One or both applications were not found."}, status=404)
    return Response(result)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def application_shortlist(request):
    try:
        limit = min(max(int(request.query_params.get("limit", 10)), 1), 50)
    except (TypeError, ValueError):
        limit = 10
    return Response({"applications": ApplicationComparison(request.user).shortlist(limit)})
