from datetime import date, timedelta

import pytest
from django.contrib.auth.models import User

from .models import JobApplication
from .services import JobApplicationService


@pytest.fixture
def user(db):
    return User.objects.create_user(username="service-user", password="safe-pass")


@pytest.fixture
def service(user):
    return JobApplicationService(user)


@pytest.fixture
def applications(user):
    return [
        JobApplication.objects.create(
            user=user,
            company="Acme",
            role="Backend Engineer",
            status="applied",
            applied_date=date.today(),
            next_action="Follow up",
            next_action_date=date.today() + timedelta(days=3),
        ),
        JobApplication.objects.create(
            user=user,
            company="Globex",
            role="Python Developer",
            status="interview",
            applied_date=date.today(),
            next_action="Technical interview",
            next_action_date=date.today() + timedelta(days=7),
        ),
        JobApplication.objects.create(
            user=user,
            company="Umbrella",
            role="Data Engineer",
            status="rejected",
        ),
    ]


def test_queryset_is_scoped_to_user(service, applications, db):
    other = User.objects.create_user(username="other", password="pass")
    JobApplication.objects.create(user=other, company="Hidden", role="Engineer")
    assert service.queryset().count() == 3
    assert all(item.user_id == service.user.id for item in service.queryset())


def test_search_matches_multiple_fields(service, applications):
    assert service.search("Acme").count() == 1
    assert service.search("Python").count() == 1
    assert service.search("interview").count() == 1


def test_search_can_filter_by_status(service, applications):
    results = service.search(status="applied")
    assert results.count() == 1
    assert results.first().company == "Acme"


def test_counts_by_status_returns_zero_for_missing_states(service, applications):
    counts = service.counts_by_status()
    assert counts["applied"] == 1
    assert counts["interview"] == 1
    assert counts["offer"] == 0
    assert counts["rejected"] == 1


def test_upcoming_returns_date_order(service, applications):
    items = list(service.upcoming(days=10))
    assert [item.company for item in items] == ["Acme", "Globex"]


def test_overdue_excludes_terminal_statuses(service, user):
    JobApplication.objects.create(
        user=user,
        company="Old Active",
        role="Engineer",
        status="applied",
        next_action_date=date.today() - timedelta(days=2),
    )
    JobApplication.objects.create(
        user=user,
        company="Old Rejected",
        role="Engineer",
        status="rejected",
        next_action_date=date.today() - timedelta(days=4),
    )
    overdue = list(service.overdue())
    assert len(overdue) == 1
    assert overdue[0].company == "Old Active"


def test_dashboard_contains_pipeline_summary(service, applications):
    dashboard = service.dashboard()
    assert dashboard["total"] == 3
    assert dashboard["active"] == 2
    assert dashboard["interviews"] == 1
    assert len(dashboard["upcoming"]) == 2


def test_pipeline_health_rates(service, applications):
    health = service.pipeline_health()
    assert health["interview_rate"] == 100.0
    assert health["offer_rate"] == 0.0
    assert health["total_tracked"] == 3


def test_pipeline_health_handles_empty_pipeline(service):
    health = service.pipeline_health()
    assert health["screening_rate"] == 0.0
    assert health["interview_rate"] == 0.0
    assert health["offer_rate"] == 0.0


def test_update_status_changes_application(service, applications):
    application = applications[0]
    service.update_status(application, "screening")
    application.refresh_from_db()
    assert application.status == "screening"


def test_update_status_rejects_invalid_value(service, applications):
    with pytest.raises(ValueError):
        service.update_status(applications[0], "unknown")


def test_bulk_status_updates_owned_rows(service, applications):
    changed = service.bulk_status([applications[0].id, applications[1].id], "withdrawn")
    assert changed == 2
    assert JobApplication.objects.filter(status="withdrawn").count() == 2


def test_export_rows_is_sorted(service, applications):
    rows = service.export_rows()
    assert rows[0]["company"] == "Acme"
    assert set(rows[0]) == {
        "company",
        "role",
        "location",
        "status",
        "job_url",
        "applied_date",
        "next_action",
        "next_action_date",
        "notes",
    }
