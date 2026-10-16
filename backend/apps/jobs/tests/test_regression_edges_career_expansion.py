"""Additional edge-case tests for validation boundaries and empty inputs."""
from datetime import date
from django.test import SimpleTestCase
from apps.jobs.application_timeline_analysis import (
    chronological_events, merge_timeline_preview, timeline_gaps, timeline_integrity_report,
)
from apps.jobs.application_status_report import outcome_audit, summarize_statuses
from apps.jobs.career_goal_tracking import goal_progress
from apps.jobs.career_reflection import reflection_trends
from apps.jobs.job_search_budget import workload_balance
from apps.jobs.job_search_experiments import summarize_observations

class EmptyInputRegressionTests(SimpleTestCase):
    def test_empty_timeline_is_valid_and_empty(self):
        self.assertEqual(chronological_events([]), [])
        self.assertTrue(timeline_integrity_report([])["consistent"])
        self.assertEqual(timeline_gaps([]), [])

    def test_empty_timeline_merge_is_non_destructive(self):
        result = merge_timeline_preview([], [])
        self.assertFalse(result["persisted"])
        self.assertEqual(result["proposed_additions"], [])

    def test_empty_status_summary_is_consistent(self):
        result = summarize_statuses([])
        self.assertEqual(result["total_records"], 0)
        self.assertEqual(result["known_status_records"], 0)

    def test_empty_outcome_report_has_no_resolved_denominator(self):
        result = outcome_audit([])
        self.assertIsNone(result["offer_percent_resolved"])

    def test_empty_reflection_trends_has_no_energy_score(self):
        result = reflection_trends([])
        self.assertIsNone(result["average_energy_rating"])
        self.assertEqual(result["reflection_count"], 0)

    def test_empty_workload_balance_has_zero_shares(self):
        result = workload_balance([])
        self.assertEqual(result["total_minutes"], 0)
        self.assertEqual(sum(result["shares_percent"].values()), 0)

    def test_empty_experiment_summary_does_not_invent_rates(self):
        result = summarize_observations([])
        self.assertIsNone(result["offer_rate_percent"])
        self.assertEqual(result["applications"], 0)

class BoundaryRegressionTests(SimpleTestCase):
    def test_goal_progress_caps_percent_at_one_hundred(self):
        result = goal_progress({"title": "Goal", "target": 10, "current": 12})
        self.assertEqual(result["progress_percent"], 100)
        self.assertEqual(result["state"], "complete")

    def test_future_timeline_events_remain_ordered(self):
        result = chronological_events([
            {"id": 2, "date": "2027-01-01", "type": "note"},
            {"id": 1, "date": "2026-01-01", "type": "note"},
        ])
        self.assertEqual(result[0]["id"], 1)

    def test_date_threshold_rejects_large_values(self):
        with self.assertRaises(ValueError):
            timeline_gaps([], threshold_days=4000)

    def test_status_report_keeps_unknown_status_visible(self):
        result = summarize_statuses([{"status": "custom_stage"}])
        self.assertEqual(result["unknown_status_records"], 1)
        self.assertIn("custom_stage", result["unknown_values"])

    def test_completed_goal_is_not_marked_overdue(self):
        result = goal_progress({"title": "Goal", "target": 1, "current": 1,
                                "due_date": "2020-01-01"}, today=date(2026, 1, 1))
        self.assertEqual(result["state"], "complete")
