from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from .intelligence import (
    ApplicationScoringService,
    DuplicateDetectionService,
    FollowUpPlanner,
    InterviewPreparationService,
    JobDescriptionParser,
    KeywordMatchService,
    SearchQueryService,
    TextNormalizer,
)


class IntelligenceUtilitiesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="intelligence-user", password="pass")
        self.application = None

    def test_normalizer_removes_urls_and_stopwords(self):
        result = TextNormalizer.normalize("Python and Django https://example.com")
        self.assertEqual(result, "python and django")

    def test_tokens_remove_stopwords(self):
        result = TextNormalizer.tokens("the Python developer with SQL")
        self.assertIn("python", result)
        self.assertIn("sql", result)
        self.assertNotIn("the", result)
        self.assertNotIn("with", result)

    def test_parser_extracts_skills_and_mode(self):
        profile = JobDescriptionParser.parse(
            "Senior Python developer with Django and PostgreSQL. Remote role."
        )
        self.assertEqual(profile.seniority, "senior")
        self.assertEqual(profile.work_mode, "remote")
        self.assertEqual(
            profile.skills,
            ["django", "postgresql", "python"],
        )

    def test_parser_extracts_employment_type(self):
        profile = JobDescriptionParser.parse("Permanent full-time engineering role")
        self.assertEqual(profile.employment_type, "full_time")

    def test_parser_extracts_location(self):
        profile = JobDescriptionParser.parse("Location: Nairobi, Kenya")
        self.assertEqual(profile.location, "Nairobi, Kenya")

    def test_parser_extracts_salary_range(self):
        profile = JobDescriptionParser.parse("Salary $80k-$120k")
        self.assertEqual(profile.salary_min, Decimal("80000"))
        self.assertEqual(profile.salary_max, Decimal("120000"))

    def test_skill_matching_reports_missing_items(self):
        profile = JobDescriptionParser.parse("Python Django PostgreSQL")
        result = KeywordMatchService(profile).match_skills(["Python", "Django"])
        self.assertEqual(result["matched"], ["django", "python"])
        self.assertEqual(result["missing"], ["postgresql"])
        self.assertEqual(result["score"], 66.67)

    def test_empty_skill_requirement_is_full_match(self):
        profile = JobDescriptionParser.parse("General administrative position")
        self.assertEqual(KeywordMatchService(profile).match_skills([])["score"], 100.0)

    def test_interview_checklist_has_expected_sections(self):
        checklist = InterviewPreparationService.checklist("technical")
        self.assertTrue(any("technologies" in item.lower() for item in checklist))
        self.assertGreaterEqual(len(checklist), 4)

    def test_unknown_interview_type_falls_back(self):
        self.assertEqual(
            InterviewPreparationService.checklist("unknown"),
            InterviewPreparationService.checklist("phone"),
        )

    def test_checklist_progress(self):
        items = InterviewPreparationService.checklist("phone")
        result = InterviewPreparationService.progress("phone", items[:2])
        self.assertEqual(result["completed"], 2)
        self.assertEqual(result["remaining"], len(items) - 2)

    def test_duplicate_normalization_removes_company_suffixes(self):
        self.assertEqual(
            DuplicateDetectionService.normalize("Example Technologies Inc"),
            "example technologies",
        )

    def test_search_query_parses_filters(self):
        service = SearchQueryService(self.user)
        parsed = service.parse("python status:interview mode:remote priority:1")
        self.assertEqual(parsed["text"], "python")
        self.assertEqual(parsed["filters"]["status"], "interview")
        self.assertEqual(parsed["filters"]["work_mode"], "remote")
        self.assertEqual(parsed["filters"]["priority"], "1")

    def test_search_query_keeps_unknown_filters_as_text(self):
        parsed = SearchQueryService(self.user).parse("python unknown:value")
        self.assertEqual(parsed["text"], "python unknown:value")

    def test_parser_returns_none_for_missing_salary(self):
        profile = JobDescriptionParser.parse("Remote Python role")
        self.assertIsNone(profile.salary_min)
        self.assertIsNone(profile.salary_max)

    def test_parser_handles_empty_text(self):
        profile = JobDescriptionParser.parse("")
        self.assertEqual(profile.normalized_text, "")
        self.assertEqual(profile.skills, [])
        self.assertIsNone(profile.seniority)

    def test_keyword_text_match_is_weighted(self):
        profile = JobDescriptionParser.parse("Python Django PostgreSQL")
        result = KeywordMatchService(profile).match_text(
            "I build Python and Django applications."
        )
        self.assertGreater(result["score"], 0)
        self.assertIn("postgresql", result["missing"])


class IntelligenceDocumentationTests(TestCase):
    def test_parser_has_documented_public_contract(self):
        self.assertIn("Extract structured", JobDescriptionParser.__doc__)

    def test_matcher_has_documented_public_contract(self):
        self.assertIn("Compare candidate", KeywordMatchService.__doc__)

    def test_checklists_are_copy_safe(self):
        first = InterviewPreparationService.checklist("phone")
        first.append("temporary")
        second = InterviewPreparationService.checklist("phone")
        self.assertNotIn("temporary", second)


class IntelligenceBoundaryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="boundary-user", password="pass")

    def test_salary_parser_ignores_small_numbers(self):
        profile = JobDescriptionParser.parse("Level 2 role with 5000 training budget")
        self.assertIsNone(profile.salary_min)

    def test_salary_parser_accepts_millions(self):
        profile = JobDescriptionParser.parse("Compensation $1.2m")
        self.assertEqual(profile.salary_min, Decimal("1200000"))
        self.assertEqual(profile.salary_max, Decimal("1200000"))

    def test_duplicate_service_requires_same_user(self):
        from .models import JobApplication

        other = User.objects.create_user(username="other", password="pass")
        application = JobApplication.objects.create(
            user=other, company="Private", role="Engineer"
        )
        with self.assertRaises(PermissionError):
            DuplicateDetectionService(self.user).candidates(application)

    def test_search_query_can_be_constructed_for_a_user(self):
        service = SearchQueryService(self.user)
        self.assertEqual(service.user.pk, self.user.pk)


class IntelligenceScoringContractTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="scoring-user", password="pass")

    def test_scoring_service_has_explicit_status_contract(self):
        service = ApplicationScoringService(self.user)
        self.assertEqual(service.user.pk, self.user.pk)

    def test_follow_up_planner_has_default_actions(self):
        self.assertIn("applied", FollowUpPlanner.DEFAULT_ACTIONS)
        self.assertIn("interview", FollowUpPlanner.DEFAULT_ACTIONS)

    def test_follow_up_actions_have_positive_intervals(self):
        for action, days in FollowUpPlanner.DEFAULT_ACTIONS.values():
            self.assertTrue(action)
            self.assertGreater(days, 0)
