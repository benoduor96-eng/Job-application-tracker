from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import JobApplication, CareerProfile, Resume, CareerTask, SavedSearch


class WorkspaceIntegrationTests(TestCase):
    """Exercise the major read-only intelligence endpoints through the HTTP layer."""

    def setUp(self):
        self.user = User.objects.create_user(username="integration", password="pass12345")
        self.other = User.objects.create_user(username="integration-other", password="pass12345")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.application = JobApplication.objects.create(
            user=self.user,
            company="Integration Co",
            role="Backend Engineer",
            status="applied",
            location="Remote",
            salary_min=Decimal("80000"),
            salary_max=Decimal("100000"),
            next_action="Follow up",
        )
        CareerProfile.objects.create(
            user=self.user,
            headline="Backend Engineer",
            professional_summary="Python developer",
            skills=["Python", "Django"],
            preferred_roles=["Backend Engineer"],
        )
        Resume.objects.create(
            user=self.user,
            name="Integration Resume",
            summary="Backend engineer",
            content="Python Django APIs",
            target_role="Backend Engineer",
            skills=["Python", "Django"],
            status="active",
        )
        CareerTask.objects.create(
            user=self.user,
            title="Integration task",
            priority="medium",
            status="todo",
        )
        SavedSearch.objects.create(
            user=self.user,
            name="Backend",
            query="Backend",
            alerts_enabled=True,
        )

    def get(self, path):
        response = self.client.get(path)
        self.assertLess(response.status_code, 500, response.data if hasattr(response, "data") else response.content)
        return response

    def test_health_endpoint(self):
        response = self.get("/api/health/")
        self.assertEqual(response.status_code, 200)

    def test_review_workspace_endpoint(self):
        response = self.get("/api/review/workspace/")
        self.assertIn("overview", response.data)
        self.assertIn("action_queue", response.data)

    def test_search_insights_endpoint(self):
        response = self.get("/api/search-insights/")
        self.assertIn("coverage", response.data)
        self.assertIn("searches", response.data)

    def test_interview_prep_endpoint(self):
        response = self.get("/api/interview-prep/")
        self.assertIn("summary", response.data)
        self.assertIn("packets", response.data)

    def test_dashboard_snapshot_endpoint(self):
        response = self.get("/api/dashboard/snapshot/")
        self.assertIn("counts", response.data)
        self.assertEqual(response.data["counts"]["applications"], 1)

    def test_comparison_summary_endpoint(self):
        response = self.get("/api/applications/compare/summary/")
        self.assertIn("shortlist", response.data)
        self.assertEqual(response.data["applications"], 1)

    def test_timeline_dashboard_endpoint(self):
        response = self.get("/api/timeline/dashboard/")
        self.assertIn("events", response.data)
        self.assertTrue(response.data["events"])

    def test_task_analytics_endpoint(self):
        response = self.get("/api/tasks/analytics/")
        self.assertIn("summary", response.data)
        self.assertEqual(response.data["summary"]["open"], 1)

    def test_asset_readiness_endpoint(self):
        response = self.get("/api/career-assets/readiness/")
        self.assertIn("profile", response.data)
        self.assertIn("resumes", response.data)

    def test_application_explorer_endpoint(self):
        response = self.get("/api/applications/explorer/")
        self.assertIn("applications", response.data)
        self.assertEqual(response.data["counts"]["total"], 1)

    def test_application_explorer_search(self):
        response = self.get("/api/applications/explorer/?q=Integration")
        self.assertEqual(response.data["counts"]["total"], 1)

    def test_application_explorer_active_filter(self):
        response = self.get("/api/applications/explorer/?active=true")
        self.assertEqual(response.data["counts"]["active"], 1)

    def test_application_explorer_salary_filter(self):
        response = self.get("/api/applications/explorer/?salary=true")
        self.assertEqual(response.data["counts"]["with_salary"], 1)

    def test_application_explorer_status_filter(self):
        response = self.get("/api/applications/explorer/?status=applied")
        self.assertEqual(response.data["counts"]["total"], 1)

    def test_user_isolation_in_snapshot(self):
        JobApplication.objects.create(
            user=self.other,
            company="Private Co",
            role="Private Engineer",
            status="offer",
        )
        response = self.get("/api/dashboard/snapshot/")
        self.assertEqual(response.data["counts"]["applications"], 1)

    def test_user_isolation_in_explorer(self):
        JobApplication.objects.create(
            user=self.other,
            company="Private Co",
            role="Private Engineer",
            status="offer",
        )
        response = self.get("/api/applications/explorer/")
        companies = response.data["facets"]["companies"]
        self.assertNotIn("Private Co", companies)

    def test_review_actions_endpoint(self):
        response = self.get("/api/review/actions/?limit=5")
        self.assertIn("actions", response.data)

    def test_review_health_endpoint(self):
        response = self.get("/api/review/health/")
        self.assertIn("contact_health", response.data)
        self.assertIn("task_health", response.data)

    def test_search_summary_endpoint(self):
        response = self.get("/api/search-insights/summary/")
        self.assertIn("recommendations", response.data)

    def test_search_role_clusters_endpoint(self):
        response = self.get("/api/search-insights/roles/")
        self.assertIn("clusters", response.data)

    def test_search_location_clusters_endpoint(self):
        response = self.get("/api/search-insights/locations/")
        self.assertIn("clusters", response.data)

    def test_dashboard_focus_endpoint(self):
        response = self.get("/api/dashboard/focus/")
        self.assertIn("focus", response.data)

    def test_dashboard_company_endpoint(self):
        response = self.get("/api/dashboard/companies/?limit=5")
        self.assertIn("companies", response.data)

    def test_dashboard_activity_endpoint(self):
        response = self.get("/api/dashboard/activity/?days=7")
        self.assertEqual(response.data["days"], 7)

    def test_task_summary_endpoint(self):
        response = self.get("/api/tasks/analytics/summary/")
        self.assertEqual(response.data["open"], 1)

    def test_asset_recommendations_endpoint(self):
        response = self.get("/api/career-assets/recommendations/")
        self.assertIn("recommendations", response.data)

    def test_comparison_requires_two_ids(self):
        response = self.client.get("/api/applications/compare/")
        self.assertEqual(response.status_code, 400)

    def test_unauthenticated_intelligence_endpoint_is_denied(self):
        client = APIClient()
        response = client.get("/api/dashboard/snapshot/")
        self.assertIn(response.status_code, [401, 403])
