from rest_framework import serializers
from apps.jobs.models import CareerContact


class CareerContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerContact
        fields = [
            "id", "application", "name", "company", "contact_type",
            "email", "phone", "profile_url", "notes",
            "last_contacted_at", "next_follow_up", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Contact name must contain at least 2 characters.")
        return value
