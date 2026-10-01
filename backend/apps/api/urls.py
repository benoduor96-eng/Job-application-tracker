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
from .planning_views import planning_summary, planning_queue, planning_quality, planning_capacity
from .job_fit_views import application_fit
from .job_fit_summary_views import application_fit_summary
from .fit_trend_views import fit_trends
from .review_views import review_workspace, review_actions, review_companies, review_funnel, review_interviews, review_health
from .search_insight_views import search_insights, search_insight_summary, search_role_clusters, search_location_clusters
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
    path('search-insights/', search_insights, name='search-insights'),
    path('search-insights/summary/', search_insight_summary, name='search-insights-summary'),
    path('search-insights/roles/', search_role_clusters, name='search-insights-roles'),
    path('search-insights/locations/', search_location_clusters, name='search-insights-locations'),
    path('review/workspace/', review_workspace, name='review-workspace'),
    path('review/actions/', review_actions, name='review-actions'),
    path('review/companies/', review_companies, name='review-companies'),
    path('review/funnel/', review_funnel, name='review-funnel'),
    path('review/interviews/', review_interviews, name='review-interviews'),
    path('review/health/', review_health, name='review-health'),
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
    path('planning/summary/', planning_summary, name='planning-summary'),
    path('planning/queue/', planning_queue, name='planning-queue'),
    path('planning/quality/', planning_quality, name='planning-quality'),
    path('planning/capacity/', planning_capacity, name='planning-capacity'),
    path('applications/<int:application_id>/fit/', application_fit, name='application-fit'),
    path('applications/fit-summary/', application_fit_summary, name='application-fit-summary'),
    path('applications/interview-readiness/', interview_readiness_summary, name='interview-readiness-summary'),
    path('applications/health/', application_health_summary, name='application-health-summary'),
    path('applications/compensation/', compensation_summary, name='compensation-summary'),
    path('applications/<int:application_id>/compensation/', compensation_analysis, name='compensation-analysis'),
    path('applications/<int:application_id>/health/', application_health, name='application-health'),
    path('applications/<int:application_id>/interview-readiness/', interview_readiness, name='interview-readiness'),
    path('applications/fit-trends/', fit_trends, name='application-fit-trends'),
    path('auth/register/', register, name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
