from django.contrib.auth.models import User
from django.test import TestCase
from .models import CareerTask, JobApplication
from .task_analytics import TaskAnalytics


class TaskAnalyticsBoundaryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="task-boundary", password="pass12345")

    def test_empty_task_dashboard_has_zero_values(self):
        data = TaskAnalytics(self.user).dashboard()
        self.assertEqual(data["summary"]["total"], 0)
        self.assertEqual(data["summary"]["open"], 0)
        self.assertEqual(data["summary"]["completion_rate"], 0)
        self.assertEqual(data["priorities"][0]["count"], 0)

    def test_completed_task_is_not_in_due_window(self):
        task = CareerTask.objects.create(
            user=self.user, title="Completed", status="done",
            priority="high"
        )
        data = TaskAnalytics(self.user).due_window()
        self.assertNotIn(task.id, {row["id"] for row in data})

    def test_cancelled_task_is_not_overdue(self):
        task = CareerTask.objects.create(
            user=self.user, title="Cancelled", status="cancelled",
            priority="urgent"
        )
        rows = TaskAnalytics(self.user).overdue()
        self.assertNotIn(task.id, {row["id"] for row in rows})

    def test_tags_ignore_blank_values(self):
        CareerTask.objects.create(
            user=self.user, title="Tagged", status="todo",
            priority="medium", tags=["", "  ", "Interview"]
        )
        tags = TaskAnalytics(self.user).tags()
        self.assertEqual(tags, [{"tag": "interview", "count": 1}])

    def test_application_load_requires_linked_application(self):
        app = JobApplication.objects.create(
            user=self.user, company="TaskCo", role="Engineer", status="applied"
        )
        CareerTask.objects.create(
            user=self.user, application=app, title="Linked",
            status="todo", priority="high"
        )
        data = TaskAnalytics(self.user).application_load()
        self.assertEqual(data, [{"application_id": app.id, "open_tasks": 1}])

    def test_priority_breakdown_includes_zero_counts(self):
        rows = TaskAnalytics(self.user).priority_breakdown()
        self.assertEqual(len(rows), 4)
        self.assertEqual({row["priority"] for row in rows}, {"urgent", "high", "medium", "low"})
