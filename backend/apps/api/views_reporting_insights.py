from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.health_metrics import HealthMetricsService
from apps.jobs.recommendations import RecommendationEngine
from apps.jobs.reporting import ReportingService
from .serializers_reporting_insights import ReportingInsightsSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reporting_insights(request):
    data = ReportingService(request.user).dashboard_summary()
    serializer = ReportingInsightsSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recommendation_insights(request):
    return Response({"actions": RecommendationEngine(request.user).rank_actions()})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pipeline_health_insights(request):
    return Response(HealthMetricsService(request.user).health_score())
