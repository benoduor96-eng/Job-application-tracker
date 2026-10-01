"""API tests for pipeline board endpoints."""
from datetime import date, timedelta
import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient
from apps.jobs.models import ApplicationActivity, JobApplication

@pytest.fixture
def client(db):
    user = User.objects.create_user(username="pipeline-user", password="strong-pass")
    api = APIClient(); api.force_authenticate(user=user); api.user = user
    return api

def make(user, **kwargs):
    data = dict(company="Acme", role="Engineer", status="applied"); data.update(kwargs)
    return JobApplication.objects.create(user=user, **data)

def column(data, status):
    return next(c for c in data["columns"] if c["status"] == status)

def test_auth_required(db):
    assert APIClient().get("/api/pipeline/board/").status_code == 401
    assert APIClient().post("/api/pipeline/move/", {}, format="json").status_code == 401

def test_board_is_user_scoped(client):
    make(client.user, company="Mine", status="interview")
    other = User.objects.create_user(username="other", password="pass")
    make(other, company="Theirs", status="interview")
    data = client.get("/api/pipeline/board/").json()
    assert [c["company"] for c in column(data, "interview")["cards"]] == ["Mine"]

def test_search_and_stale_validation(client):
    make(client.user, company="Globex")
    make(client.user, company="Initech")
    assert client.get("/api/pipeline/board/?q=glob").json()["totals"]["applications"] == 1
    assert client.get("/api/pipeline/board/?stale_days=abc").status_code == 400
    assert client.get("/api/pipeline/board/?stale_days=0").status_code == 400

def test_move_logs_activity_and_sets_applied_date(client):
    app = make(client.user, status="saved", applied_date=None)
    response = client.post("/api/pipeline/move/", {"ids":[app.id],"status":"applied"}, format="json")
    assert response.status_code == 200
    app.refresh_from_db()
    assert app.status == "applied" and app.applied_date is not None
    activity = ApplicationActivity.objects.get(application=app)
    assert activity.metadata == {"from":"saved","to":"applied","source":"pipeline_board"}
