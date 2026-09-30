from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from apps.jobs.cover_letter import CoverLetterBuilder, validate_cover_letter_source
from apps.jobs.models import CareerProfile, JobApplication, JobDescription, Resume


User = get_user_model()


@pytest.mark.django_db
class TestCoverLetterBuilder:
    def setup_data(self):
        user = User.objects.create_user(
            username="coverwriter",
            first_name="Benard",
            password="test-pass-123",
        )
        profile = CareerProfile.objects.create(
            user=user,
            headline="Backend Engineer",
            professional_summary="I build reliable web applications and APIs.",
            skills=["python", "django", "postgresql"],
            preferred_roles=["Backend Engineer"],
        )
        application = JobApplication.objects.create(
            user=user,
            company="Example Labs",
            role="Backend Engineer",
            location="Remote",
        )
        description = JobDescription.objects.create(
            user=user,
            application=application,
            title="Backend Engineer",
            company="Example Labs",
            raw_text="Python Django PostgreSQL Docker",
            required_skills=["python", "django"],
            preferred_skills=["docker"],
            salary_min=Decimal("60000"),
            salary_max=Decimal("90000"),
        )
        resume = Resume.objects.create(
            user=user,
            name="Backend Resume",
            summary="Experienced backend engineer focused on APIs.",
            content="Python and Django projects",
            status="active",
            skills=["python", "django"],
        )
        return user, profile, application, description, resume

    def test_build_contains_application_details(self):
        _, profile, application, description, resume = self.setup_data()
        draft = CoverLetterBuilder(
            profile=profile,
            resume=resume,
            description=description,
            application=application,
        ).build()
        assert "Backend Engineer" in draft.subject
        assert "Example Labs" in draft.full_text
        assert "Python" in draft.full_text or "python" in draft.full_text

    def test_builder_does_not_invent_missing_resume_data(self):
        _, profile, application, description, _ = self.setup_data()
        draft = CoverLetterBuilder(
            profile=profile,
            description=description,
            application=application,
        ).build()
        assert "invented" not in draft.full_text.lower()
        assert draft.evidence

    def test_validation_reports_missing_profile(self):
        _, _, application, description, resume = self.setup_data()
        warnings = validate_cover_letter_source(
            application,
            None,
            resume,
            description,
        )
        assert any("career profile" in warning for warning in warnings)

    def test_validation_reports_missing_resume(self):
        _, profile, application, description, _ = self.setup_data()
        warnings = validate_cover_letter_source(
            application,
            profile,
            None,
            description,
        )
        assert any("resume" in warning.lower() for warning in warnings)
