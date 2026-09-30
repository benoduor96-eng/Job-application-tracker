from rest_framework import serializers
from apps.jobs.models import ApplicationActivity


class ApplicationActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationActivity
        exclude = ["user"]
        read_only_fields = ["created_at"]
