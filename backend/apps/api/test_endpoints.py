import pytest
from datetime import date, timedelta
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from apps.jobs.models import JobApplication


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(db, api_client):
    user = User.objects.create_user(username="api-user", password="strong-pass")
    api_client.force_authenticate(user=user)
    return api_client


def test_application_create_requires_company_and_role(authenticated_client):
    response = authenticated_client.post("/api/applications/", {"company": "A"})
    assert response.status_code == 400
    assert "role" in response.data


def test_application_list_is_private(authenticated_client, db):
    user = User.objects.get(username="api-user")
    JobApplication.objects.create(user=user, company="Visible", role="Engineer")
    other = User.objects.create_user(username="other-api", password="pass")
    JobApplication.objects.create(user=other, company="Hidden", role="Engineer")

    response = authenticated_client.get("/api/applications/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["company"] == "Visible"


def test_search_endpoint(authenticated_client):
    user = User.objects.get(username="api-user")
    JobApplication.objects.create(user=user, company="Acme", role="Python Engineer")
    JobApplication.objects.create(user=user, company="Globex", role="Java Engineer")

    response = authenticated_client.get("/api/applications/?q=Python")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["company"] == "Acme"


def test_dashboard_returns_operational_summary(authenticated_client):
    user = User.objects.get(username="api-user")
    JobApplication.objects.create(user=user, company="Acme", role="Engineer", status="applied")
    JobApplication.objects.create(
        user=user,
        company="Globex",
        role="Engineer",
        status="interview",
        next_action="Interview",
        next_action_date=date.today() + timedelta(days=2),
    )

    response = authenticated_client.get("/api/applications/dashboard/")
    assert response.status_code == 200
    assert response.data["total"] == 2
    assert response.data["active"] == 2
    assert response.data["by_status"]["interview"] == 1
    assert len(response.data["upcoming"]) == 1


def test_health_metrics_endpoint(authenticated_client):
    response = authenticated_client.get("/api/applications/health_metrics/")
    assert response.status_code == 200
    assert response.data["total_tracked"] == 0
    assert response.data["offer_rate"] == 0.0


def test_export_endpoint_returns_application_rows(authenticated_client):
    user = User.objects.get(username="api-user")
    JobApplication.objects.create(user=user, company="Acme", role="Engineer")

    response = authenticated_client.get("/api/applications/export/")
    assert response.status_code == 200
    assert response.data[0]["company"] == "Acme"
    assert "role" in response.data[0]


def test_update_status(authenticated_client):
    user = User.objects.get(username="api-user")
    job = JobApplication.objects.create(user=user, company="Acme", role="Engineer")

    response = authenticated_client.patch(
        f"/api/applications/{job.id}/",
        {"status": "interview"},
        format="json",
    )
    assert response.status_code == 200
    assert response.data["status"] == "interview"


def test_delete_application(authenticated_client):
    user = User.objects.get(username="api-user")
    job = JobApplication.objects.create(user=user, company="Acme", role="Engineer")

    response = authenticated_client.delete(f"/api/applications/{job.id}/")
    assert response.status_code == 204
    assert not JobApplication.objects.filter(id=job.id).exists()


def test_registration_creates_account(api_client, db):
    response = api_client.post(
        "/api/auth/register/",
        {"username": "new-user", "password": "strong-pass", "email": "new@example.com"},
        format="json",
    )
    assert response.status_code == 201
    assert response.data["username"] == "new-user"
    assert User.objects.filter(username="new-user").exists()


def test_registration_rejects_duplicate_username(api_client, db):
    User.objects.create_user(username="taken", password="pass")
    response = api_client.post(
        "/api/auth/register/",
        {"username": "taken", "password": "new-pass"},
        format="json",
    )
    assert response.status_code == 400


def test_application_crud_round_trip_supports_flask_fields(authenticated_client):
    """The Django API preserves the core fields from the former Flask example."""
    created = authenticated_client.post(
        "/api/applications/",
        {
            "company": "Northwind",
            "role": "Data Analyst",
            "location": "Nairobi",
            "status": "applied",
            "job_url": "https://example.com/jobs/123",
            "applied_date": "2026-10-01",
            "notes": "Follow up next week",
        },
        format="json",
    )
    assert created.status_code == 201
    application_id = created.data["id"]
    assert created.data["company"] == "Northwind"
    assert created.data["location"] == "Nairobi"
    assert created.data["job_url"] == "https://example.com/jobs/123"
    assert created.data["applied_date"] == "2026-10-01"
    assert created.data["notes"] == "Follow up next week"

    updated = authenticated_client.patch(
        f"/api/applications/{application_id}/",
        {"status": "interview", "notes": "Technical interview scheduled"},
        format="json",
    )
    assert updated.status_code == 200
    assert updated.data["status"] == "interview"
    assert updated.data["notes"] == "Technical interview scheduled"

    retrieved = authenticated_client.get(f"/api/applications/{application_id}/")
    assert retrieved.status_code == 200
    assert retrieved.data["role"] == "Data Analyst"

    deleted = authenticated_client.delete(f"/api/applications/{application_id}/")
    assert deleted.status_code == 204
    assert not JobApplication.objects.filter(id=application_id).exists()


def test_application_status_filter(authenticated_client):
    user = User.objects.get(username="api-user")
    JobApplication.objects.create(user=user, company="Acme", role="Engineer", status="applied")
    JobApplication.objects.create(user=user, company="Globex", role="Analyst", status="interview")

    response = authenticated_client.get("/api/applications/?status=interview")

    assert response.status_code == 200
    assert [item["company"] for item in response.data] == ["Globex"]


def test_user_cannot_retrieve_update_or_delete_another_users_application(authenticated_client, db):
    other = User.objects.create_user(username="private-owner", password="strong-pass")
    private_job = JobApplication.objects.create(
        user=other,
        company="Private Company",
        role="Private Role",
        status="applied",
    )

    retrieved = authenticated_client.get(f"/api/applications/{private_job.id}/")
    updated = authenticated_client.patch(
        f"/api/applications/{private_job.id}/",
        {"status": "offer"},
        format="json",
    )
    deleted = authenticated_client.delete(f"/api/applications/{private_job.id}/")

    assert retrieved.status_code == 404
    assert updated.status_code == 404
    assert deleted.status_code == 404
    private_job.refresh_from_db()
    assert private_job.status == "applied"


def test_salary_max_must_not_be_less_than_salary_min(authenticated_client):
    invalid_create = authenticated_client.post(
        "/api/applications/",
        {
            "company": "Acme",
            "role": "Engineer",
            "salary_min": "90000",
            "salary_max": "70000",
        },
        format="json",
    )
    assert invalid_create.status_code == 400
    assert "salary_max" in invalid_create.data

    user = User.objects.get(username="api-user")
    job = JobApplication.objects.create(
        user=user,
        company="Globex",
        role="Analyst",
        salary_min=50000,
        salary_max=80000,
    )
    invalid_update = authenticated_client.patch(
        f"/api/applications/{job.id}/",
        {"salary_min": "95000"},
        format="json",
    )
    assert invalid_update.status_code == 400
    assert "salary_max" in invalid_update.data
    job.refresh_from_db()
    assert str(job.salary_min) == "50000.00"
