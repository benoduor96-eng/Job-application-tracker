from django.db.models import Q
from rest_framework import decorators, response, serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.jobs.models import CareerContact
from .contact_serializers import CareerContactSerializer


class CareerContactViewSet(viewsets.ModelViewSet):
    serializer_class = CareerContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = CareerContact.objects.filter(user=self.request.user).select_related("application")
        query = self.request.query_params.get("q", "").strip()
        contact_type = self.request.query_params.get("type")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(company__icontains=query)
                | Q(email__icontains=query)
                | Q(notes__icontains=query)
            )
        if contact_type:
            queryset = queryset.filter(contact_type=contact_type)
        return queryset

    def perform_create(self, serializer):
        application_id = self.request.data.get("application")
        if application_id:
            from apps.jobs.models import JobApplication
            if not JobApplication.objects.filter(id=application_id, user=self.request.user).exists():
                raise serializers.ValidationError({"application": "Application not found."})
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        application_id = self.request.data.get("application")
        if application_id:
            from apps.jobs.models import JobApplication
            if not JobApplication.objects.filter(id=application_id, user=self.request.user).exists():
                raise serializers.ValidationError({"application": "Application not found."})
        serializer.save()

    @decorators.action(detail=False, methods=["get"])
    def follow_ups(self, request):
        contacts = self.get_queryset().filter(next_follow_up__isnull=False).order_by("next_follow_up")
        return response.Response(self.get_serializer(contacts, many=True).data)

    @decorators.action(detail=False, methods=["get"])
    def summary(self, request):
        queryset = self.get_queryset()
        return response.Response({
            "total": queryset.count(),
            "recruiters": queryset.filter(contact_type="recruiter").count(),
            "hiring_managers": queryset.filter(contact_type="hiring_manager").count(),
            "referrals": queryset.filter(contact_type="referral").count(),
            "with_follow_up": queryset.filter(next_follow_up__isnull=False).count(),
        })
