from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.jobs.task_analytics import TaskAnalytics


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def task_analytics(request):
    return Response(TaskAnalytics(request.user).dashboard())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def task_analytics_summary(request):
    return Response(TaskAnalytics(request.user).summary())
