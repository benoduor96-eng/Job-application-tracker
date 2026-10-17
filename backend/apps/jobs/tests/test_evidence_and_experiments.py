"""Tests for truthful resume evidence and cautious job-search experiment reporting."""
from django.test import SimpleTestCase
from apps.jobs.resume_evidence import (
    claim_audit, claim_readiness, claim_revision_prompt, match_claims_to_role, validate_claim,
)
from apps.jobs.job_search_experiments import (
    compare_experiments, experiment_report, group_observations, summarize_observations,
    validate_experiment, validate_observation,
)

class ResumeEvidenceTests(SimpleTestCase):
    def test_claim_requires_text(self):
        with self.assertRaises(ValueError):
            validate_claim({})

    def test_claim_readiness_requires_reference_and_confidentiality_review(self):
        result = claim_readiness({"claim": "Improved pipeline by 20%", "quantified": True})
        self.assertFalse(result["ready_for_review"])
        self.assertTrue(result["issues"])

    def test_claim_audit_counts_unsupported_claims(self):
        result = claim_audit([{"claim": "Worked with Python", "claim_type": "skill"}])
        self.assertEqual(result["claim_count"], 1)
        self.assertEqual(result["ready_count"], 0)

    def test_role_matching_is_explainable(self):
        result = match_claims_to_role([{"id": 1, "claim": "Built Python ETL pipeline"}], ["Python", "Docker"])
        self.assertEqual(result["matched_skills"], 1)
        self.assertEqual(result["unmatched_skills"][0]["skill"], "docker")

    def test_revision_prompt_asks_for_evidence(self):
        result = claim_revision_prompt({"claim": "Created dashboard"})
        self.assertTrue(any("evidence" in question.lower() for question in result["questions"]))

class SearchExperimentTests(SimpleTestCase):
    def test_experiment_requires_hypothesis_and_title(self):
        with self.assertRaises(ValueError):
            validate_experiment({"title": "Test"})

    def test_observation_validates_count_relationships(self):
        with self.assertRaises(ValueError):
            validate_observation({"applications": 2, "interviews": 3, "offers": 1})

    def test_summary_handles_empty_sample(self):
        result = summarize_observations([])
        self.assertIsNone(result["interview_rate_percent"])
        self.assertTrue(result["sample_warning"])

    def test_rates_and_small_sample_warning(self):
        result = summarize_observations([
            {"applications": 10, "interviews": 3, "offers": 1, "segment": "referral"},
        ])
        self.assertEqual(result["interview_rate_percent"], 30)
        self.assertTrue(result["sample_warning"])

    def test_comparison_does_not_claim_causation(self):
        result = compare_experiments(
            [{"applications": 20, "interviews": 5, "offers": 2}],
            [{"applications": 20, "interviews": 6, "offers": 3}])
        self.assertFalse(result["causal_claim_supported"])
        self.assertIsNotNone(result["percentage_point_delta"]["interview_rate_percent"])

    def test_experiment_report_filters_by_id(self):
        result = experiment_report({"id": "x", "title": "Resume version", "hypothesis": "Clearer bullets help"},
            [{"experiment_id": "x", "applications": 5, "interviews": 2, "offers": 1},
             {"experiment_id": "y", "applications": 5, "interviews": 0, "offers": 0}])
        self.assertEqual(result["summary"]["applications"], 5)
        self.assertFalse(result["report_is_predictive"])

    def test_grouping_rejects_unapproved_fields(self):
        with self.assertRaises(ValueError):
            group_observations([], group_field="salary")
