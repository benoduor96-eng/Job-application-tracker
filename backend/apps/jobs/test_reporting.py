from datetime import date, timedelta

from django.test import TestCase

from apps.jobs.models import JobApplication, Task
from apps.jobs.reporting import ReportingService


class ReportingServiceTests(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.app1 = JobApplication.objects.create(
            user=self.user,
            company="Acme",
            role="Senior Python Engineer",
            status="interview",
            priority=2,
            next_action="Prepare for technical review",
            next_action_date=date.today() + timedelta(days=2),
            salary_min=120000,
            salary_max=170000,
        )
        self.app2 = JobApplication.objects.create(
            user=self.user,
            company="Globex",
            role="Backend Engineer",
            status="applied",
            priority=1,
            next_action="Follow up",
            next_action_date=date.today() - timedelta(days=1),
            salary_min=100000,
            salary_max=140000,
        )

    def make_user(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.create_user(username="reporter", password="secret123")

    def test_dashboard_summary(self):
        service = ReportingService(self.user)
        summary = service.dashboard_summary()
        self.assertGreaterEqual(summary["total_applications"], 2)
        self.assertIn("by_status", summary)

    def test_status_distribution(self):
        service = ReportingService(self.user)
        distribution = service.status_distribution()
        self.assertTrue(distribution)

    def test_pipeline_health(self):
        service = ReportingService(self.user)
        health = service.pipeline_health()
        self.assertIn("screening_rate", health)
        self.assertIn("interview_rate", health)
        self.assertIn("offer_rate", health)

    def test_salary_statistics(self):
        service = ReportingService(self.user)
        salary = service.salary_statistics()
        self.assertIn("count", salary)
        self.assertEqual(salary["count"], 2)

    def test_recent_activity(self):
        service = ReportingService(self.user)
        activity = service.recent_activity(limit=5)
        self.assertTrue(activity)
