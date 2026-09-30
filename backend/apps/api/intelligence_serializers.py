from rest_framework import serializers
from apps.jobs.models import JobDescription


class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        exclude = ["user"]
        read_only_fields = ["extracted_keywords", "analyzed_at", "created_at", "updated_at"]

    def validate_required_skills(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("required_skills must be a list.")
        return [str(item).strip() for item in value if str(item).strip()]

    def validate_preferred_skills(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("preferred_skills must be a list.")
        return [str(item).strip() for item in value if str(item).strip()]
