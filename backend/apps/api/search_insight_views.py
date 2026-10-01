from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.jobs.search_insights import SearchInsights


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_insights(request):
    return Response(SearchInsights(request.user).dashboard())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_insight_summary(request):
    return Response({
        "coverage": SearchInsights(request.user).coverage(),
        "recommendations": SearchInsights(request.user).recommendations(),
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_role_clusters(request):
    return Response({"clusters": SearchInsights(request.user).role_clusters()})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_location_clusters(request):
    return Response({"clusters": SearchInsights(request.user).location_clusters()})
