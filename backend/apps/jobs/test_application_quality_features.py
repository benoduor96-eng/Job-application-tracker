import pytest
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.jobs.models import CareerContact, CareerTask, Interview, JobApplication, JobDescription
from apps.jobs.application_audit import ApplicationAuditService
from apps.jobs.company_intelligence import CompanyIntelligenceService

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="quality-user", password="pass")

@pytest.fixture
def application(user):
    return JobApplication.objects.create(
        user=user, company="Acme", role="Backend Engineer",
        status="applied", location="Nairobi",
    )

@pytest.mark.django_db
def test_audit_detects_missing_next_action(user, application):
    data = ApplicationAuditService(user).summary()
    assert data["by_category"]["missing_next_action"] == 1
    assert data["total_findings"] >= 1

@pytest.mark.django_db
def test_audit_detects_missing_job_description(user, application):
    findings = ApplicationAuditService(user).all_findings()
    assert any(x["code"] == "missing_job_description" for x in findings)

@pytest.mark.django_db
def test_audit_detects_overdue_action(user, application):
    application.next_action_date = timezone.localdate() - timedelta(days=3)
    application.save()
    findings = ApplicationAuditService(user).all_findings()
    assert any(x["code"] == "overdue_next_action" for x in findings)

@pytest.mark.django_db
def test_audit_is_user_scoped(user, application):
    other = User.objects.create_user(username="other-quality", password="pass")
    JobApplication.objects.create(user=other, company="Private", role="Engineer", status="applied")
    summary = ApplicationAuditService(user).summary()
    assert summary["applications"] == 1

@pytest.mark.django_db
def test_audit_dashboard_contains_sections(user, application):
    data = ApplicationAuditService(user).dashboard()
    assert set(data) == {"summary", "findings", "applications", "companies", "recommendations"}

@pytest.mark.django_db
def test_company_overview_aggregates_pipeline(user, application):
    JobApplication.objects.create(user=user, company="Acme", role="Data Engineer", status="interview")
    data = CompanyIntelligenceService(user).dashboard()
    row = next(x for x in data["companies"] if x["company"] == "Acme")
    assert row["applications"] == 2
    assert row["active"] == 2

@pytest.mark.django_db
def test_company_detail_includes_related_records(user, application):
    Interview.objects.create(application=application, outcome="scheduled")
    CareerContact.objects.create(user=user, name="Recruiter", company="Acme", application=application)
    CareerTask.objects.create(user=user, title="Prepare", application=application, status="todo")
    JobDescription.objects.create(user=user, application=application, title="Backend", company="Acme")
    detail = CompanyIntelligenceService(user).company_detail("Acme")
    assert detail["interviews"] == 1
    assert detail["contacts"] == 1
    assert detail["open_tasks"] == 1
    assert detail["job_descriptions"] == 1

@pytest.mark.django_db
def test_company_relationship_gap_is_reported(user, application):
    data = CompanyIntelligenceService(user).dashboard()
    assert any(x["company"] == "Acme" for x in data["relationship_gaps"])

@pytest.mark.django_db
def test_company_detail_is_case_insensitive(user, application):
    detail = CompanyIntelligenceService(user).company_detail("acme")
    assert detail["company"] == "Acme"

@pytest.mark.django_db
def test_company_missing_returns_none(user):
    assert CompanyIntelligenceService(user).company_detail("Unknown") is None

@pytest.mark.django_db
def test_company_salary_uses_midpoints(user):
    JobApplication.objects.filter(id__isnull=False).delete()
    app = JobApplication.objects.create(user=user, company="SalaryCo", role="Engineer", status="applied", salary_min=80000, salary_max=100000)
    detail = CompanyIntelligenceService(user).company_detail("SalaryCo")
    assert detail["salary"]["minimum"] == "90000"
    assert detail["salary"]["maximum"] == "90000"
