"""API-level tests for authenticated career platform expansion endpoints."""
from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from apps.jobs.models import JobApplication

User = get_user_model()

class PlatformExpansionEndpointTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="platform-owner", password="strong-pass-123")
        self.other = User.objects.create_user(username="other-owner", password="strong-pass-123")
        self.client.force_authenticate(self.user)
        self.owned = JobApplication.objects.create(
            user=self.user, company="Acme Ltd", role="Data Analyst", location="Remote",
            status="interview", job_url="https://jobs.example/role/1",
            applied_date=date(2026, 1, 5), salary_min=60000, salary_max=80000,
        )
        self.private = JobApplication.objects.create(
            user=self.other, company="Private Co", role="Private Role", status="offer",
        )

    def test_advanced_search_only_returns_owned_records(self):
        response = self.client.get("/api/applications/search-advanced/?q=role:analyst")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["items"][0]["id"], self.owned.id)
        self.assertNotIn(self.private.id, [item["id"] for item in response.data["items"]])

    def test_advanced_search_rejects_unknown_fields(self):
        response = self.client.get("/api/applications/search-advanced/?q=password:secret")
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.data)

    def test_duplicate_review_does_not_mutate_records(self):
        response = self.client.get("/api/applications/duplicate-review/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("pairs", response.data)
        self.assertIn("No records were merged", response.data["warning"])
        self.owned.refresh_from_db()
        self.assertEqual(self.owned.status, "interview")
        self.assertEqual(JobApplication.objects.filter(user=self.other).count(), 1)

    def test_duplicate_review_validates_threshold_and_limit(self):
        self.assertEqual(self.client.get("/api/applications/duplicate-review/?threshold=2").status_code, 400)
        self.assertEqual(self.client.get("/api/applications/duplicate-review/?limit=0").status_code, 400)

    def test_cohort_analytics_has_explicit_quality_and_truncation_fields(self):
        response = self.client.get("/api/reports/cohort-analytics/?weeks=4&periods=4")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertIn("funnel", response.data)
        self.assertIn("quality", response.data)
        self.assertFalse(response.data["truncated"])

    def test_cohort_analytics_rejects_unbounded_parameters(self):
        self.assertEqual(self.client.get("/api/reports/cohort-analytics/?weeks=500").status_code, 400)
        self.assertEqual(self.client.get("/api/reports/cohort-analytics/?periods=0").status_code, 400)

    def test_retention_preview_never_deletes_records(self):
        before = JobApplication.objects.filter(user=self.user).count()
        response = self.client.get("/api/account/retention-preview/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["automatic_deletion_performed"])
        self.assertEqual(JobApplication.objects.filter(user=self.user).count(), before)

    def test_all_expansion_endpoints_require_authentication(self):
        anonymous = APIClient()
        urls = [
            "/api/applications/search-advanced/",
            "/api/applications/duplicate-review/",
            "/api/reports/cohort-analytics/",
            "/api/account/retention-preview/",
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertIn(anonymous.get(url).status_code, (401, 403))
