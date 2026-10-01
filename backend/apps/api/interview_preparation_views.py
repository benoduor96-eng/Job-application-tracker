from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.jobs.interview_preparation import InterviewPreparationService

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def interview_preparation(request):
    try: days=int(request.query_params.get("days",45))
    except (TypeError,ValueError): return Response({"detail":"days must be an integer."},status=400)
    if not 1<=days<=180: return Response({"detail":"days must be between 1 and 180."},status=400)
    service=InterviewPreparationService(request.user)
    return Response(service.dashboard())
