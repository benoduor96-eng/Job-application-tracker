from rest_framework import serializers

from apps.jobs.models import CareerTask, JobDescription
from apps.jobs.career_intelligence import extract_keywords, extract_skills


class JobDescriptionAnalysisSerializer(serializers.Serializer):
    raw_text = serializers.CharField()
    required_skills = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )
    preferred_skills = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )


class MatchRequestSerializer(serializers.Serializer):
    application_id = serializers.IntegerField(required=False)
    required_skills = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )
    preferred_skills = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )
    role = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    salary_min = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False, allow_null=True
    )
    salary_max = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False, allow_null=True
    )


class CareerTaskSerializer(serializers.ModelSerializer):
    application_company = serializers.CharField(
        source="application.company", read_only=True
    )
    application_role = serializers.CharField(
        source="application.role", read_only=True
    )

    class Meta:
        model = CareerTask
        exclude = ["user"]
        read_only_fields = ["created_at", "updated_at", "completed_at"]


class JobDescriptionSerializer(serializers.ModelSerializer):
    skill_count = serializers.SerializerMethodField()
    keyword_count = serializers.SerializerMethodField()

    class Meta:
        model = JobDescription
        exclude = ["user"]
        read_only_fields = [
            "extracted_keywords",
            "analyzed_at",
            "created_at",
            "updated_at",
        ]

    def get_skill_count(self, obj):
        return len(obj.required_skills or []) + len(obj.preferred_skills or [])

    def get_keyword_count(self, obj):
        return len(obj.extracted_keywords or [])


class DescriptionPreviewSerializer(serializers.Serializer):
    raw_text = serializers.CharField(min_length=20)

    def validate_raw_text(self, value):
        return value.strip()


class DescriptionPreviewResultSerializer(serializers.Serializer):
    skills = serializers.ListField(child=serializers.CharField())
    keywords = serializers.ListField(child=serializers.CharField())
    skill_count = serializers.IntegerField()
    keyword_count = serializers.IntegerField()


class ResumeTargetingSerializer(serializers.Serializer):
    description_id = serializers.IntegerField()
    matched_keywords = serializers.ListField(child=serializers.CharField())
    missing_keywords = serializers.ListField(child=serializers.CharField())
    notes = serializers.ListField(child=serializers.CharField())


class FollowUpGenerationSerializer(serializers.Serializer):
    application_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_empty=True
    )
    create = serializers.BooleanField(default=False)


class PriorityItemSerializer(serializers.Serializer):
    application_id = serializers.IntegerField()
    score = serializers.FloatField()
    urgency = serializers.CharField()
    reasons = serializers.ListField(child=serializers.CharField())


class CareerSummarySerializer(serializers.Serializer):
    total_applications = serializers.IntegerField()
    active_applications = serializers.IntegerField()
    priority_items = PriorityItemSerializer(many=True)
    status_counts = serializers.DictField(child=serializers.IntegerField())
