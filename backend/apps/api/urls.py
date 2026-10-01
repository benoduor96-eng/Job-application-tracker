from apps.api.reporting_views import reporting_dashboard, stale_applications, interview_preparation, follow_up_sequence
from apps.api.views_reporting_insights import reporting_insights, recommendation_insights, pipeline_health_insights
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import JobApplicationViewSet, InterviewViewSet, health, register
from .application_matching_views import possible_duplicates
from .notification_views import notification_plan
from .contact_views import CareerContactViewSet
from .profile_views import CareerProfileViewSet
from .career_asset_views import ResumeViewSet, CareerTaskViewSet
from .intelligence_views import ApplicationActivityViewSet, JobDescriptionViewSet, skill_match
from .analytics_views import analytics_summary, stale_application_list
from .import_export import export_applications, import_applications
from .pipeline_views import pipeline_board, pipeline_move
from .calendar_views import calendar_export
from .career_intelligence_views import (
    CareerTaskIntelligenceViewSet, JobDescriptionIntelligenceViewSet,
    skill_match_advanced, career_summary, pipeline_priority,
    generate_follow_ups, generate_cover_letter,
)

router = DefaultRouter()
router.register(r'applications', JobApplicationViewSet, basename='application')
router.register(r'interviews', InterviewViewSet, basename='interview')
router.register(r'contacts', CareerContactViewSet, basename='contact')
router.register(r'profile', CareerProfileViewSet, basename='career-profile')
router.register(r'resumes', ResumeViewSet, basename='resume')
router.register(r'tasks', CareerTaskViewSet, basename='career-task')
router.register(r'job-descriptions', JobDescriptionViewSet, basename='job-description')
router.register(r'activities', ApplicationActivityViewSet, basename='application-activity')
router.register(r'intelligence/tasks', CareerTaskIntelligenceViewSet, basename='intelligence-task')
router.register(r'intelligence/descriptions', JobDescriptionIntelligenceViewSet, basename='intelligence-description')

urlpatterns = [
    path('applications/import/', import_applications, name='applications-import'),
    path('applications/export/', export_applications, name='applications-export'),
    path('', include(router.urls)),
    path('health/', health, name='health'),
    path('intelligence/skill-match/', skill_match, name='skill-match'),
    path('analytics/summary/', analytics_summary, name='analytics-summary'),
    path('analytics/stale/', stale_application_list, name='analytics-stale'),
    path('applications/export/', export_applications, name='applications-export'),
    path('applications/<int:application_id>/possible-duplicates/', possible_duplicates, name='possible-duplicates'),
    path('notifications/plan/', notification_plan, name='notification-plan'),
    path('applications/import/', import_applications, name='applications-import'),
    path('intelligence/skill-match/advanced/', skill_match_advanced, name='skill-match-advanced'),
    path('intelligence/summary/', career_summary, name='career-summary'),
    path('intelligence/pipeline-priority/', pipeline_priority, name='pipeline-priority'),
    path('intelligence/follow-ups/', generate_follow_ups, name='generate-follow-ups'),
    path('intelligence/cover-letter/', generate_cover_letter, name='generate-cover-letter'),
    path('reports/insights/', reporting_insights, name='reports-insights'),
    path('reports/recommendations/', recommendation_insights, name='reports-recommendations'),
    path('reports/health/', pipeline_health_insights, name='reports-health'),
    path('reports/dashboard/', reporting_dashboard, name='reports-dashboard'),
    path('reports/stale/', stale_applications, name='reports-stale'),
    path('applications/<int:application_id>/interview-preparation/', interview_preparation, name='interview-preparation'),
    path('applications/<int:application_id>/follow-up-sequence/', follow_up_sequence, name='follow-up-sequence'),
    path('pipeline/board/', pipeline_board, name='pipeline-board'),
    path('pipeline/move/', pipeline_move, name='pipeline-move'),
    path('calendar/export/', calendar_export, name='calendar-export'),
    path('auth/register/', register, name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
