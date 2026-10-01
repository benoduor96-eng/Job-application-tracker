from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.jobs.interview_packet import InterviewPacket
from apps.jobs.models import Interview


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def interview_packet_dashboard(request):
    return Response(InterviewPacket(request.user).dashboard())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def interview_packet(request, interview_id):
    interview = Interview.objects.filter(id=interview_id, application__user=request.user).select_related("application").first()
    if not interview:
        return Response({"detail": "Interview not found."}, status=404)
    packet = InterviewPacket(request.user).packet_for_interview(interview)
    return Response(packet)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def application_interview_packet(request, application_id):
    from apps.jobs.models import JobApplication
    application = JobApplication.objects.filter(id=application_id, user=request.user).first()
    if not application:
        return Response({"detail": "Application not found."}, status=404)
    return Response(InterviewPacket(request.user, application.id).packet_for_application(application))
