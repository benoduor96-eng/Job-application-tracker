from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.contact_intelligence import ContactIntelligenceService


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def contact_intelligence(request):
    return Response(ContactIntelligenceService(request.user).summary())
