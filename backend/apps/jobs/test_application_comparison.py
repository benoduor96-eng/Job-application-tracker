from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from .models import JobApplication, JobDescription, Interview, ApplicationActivity
from .application_comparison import ApplicationComparison


class ApplicationComparisonTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="compare", password="pass12345")
        self.other = User.objects.create_user(username="other-compare", password="pass12345")
        self.left = self.app("Alpha", "Backend Engineer", "interview", "Remote", 90000, 110000)
        self.right = self.app("Beta", "Platform Engineer", "applied", "Nairobi", 70000, 90000)
        JobDescription.objects.create(
            user=self.user, application=self.left, title="Backend", company="Alpha",
            raw_text="Python Django SQL", required_skills=["Python", "Django", "SQL"],
            preferred_skills=["Docker"],
        )
        JobDescription.objects.create(
            user=self.user, application=self.right, title="Platform", company="Beta",
            raw_text="Python Kubernetes", required_skills=["Python", "Kubernetes"],
            preferred_skills=["Docker"],
        )
        Interview.objects.create(application=self.left, interview_type="technical", outcome="passed")
        Interview.objects.create(application=self.left, interview_type="behavioral", outcome="scheduled")
        ApplicationActivity.objects.create(user=self.user, application=self.left, activity_type="email", title="Email", occurred_at="2026-10-02T10:00:00Z")

    def app(self, company, role, status, location, minimum, maximum):
        return JobApplication.objects.create(
            user=self.user, company=company, role=role, status=status,
            location=location, salary_min=minimum, salary_max=maximum,
        )

    def service(self):
        return ApplicationComparison(self.user)

    def test_compare_is_user_scoped(self):
        other_app = JobApplication.objects.create(user=self.other, company="Secret", role="Engineer", status="offer")
        self.assertIsNone(self.service().compare(self.left.id, other_app.id))

    def test_compare_returns_both_rows(self):
        data = self.service().compare(self.left.id, self.right.id)
        self.assertEqual(data["left"]["company"], "Alpha")
        self.assertEqual(data["right"]["company"], "Beta")

    def test_shared_and_distinct_skills_are_reported(self):
        data = self.service().compare(self.left.id, self.right.id)
        self.assertIn("python", data["differences"]["shared_skills"])
        self.assertIn("django", data["differences"]["left_only_skills"])
        self.assertIn("kubernetes", data["differences"]["right_only_skills"])

    def test_salary_delta_is_computed(self):
        data = self.service().compare(self.left.id, self.right.id)
        self.assertEqual(Decimal(data["differences"]["salary_midpoint_delta"]), Decimal("20000"))

    def test_dimensions_describe_stored_metrics(self):
        data = self.service().compare(self.left.id, self.right.id)
        labels = {item["label"] for item in data["dimensions"]}
        self.assertEqual(labels, {"Salary midpoint", "Skill coverage", "Interviews", "Activities", "Passed interviews"})

    def test_left_has_more_interviews(self):
        data = self.service().compare(self.left.id, self.right.id)
        row = next(item for item in data["dimensions"] if item["label"] == "Interviews")
        self.assertEqual(row["relation"], "left")

    def test_compare_many_deduplicates_ids(self):
        rows = self.service().compare_many([self.left.id, self.left.id, self.right.id, "invalid"])
        self.assertEqual(len(rows), 2)

    def test_compare_many_ignores_other_user(self):
        other = JobApplication.objects.create(user=self.other, company="Secret", role="Engineer")
        rows = self.service().compare_many([self.left.id, other.id])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], self.left.id)

    def test_shortlist_is_user_scoped(self):
        rows = self.service().shortlist()
        ids = {row["id"] for row in rows}
        self.assertIn(self.left.id, ids)
        self.assertIn(self.right.id, ids)

    def test_shortlist_prioritizes_offer_before_interview(self):
        offer = self.app("OfferCo", "Engineer", "offer", "Remote", 80000, 100000)
        rows = self.service().shortlist()
        self.assertEqual(rows[0]["id"], offer.id)

    def test_summary_counts_descriptions(self):
        data = self.service().summary()
        self.assertEqual(data["applications"], 2)
        self.assertEqual(data["described"], 2)
        self.assertEqual(data["without_description"], 0)

    def test_summary_calculates_average_salary(self):
        data = self.service().summary()
        self.assertEqual(Decimal(data["average_salary_midpoint"]), Decimal("90000"))

    def test_missing_application_returns_none(self):
        self.assertIsNone(self.service().compare(99999, self.right.id))

    def test_application_without_salary_is_supported(self):
        plain = JobApplication.objects.create(user=self.user, company="Plain", role="Engineer", status="saved")
        data = self.service().compare(plain.id, self.right.id)
        self.assertIsNone(data["differences"]["salary_midpoint_delta"])

    def test_no_description_has_zero_skills(self):
        plain = JobApplication.objects.create(user=self.user, company="Plain", role="Engineer", status="saved")
        data = self.service().compare(plain.id, self.right.id)
        self.assertEqual(data["left"]["skill_count"], 0)

    def test_location_and_company_flags_are_explicit(self):
        data = self.service().compare(self.left.id, self.right.id)
        self.assertFalse(data["differences"]["location_same"])
        self.assertFalse(data["differences"]["company_same"])

    def test_next_action_flag_is_boolean(self):
        data = self.service().compare(self.left.id, self.right.id)
        self.assertIsInstance(data["left"]["has_next_action"], bool)
