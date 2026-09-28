from rest_framework import serializers
from apps.jobs.models import JobApplication
class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model=JobApplication
        exclude=['user']