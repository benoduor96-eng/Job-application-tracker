"""API endpoint for deterministic application fit analysis."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.jobs.models import JobApplication
from apps.jobs.job_fit import JobFitAnalyzer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def application_fit(request, application_id):
    try:
        application = JobApplication.objects.get(id=application_id, user=request.user)
    except JobApplication.DoesNotExist:
        return Response({"detail": "Application not found."}, status=404)
    return Response(JobFitAnalyzer(request.user).analyze(application).to_dict())
