from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.jobs.company_intelligence import CompanyIntelligenceService

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def company_intelligence(request):
    service=CompanyIntelligenceService(request.user)
    company=(request.query_params.get("company") or "").strip()
    if company:
        result=service.company_detail(company)
        return Response(result or {"detail":"Company not found."},status=200 if result else 404)
    try: limit=int(request.query_params.get("limit",50))
    except (TypeError,ValueError): return Response({"detail":"limit must be an integer."},status=400)
    if not 1<=limit<=200: return Response({"detail":"limit must be between 1 and 200."},status=400)
    return Response(service.dashboard(limit))
