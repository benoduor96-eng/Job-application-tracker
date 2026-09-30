from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import JobApplicationViewSet, InterviewViewSet, health, register
from .contact_views import CareerContactViewSet
from .profile_views import CareerProfileViewSet
from .career_asset_views import ResumeViewSet, CareerTaskViewSet
from .intelligence_views import ApplicationActivityViewSet, JobDescriptionViewSet, skill_match
from .analytics_views import analytics_summary, stale_application_list
from .import_export import export_applications, import_applications

router = DefaultRouter()
router.register(r'applications', JobApplicationViewSet, basename='application')
router.register(r'interviews', InterviewViewSet, basename='interview')
router.register(r'contacts', CareerContactViewSet, basename='contact')
router.register(r'profile', CareerProfileViewSet, basename='career-profile')
router.register(r'resumes', ResumeViewSet, basename='resume')
router.register(r'tasks', CareerTaskViewSet, basename='career-task')
router.register(r'job-descriptions', JobDescriptionViewSet, basename='job-description')
router.register(r'activities', ApplicationActivityViewSet, basename='application-activity')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health, name='health'),
    path('intelligence/skill-match/', skill_match, name='skill-match'),
    path('analytics/summary/', analytics_summary, name='analytics-summary'),
    path('analytics/stale/', stale_application_list, name='analytics-stale'),
    path('applications/export/', export_applications, name='applications-export'),
    path('applications/import/', import_applications, name='applications-import'),
    path('auth/register/', register, name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
