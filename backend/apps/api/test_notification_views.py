from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from apps.jobs.models import JobApplication, CareerTask


class NotificationPlanApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="notification-api",
            password="test-password",
        )
        self.client.force_authenticate(self.user)

    def test_plan_returns_only_active_pipeline(self):
        active = JobApplication.objects.create(
            user=self.user,
            company="Acme",
            role="Backend Engineer",
            status="applied",
        )
        JobApplication.objects.create(
            user=self.user,
            company="Closed",
            role="Engineer",
            status="rejected",
        )

        response = self.client.get("/api/notifications/plan/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["summary"]["count"], 1)
        self.assertEqual(response.data["plans"][0]["application_id"], active.id)

    def test_post_creates_idempotent_tasks(self):
        JobApplication.objects.create(
            user=self.user,
            company="Acme",
            role="Backend Engineer",
            status="interview",
        )

        first = self.client.post("/api/notifications/plan/")
        second = self.client.post("/api/notifications/plan/")

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(CareerTask.objects.filter(user=self.user).count(), 1)
