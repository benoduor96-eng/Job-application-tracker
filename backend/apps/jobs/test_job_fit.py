"""Tests for deterministic job fit analysis."""
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from apps.jobs.models import CareerProfile, JobApplication, JobDescription
from apps.jobs.job_fit import JobFitAnalyzer

@pytest.fixture
def user(db): return User.objects.create_user(username="fit-user",password="pass")

@pytest.fixture
def application(user):
    return JobApplication.objects.create(user=user,company="Acme",role="Backend Engineer",location="Nairobi",salary_min=Decimal("1500"),salary_max=Decimal("2500"))

def test_fit_matches_required_preferred_and_role(user,application):
    CareerProfile.objects.create(user=user,skills=["Python","Django"],preferred_roles=["Backend Engineer"],preferred_locations=["Nairobi"],minimum_salary=Decimal("1200"))
    JobDescription.objects.create(user=user,application=application,title="Backend Engineer",company="Acme",raw_text="Python Django",required_skills=["Python","Django"],preferred_skills=["Docker"])
    result=JobFitAnalyzer(user).analyze(application)
    assert result.score==80
    assert result.required_matches==["django","python"]
    assert result.required_gaps==[]
    assert result.role_match is True
    assert result.location_match is True
    assert result.salary_match is True

def test_fit_reports_missing_required_skills(user,application):
    CareerProfile.objects.create(user=user,skills=["Python"])
    JobDescription.objects.create(user=user,application=application,title="Backend Engineer",company="Acme",raw_text="x",required_skills=["Python","Django"],preferred_skills=[])
    result=JobFitAnalyzer(user).analyze(application)
    assert "django" in result.required_gaps
    assert result.score < 100
    assert result.recommendations

def test_fit_without_description_is_actionable(user,application):
    result=JobFitAnalyzer(user).analyze(application)
    assert result.score==0
    assert "Add a job description" in result.recommendations[0]

def test_fit_scopes_other_user(user,db):
    other=User.objects.create_user(username="other-fit",password="pass")
    app=JobApplication.objects.create(user=other,company="Other",role="Engineer")
    with pytest.raises(PermissionError):
        JobFitAnalyzer(user).analyze(app)
