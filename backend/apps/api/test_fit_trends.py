"""API tests for fit trend analytics."""
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from apps.jobs.models import CareerProfile, JobApplication, JobDescription

@pytest.mark.django_db
def test_fit_trends_endpoint_returns_summary():
    user = User.objects.create_user(username="trend-api", password="pass")
    CareerProfile.objects.create(user=user, skills=["Python"], preferred_roles=["Engineer"])
    app = JobApplication.objects.create(user=user, company="Acme", role="Engineer", status="applied", salary_max=Decimal("2000"))
    JobDescription.objects.create(user=user, application=app, title="Engineer", company="Acme", raw_text="x", required_skills=["Python"])
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/applications/fit-trends/")
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["average_score"] == response.data["applications"][0]["score"]

@pytest.mark.django_db
def test_fit_trends_rejects_invalid_limit():
    user = User.objects.create_user(username="trend-limit", password="pass")
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/applications/fit-trends/?limit=101")
    assert response.status_code == 400
