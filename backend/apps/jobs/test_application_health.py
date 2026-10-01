from django.contrib.auth import get_user_model
from django.test import TestCase

from .application_health import ApplicationHealthService
from .models import JobApplication


class ApplicationHealthTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="health", password="pass")
        self.app = JobApplication.objects.create(
            user=self.user, company="Acme", role="Engineer", status="interview"
        )

    def test_summary_contains_active_application(self):
        result = ApplicationHealthService(self.user).summary()
        self.assertEqual(result["count"], 1)
        self.assertIn("applications", result)

    def test_analysis_contains_health_signals(self):
        result = ApplicationHealthService(self.user).analyze(self.app.id)
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result.health_score, 0)
        self.assertLessEqual(result.health_score, 100)
        self.assertTrue(result.signals)

    def test_user_scoping(self):
        other = get_user_model().objects.create_user(username="other-health", password="pass")
        self.assertIsNone(ApplicationHealthService(other).analyze(self.app.id))

    def test_terminal_applications_are_not_in_summary(self):
        self.app.status = "rejected"
        self.app.save()
        self.assertEqual(ApplicationHealthService(self.user).summary()["count"], 0)
