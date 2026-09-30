import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.jobs.models import CareerProfile, JobApplication, JobDescription, Resume


User = get_user_model()


@pytest.mark.django_db
class TestCareerIntelligenceEndpoints:
    def setup(self):
        self.user = User.objects.create_user(
            username="api-intelligence",
            password="test-pass-123",
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_summary_is_user_scoped(self):
        self.setup()
        JobApplication.objects.create(
            user=self.user,
            company="Example",
            role="Engineer",
            status="applied",
        )
        other = User.objects.create_user(
            username="other-intelligence",
            password="test-pass-123",
        )
        JobApplication.objects.create(
            user=other,
            company="Private",
            role="Engineer",
            status="offer",
        )

        response = self.client.get("/api/intelligence/summary/")

        assert response.status_code == 200
        assert response.data["total_applications"] == 1
        assert response.data["status_counts"]["applied"] == 1
        assert "offer" not in response.data["status_counts"]

    def test_skill_match_uses_profile(self):
        self.setup()
        CareerProfile.objects.create(
            user=self.user,
            skills=["python", "django"],
            preferred_roles=["Backend Engineer"],
            preferred_locations=["Remote"],
        )
        response = self.client.post(
            "/api/intelligence/skill-match/advanced/",
            {
                "required_skills": ["python", "django"],
                "preferred_skills": ["docker"],
                "role": "Backend Engineer",
                "location": "Remote",
            },
            format="json",
        )

        assert response.status_code == 200
        assert response.data["required_score"] == 100.0
        assert response.data["matched_required"] == ["django", "python"]
        assert "docker" not in response.data["matched_required"]

    def test_description_preview(self):
        self.setup()
        response = self.client.post(
            "/api/intelligence/descriptions/preview/",
            {"raw_text": "Python Django PostgreSQL Docker"},
            format="json",
        )

        assert response.status_code == 200
        assert "python" in response.data["skills"]
        assert response.data["skill_count"] >= 4

    def test_description_create_analyzes_content(self):
        self.setup()
        response = self.client.post(
            "/api/intelligence/descriptions/",
            {
                "title": "Backend Engineer",
                "company": "Example",
                "raw_text": "Python Django PostgreSQL Docker API",
            },
            format="json",
        )

        assert response.status_code == 201
        assert "python" in response.data["required_skills"]
        assert response.data["analyzed_at"] is not None

    def test_description_match_is_user_scoped(self):
        self.setup()
        description = JobDescription.objects.create(
            user=self.user,
            title="Backend Engineer",
            company="Example",
            raw_text="Python Django",
            required_skills=["python", "django"],
        )
        response = self.client.get(
            f"/api/intelligence/descriptions/{description.id}/match/"
        )
        assert response.status_code == 200
        assert response.data["description_id"] == description.id

    def test_other_users_description_is_hidden(self):
        self.setup()
        other = User.objects.create_user(
            username="private-description",
            password="test-pass-123",
        )
        description = JobDescription.objects.create(
            user=other,
            title="Private",
            company="Private",
            raw_text="Python",
        )
        response = self.client.get(
            f"/api/intelligence/descriptions/{description.id}/"
        )
        assert response.status_code == 404

    def test_resume_targeting_requires_profile(self):
        self.setup()
        description = JobDescription.objects.create(
            user=self.user,
            title="Engineer",
            company="Example",
            raw_text="Python Django",
            required_skills=["python"],
        )
        response = self.client.get(
            f"/api/intelligence/descriptions/{description.id}/resume_targeting/"
        )
        assert response.status_code == 400

    def test_resume_targeting_returns_matched_skills(self):
        self.setup()
        CareerProfile.objects.create(
            user=self.user,
            skills=["python", "django"],
        )
        description = JobDescription.objects.create(
            user=self.user,
            title="Engineer",
            company="Example",
            raw_text="Python Django",
            required_skills=["python", "django"],
            preferred_skills=["docker"],
        )
        response = self.client.get(
            f"/api/intelligence/descriptions/{description.id}/resume_targeting/"
        )
        assert response.status_code == 200
        assert response.data["matched_keywords"] == ["django", "python"]
        assert response.data["missing_keywords"] == []

    def test_follow_up_preview_does_not_create_tasks(self):
        self.setup()
        JobApplication.objects.create(
            user=self.user,
            company="Example",
            role="Engineer",
            status="applied",
        )
        response = self.client.post(
            "/api/intelligence/follow-ups/",
            {"create": False},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["created"] == 0

    def test_follow_up_creation_creates_tasks(self):
        self.setup()
        JobApplication.objects.create(
            user=self.user,
            company="Example",
            role="Engineer",
            status="interview",
        )
        response = self.client.post(
            "/api/intelligence/follow-ups/",
            {"create": True},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["created"] == 1

    def test_cover_letter_endpoint_uses_user_records(self):
        self.setup()
        application = JobApplication.objects.create(
            user=self.user,
            company="Example Labs",
            role="Backend Engineer",
        )
        CareerProfile.objects.create(
            user=self.user,
            headline="Backend Engineer",
            professional_summary="I build web APIs.",
            skills=["python", "django"],
        )
        Resume.objects.create(
            user=self.user,
            name="Active",
            summary="Backend engineering experience.",
            status="active",
        )
        response = self.client.post(
            "/api/intelligence/cover-letter/",
            {"application_id": application.id},
            format="json",
        )
        assert response.status_code == 200
        assert "Example Labs" in response.data["full_text"]
        assert "Backend Engineer" in response.data["subject"]

    def test_cover_letter_rejects_foreign_application(self):
        self.setup()
        other = User.objects.create_user(
            username="foreign-application",
            password="test-pass-123",
        )
        application = JobApplication.objects.create(
            user=other,
            company="Private",
            role="Private Role",
        )
        response = self.client.post(
            "/api/intelligence/cover-letter/",
            {"application_id": application.id},
            format="json",
        )
        assert response.status_code == 404
