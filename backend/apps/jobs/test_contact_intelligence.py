from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.jobs.contact_intelligence import ContactIntelligenceService
from apps.jobs.models import CareerContact


User = get_user_model()


@pytest.mark.django_db
class TestContactIntelligenceService:
    def setup_user(self):
        return User.objects.create_user(username="contacts", password="test-pass-123")

    def test_summary_counts_follow_up_states(self):
        user = self.setup_user()
        now = timezone.now()
        CareerContact.objects.create(
            user=user, name="Overdue Recruiter", company="Acme",
            contact_type="recruiter", next_follow_up=now - timedelta(days=2),
        )
        CareerContact.objects.create(
            user=user, name="Upcoming Recruiter", company="Acme",
            contact_type="recruiter", next_follow_up=now + timedelta(days=3),
            last_contacted_at=now,
        )
        CareerContact.objects.create(
            user=user, name="New Referral", company="Beta",
            contact_type="referral",
        )

        data = ContactIntelligenceService(user, now=now).summary()

        assert data["total"] == 3
        assert data["overdue"] == 1
        assert data["upcoming"] == 1
        assert data["never_contacted"] == 2
        assert data["by_type"]["recruiter"] == 2
        assert data["by_type"]["referral"] == 1
        assert len(data["actions"]) == 3

    def test_summary_is_user_scoped(self):
        user = self.setup_user()
        other = User.objects.create_user(username="other-contact", password="test-pass-123")
        CareerContact.objects.create(user=user, name="Mine", company="Acme")
        CareerContact.objects.create(user=other, name="Other", company="Beta")

        data = ContactIntelligenceService(user).summary()

        assert data["total"] == 1
        assert data["by_company"] == {"Acme": 1}
