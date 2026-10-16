import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.jobs.models import Interview, JobApplication


@pytest.mark.django_db
def test_interview_create_rejects_application_owned_by_another_user():
    owner = User.objects.create_user(username="owner", password="test-password")
    other_user = User.objects.create_user(username="other", password="test-password")
    application = JobApplication.objects.create(
        user=owner,
        company="Private Company",
        role="Private Role",
    )
    client = APIClient()
    client.force_authenticate(user=other_user)

    response = client.post(
        "/api/interviews/",
        {"application": application.pk, "interview_type": "phone"},
        format="json",
    )

    assert response.status_code == 404
    assert response.data["detail"] == "Application not found"
    assert Interview.objects.count() == 0


@pytest.mark.django_db
def test_interview_create_rejects_nonexistent_application():
    user = User.objects.create_user(username="interviewer", password="test-password")
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        "/api/interviews/",
        {"application": 999999, "interview_type": "phone"},
        format="json",
    )

    assert response.status_code == 404
    assert response.data["detail"] == "Application not found"
    assert Interview.objects.count() == 0


@pytest.mark.django_db
def test_interview_create_succeeds_for_users_own_application():
    user = User.objects.create_user(username="applicant", password="test-password")
    application = JobApplication.objects.create(
        user=user,
        company="My Company",
        role="My Role",
    )
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        "/api/interviews/",
        {"application": application.pk, "interview_type": "phone"},
        format="json",
    )

    assert response.status_code == 201
    assert Interview.objects.filter(application=application).count() == 1
