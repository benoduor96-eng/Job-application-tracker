from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from .models import CareerProfile, Resume, JobApplication, JobDescription
from .career_asset_readiness import CareerAssetReadiness


class CareerAssetReadinessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="assets", password="pass12345")
        self.application = JobApplication.objects.create(user=self.user, company="Acme", role="Engineer", status="applied")
        self.make_profile()

    def make_profile(self):
        CareerProfile.objects.create(
            user=self.user, headline="Engineer", professional_summary="Backend developer",
            skills=["Python"], preferred_roles=["Engineer"], preferred_locations=["Remote"],
            portfolio_url="https://example.com", github_url="https://github.com/example",
            linkedin_url="https://linkedin.com/in/example", target_salary=Decimal("90000"),
        )

    def service(self):
        return CareerAssetReadiness(self.user)

    def test_profile_score_is_high_when_fields_are_present(self):
        data = self.service().profile()
        self.assertTrue(data["exists"])
        self.assertGreaterEqual(data["score"], 80)

    def test_profile_missing_fields_are_reported(self):
        profile = CareerProfile.objects.get(user=self.user)
        profile.skills = []
        profile.save()
        data = self.service().profile()
        self.assertIn("skills", data["missing"])

    def test_resumes_are_scored(self):
        Resume.objects.create(user=self.user, name="Resume", summary="Summary", content="Experience", target_role="Engineer", skills=["Python"], status="active")
        rows = self.service().resumes()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["score"], 100)

    def test_empty_resume_is_not_full_score(self):
        Resume.objects.create(user=self.user, name="Draft", status="draft")
        row = self.service().resumes()[0]
        self.assertLess(row["score"], 100)
        self.assertIn("content", row["missing"])

    def test_application_coverage_uses_job_descriptions(self):
        JobDescription.objects.create(user=self.user, application=self.application, title="Engineer", company="Acme", raw_text="Python")
        data = self.service().application_coverage()
        self.assertEqual(data["applications"], 1)
        self.assertEqual(data["with_job_description"], 1)
        self.assertEqual(data["coverage_rate"], 100)

    def test_missing_job_description_is_reported(self):
        data = self.service().application_coverage()
        self.assertEqual(data["without_job_description"], 1)

    def test_asset_summary_contains_resume_and_profile_metrics(self):
        data = self.service().asset_summary()
        self.assertIn("profile_score", data)
        self.assertIn("best_resume_score", data)
        self.assertIn("application_coverage", data)

    def test_recommendation_is_generated_for_missing_resume(self):
        rows = self.service().recommendations()
        self.assertTrue(any(item["type"] == "resume" for item in rows))

    def test_active_resume_recommendation_disappears(self):
        Resume.objects.create(user=self.user, name="Active", summary="Summary", content="Content", target_role="Engineer", skills=["Python"], status="active")
        rows = self.service().recommendations()
        self.assertFalse(any(item["title"] == "Mark a resume active" for item in rows))

    def test_missing_profile_is_handled(self):
        self.user.career_profile.delete()
        data = self.service().profile()
        self.assertFalse(data["exists"])
        self.assertEqual(data["score"], 0)

    def test_empty_user_is_safe(self):
        user = User.objects.create_user(username="empty-assets", password="pass12345")
        data = CareerAssetReadiness(user).dashboard()
        self.assertEqual(data["summary"]["resume_count"], 0)
        self.assertEqual(data["summary"]["application_coverage"]["applications"], 0)
