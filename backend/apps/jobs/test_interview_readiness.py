from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from .interview_readiness import InterviewReadinessService
from .models import CareerTask, Interview, JobApplication, JobDescription


class InterviewReadinessTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="ready", password="pass")
        self.app = JobApplication.objects.create(
            user=self.user, company="Acme", role="Engineer",
            status="interview", notes="Prepare system design"
        )

    def test_readiness_rewards_preparation(self):
        Interview.objects.create(application=self.app, outcome="passed")
        JobDescription.objects.create(
            user=self.user, application=self.app, title="Engineer",
            company="Acme", raw_text="Build software", required_skills=["Python"]
        )
        result = InterviewReadinessService(self.user).analyze(self.app.id)
        self.assertEqual(result.score, 90)
        self.assertEqual(result.completed_interviews, 1)

    def test_open_and_overdue_tasks_reduce_readiness(self):
        CareerTask.objects.create(
            user=self.user, application=self.app, title="Study",
            status="todo", due_date=timezone.now() - timedelta(days=1)
        )
        result = InterviewReadinessService(self.user).analyze(self.app.id)
        self.assertEqual(result.overdue_tasks, 1)
        self.assertTrue(result.recommendations)

    def test_user_scoping(self):
        other = get_user_model().objects.create_user(username="other", password="pass")
        self.assertIsNone(InterviewReadinessService(other).analyze(self.app.id))

    def test_summary_only_active_pipeline(self):
        result = InterviewReadinessService(self.user).summary()
        self.assertEqual(result["count"], 1)
        self.app.status = "rejected"
        self.app.save()
        self.assertEqual(InterviewReadinessService(self.user).summary()["count"], 0)
