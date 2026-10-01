"""Tests for application-fit trend analytics."""
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from apps.jobs.models import CareerProfile, JobApplication, JobDescription
from apps.jobs.fit_trends import FitTrendService

@pytest.mark.django_db
def test_fit_trend_summary_groups_status_and_gaps():
    user = User.objects.create_user(username="trend-user", password="pass")
    CareerProfile.objects.create(user=user, skills=["python"], preferred_roles=["Engineer"], minimum_salary=Decimal("1000"))
    first = JobApplication.objects.create(user=user, company="A", role="Engineer", status="applied", salary_max=Decimal("2000"))
    second = JobApplication.objects.create(user=user, company="B", role="Engineer", status="screening", salary_max=Decimal("2000"))
    JobDescription.objects.create(user=user, application=first, title="Engineer", company="A", raw_text="x", required_skills=["Python","Django"])
    JobDescription.objects.create(user=user, application=second, title="Engineer", company="B", raw_text="x", required_skills=["Python"])
    result = FitTrendService(user).summary()
    assert result["count"] == 2
    assert result["average_score"] > 0
    assert "applied" in result["by_status"]
    assert result["common_skill_gaps"][0]["skill"] == "django"

@pytest.mark.django_db
def test_fit_trend_is_user_scoped():
    user = User.objects.create_user(username="owner", password="pass")
    other = User.objects.create_user(username="other", password="pass")
    JobApplication.objects.create(user=other, company="Private", role="Engineer")
    assert FitTrendService(user).summary()["count"] == 0
