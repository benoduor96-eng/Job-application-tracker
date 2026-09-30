from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.jobs.models import CareerTask, Resume


User = get_user_model()


class CareerAssetApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="assets-user", password="pass12345")
        self.other = User.objects.create_user(username="other-user", password="pass12345")
        self.client.force_authenticate(self.user)

    def test_resume_is_scoped_to_authenticated_user(self):
        Resume.objects.create(user=self.other, name="Private", version=1)
        response = self.client.get("/api/resumes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)

    def test_resume_active_endpoint_returns_active_resume(self):
        resume = Resume.objects.create(
            user=self.user,
            name="Backend Resume",
            target_role="Backend Engineer",
            status="active",
            skills=["Python", "Django"],
        )
        response = self.client.get("/api/resumes/active/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], resume.id)

    def test_task_cannot_reference_another_users_application(self):
        from apps.jobs.models import JobApplication
        application = JobApplication.objects.create(
            user=self.other,
            company="Other Co",
            role="Engineer",
        )
        response = self.client.post(
            "/api/tasks/",
            {"title": "Private task", "application": application.id},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_overdue_excludes_completed_tasks(self):
        CareerTask.objects.create(
            user=self.user,
            title="Overdue",
            due_date=timezone.now() - timedelta(days=1),
        )
        CareerTask.objects.create(
            user=self.user,
            title="Completed",
            status="done",
            due_date=timezone.now() - timedelta(days=1),
        )
        response = self.client.get("/api/tasks/overdue/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Overdue")

    def test_complete_action_sets_completion_timestamp(self):
        task = CareerTask.objects.create(user=self.user, title="Follow up")
        response = self.client.post(f"/api/tasks/{task.id}/complete/")
        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.status, "done")
        self.assertIsNotNone(task.completed_at)
