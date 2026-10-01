from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from .models import JobApplication, Interview, JobDescription, ApplicationActivity, CareerTask
from .interview_packet import InterviewPacket


class InterviewPacketTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="candidate", password="pass12345")
        self.other = User.objects.create_user(username="other-candidate", password="pass12345")
        self.application = JobApplication.objects.create(
            user=self.user, company="Acme", role="Senior Backend Engineer",
            status="interview", notes="Discussed platform migration and API reliability.",
            next_action="Prepare technical examples",
        )
        self.description = JobDescription.objects.create(
            user=self.user, application=self.application,
            title="Senior Backend Engineer", company="Acme",
            raw_text="Build Python Django APIs and collaborate with product teams.",
            required_skills=["Python", "Django", "SQL"],
            preferred_skills=["React", "Cloud"],
            responsibilities=["Build APIs", "Collaborate with stakeholders"],
            extracted_keywords=["API", "reliability"],
        )
        self.interview = Interview.objects.create(
            application=self.application, interview_type="technical",
            scheduled_date=timezone.now()+timedelta(days=4),
            interviewer_name="Jane Doe", interviewer_title="Engineering Manager",
        )
        ApplicationActivity.objects.create(
            user=self.user, application=self.application,
            activity_type="interview", title="Technical round",
            occurred_at=timezone.now(),
        )
        CareerTask.objects.create(
            user=self.user, application=self.application,
            title="Review API examples", priority="high", status="todo",
        )

    def service(self):
        return InterviewPacket(self.user)

    def test_upcoming_interviews_are_user_scoped(self):
        rows = self.service().upcoming_interviews()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["company"], "Acme")

    def test_skills_include_required_and_preferred(self):
        packet = self.service().packet_for_interview(self.interview)
        names = {item["name"] for item in packet["skills"]}
        self.assertTrue({"Python", "Django", "SQL", "React", "Cloud"}.issubset(names))

    def test_required_skill_is_marked_required(self):
        packet = self.service().packet_for_interview(self.interview)
        required = {item["name"] for item in packet["skills"] if item["required"]}
        self.assertIn("Python", required)
        self.assertNotIn("React", required)

    def test_topics_are_derived_from_stored_text(self):
        packet = self.service().packet_for_interview(self.interview)
        self.assertIn("python", packet["topics"]["technical"])
        self.assertIn("collaborate", packet["topics"]["delivery"])

    def test_activity_context_is_application_scoped(self):
        packet = self.service().packet_for_interview(self.interview)
        self.assertEqual(len(packet["activity"]), 1)
        self.assertEqual(packet["activity"][0]["type"], "interview")

    def test_task_context_excludes_completed_tasks(self):
        CareerTask.objects.create(user=self.user, application=self.application, title="Done", status="done")
        packet = self.service().packet_for_interview(self.interview)
        self.assertEqual(len(packet["tasks"]), 1)
        self.assertEqual(packet["tasks"][0]["title"], "Review API examples")

    def test_preparation_score_rewards_completed_context(self):
        packet = self.service().packet_for_interview(self.interview)
        self.assertGreaterEqual(packet["preparation"]["score"], 70)
        self.assertEqual(len(packet["preparation"]["checks"]), 8)

    def test_missing_context_reduces_score(self):
        application = JobApplication.objects.create(user=self.user, company="Empty", role="Engineer", status="interview")
        interview = Interview.objects.create(application=application, interview_type="phone")
        packet = self.service().packet_for_interview(interview)
        self.assertLess(packet["preparation"]["score"], 30)

    def test_packet_contains_application_snapshot(self):
        packet = self.service().packet_for_interview(self.interview)
        self.assertEqual(packet["application"]["id"], self.application.id)
        self.assertEqual(packet["application"]["company"], "Acme")
        self.assertEqual(packet["job_description"]["title"], "Senior Backend Engineer")

    def test_other_user_interview_returns_none(self):
        other_app = JobApplication.objects.create(user=self.other, company="Secret", role="Engineer", status="interview")
        other_interview = Interview.objects.create(application=other_app)
        self.assertIsNone(self.service().packet_for_interview(other_interview))

    def test_dashboard_has_summary_and_packets(self):
        data = self.service().dashboard()
        self.assertEqual(data["summary"]["interviews"], 1)
        self.assertEqual(len(data["packets"]), 1)
        self.assertIn("average_score", data["summary"])

    def test_application_packet_without_interview_is_safe(self):
        app = JobApplication.objects.create(user=self.user, company="No Interview", role="Engineer")
        packet = self.service().packet_for_application(app)
        self.assertIsNone(packet["interview"])
        self.assertIn("message", packet)

    def test_application_packet_uses_latest_interview(self):
        old = Interview.objects.create(application=self.application, interview_type="phone", scheduled_date=timezone.now()-timedelta(days=3))
        packet = self.service().packet_for_application(self.application)
        self.assertEqual(packet["interview"]["id"], self.interview.id)

    def test_dashboard_prepared_count_uses_score_threshold(self):
        data = self.service().dashboard()
        prepared = data["summary"]["prepared"]
        needs = data["summary"]["needs_preparation"]
        self.assertEqual(prepared + needs, data["summary"]["interviews"])

    def test_feedback_is_exposed_for_review(self):
        self.interview.feedback = "Strong API discussion"
        self.interview.save()
        packet = self.service().packet_for_interview(self.interview)
        self.assertEqual(packet["interview"]["feedback"], "Strong API discussion")

    def test_missing_job_description_is_represented(self):
        self.description.delete()
        packet = self.service().packet_for_interview(self.interview)
        self.assertIsNone(packet["job_description"]["title"])
        self.assertEqual(packet["skills"], [])

    def test_future_window_excludes_distant_interviews(self):
        far = Interview.objects.create(application=self.application, scheduled_date=timezone.now()+timedelta(days=60))
        rows = self.service().upcoming_interviews(days=30)
        self.assertEqual(len(rows), 1)
        self.assertNotEqual(rows[0]["id"], far.id)
