from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase

from .compensation_analysis import CompensationAnalysisService
from .models import CareerProfile, JobApplication


class CompensationAnalysisTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="pay", password="pass")
        CareerProfile.objects.create(
            user=self.user,
            minimum_salary=Decimal("70000"),
            target_salary=Decimal("100000"),
        )
        self.app = JobApplication.objects.create(
            user=self.user, company="Acme", role="Engineer",
            status="offer", salary_min=Decimal("90000"),
            salary_max=Decimal("110000"),
        )

    def test_midpoint_and_target_position(self):
        result = CompensationAnalysisService(self.user).analyze(self.app.id)
        self.assertEqual(result.midpoint, Decimal("100000"))
        self.assertEqual(result.position, "at_or_above_target")
        self.assertEqual(result.midpoint_vs_minimum, Decimal("42.85714285714285714285714286"))

    def test_missing_salary_is_unknown(self):
        self.app.salary_min = None
        self.app.salary_max = None
        self.app.save()
        result = CompensationAnalysisService(self.user).analyze(self.app.id)
        self.assertIsNone(result.midpoint)
        self.assertEqual(result.position, "unknown")

    def test_user_scoping(self):
        other = get_user_model().objects.create_user(username="other-pay", password="pass")
        self.assertIsNone(CompensationAnalysisService(other).analyze(self.app.id))

    def test_summary_counts_salary_records(self):
        result = CompensationAnalysisService(self.user).summary()
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["with_salary"], 1)
