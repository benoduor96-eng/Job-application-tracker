from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from .models import CareerContact, JobApplication


@pytest.mark.django_db
def test_contact_is_scoped_to_owner():
    first = User.objects.create_user(username="first", password="pass12345")
    second = User.objects.create_user(username="second", password="pass12345")
    CareerContact.objects.create(user=first, name="Recruiter One", company="Example")
    CareerContact.objects.create(user=second, name="Recruiter Two", company="Other")

    assert list(CareerContact.objects.filter(user=first).values_list("name", flat=True)) == ["Recruiter One"]


@pytest.mark.django_db
def test_contact_can_link_to_owned_application():
    user = User.objects.create_user(username="owner", password="pass12345")
    application = JobApplication.objects.create(user=user, company="Acme", role="Engineer")
    contact = CareerContact.objects.create(
        user=user,
        application=application,
        name="Hiring Manager",
        contact_type="hiring_manager",
        next_follow_up=timezone.now() + timedelta(days=2),
    )

    assert contact.application_id == application.id
    assert contact.next_follow_up is not None
