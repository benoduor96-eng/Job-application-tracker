from rest_framework import serializers

from apps.jobs.models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        exclude = ["user"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_company(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Company name is too short.")
        return value

    def validate_role(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Role name is too short.")
        return value

    def validate(self, attrs):
        minimum = attrs.get("salary_min")
        maximum = attrs.get("salary_max")
        if minimum is not None and maximum is not None and minimum > maximum:
            raise serializers.ValidationError(
                {"salary_max": "Maximum salary must be greater than minimum salary."}
            )
        next_date = attrs.get("next_action_date")
        if next_date and attrs.get("status") in {"rejected", "withdrawn"}:
            raise serializers.ValidationError(
                {"next_action_date": "Closed applications cannot have a next action date."}
            )
        return attrs
