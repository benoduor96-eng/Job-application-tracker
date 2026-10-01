from rest_framework import serializers


class ReportingInsightsSerializer(serializers.Serializer):
    total_applications = serializers.IntegerField()
    active_applications = serializers.IntegerField()
    interviews = serializers.IntegerField()
    offers = serializers.IntegerField()
    rejected = serializers.IntegerField()
    saved = serializers.IntegerField()
    applied = serializers.IntegerField()
    screening = serializers.IntegerField()
    overdue_tasks = serializers.IntegerField()
    upcoming_tasks = serializers.IntegerField()
    conversion_rate = serializers.FloatField()
    by_status = serializers.ListField()
