from rest_framework import serializers
from apps.jobs.models import JobApplication, Interview


class JobApplicationSerializer(serializers.ModelSerializer):
    interview_count = serializers.SerializerMethodField()
    
    class Meta:
        model = JobApplication
        exclude = ['user']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_interview_count(self, obj):
        return obj.interviews.count()


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = [
            'id', 'interview_type', 'scheduled_date', 'completed_date',
            'outcome', 'interviewer_name', 'interviewer_title',
            'feedback', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class DetailedApplicationSerializer(serializers.ModelSerializer):
    interviews = InterviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobApplication
        exclude = ['user']
        read_only_fields = ['created_at', 'updated_at']
