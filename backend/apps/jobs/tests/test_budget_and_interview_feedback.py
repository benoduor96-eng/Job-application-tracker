"""Tests for sustainable effort budgeting and interview debrief analysis."""
from datetime import date
from django.test import SimpleTestCase
from apps.jobs.job_search_budget import (
    compare_effort_periods, estimate_activity_plan, summarize_effort, weekly_effort_report, workload_balance,
)
from apps.jobs.interview_feedback import (
    compare_debriefs, debrief_action_queue, debrief_summary, improvement_plan, validate_debrief,
)

class EffortBudgetTests(SimpleTestCase):
    def test_activity_requires_type_and_valid_date(self):
        with self.assertRaises(ValueError):
            summarize_effort([{"type": "unknown", "date": "2026-01-01"}])
        with self.assertRaises(ValueError):
            summarize_effort([{"type": "application"}])

    def test_weekly_budget_calculates_remaining_minutes(self):
        result = weekly_effort_report([
            {"type": "application", "date": "2026-01-05", "minutes": 40}], date(2026, 1, 6), 100)
        self.assertEqual(result["remaining_minutes"], 60)

    def test_compare_effort_reports_deltas(self):
        result = compare_effort_periods(
            [{"type": "application", "date": "2026-01-01", "minutes": 20}],
            [{"type": "application", "date": "2026-01-01", "minutes": 40}])
        self.assertEqual(result["delta_minutes"], 20)

    def test_workload_balance_has_shares(self):
        result = workload_balance([{"type": "learning", "date": "2026-01-01", "minutes": 60}])
        self.assertEqual(result["shares_percent"]["preparation_and_learning"], 100)

    def test_activity_plan_rejects_unknown_type(self):
        with self.assertRaises(ValueError):
            estimate_activity_plan({"gaming": 2})

class InterviewFeedbackTests(SimpleTestCase):
    def test_debrief_requires_company_and_role(self):
        with self.assertRaises(ValueError):
            validate_debrief({"company": "Acme"})

    def test_debrief_summary_averages_only_provided_scores(self):
        result = debrief_summary([{"company": "Acme", "role": "Analyst", "communication": 4}])
        self.assertEqual(result["score_averages"]["communication"], 4)
        self.assertEqual(result["score_sample_sizes"]["technical_reasoning"], 0)

    def test_improvement_plan_uses_threshold(self):
        result = improvement_plan([
            {"company": "Acme", "role": "Analyst", "communication": 2}], threshold=3)
        self.assertTrue(any(item["dimension"] == "communication" for item in result))

    def test_action_queue_includes_follow_up_questions(self):
        result = debrief_action_queue([{"id": 3, "company": "Acme", "role": "Analyst",
                                        "questions_to_follow_up": ["Ask about timeline"]}])
        self.assertEqual(result[0]["interview_id"], 3)

    def test_compare_debriefs_explains_delta(self):
        result = compare_debriefs(
            {"company": "A", "role": "B", "communication": 2},
            {"company": "A", "role": "B", "communication": 4})
        self.assertEqual(result["score_changes"]["communication"]["delta"], 2)

    def test_invalid_score_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_debrief({"company": "A", "role": "B", "communication": 8})
