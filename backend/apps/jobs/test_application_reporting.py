import pytest
from django.contrib.auth import get_user_model

from apps.jobs.application_reporting import (
    company_report,
    dashboard_report,
    funnel_report,
    salary_report,
    stale_report,
    status_report,
)
from apps.jobs.models import JobApplication


User = get_user_model()


@pytest.mark.django_db
def test_status_report_is_user_scoped():
    user = User.objects.create_user(username="report", password="password")
    other = User.objects.create_user(username="report-other", password="password")
    JobApplication.objects.create(user=user, company="A", role="Engineer", status="applied")
    JobApplication.objects.create(user=other, company="B", role="Engineer", status="offer")
    result = status_report(user)
    assert result["total"] == 1
    assert result["counts"]["applied"] == 1


@pytest.mark.django_db
def test_company_report_groups_applications():
    user = User.objects.create_user(username="companies", password="password")
    JobApplication.objects.create(user=user, company="A", role="One")
    JobApplication.objects.create(user=user, company="A", role="Two")
    rows = company_report(user)
    assert rows[0]["company"] == "A"
    assert rows[0]["applications"] == 2


@pytest.mark.django_db
def test_funnel_report_calculates_rates():
    user = User.objects.create_user(username="funnel", password="password")
    JobApplication.objects.create(user=user, company="A", role="One", status="applied")
    JobApplication.objects.create(user=user, company="B", role="Two", status="interview")
    result = funnel_report(user)
    assert result["applied"] == 2
    assert result["interview"] == 1
    assert result["interview_rate"] == 50.0


@pytest.mark.django_db
def test_dashboard_report_has_all_sections():
    user = User.objects.create_user(username="dashboard-report", password="password")
    result = dashboard_report(user)
    assert set(result) == {"status", "companies", "salary", "funnel", "stale"}


@pytest.mark.django_db
def test_salary_report_handles_empty_data():
    user = User.objects.create_user(username="salary", password="password")
    result = salary_report(user)
    assert result["minimum"] is None
    assert result["maximum"] is None


@pytest.mark.django_db
def test_stale_report_excludes_terminal_statuses():
    user = User.objects.create_user(username="stale", password="password")
    JobApplication.objects.create(user=user, company="A", role="One", status="rejected")
    assert stale_report(user, days=1) == []
