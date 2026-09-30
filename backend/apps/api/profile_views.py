from rest_framework import response, status, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.jobs.models import CareerProfile
from .profile_serializers import CareerProfileSerializer


class CareerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CareerProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete", "head", "options"]

    def get_queryset(self):
        return CareerProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if CareerProfile.objects.filter(user=self.request.user).exists():
            raise serializers.ValidationError("A career profile already exists.")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if CareerProfile.objects.filter(user=request.user).exists():
            return response.Response(
                {"detail": "A career profile already exists. Use PATCH or PUT to update it."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)
