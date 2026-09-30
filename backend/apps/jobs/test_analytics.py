from django.contrib.auth import get_user_model
from django.test import TestCase
from apps.jobs.analytics import application_funnel, company_breakdown, response_metrics, stale_applications
from apps.jobs.models import JobApplication


User = get_user_model()


class AnalyticsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="analytics", password="pass12345")

    def make(self, company, status):
        return JobApplication.objects.create(user=self.user, company=company, role="Engineer", status=status)

    def test_funnel_contains_all_stages(self):
        self.make("Acme", "applied")
        result = application_funnel(JobApplication.objects.filter(user=self.user))
        self.assertEqual(result["total"], 1)
        self.assertEqual(len(result["stages"]), 7)
        self.assertEqual(result["stages"][1]["count"], 1)

    def test_response_metrics_calculates_rates(self):
        self.make("Acme", "interview")
        self.make("Beta", "offer")
        result = response_metrics(JobApplication.objects.filter(user=self.user))
        self.assertEqual(result["interview_rate"], 50.0)
        self.assertEqual(result["offer_rate"], 50.0)

    def test_company_breakdown_groups_applications(self):
        self.make("Acme", "applied")
        self.make("Acme", "interview")
        rows = company_breakdown(JobApplication.objects.filter(user=self.user))
        self.assertEqual(rows[0]["company"], "Acme")
        self.assertEqual(rows[0]["total"], 2)
