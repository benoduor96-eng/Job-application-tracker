from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.analytics import application_funnel, company_breakdown, response_metrics, salary_metrics, stale_applications
from apps.jobs.models import JobApplication


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def analytics_summary(request):
    queryset = JobApplication.objects.filter(user=request.user)
    return Response({
        "funnel": application_funnel(queryset),
        "responses": response_metrics(queryset),
        "salary": salary_metrics(queryset),
        "companies": company_breakdown(queryset),
        "stale_application_count": stale_applications(queryset).count(),
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def stale_application_list(request):
    days = int(request.query_params.get("days", 14))
    queryset = stale_applications(JobApplication.objects.filter(user=request.user), max(1, min(days, 365)))
    return Response([
        {"id": item.id, "company": item.company, "role": item.role, "status": item.status, "updated_at": item.updated_at}
        for item in queryset
    ])
