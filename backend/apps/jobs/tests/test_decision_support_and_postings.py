"""Tests for explainable decision support and job posting analysis."""
from django.test import SimpleTestCase
from apps.jobs.application_decision_support import (
    compare_priority_scenarios, decision_log_entry, decision_review_template,
    effort_budget_report, rank_applications, rating_scale, score_application,
)
from apps.jobs.job_description_intelligence import (
    build_application_questions, compare_postings, detect_recruitment_red_flags,
    extract_requirement_bullets, posting_completeness, split_sections, summarize_posting,
)

class DecisionSupportTests(SimpleTestCase):
    def test_ratings_are_validated(self):
        with self.assertRaises(ValueError):
            score_application({"role_fit": 6})

    def test_score_discloses_missing_ratings(self):
        result = score_application({"id": 1, "role_fit": 5})
        self.assertIn("interest", result["missing_ratings"])
        self.assertLess(result["rated_weight_percent"], 100)

    def test_rankings_are_deterministic(self):
        records = [{"id": 1, "role_fit": 2, "interest": 2},
                   {"id": 2, "role_fit": 5, "interest": 5}]
        result = rank_applications(records)
        self.assertEqual(result[0]["id"], 2)
        self.assertEqual([item["rank"] for item in result], [1, 2])

    def test_scenarios_show_rank_positions(self):
        records = [{"id": 1, "compensation": 5, "role_fit": 2},
                   {"id": 2, "compensation": 2, "role_fit": 5}]
        result = compare_priority_scenarios(records, {
            "pay": {"compensation": 100}, "fit": {"role_fit": 100}})
        self.assertIn("1", result["rank_positions_by_application"])
        self.assertNotIn("objective prediction", result["warning"])

    def test_decision_log_requires_rationale(self):
        with self.assertRaises(ValueError):
            decision_log_entry(1, "continue", "no")
        result = decision_log_entry(1, "research", "Need to verify contract terms")
        self.assertFalse(result["saved"])

    def test_effort_budget_excludes_closed_applications(self):
        result = effort_budget_report([
            {"id": 1, "status": "applied", "estimated_minutes": 100},
            {"id": 2, "status": "rejected", "estimated_minutes": 500}], weekly_minutes=120)
        self.assertEqual(result["estimated_minutes"], 100)

    def test_rating_scale_is_subjective(self):
        self.assertIn("subjective", rating_scale()["caution"])

    def test_review_template_does_not_infer_eligibility(self):
        result = decision_review_template({"id": 1, "company": "Acme", "role": "Analyst"})
        self.assertFalse(result["reviewed"])
        self.assertIn("does not infer", result["note"])

class PostingIntelligenceTests(SimpleTestCase):
    def test_section_splitting_recognizes_requirements(self):
        result = split_sections("About us:\\nA company\\nRequirements:\\n- Python\\nResponsibilities:\\n- Build APIs")
        self.assertIn("requirements", result)
        self.assertIn("Python", result["requirements"])

    def test_requirement_bullets_are_extracted(self):
        result = extract_requirement_bullets("Requirements:\\n- Python\\n- SQL")
        self.assertEqual(result["requirements"], ["Python", "SQL"])

    def test_red_flags_are_review_cues(self):
        result = detect_recruitment_red_flags("Pay a training fee before the interview.")
        self.assertTrue(any(item["code"] == "upfront_payment" for item in result))

    def test_personal_financial_secret_request_is_high_severity(self):
        result = detect_recruitment_red_flags("Send your bank password to verify payroll.")
        self.assertTrue(any(item["severity"] == "high" for item in result))

    def test_posting_questions_are_relevant(self):
        result = build_application_questions("Remote contract role with visa sponsorship.")
        topics = {item["topic"] for item in result}
        self.assertIn("location", topics)
        self.assertIn("employment_type", topics)
        self.assertIn("authorization", topics)

    def test_completeness_report_is_bounded(self):
        result = posting_completeness("Responsibilities:\\nBuild APIs")
        self.assertGreaterEqual(result["completeness_percent"], 0)
        self.assertLessEqual(result["completeness_percent"], 100)

    def test_summary_discloses_heuristic_limits(self):
        result = summarize_posting("About us:\\nWe build software.\\nRequirements:\\n- Python")
        self.assertIn("potential_red_flags", result)
        self.assertIn("not a determination", result["disclaimer"])

    def test_posting_comparison_returns_shared_terms(self):
        result = compare_postings("Python Django API", "Python SQL API")
        self.assertIn("python", result["shared_terms"])
        self.assertIn("not a measure", result["warning"])
