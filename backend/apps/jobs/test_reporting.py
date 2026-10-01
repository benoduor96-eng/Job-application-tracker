from datetime import date, timedelta

from django.test import TestCase

from apps.jobs.models import JobApplication
from apps.jobs.reporting import ReportingService


class ReportingServiceTests(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.app1 = JobApplication.objects.create(
            user=self.user, company="Acme", role="Senior Python Engineer",
            status="interview", next_action="Prepare for technical review",
            next_action_date=date.today() + timedelta(days=2), salary_min=120000, salary_max=170000,
        )
        self.app2 = JobApplication.objects.create(
            user=self.user, company="Globex", role="Backend Engineer",
            status="applied", next_action="Follow up",
            next_action_date=date.today() - timedelta(days=1), salary_min=100000, salary_max=140000,
        )

    def make_user(self):
        from django.contrib.auth import get_user_model
        return get_user_model().objects.create_user(username="reporter", password="secret123")

    def test_dashboard_summary(self):
        summary = ReportingService(self.user).dashboard_summary()
        self.assertGreaterEqual(summary["total_applications"], 2)
        self.assertIn("by_status", summary)

    def test_status_distribution(self):
        self.assertTrue(ReportingService(self.user).status_distribution())

    def test_pipeline_health(self):
        health = ReportingService(self.user).pipeline_health()
        self.assertIn("screening_rate", health)
        self.assertIn("interview_rate", health)
        self.assertIn("offer_rate", health)

    def test_salary_statistics(self):
        salary = ReportingService(self.user).salary_statistics()
        self.assertIn("count", salary)
        self.assertEqual(salary["count"], 2)

    def test_recent_activity(self):
        self.assertTrue(ReportingService(self.user).recent_activity(limit=5))
