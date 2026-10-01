from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.reporting import ReportingService
from apps.api.serializers_reporting import ReportingOverviewSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reporting_dashboard(request):
    service = ReportingService(request.user)
    data = service.dashboard_summary()
    serializer = ReportingOverviewSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data)
