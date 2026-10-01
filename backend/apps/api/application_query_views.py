from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.jobs.application_query import ApplicationQueryService


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def application_explorer(request):
    statuses = request.query_params.getlist("status")
    companies = request.query_params.getlist("company")
    locations = request.query_params.getlist("location")
    service = ApplicationQueryService(request.user)
    data = service.explorer(
        query=request.query_params.get("q", ""),
        statuses=statuses,
        companies=companies,
        locations=locations,
        role_keyword=request.query_params.get("role", ""),
        active_only=request.query_params.get("active") == "true",
        has_salary=request.query_params.get("salary") == "true",
        has_follow_up=request.query_params.get("follow_up") == "true",
        sort=request.query_params.get("sort", "updated"),
    )
    return Response(data)
