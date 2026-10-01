from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from .health_metrics import HealthMetricsService
from .models import JobApplication, JobDescription
from .recommendations import RecommendationEngine
from .reporting import ReportingService


class ReportingInsightsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="insights-user", password="test-password")
        self.interview = JobApplication.objects.create(
            user=self.user, company="Acme", role="Backend Engineer",
            status="interview", salary_min=90000, salary_max=130000,
            requirements="python django postgres api",
            next_action="Prepare technical interview",
            next_action_date=date.today() + timedelta(days=2),\n        )\n        JobDescription.objects.create(user=self.user, application=self.interview, title="Backend Engineer", company="Acme", raw_text="python django postgres api", required_skills=["python", "django", "postgres"])
        )
        self.applied = JobApplication.objects.create(
            user=self.user, company="Globex", role="Platform Engineer",
            status="applied", salary_min=80000, salary_max=110000,
            requirements="python docker kubernetes",
            next_action="Send follow-up",
            next_action_date=date.today() - timedelta(days=1),\n        )\n        JobDescription.objects.create(user=self.user, application=self.applied, title="Platform Engineer", company="Globex", raw_text="python docker kubernetes", required_skills=["python", "docker", "kubernetes"])
        )

    def test_dashboard_contains_pipeline_totals(self):
        summary = ReportingService(self.user).dashboard_summary()
        self.assertEqual(summary["total_applications"], 2)
        self.assertEqual(summary["interviews"], 1)
        self.assertIn("by_status", summary)

    def test_salary_statistics(self):
        stats = ReportingService(self.user).salary_statistics()
        self.assertEqual(stats["count"], 2)
        self.assertEqual(stats["avg_min"], 85000)

    def test_attention_queue_finds_active_work(self):
        queue = ReportingService(self.user).attention_queue()
        self.assertTrue(any(row["company"] == "Globex" for row in queue))

    def test_recommendation_engine_ranks_actions(self):
        actions = RecommendationEngine(self.user).rank_actions()
        self.assertTrue(actions)
        self.assertIn("score", actions[0])

    def test_health_score_is_bounded(self):
        result = HealthMetricsService(self.user).health_score()
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)
