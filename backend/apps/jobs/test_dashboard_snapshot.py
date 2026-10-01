from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from .models import JobApplication, Interview, CareerContact, CareerTask, ApplicationActivity
from .dashboard_snapshot import DashboardSnapshot


class DashboardSnapshotTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="snapshot", password="pass12345")
        self.today = date(2026, 10, 2)
        self.saved = self.app("Alpha", "Python Engineer", "saved")
        self.applied = self.app("Beta", "Backend Engineer", "applied", applied_date=self.today - timedelta(days=8))
        self.interview = self.app("Gamma", "Platform Engineer", "interview", applied_date=self.today - timedelta(days=12), next_action_date=self.today)
        self.offer = self.app("Gamma", "Senior Platform Engineer", "offer", applied_date=self.today - timedelta(days=20), salary_min=90000, salary_max=120000)
        self.rejected = self.app("Delta", "Engineer", "rejected", applied_date=self.today - timedelta(days=30), salary_min=50000, salary_max=60000)
        Interview.objects.create(application=self.interview, interview_type="technical", scheduled_date=timezone.now()+timedelta(days=3), outcome="scheduled", interviewer_name="Jane")
        CareerContact.objects.create(user=self.user, name="Recruiter", company="Gamma", application=self.interview, next_follow_up=timezone.now()-timedelta(days=1))
        CareerContact.objects.create(user=self.user, name="Coach", company="Other")
        CareerTask.objects.create(user=self.user, title="Prepare", priority="urgent", status="todo", due_date=timezone.now()-timedelta(days=1))
        CareerTask.objects.create(user=self.user, title="Done", priority="low", status="done")
        ApplicationActivity.objects.create(user=self.user, application=self.applied, activity_type="email", title="Email sent", occurred_at=timezone.now())

    def app(self, company, role, status, **extra):
        values = {"user": self.user, "company": company, "role": role, "status": status}
        values.update(extra)
        return JobApplication.objects.create(**values)

    def service(self):
        return DashboardSnapshot(self.user, now=timezone.make_aware(timezone.datetime(2026, 10, 2, 12, 0)))

    def test_counts_include_pipeline_and_workload(self):
        counts = self.service().counts()
        self.assertEqual(counts["applications"], 5)
        self.assertEqual(counts["active"], 4)
        self.assertEqual(counts["closed"], 1)
        self.assertEqual(counts["open_tasks"], 1)
        self.assertEqual(counts["contacts"], 2)

    def test_activity_window_groups_types_and_dates(self):
        data = self.service().activity_window()
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["by_type"]["email"], 1)
        self.assertEqual(len(data["daily"]), 1)

    def test_velocity_has_current_and_previous_windows(self):
        data = self.service().application_velocity()
        self.assertEqual(data["window_days"], 30)
        self.assertGreaterEqual(data["applications"], 1)
        self.assertIn(data["direction"], {"up", "down", "steady"})

    def test_response_metrics_use_interview_records(self):
        data = self.service().response_metrics()
        self.assertEqual(data["applied_with_date"], 4)
        self.assertEqual(data["applications_reaching_interview"], 1)
        self.assertGreater(data["interview_rate"], 0)

    def test_salary_snapshot_uses_midpoints(self):
        data = self.service().salary_snapshot()
        self.assertEqual(data["applications_with_salary"], 2)
        self.assertEqual(Decimal(data["average_midpoint"]), Decimal("80000.00"))
        self.assertEqual(data["active_with_salary"], 1)

    def test_deadlines_separate_due_and_overdue(self):
        data = self.service().deadlines()
        self.assertEqual(data["due_today"], 1)
        self.assertEqual(data["overdue"], 0)

    def test_interview_window_is_user_scoped(self):
        other = User.objects.create_user(username="other", password="pass12345")
        other_app = JobApplication.objects.create(user=other, company="Secret", role="Engineer", status="interview")
        Interview.objects.create(application=other_app, scheduled_date=timezone.now()+timedelta(days=2))
        rows = self.service().interview_window()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["company"], "Gamma")

    def test_workload_detects_urgent_and_overdue_contact(self):
        data = self.service().workload()
        self.assertEqual(data["urgent_tasks"], 1)
        self.assertEqual(data["overdue_tasks"], 1)
        self.assertEqual(data["overdue_contact_followups"], 1)
        self.assertEqual(data["never_contacted"], 1)

    def test_company_leaderboard_groups_company_records(self):
        self.app("Gamma", "QA Engineer", "applied")
        rows = self.service().company_leaderboard()
        gamma = next(row for row in rows if row["company"] == "Gamma")
        self.assertEqual(gamma["applications"], 3)
        self.assertEqual(gamma["active"], 3)
        self.assertEqual(gamma["interviews"], 1)
        self.assertEqual(gamma["offers"], 1)

    def test_focus_items_prioritize_interviews_and_tasks(self):
        items = self.service().focus_items()
        self.assertTrue(items)
        priorities = [item["priority"] for item in items]
        self.assertEqual(priorities, sorted(priorities, reverse=True))
        self.assertTrue(any(item["type"] == "interview" for item in items))
        self.assertTrue(any(item["type"] == "task" for item in items))

    def test_dashboard_contains_all_sections(self):
        data = self.service().dashboard()
        expected = {"generated_at","counts","velocity","activity","response","salary","deadlines","interviews","workload","companies","focus"}
        self.assertEqual(set(data), expected)

    def test_empty_user_returns_safe_defaults(self):
        user = User.objects.create_user(username="empty-snapshot", password="pass12345")
        data = DashboardSnapshot(user).dashboard()
        self.assertEqual(data["counts"]["applications"], 0)
        self.assertEqual(data["salary"]["applications_with_salary"], 0)
        self.assertEqual(data["response"]["interview_rate"], 0)
        self.assertEqual(data["focus"], [])

    def test_company_limit_is_respected(self):
        for index in range(20):
            self.app(f"Company {index}", "Engineer", "applied")
        rows = self.service().company_leaderboard(limit=5)
        self.assertEqual(len(rows), 5)

    def test_activity_window_can_be_shortened(self):
        data = self.service().activity_window(days=1)
        self.assertEqual(data["days"], 1)

    def test_velocity_can_be_shortened(self):
        data = self.service().application_velocity(days=7)
        self.assertEqual(data["window_days"], 7)
        self.assertGreaterEqual(data["daily_average"], 0)

    def test_interview_window_can_be_shortened(self):
        rows = self.service().interview_window(days=1)
        self.assertEqual(rows, [])

    def test_salary_min_only_is_supported(self):
        self.app("Minimum", "Engineer", "applied", salary_min=Decimal("100000"))
        data = self.service().salary_snapshot()
        self.assertEqual(data["applications_with_salary"], 3)
        self.assertEqual(data["maximum"], "105000")

    def test_salary_max_only_is_supported(self):
        self.app("Maximum", "Engineer", "applied", salary_max=Decimal("70000"))
        data = self.service().salary_snapshot()
        self.assertEqual(data["applications_with_salary"], 3)
        self.assertEqual(data["minimum"], "55000")

    def test_closed_records_do_not_count_as_active(self):
        self.app("Closed", "Engineer", "withdrawn")
        self.assertEqual(self.service().counts()["active"], 4)
        self.assertEqual(self.service().counts()["closed"], 2)

    def test_dashboard_focus_contains_application_identifiers(self):
        items = self.service().focus_items()
        interview_items = [item for item in items if item["type"] == "interview"]
        self.assertEqual(interview_items[0]["application_id"], self.interview.id)
