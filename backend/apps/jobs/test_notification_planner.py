from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from .models import CareerTask, JobApplication
from .notification_planner import (
    create_notification_tasks,
    plan_application_notifications,
    summarize_notification_plan,
)


class NotificationPlannerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="planner",
            password="test-password",
        )
        self.now = timezone.now()

    def test_plan_uses_status_specific_delay(self):
        application = JobApplication.objects.create(
            user=self.user,
            company="Acme",
            role="Backend Engineer",
            status="applied",
        )
        application.updated_at = self.now
        application.save(update_fields=["updated_at"])

        plans = plan_application_notifications([application], self.now)
        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0].priority, "medium")
        self.assertEqual(plans[0].due_at.date(), (self.now + timedelta(days=5)).date())

    def test_ignores_terminal_statuses(self):
        application = JobApplication.objects.create(
            user=self.user,
            company="Acme",
            role="Backend Engineer",
            status="rejected",
        )
        self.assertEqual(plan_application_notifications([application], self.now), [])

    def test_task_creation_is_idempotent(self):
        application = JobApplication.objects.create(
            user=self.user,
            company="Acme",
            role="Backend Engineer",
            status="interview",
        )
        first = create_notification_tasks(self.user, [application], self.now)
        second = create_notification_tasks(self.user, [application], self.now)

        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 1)
        self.assertEqual(CareerTask.objects.count(), 1)

    def test_summary_counts_priorities(self):
        applications = [
            JobApplication.objects.create(
                user=self.user,
                company="Acme",
                role="Backend",
                status="interview",
            ),
            JobApplication.objects.create(
                user=self.user,
                company="Beta",
                role="Engineer",
                status="applied",
            ),
        ]
        summary = summarize_notification_plan(
            plan_application_notifications(applications, self.now)
        )
        self.assertEqual(summary["count"], 2)
        self.assertEqual(summary["by_priority"]["high"], 1)
        self.assertEqual(summary["by_priority"]["medium"], 1)
