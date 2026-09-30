from rest_framework import serializers
from apps.jobs.models import CareerProfile


class CareerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerProfile
        fields = [
            "id", "headline", "professional_summary", "skills",
            "preferred_roles", "preferred_locations", "work_preference",
            "minimum_salary", "target_salary", "salary_currency",
            "years_experience", "portfolio_url", "linkedin_url",
            "github_url", "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]

    def validate_skills(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Skills must be a list.")
        cleaned = [str(item).strip() for item in value if str(item).strip()]
        if len(cleaned) > 100:
            raise serializers.ValidationError("A profile can contain at most 100 skills.")
        return cleaned

    def validate_salary_currency(self, value):
        value = value.strip().upper()
        if len(value) != 3 or not value.isalpha():
            raise serializers.ValidationError("Salary currency must be a 3-letter code.")
        return value

    def validate(self, attrs):
        minimum = attrs.get("minimum_salary", getattr(self.instance, "minimum_salary", None))
        target = attrs.get("target_salary", getattr(self.instance, "target_salary", None))
        if minimum is not None and target is not None and target < minimum:
            raise serializers.ValidationError({"target_salary": "Target salary cannot be below minimum salary."})
        return attrs
