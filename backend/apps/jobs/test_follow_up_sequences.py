import pytest
from django.contrib.auth import get_user_model

from apps.jobs.follow_up_sequences import (
    build_sequence,
    cancel_open_sequence,
    create_sequence,
    sequence_summary,
)
from apps.jobs.models import JobApplication


User = get_user_model()


@pytest.mark.django_db
def test_applied_sequence_contains_progressive_followups():
    user = User.objects.create_user(username="sequence", password="password")
    application = JobApplication.objects.create(
        user=user, company="Example", role="Engineer", status="applied"
    )
    plans = build_sequence(application)
    assert len(plans) == 3
    assert plans[0]["due_date"] < plans[-1]["due_date"]


@pytest.mark.django_db
def test_sequence_creation_is_idempotent():
    user = User.objects.create_user(username="sequence2", password="password")
    application = JobApplication.objects.create(
        user=user, company="Example", role="Engineer", status="interview"
    )
    first = create_sequence(application)
    second = create_sequence(application)
    assert len(first) == 2
    assert second == []
    assert sequence_summary(application)["open"] == 2


@pytest.mark.django_db
def test_cancel_sequence_marks_only_followups():
    user = User.objects.create_user(username="sequence3", password="password")
    application = JobApplication.objects.create(
        user=user, company="Example", role="Engineer", status="applied"
    )
    create_sequence(application)
    changed = cancel_open_sequence(application)
    assert changed == 3
    assert sequence_summary(application)["cancelled"] == 3
