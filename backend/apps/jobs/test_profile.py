import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import CareerProfile


@pytest.mark.django_db
def test_profile_is_unique_per_user():
    user = User.objects.create_user(username="profile-owner", password="pass12345")
    CareerProfile.objects.create(user=user, headline="Backend Engineer")

    with pytest.raises(IntegrityError):
        CareerProfile.objects.create(user=user, headline="Second profile")


@pytest.mark.django_db
def test_profile_stores_job_search_preferences():
    user = User.objects.create_user(username="job-seeker", password="pass12345")
    profile = CareerProfile.objects.create(
        user=user,
        skills=["Python", "Django", "PostgreSQL"],
        preferred_roles=["Backend Engineer", "Software Engineer"],
        preferred_locations=["Remote", "Nairobi"],
        work_preference="remote",
        minimum_salary=50000,
        target_salary=75000,
    )

    assert "Django" in profile.skills
    assert "Backend Engineer" in profile.preferred_roles
    assert profile.work_preference == "remote"
    assert profile.target_salary > profile.minimum_salary
