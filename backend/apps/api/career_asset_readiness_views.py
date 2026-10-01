from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.jobs.career_asset_readiness import CareerAssetReadiness


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def career_asset_readiness(request):
    return Response(CareerAssetReadiness(request.user).dashboard())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def career_asset_recommendations(request):
    return Response({"recommendations": CareerAssetReadiness(request.user).recommendations()})
