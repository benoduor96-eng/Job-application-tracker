import pytest
from django.contrib.auth import get_user_model

from apps.jobs.interview_prep import interview_readiness, questions_for_application
from apps.jobs.models import Interview, JobApplication


User = get_user_model()


@pytest.mark.django_db
def test_engineer_questions_include_backend_topics():
    user = User.objects.create_user(username="prep", password="password")
    application = JobApplication.objects.create(
        user=user, company="Example", role="Backend Engineer"
    )
    questions = questions_for_application(application)
    assert any("database query" in item.question for item in questions)
    assert any(item.category == "technical" for item in questions)


@pytest.mark.django_db
def test_ai_role_questions_include_data_quality_topics():
    user = User.objects.create_user(username="ai-prep", password="password")
    application = JobApplication.objects.create(
        user=user, company="Example", role="AI Data Specialist"
    )
    questions = questions_for_application(application)
    assert any("dataset" in item.question for item in questions)


@pytest.mark.django_db
def test_readiness_recommends_interviewer_details():
    user = User.objects.create_user(username="ready", password="password")
    application = JobApplication.objects.create(
        user=user, company="Example", role="Engineer"
    )
    Interview.objects.create(application=application, interview_type="technical")
    result = interview_readiness(application)
    assert result["interview_count"] == 1
    assert result["has_interviewer"] is False
    assert any("interviewer" in item.lower() for item in result["recommended_actions"])
