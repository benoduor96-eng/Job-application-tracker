from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from .models import JobApplication, SavedSearch
from .search_insights import SearchInsights


class SearchInsightsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="searcher", password="pass12345")
        self.other = User.objects.create_user(username="other-searcher", password="pass12345")
        self.remote = SavedSearch.objects.create(
            user=self.user, name="Remote Python", query="Python Engineer",
            location="Remote", remote_only=True, min_salary=Decimal("70000"), alerts_enabled=True
        )
        self.backend = SavedSearch.objects.create(
            user=self.user, name="Backend", query="backend", location="Nairobi", status="applied"
        )
        self.make_app("Acme", "Python Engineer", "applied", "Remote", 80000, 90000)
        self.make_app("Beta", "Backend Engineer", "screening", "Nairobi", 60000, 70000)
        self.make_app("Gamma", "Designer", "rejected", "Nairobi", 50000, 60000)
        JobApplication.objects.create(user=self.other, company="Secret", role="Python Engineer", status="applied", location="Remote")

    def make_app(self, company, role, status, location, minimum, maximum):
        return JobApplication.objects.create(
            user=self.user, company=company, role=role, status=status,
            location=location, salary_min=minimum, salary_max=maximum
        )

    def service(self):
        return SearchInsights(self.user)

    def test_query_tokens_match_role(self):
        summary = self.service().search_summary(self.remote)
        self.assertEqual(summary["applications"], 1)
        self.assertEqual(summary["active_applications"], 1)

    def test_salary_floor_is_respected(self):
        summary = self.service().search_summary(self.remote)
        self.assertEqual(summary["applications"], 1)

    def test_location_and_status_filters_work_together(self):
        summary = self.service().search_summary(self.backend)
        self.assertEqual(summary["applications"], 1)
        self.assertEqual(summary["active_applications"], 1)

    def test_all_summaries_are_user_scoped(self):
        rows = self.service().all_summaries()
        self.assertEqual(len(rows), 2)
        self.assertEqual({row["name"] for row in rows}, {"Remote Python", "Backend"})

    def test_coverage_is_calculated(self):
        coverage = self.service().coverage()
        self.assertEqual(coverage["applications"], 3)
        self.assertGreaterEqual(coverage["covered_applications"], 1)
        self.assertLessEqual(coverage["coverage_rate"], 100)

    def test_role_clusters_are_sorted_by_volume(self):
        rows = self.service().role_clusters()
        self.assertGreaterEqual(len(rows), 2)
        self.assertGreaterEqual(rows[0]["applications"], rows[-1]["applications"])

    def test_location_clusters_include_unspecified_when_needed(self):
        JobApplication.objects.create(user=self.user, company="NoLocation", role="Engineer", status="saved")
        rows = self.service().location_clusters()
        self.assertTrue(any(row["location"] == "Unspecified" for row in rows))

    def test_recommendations_detect_empty_search(self):
        empty = SavedSearch.objects.create(user=self.user, name="Unused", query="Astronaut")
        rows = self.service().recommendations()
        match = [row for row in rows if row["search_id"] == empty.id]
        self.assertEqual(match[0]["type"], "no_matches")

    def test_recommendations_detect_large_active_pipeline(self):
        for index in range(5):
            self.make_app(f"Large{index}", "Python Engineer", "applied", "Remote", 80000, 90000)
        rows = self.service().recommendations()
        self.assertTrue(any(row["type"] == "attention" for row in rows))

    def test_dashboard_has_all_analysis_sections(self):
        data = self.service().dashboard()
        self.assertEqual(set(data), {"coverage", "searches", "role_clusters", "location_clusters", "recommendations"})

    def test_other_users_are_not_counted(self):
        self.assertEqual(self.service().coverage()["applications"], 3)

    def test_empty_dataset_is_safe(self):
        user = User.objects.create_user(username="empty", password="pass12345")
        data = SearchInsights(user).dashboard()
        self.assertEqual(data["coverage"]["applications"], 0)
        self.assertEqual(data["coverage"]["coverage_rate"], 0.0)
        self.assertEqual(data["recommendations"], [])

    def test_salary_max_does_not_exclude_application_without_minimum(self):
        search = SavedSearch.objects.create(user=self.user, name="Salary Cap", query="Designer", max_salary=Decimal("70000"))
        summary = self.service().search_summary(search)
        self.assertEqual(summary["applications"], 1)

    def test_blank_query_matches_all_other_filters(self):
        search = SavedSearch.objects.create(user=self.user, name="All Nairobi", location="Nairobi")
        summary = self.service().search_summary(search)
        self.assertEqual(summary["applications"], 2)

    def test_status_filter_excludes_other_statuses(self):
        search = SavedSearch.objects.create(user=self.user, name="Only Offers", status="offer")
        self.assertEqual(self.service().search_summary(search)["applications"], 0)

    def test_dashboard_recommendations_are_structured(self):
        for item in self.service().recommendations():
            self.assertIn(item["type"], {"no_matches","inactive","attention","missing_search"})
            self.assertIn(item["priority"], {"low","medium","high"})
            self.assertTrue(item["title"])
            self.assertTrue(item["detail"])
