from django.utils import timezone
from rest_framework import decorators, permissions, response, status, viewsets, serializers

from apps.jobs.career_intelligence import (
    CareerDashboardService,
    FollowUpPlanner,
    JobDescriptionAnalyzer,
    JobMatchingEngine,
    PipelinePrioritizer,
    ResumeTargetingService,
)
from apps.jobs.models import CareerProfile, CareerTask, JobApplication, JobDescription
from .career_intelligence_serializers import (
    CareerSummarySerializer,
    CareerTaskSerializer,
    DescriptionPreviewResultSerializer,
    DescriptionPreviewSerializer,
    FollowUpGenerationSerializer,
    JobDescriptionSerializer,
    MatchRequestSerializer,
    ResumeTargetingSerializer,
)


class CareerTaskIntelligenceViewSet(viewsets.ModelViewSet):
    serializer_class = CareerTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CareerTask.objects.filter(user=self.request.user).select_related(
            "application"
        )

    def perform_create(self, serializer):
        application = serializer.validated_data.get("application")
        if application and application.user_id != self.request.user.id:
            raise serializers.ValidationError({"application": "Invalid application."})
        serializer.save(user=self.request.user)

    @decorators.action(detail=False, methods=["get"])
    def overdue(self, request):
        now = timezone.now()
        queryset = self.get_queryset().filter(
            due_date__lt=now,
            status__in=["todo", "in_progress"],
        )
        return response.Response(self.get_serializer(queryset, many=True).data)

    @decorators.action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.status = "done"
        task.completed_at = timezone.now()
        task.save(update_fields=["status", "completed_at", "updated_at"])
        return response.Response(self.get_serializer(task).data)


class JobDescriptionIntelligenceViewSet(viewsets.ModelViewSet):
    serializer_class = JobDescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobDescription.objects.filter(user=self.request.user).select_related(
            "application"
        )

    def perform_create(self, serializer):
        application = serializer.validated_data.get("application")
        if application and application.user_id != self.request.user.id:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"application": "Invalid application."})
        description = serializer.save(user=self.request.user)
        JobDescriptionAnalyzer().analyze(description)
        description.save(update_fields=[
            "required_skills",
            "extracted_keywords",
            "analyzed_at",
            "updated_at",
        ])

    @decorators.action(detail=True, methods=["post"])
    def analyze(self, request, pk=None):
        description = self.get_object()
        JobDescriptionAnalyzer().analyze(description)
        description.save(update_fields=[
            "required_skills",
            "extracted_keywords",
            "analyzed_at",
            "updated_at",
        ])
        return response.Response(self.get_serializer(description).data)

    @decorators.action(detail=False, methods=["post"])
    def preview(self, request):
        serializer = DescriptionPreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = JobDescriptionAnalyzer().preview(serializer.validated_data["raw_text"])
        return response.Response(DescriptionPreviewResultSerializer(result).data)

    @decorators.action(detail=True, methods=["get"])
    def match(self, request, pk=None):
        description = self.get_object()
        profile = CareerProfile.objects.filter(user=request.user).first()
        result = JobMatchingEngine(profile).score_description(description)
        return response.Response({
            "description_id": description.id,
            "score": result.score,
            "required_score": result.required_score,
            "preferred_score": result.preferred_score,
            "profile_score": result.profile_score,
            "salary_score": result.salary_score,
            "location_score": result.location_score,
            "matched_required": list(result.matched_required),
            "missing_required": list(result.missing_required),
            "matched_preferred": list(result.matched_preferred),
            "recommendations": list(result.recommendations),
        })

    @decorators.action(detail=True, methods=["get"])
    def resume_targeting(self, request, pk=None):
        description = self.get_object()
        profile = CareerProfile.objects.filter(user=request.user).first()
        if not profile:
            return response.Response(
                {"detail": "Create a career profile before targeting a resume."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        service = ResumeTargetingService(profile)
        payload = {
            "description_id": description.id,
            "matched_keywords": service.target_keywords(description),
            "missing_keywords": service.missing_keywords(description),
            "notes": service.tailoring_notes(description),
        }
        return response.Response(ResumeTargetingSerializer(payload).data)


@decorators.api_view(["post"])
@decorators.permission_classes([permissions.IsAuthenticated])
def skill_match_advanced(request):
    serializer = MatchRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    profile = CareerProfile.objects.filter(user=request.user).first()
    values = serializer.validated_data
    application = None
    if values.get("application_id"):
        application = JobApplication.objects.filter(
            id=values["application_id"], user=request.user
        ).first()
        if not application:
            return response.Response(
                {"detail": "Application not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
    role = values.get("role", "") or (application.role if application else "")
    location = values.get("location", "") or (application.location if application else "")
    result = JobMatchingEngine(profile).score(
        values.get("required_skills", []),
        values.get("preferred_skills", []),
        role=role,
        location=location,
        salary_min=values.get("salary_min"),
        salary_max=values.get("salary_max"),
    )
    return response.Response({
        "score": result.score,
        "required_score": result.required_score,
        "preferred_score": result.preferred_score,
        "profile_score": result.profile_score,
        "salary_score": result.salary_score,
        "location_score": result.location_score,
        "matched_required": list(result.matched_required),
        "missing_required": list(result.missing_required),
        "matched_preferred": list(result.matched_preferred),
        "recommendations": list(result.recommendations),
    })


@decorators.api_view(["get"])
@decorators.permission_classes([permissions.IsAuthenticated])
def career_summary(request):
    payload = CareerDashboardService(request.user).summary()
    return response.Response(CareerSummarySerializer(payload).data)


@decorators.api_view(["get"])
@decorators.permission_classes([permissions.IsAuthenticated])
def pipeline_priority(request):
    applications = JobApplication.objects.filter(user=request.user).prefetch_related(
        "interviews"
    )
    scores = PipelinePrioritizer().prioritize(applications)
    return response.Response({
        "items": [
            {
                "application_id": item.application_id,
                "score": item.score,
                "urgency": item.urgency,
                "reasons": list(item.reasons),
            }
            for item in scores
        ]
    })


@decorators.api_view(["post"])
@decorators.permission_classes([permissions.IsAuthenticated])
def generate_follow_ups(request):
    serializer = FollowUpGenerationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    ids = serializer.validated_data.get("application_ids", [])
    queryset = JobApplication.objects.filter(user=request.user)
    if ids:
        queryset = queryset.filter(id__in=ids)
    plans = [
        plan for plan in (
            FollowUpPlanner().plan_for(application)
            for application in queryset
        ) if plan
    ]
    created = 0
    if serializer.validated_data.get("create"):
        tasks = FollowUpPlanner().create_tasks(queryset)
        if tasks:
            CareerTask.objects.bulk_create(tasks)
            created = len(tasks)
    return response.Response({
        "created": created,
        "plans": [
            {
                "application_id": plan.application_id,
                "action": plan.action,
                "due_date": plan.due_date.isoformat(),
                "priority": plan.priority,
                "reason": plan.reason,
            }
            for plan in plans
        ],
    })
