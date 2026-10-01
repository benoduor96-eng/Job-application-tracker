from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from .models import JobApplication, Interview, ApplicationActivity, CareerTask
from .application_timeline import ApplicationTimeline


class ApplicationTimelineTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="timeline", password="pass12345")
        self.other = User.objects.create_user(username="other-timeline", password="pass12345")
        self.application = JobApplication.objects.create(
            user=self.user, company="Acme", role="Backend Engineer", status="interview"
        )
        self.second = JobApplication.objects.create(
            user=self.user, company="Beta", role="Python Engineer", status="applied"
        )
        ApplicationActivity.objects.create(
            user=self.user, application=self.application, activity_type="email",
            title="Recruiter email", description="Scheduling", occurred_at=timezone.now()-timedelta(days=2)
        )
        ApplicationActivity.objects.create(
            user=self.user, application=self.application, activity_type="note",
            title="Research notes", occurred_at=timezone.now()-timedelta(days=1)
        )
        Interview.objects.create(
            application=self.application, interview_type="technical",
            scheduled_date=timezone.now()+timedelta(days=2), outcome="scheduled",
            interviewer_name="Jane"
        )
        CareerTask.objects.create(
            user=self.user, application=self.application, title="Prepare examples",
            priority="high", status="todo", due_date=timezone.now()+timedelta(days=1)
        )

    def service(self):
        return ApplicationTimeline(self.user)

    def test_application_events_include_all_sources(self):
        events = self.service().events_for_application(self.application.id)
        sources = {event["source"] for event in events}
        self.assertEqual(sources, {"application", "activity", "interview", "task"})

    def test_application_created_event_is_present(self):
        events = self.service().events_for_application(self.application.id)
        self.assertTrue(any(event["kind"] == "created" for event in events))

    def test_activity_metadata_is_preserved(self):
        activity = ApplicationActivity.objects.create(
            user=self.user, application=self.application, activity_type="document",
            title="Resume", metadata={"version": 2}, occurred_at=timezone.now()
        )
        events = self.service().events_for_application(self.application.id)
        row = next(event for event in events if event["id"] == f"activity-{activity.id}")
        self.assertEqual(row["metadata"]["version"], 2)

    def test_interview_metadata_contains_outcome(self):
        events = self.service().events_for_application(self.application.id)
        row = next(event for event in events if event["kind"] == "interview_scheduled")
        self.assertEqual(row["metadata"]["outcome"], "scheduled")
        self.assertEqual(row["metadata"]["interviewer"], "Jane")

    def test_task_metadata_contains_priority(self):
        events = self.service().events_for_application(self.application.id)
        row = next(event for event in events if event["source"] == "task")
        self.assertEqual(row["metadata"]["priority"], "high")

    def test_events_are_newest_first(self):
        events = self.service().events_for_application(self.application.id)
        timestamps = [event["occurred_at"] for event in events]
        self.assertEqual(timestamps, sorted(timestamps, reverse=True))

    def test_missing_application_returns_none(self):
        self.assertIsNone(self.service().events_for_application(99999))

    def test_all_events_are_user_scoped(self):
        other_app = JobApplication.objects.create(user=self.other, company="Secret", role="Engineer")
        ApplicationActivity.objects.create(
            user=self.other, application=other_app, activity_type="email",
            title="Private", occurred_at=timezone.now()
        )
        events = self.service().all_events()
        ids = {event["application_id"] for event in events}
        self.assertNotIn(other_app.id, ids)
        self.assertIn(self.application.id, ids)

    def test_filter_by_kind(self):
        events = self.service().filter_events(kind="email")
        self.assertTrue(events)
        self.assertTrue(all(event["kind"] == "email" for event in events))

    def test_filter_by_source(self):
        events = self.service().filter_events(source="interview")
        self.assertTrue(events)
        self.assertTrue(all(event["source"] == "interview" for event in events))

    def test_filter_by_application(self):
        events = self.service().filter_events(application_id=self.application.id)
        self.assertTrue(events)
        self.assertTrue(all(event["application_id"] == self.application.id for event in events))

    def test_invalid_application_filter_returns_empty(self):
        self.assertEqual(self.service().filter_events(application_id="not-a-number"), [])

    def test_limit_is_respected(self):
        events = self.service().all_events(limit=2)
        self.assertLessEqual(len(events), 2)

    def test_activity_counts_have_source_and_kind(self):
        data = self.service().activity_counts()
        self.assertGreaterEqual(data["total"], 1)
        self.assertIn("activity", data["by_source"])
        self.assertIn("email", data["by_kind"])

    def test_recent_window_is_structured(self):
        data = self.service().recent_window(days=30)
        self.assertEqual(data["days"], 30)
        self.assertIn("items", data)
        self.assertEqual(data["events"], len(data["items"]))

    def test_application_summary_has_each_user_application(self):
        rows = self.service().application_summary()
        ids = {row["application_id"] for row in rows}
        self.assertEqual(ids, {self.application.id, self.second.id})

    def test_application_summary_counts_sources(self):
        row = next(item for item in self.service().application_summary() if item["application_id"] == self.application.id)
        self.assertEqual(row["activity_count"], 2)
        self.assertEqual(row["interview_count"], 1)
        self.assertEqual(row["task_count"], 1)

    def test_completed_interview_creates_second_interview_event(self):
        interview = Interview.objects.filter(application=self.application).first()
        interview.completed_date = timezone.now()
        interview.feedback = "Good"
        interview.save()
        events = self.service().events_for_application(self.application.id)
        kinds = [event["kind"] for event in events]
        self.assertIn("interview_completed", kinds)

    def test_dashboard_contains_all_sections(self):
        data = self.service().dashboard()
        self.assertEqual(set(data), {"recent", "counts", "applications", "events"})
        self.assertTrue(data["events"])

    def test_event_labels_are_readable(self):
        events = self.service().events_for_application(self.application.id)
        self.assertTrue(all(event["title"] for event in events))
