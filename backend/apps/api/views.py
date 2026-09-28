from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Count
from rest_framework import viewsets, decorators, response, status
from rest_framework.permissions import AllowAny

from apps.jobs.models import JobApplication
from apps.jobs.services import JobApplicationService
from .serializers import JobApplicationSerializer


class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer

    def get_queryset(self):
        service = JobApplicationService(self.request.user)
        query = self.request.query_params.get("q", "").strip()
        status_filter = self.request.query_params.get("status")
        return service.search(query, status_filter)

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
        return response.Response(JobApplicationService(request.user).pipeline_health())

    @decorators.action(detail=False, methods=["get"])
    def export(self, request):
        return response.Response(JobApplicationService(request.user).export_rows())


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
