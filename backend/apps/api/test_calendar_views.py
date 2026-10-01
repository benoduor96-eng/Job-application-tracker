"""API tests for the calendar export."""
from datetime import timedelta
import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient
from apps.jobs.models import Interview, JobApplication

@pytest.fixture
def client(db):
    user = User.objects.create_user(username="calendar-user", password="strong-pass")
    api = APIClient()
    api.force_authenticate(user=user)
    api.user = user
    return api

def test_export_requires_authentication(db):
    assert APIClient().get("/api/calendar/export/").status_code == 401

def test_export_returns_ics_download_with_my_events(client):
    application = JobApplication.objects.create(user=client.user, company="Acme", role="Engineer", status="interview", next_action="Send thank-you", next_action_date=(timezone.now() + timedelta(days=2)).date())
    Interview.objects.create(application=application, interview_type="technical", scheduled_date=timezone.now() + timedelta(days=3))
    response = client.get("/api/calendar/export/")
    body = response.content.decode()
    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/calendar")
    assert "attachment" in response["Content-Disposition"]
    assert body.startswith("BEGIN:VCALENDAR") and body.count("BEGIN:VEVENT") == 2
    assert "Technical interview: Engineer at Acme" in body

def test_export_excludes_other_users_data(client):
    other = User.objects.create_user(username="calendar-other", password="pass")
    theirs = JobApplication.objects.create(user=other, company="Secret Corp", role="Spy", status="interview")
    Interview.objects.create(application=theirs, scheduled_date=timezone.now() + timedelta(days=1))
    assert "Secret Corp" not in client.get("/api/calendar/export/").content.decode()

def test_export_include_past_flag(client):
    application = JobApplication.objects.create(user=client.user, company="Acme", role="Engineer")
    Interview.objects.create(application=application, scheduled_date=timezone.now() - timedelta(days=10))
    assert "BEGIN:VEVENT" not in client.get("/api/calendar/export/").content.decode()
    assert "BEGIN:VEVENT" in client.get("/api/calendar/export/?include_past=true").content.decode()

@pytest.mark.parametrize("query", ["duration=abc", "duration=5", "duration=9999", "include_past=maybe"])
def test_export_rejects_invalid_parameters(client, query):
    response = client.get(f"/api/calendar/export/?{query}")
    assert response.status_code == 400
    assert "detail" in response.json()
