from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import JobApplicationViewSet, InterviewViewSet, health, register
from .contact_views import CareerContactViewSet

router = DefaultRouter()
router.register(r'applications', JobApplicationViewSet, basename='application')
router.register(r'interviews', InterviewViewSet, basename='interview')
router.register(r'contacts', CareerContactViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health, name='health'),
    path('auth/register/', register, name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
