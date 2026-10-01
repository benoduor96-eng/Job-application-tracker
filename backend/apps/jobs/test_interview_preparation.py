import pytest
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.jobs.models import JobApplication, Interview, JobDescription
from apps.jobs.interview_preparation import InterviewPreparationService

@pytest.mark.django_db
def test_interview_preparation_builds_type_checklist():
    user=get_user_model().objects.create_user(username="prep-user",password="pass")
    app=JobApplication.objects.create(user=user,company="PrepCo",role="Engineer",status="interview")
    interview=Interview.objects.create(application=app,interview_type="technical",
        outcome="scheduled",scheduled_date=timezone.now()+timedelta(days=3))
    data=InterviewPreparationService(user).dashboard()
    assert data["stats"]["upcoming"]==1
    assert "core technical skills" in data["upcoming"][0]["checklist"]

@pytest.mark.django_db
def test_interview_preparation_includes_description_skills():
    user=get_user_model().objects.create_user(username="prep-user2",password="pass")
    app=JobApplication.objects.create(user=user,company="PrepCo",role="Engineer",status="interview")
    Interview.objects.create(application=app,interview_type="behavioral",outcome="scheduled",
        scheduled_date=timezone.now()+timedelta(days=2))
    JobDescription.objects.create(user=user,application=app,title="Engineer",company="PrepCo",
        raw_text="Python",required_skills=["Python","Django"])
    rows=InterviewPreparationService(user).upcoming()
    assert any("review required skills" in item for item in rows[0]["checklist"])

@pytest.mark.django_db
def test_interview_preparation_is_user_scoped():
    user=get_user_model().objects.create_user(username="prep-user3",password="pass")
    other=get_user_model().objects.create_user(username="prep-other",password="pass")
    app=JobApplication.objects.create(user=other,company="OtherCo",role="Engineer",status="interview")
    Interview.objects.create(application=app,outcome="scheduled",scheduled_date=timezone.now()+timedelta(days=1))
    assert InterviewPreparationService(user).dashboard()["stats"]["upcoming"]==0
