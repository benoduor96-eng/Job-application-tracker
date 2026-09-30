from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.jobs.models import CareerTask, Resume
from .career_asset_serializers import CareerTaskSerializer, ResumeSerializer


class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer

    def get_queryset(self):
        queryset = Resume.objects.filter(user=self.request.user)
        status_filter = self.request.query_params.get("status")
        target_role = self.request.query_params.get("target_role")
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if target_role:
            queryset = queryset.filter(target_role__icontains=target_role)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def active(self, request):
        resume = self.get_queryset().filter(status="active").first()
        if not resume:
            return Response({"detail": "No active resume."}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(resume).data)


class CareerTaskViewSet(viewsets.ModelViewSet):
    serializer_class = CareerTaskSerializer

    def get_queryset(self):
        queryset = CareerTask.objects.filter(user=self.request.user)
        task_status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")
        application = self.request.query_params.get("application")
        if task_status:
            queryset = queryset.filter(status=task_status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if application:
            queryset = queryset.filter(application_id=application)
        return queryset

    def perform_create(self, serializer):
        application = serializer.validated_data.get("application")
        if application and application.user_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You cannot attach a task to another user's application.")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        application = serializer.validated_data.get("application", serializer.instance.application)
        if application and application.user_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You cannot attach a task to another user's application.")
        serializer.save()

    @action(detail=False, methods=["get"])
    def overdue(self, request):
        now = timezone.now()
        tasks = self.get_queryset().filter(
            due_date__lt=now,
        ).exclude(status__in=["done", "cancelled"])
        return Response(self.get_serializer(tasks, many=True).data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.status = "done"
        task.completed_at = timezone.now()
        task.save(update_fields=["status", "completed_at", "updated_at"])
        return Response(self.get_serializer(task).data)
