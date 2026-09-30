from rest_framework import serializers
from apps.jobs.models import CareerTask, Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        exclude = ["user"]
        read_only_fields = ["created_at", "updated_at"]

    def validate_skills(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Skills must be a list.")
        if any(not isinstance(item, str) or not item.strip() for item in value):
            raise serializers.ValidationError("Skills must contain non-empty strings.")
        return [item.strip() for item in value]


class CareerTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerTask
        exclude = ["user"]
        read_only_fields = ["created_at", "updated_at", "completed_at"]

    def validate_tags(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Tags must be a list.")
        return [str(item).strip() for item in value if str(item).strip()]
