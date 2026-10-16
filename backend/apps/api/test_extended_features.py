from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from rest_framework.test import APIClient

from apps.jobs.career_assistant import build_job_fit_report, compare_skills, interview_question_set, resume_review
from apps.jobs.job_board_adapters import JobImportError, normalize_generic, normalize_greenhouse, normalize_lever, parse_jobs_csv
from apps.jobs.models import JobApplication

User = get_user_model()


class CareerAssistantServiceTests(SimpleTestCase):
    def test_skill_comparison_is_case_insensitive_and_reports_gaps(self):
        result = compare_skills(["Python", "Django"], ["python", "Java"], ["django"])
        self.assertEqual(result["required_matches"], ["python"])
        self.assertEqual(result["missing_required"], ["java"])
        self.assertEqual(result["preferred_matches"], ["django"])
        self.assertEqual(result["required_coverage_percent"], 50.0)

    def test_resume_review_returns_actionable_checks(self):
        resume = "Email ben@example.com\nSkills\nPython\nExperience\n- Developed a tool for 20 users"
        result = resume_review(resume)
        self.assertGreater(result["word_count"], 0)
        self.assertEqual(result["quantified_bullet_count"], 1)
        self.assertTrue(any(c["key"] == "contact_details" and c["passed"] for c in result["checks"]))

    def test_interview_question_count_is_bounded(self):
        self.assertEqual(len(interview_question_set("Data Analyst", ["SQL", "Python"], 3)), 3)
        self.assertEqual(len(interview_question_set("Data Analyst", ["SQL"], 20)), 9)

    def test_fit_report_discloses_limitations(self):
        result = build_job_fit_report(["Python"], "Python SQL communication")
        self.assertIn("disclaimer", result)
        self.assertIn("review_guidance", result)


class JobBoardAdapterTests(SimpleTestCase):
    def test_generic_normalization_accepts_common_aliases(self):
        result = normalize_generic({
            "company_name": "Example Ltd", "title": "Backend Engineer",
            "url": "https://jobs.example.org/123", "salary_min": "50000", "salary_max": "70000",
        })
        self.assertEqual(result["company"], "Example Ltd")
        self.assertEqual(result["role"], "Backend Engineer")
        self.assertEqual(result["salary_min"], 50000.0)

    def test_invalid_url_and_salary_range_are_rejected(self):
        with self.assertRaises(JobImportError):
            normalize_generic({"company": "X", "role": "Y", "url": "file:///etc/passwd"})
        with self.assertRaises(JobImportError):
            normalize_generic({"company": "X", "role": "Y", "salary_min": 900, "salary_max": 100})

    def test_greenhouse_adapter_maps_location_and_url(self):
        result = normalize_greenhouse({
            "id": 12, "title": "Engineer", "company_name": "Acme",
            "absolute_url": "https://boards.example/jobs/12", "location": {"name": "Remote"},
        })
        self.assertEqual(result["source"], "greenhouse")
        self.assertEqual(result["location"], "Remote")

    def test_lever_adapter_maps_categories(self):
        result = normalize_lever({
            "id": "abc", "text": "Analyst", "hostedUrl": "https://jobs.example/abc",
            "categories": {"location": "Nairobi", "commitment": "Full time"},
        })
        self.assertEqual(result["role"], "Analyst")
        self.assertEqual(result["location"], "Nairobi")

    def test_csv_parser_returns_row_level_errors(self):
        result = parse_jobs_csv(
            "company,title,url\nGood Co,Engineer,https://jobs.example/1\nMissing Role,,https://jobs.example/2"
        )
        self.assertEqual(result["accepted"], 1)
        self.assertEqual(result["rejected"], 1)
        self.assertEqual(result["errors"][0]["line"], 3)


class ExtendedFeatureApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="extended-test", password="pass12345")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_career_assistant_requires_authentication(self):
        client = APIClient()
        response = client.post("/api/career-assistant/analyze/", {"resume_text": "Skills Python"}, format="json")
        self.assertEqual(response.status_code, 401)

    def test_career_assistant_analyzes_user_text(self):
        response = self.client.post(
            "/api/career-assistant/analyze/",
            {"resume_text": "Email ben@example.com\nSkills\nPython\nExperience\n- Developed 3 tools",
             "job_description": "Python SQL", "skills": ["Python"]},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["provider"], "local-deterministic")
        self.assertIn("job_fit_review", response.data)

    def test_job_import_endpoint_rejects_unsafe_url(self):
        response = self.client.post(
            "/api/integrations/jobs/normalize/",
            {"job": {"company": "Example", "role": "Engineer", "url": "file:///tmp/a"}},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_csv_preview_does_not_create_applications(self):
        response = self.client.post(
            "/api/integrations/jobs/normalize/",
            {"csv": "company,title,url\nExample,Engineer,https://jobs.example/1"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["accepted"], 1)
        self.assertEqual(JobApplication.objects.filter(user=self.user).count(), 0)

    def test_personal_export_is_scoped_to_authenticated_user(self):
        JobApplication.objects.create(user=self.user, company="Owned Co", role="Engineer")
        other = User.objects.create_user(username="other-user", password="pass12345")
        JobApplication.objects.create(user=other, company="Private Co", role="Analyst")
        response = self.client.get("/api/account/export/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertIn("Owned Co", response.content.decode())
        self.assertNotIn("Private Co", response.content.decode())


    def test_provider_specific_job_adapter_is_selectable(self):
        response = self.client.post(
            "/api/integrations/jobs/normalize/",
            {"provider": "greenhouse", "job": {
                "id": 21, "title": "Engineer", "company_name": "Example",
                "absolute_url": "https://jobs.example/21", "location": {"name": "Remote"},
            }},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["job"]["source"], "greenhouse")

    def test_unknown_job_adapter_is_rejected(self):
        response = self.client.post(
            "/api/integrations/jobs/normalize/",
            {"provider": "unknown", "job": {"company": "Example", "role": "Engineer"}},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
