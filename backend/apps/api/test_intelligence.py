from django.contrib.auth import get_user_model
from django.test import TestCase
from apps.api.intelligence import extract_keywords, match_skills, salary_position
from apps.jobs.models import JobApplication, JobDescription


User = get_user_model()


class IntelligenceUnitTests(TestCase):
    def test_extract_keywords_ranks_frequent_terms(self):
        words = extract_keywords("Python Python Django REST REST REST PostgreSQL")
        self.assertEqual(words[0], "rest")
        self.assertIn("python", words)

    def test_match_skills_reports_required_gaps(self):
        result = match_skills(["Python", "Django"], ["Python", "Java"], ["Django"])
        self.assertEqual(result["required_matches"], ["python"])
        self.assertEqual(result["missing_required"], ["java"])
        self.assertEqual(result["preferred_matches"], ["django"])

    def test_salary_position_interpolates_range(self):
        self.assertEqual(salary_position(75000, 50000, 100000), 50.0)
        self.assertIsNone(salary_position(75000, 75000, 75000))


class JobDescriptionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="intel", password="pass12345")

    def test_description_belongs_to_user_and_application(self):
        application = JobApplication.objects.create(
            user=self.user, company="Example", role="Backend Engineer"
        )
        description = JobDescription.objects.create(
            user=self.user,
            application=application,
            title="Backend Engineer",
            company="Example",
            raw_text="Python Django PostgreSQL",
            required_skills=["Python", "Django"],
        )
        self.assertEqual(application.job_description, description)
        self.assertEqual(description.user, self.user)
