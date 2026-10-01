"""API tests for batch job-fit insights."""
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from apps.jobs.models import CareerProfile, JobApplication, JobDescription

@pytest.fixture
def user(db):
    return User.objects.create_user(username="fit-api", password="pass")

@pytest.fixture
def client(user):
    api = APIClient()
    api.force_authenticate(user=user)
    return api

def make_app(user, company, role, score_data=True):
    app = JobApplication.objects.create(user=user, company=company, role=role, location="Nairobi", salary_max=Decimal("2500"))
    if score_data:
        JobDescription.objects.create(
            user=user, application=app, title=role, company=company,
            raw_text="Python", required_skills=["Python"], preferred_skills=[],
        )
    return app

@pytest.mark.django_db
def test_fit_summary_returns_scoped_ranked_results(client, user):
    CareerProfile.objects.create(user=user, skills=["Python"], preferred_roles=["Engineer"])
    low = make_app(user, "Low Co", "Other Role")
    high = make_app(user, "High Co", "Engineer")
    response = client.get("/api/applications/fit-summary/")
    assert response.status_code == 200
    assert response.data["count"] == 2
    assert response.data["applications"][0]["application_id"] == high.id
    assert response.data["applications"][0]["score"] >= response.data["applications"][1]["score"]

@pytest.mark.django_db
def test_fit_summary_supports_minimum_score(client, user):
    CareerProfile.objects.create(user=user, skills=["Python"], preferred_roles=["Engineer"])
    make_app(user, "High Co", "Engineer")
    make_app(user, "Low Co", "Other")
    response = client.get("/api/applications/fit-summary/?min_score=80")
    assert response.status_code == 200
    assert all(item["score"] >= 80 for item in response.data["applications"])

@pytest.mark.django_db
def test_fit_summary_caps_limit(client, user):
    for index in range(3):
        make_app(user, "Company "+str(index), "Engineer")
    response = client.get("/api/applications/fit-summary/?limit=2")
    assert response.status_code == 200
    assert response.data["count"] == 2
