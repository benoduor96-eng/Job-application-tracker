from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Count
from rest_framework import viewsets, decorators, response, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.jobs.models import JobApplication, Interview
from apps.jobs.services import JobApplicationService
from .serializers import JobApplicationSerializer, DetailedApplicationSerializer, InterviewSerializer


class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        service = JobApplicationService(self.request.user)
        query = self.request.query_params.get("q", "").strip()
        status_filter = self.request.query_params.get("status")
        return service.search(query, status_filter)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedApplicationSerializer
        return JobApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @decorators.action(detail=False, methods=["get"])
    def dashboard(self, request):
        service = JobApplicationService(request.user)
        data = service.dashboard()
        data["upcoming"] = JobApplicationSerializer(
            data["upcoming"], many=True
        ).data
        data["overdue"] = JobApplicationSerializer(
            data["overdue"], many=True
        ).data
        return response.Response(data)

    @decorators.action(detail=False, methods=["get"])
    def health_metrics(self, request):
        service = JobApplicationService(request.user)
        return response.Response(service.pipeline_health())

    @decorators.action(detail=False, methods=["get"])
    def export(self, request):
        service = JobApplicationService(request.user)
        return response.Response(service.export_rows())

    @decorators.action(detail=False, methods=["get"])
    def salary_stats(self, request):
        """Get salary statistics across applications."""
        service = JobApplicationService(request.user)
        return response.Response(service.salary_statistics())

    @decorators.action(detail="pk", methods=["get"])
    def timeline(self, request, pk=None):
        """Get timeline of events for an application."""
        try:
            app = JobApplication.objects.get(id=pk, user=request.user)
            service = JobApplicationService(request.user)
            timeline = service.application_timeline(app)
            return response.Response({"timeline": timeline})
        except JobApplication.DoesNotExist:
            return response.Response(
                {"detail": "Application not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @decorators.action(detail="pk", methods=["get"])
    def interviews_summary(self, request, pk=None):
        """Get interview summary for an application."""
        try:
            app = JobApplication.objects.get(id=pk, user=request.user)
            service = JobApplicationService(request.user)
            summary = service.interviews_summary(app)
            return response.Response(summary)
        except JobApplication.DoesNotExist:
            return response.Response(
                {"detail": "Application not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @decorators.action(detail=False, methods=["get"])
    def active_pipeline(self, request):
        """Get applications in active pipeline stages."""
        service = JobApplicationService(request.user)
        pipeline = service.get_active_pipeline()
        return response.Response(
            JobApplicationSerializer(pipeline, many=True).data
        )


class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Interview.objects.filter(
            application__user=user
        ).select_related('application')

    def perform_create(self, serializer):
        application_id = self.request.data.get('application')
        try:
            app = JobApplication.objects.get(id=application_id, user=self.request.user)
            serializer.save(application=app)
        except JobApplication.DoesNotExist:
            return response.Response(
                {"detail": "Application not found"},
                status=status.HTTP_404_NOT_FOUND
            )


@decorators.api_view(["get"])
def health(request):
    return JsonResponse({"status": "ok", "service": "job-tracker-api"})


@decorators.api_view(["post"])
@decorators.permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email", "")
    if not username or not password:
        return response.Response(
            {"detail": "username and password are required"}, status=400
        )
    if User.objects.filter(username=username).exists():
        return response.Response(
            {"detail": "username already exists"}, status=400
        )
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
    )
    return response.Response(
        {"id": user.id, "username": user.username},
        status=status.HTTP_201_CREATED,
    )
