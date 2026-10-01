from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from .models import CareerTask
from .task_analytics import TaskAnalytics


class TaskAnalyticsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tasks", password="pass12345")
        self.now = timezone.now()
        self.make("Urgent", "urgent", "todo", self.now-timedelta(days=1), ["interview", "prep"])
        self.make("Today", "high", "in_progress", self.now, ["interview"])
        self.make("Done", "medium", "done", self.now-timedelta(days=2), ["complete"])
        self.make("Future", "low", "todo", self.now+timedelta(days=5), ["research"])
        self.make("Cancelled", "low", "cancelled", None, [])

    def make(self, title, priority, status, due_date, tags):
        return CareerTask.objects.create(user=self.user, title=title, priority=priority, status=status, due_date=due_date, tags=tags)

    def service(self):
        return TaskAnalytics(self.user, now=self.now)

    def test_summary_counts_open_and_terminal_tasks(self):
        data = self.service().summary()
        self.assertEqual(data["total"], 5)
        self.assertEqual(data["open"], 3)
        self.assertEqual(data["done"], 1)
        self.assertEqual(data["cancelled"], 1)

    def test_summary_detects_overdue_and_today(self):
        data = self.service().summary()
        self.assertEqual(data["overdue"], 1)
        self.assertEqual(data["due_today"], 1)

    def test_completion_rate_is_percentage(self):
        self.assertEqual(self.service().summary()["completion_rate"], 20.0)

    def test_priority_breakdown_has_stable_order(self):
        rows = self.service().priority_breakdown()
        self.assertEqual([row["priority"] for row in rows], ["urgent", "high", "medium", "low"])
        self.assertEqual(rows[0]["count"], 1)

    def test_due_window_excludes_overdue(self):
        rows = self.service().due_window(days=14)
        titles = {row["title"] for row in rows}
        self.assertEqual(titles, {"Today", "Future"})

    def test_overdue_returns_oldest_first(self):
        rows = self.service().overdue()
        self.assertEqual(rows[0]["title"], "Urgent")

    def test_tags_are_case_insensitive(self):
        self.make("Tag", "low", "todo", None, ["Interview", "interview"])
        rows = self.service().tags()
        interview = next(row for row in rows if row["tag"] == "interview")
        self.assertEqual(interview["count"], 3)

    def test_application_load_ignores_unlinked_tasks(self):
        self.make("Unlinked", "medium", "todo", None, [])
        rows = self.service().application_load()
        self.assertEqual(rows, [])

    def test_other_users_are_not_counted(self):
        other = User.objects.create_user(username="other-tasks", password="pass12345")
        CareerTask.objects.create(user=other, title="Private", priority="urgent", status="todo")
        self.assertEqual(self.service().summary()["total"], 5)

    def test_dashboard_has_all_sections(self):
        data = self.service().dashboard()
        self.assertEqual(set(data), {"summary", "priorities", "due_window", "overdue", "application_load", "tags"})
