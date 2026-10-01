from datetime import date, timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from .models import JobApplication, Interview, CareerContact, CareerTask, ApplicationActivity
from .review_workspace import ReviewWorkspace


class ReviewWorkspaceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reviewer", password="pass12345")
        self.today = date(2026, 10, 2)
        self.saved = self.make_app("Acme", "Backend Engineer", "saved")
        self.applied = self.make_app("Beta", "Python Engineer", "applied", applied_date=self.today - timedelta(days=10))
        self.interview = self.make_app("Gamma", "Platform Engineer", "interview", applied_date=self.today - timedelta(days=25), next_action_date=self.today)
        self.offer = self.make_app("Gamma", "Senior Platform Engineer", "offer", applied_date=self.today - timedelta(days=18))
        self.rejected = self.make_app("Delta", "Developer", "rejected", applied_date=self.today - timedelta(days=40))
        Interview.objects.create(application=self.interview, interview_type="technical", scheduled_date=timezone.now()+timedelta(days=3), outcome="scheduled")
        CareerContact.objects.create(user=self.user, name="Recruiter", company="Gamma", application=self.interview, next_follow_up=timezone.now()-timedelta(days=2))
        CareerContact.objects.create(user=self.user, name="Coach", company="Other")
        CareerTask.objects.create(user=self.user, title="Prepare interview", priority="high", status="todo", due_date=timezone.now()-timedelta(days=1))
        ApplicationActivity.objects.create(user=self.user, application=self.applied, activity_type="email", title="Follow up", occurred_at=timezone.now())

    def make_app(self, company, role, status, **kwargs):
        values = {"user": self.user, "company": company, "role": role, "status": status}
        values.update(kwargs)
        return JobApplication.objects.create(**values)

    def service(self):
        return ReviewWorkspace(self.user, today=self.today)

    def test_overview_counts_real_records(self):
        data = self.service().overview()
        self.assertEqual(data["totals"]["applications"], 5)
        self.assertEqual(data["totals"]["active"], 4)
        self.assertEqual(data["attention"]["due_today"], 1)
        self.assertEqual(data["totals"]["contacts"], 2)

    def test_status_counts_contains_every_pipeline_status(self):
        counts = self.service().status_counts()
        self.assertEqual(set(counts), {"saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn"})
        self.assertEqual(counts["offer"], 1)

    def test_action_queue_prioritizes_due_work(self):
        actions = self.service().action_queue()
        self.assertTrue(actions)
        self.assertEqual(actions[0]["application_id"], self.interview.id)
        self.assertGreaterEqual(actions[0]["priority"], 90)

    def test_missing_next_action_is_actionable(self):
        actions = self.service().action_queue()
        saved = [x for x in actions if x.get("application_id") == self.saved.id]
        self.assertTrue(saved)
        self.assertEqual(saved[0]["kind"], "missing_plan")

    def test_company_summary_groups_case_insensitively(self):
        JobApplication.objects.create(user=self.user, company="gamma", role="QA", status="applied")
        companies = self.service().company_summary()
        gamma = [x for x in companies if x["company"].lower() == "gamma"][0]
        self.assertEqual(gamma["applications"], 3)
        self.assertEqual(gamma["active"], 3)

    def test_funnel_rates_are_bounded_percentages(self):
        funnel = self.service().funnel()
        for value in funnel["conversion_rates"].values():
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 100)

    def test_interview_calendar_is_user_scoped(self):
        other = User.objects.create_user(username="other", password="pass12345")
        other_app = JobApplication.objects.create(user=other, company="Secret", role="Engineer", status="interview")
        Interview.objects.create(application=other_app, scheduled_date=timezone.now()+timedelta(days=2))
        rows = self.service().interview_calendar()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["application_id"], self.interview.id)

    def test_contact_health(self):
        health = self.service().contact_health()
        self.assertEqual(health["total"], 2)
        self.assertEqual(health["never_contacted"], 1)
        self.assertEqual(health["with_application"], 1)
        self.assertEqual(health["overdue_followups"], 1)

    def test_task_health(self):
        health = self.service().task_health()
        self.assertEqual(health["open"], 1)
        self.assertEqual(health["overdue"], 1)
        self.assertEqual(health["completed"], 0)

    def test_risk_detects_aging_early_stage(self):
        risk = self.service().risk_summary()
        self.assertGreaterEqual(risk.get("aging_early_stage", 0), 1)

    def test_full_review_contains_all_sections(self):
        review = self.service().full_review()
        self.assertEqual(set(review), {"overview", "action_queue", "companies", "funnel", "interviews", "contact_health", "task_health"})

    def test_limit_is_respected(self):
        actions = self.service().action_queue(limit=1)
        self.assertLessEqual(len(actions), 1)

    def test_momentum_has_current_and_previous_periods(self):
        momentum = self.service().momentum()
        self.assertIn("applications_this_week", momentum)
        self.assertIn("applications_previous_week", momentum)
        self.assertIn(momentum["direction"], {"up", "down", "steady"})

    def test_closed_applications_do_not_receive_missing_plan(self):
        actions = self.service().action_queue()
        ids = {x.get("application_id") for x in actions}
        self.assertNotIn(self.rejected.id, ids)

    def test_interview_window_can_be_customized(self):
        rows = self.service().interview_calendar(days=1)
        self.assertEqual(rows, [])

    def test_review_is_deterministic_for_same_snapshot(self):
        first = self.service().full_review()
        second = self.service().full_review()
        self.assertEqual(first["overview"]["status_counts"], second["overview"]["status_counts"])
        self.assertEqual(first["funnel"], second["funnel"])
