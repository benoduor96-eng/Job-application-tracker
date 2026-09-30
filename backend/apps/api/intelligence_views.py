from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.models import ApplicationActivity, JobDescription
from .intelligence import extract_keywords, match_skills


class JobDescriptionViewSet(viewsets.ModelViewSet):
    from .intelligence_serializers import JobDescriptionSerializer
    serializer_class = JobDescriptionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = JobDescription.objects.filter(user=self.request.user)
        company = self.request.query_params.get("company")
        if company:
            queryset = queryset.filter(company__icontains=company)
        return queryset

    def list(self, request, *args, **kwargs):
        rows = self.get_queryset()
        return Response([
            {
                "id": item.id,
                "title": item.title,
                "company": item.company,
                "source": item.source,
                "source_url": item.source_url,
                "updated_at": item.updated_at,
            }
            for item in rows
        ])

    @action(detail=False, methods=["post"])
    def analyze(self, request):
        text = str(request.data.get("raw_text", "")).strip()
        if not text:
            return Response({"detail": "raw_text is required."}, status=status.HTTP_400_BAD_REQUEST)
        keywords = extract_keywords(text)
        return Response({"keywords": keywords, "keyword_count": len(keywords)})

    @action(detail=True, methods=["post"])
    def analyze_saved(self, request, pk=None):
        item = self.get_queryset().get(pk=pk)
        item.extracted_keywords = extract_keywords(item.raw_text)
        item.analyzed_at = timezone.now()
        item.save(update_fields=["extracted_keywords", "analyzed_at", "updated_at"])
        return Response({"id": item.id, "keywords": item.extracted_keywords, "analyzed_at": item.analyzed_at})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def skill_match(request):
    result = match_skills(
        request.data.get("candidate_skills", []),
        request.data.get("required_skills", []),
        request.data.get("preferred_skills", []),
    )
    return Response(result)


class ApplicationActivityViewSet(viewsets.ModelViewSet):
    from .activity_serializers import ApplicationActivitySerializer
    serializer_class = ApplicationActivitySerializer

    def get_queryset(self):
        return ApplicationActivity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        application = serializer.validated_data["application"]
        if application.user_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You cannot add activity to another user's application.")
        serializer.save(user=self.request.user)
