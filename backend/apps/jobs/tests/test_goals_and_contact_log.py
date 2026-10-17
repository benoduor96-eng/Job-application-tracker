"""Tests for career goal progress and contact interaction history."""
from datetime import date
from django.test import SimpleTestCase
from apps.jobs.career_goal_tracking import (
    compare_goal_snapshots, goal_check_in, goal_progress, goals_dashboard, validate_goal,
)
from apps.jobs.application_contact_log import (
    interaction_gaps, interaction_summary, interaction_timeline, next_step_queue,
    redact_interaction, validate_interaction,
)

class GoalTrackingTests(SimpleTestCase):
    def test_goal_requires_title_and_positive_target(self):
        with self.assertRaises(ValueError):
            validate_goal({"title": "", "target": 5})
        with self.assertRaises(ValueError):
            validate_goal({"title": "Apply", "target": 0})

    def test_goal_progress_detects_completion_and_overdue(self):
        complete = goal_progress({"id": 1, "title": "Applications", "target": 5, "current": 5})
        overdue = goal_progress({"id": 2, "title": "Course", "target": 10, "current": 1,
                                 "due_date": "2026-01-01"}, today=date(2026, 2, 1))
        self.assertEqual(complete["state"], "complete")
        self.assertEqual(overdue["state"], "overdue")

    def test_dashboard_summarizes_goals(self):
        result = goals_dashboard([{"id": 1, "title": "Learn SQL", "target": 10, "current": 2}])
        self.assertEqual(result["goal_count"], 1)
        self.assertEqual(result["completed_count"], 0)

    def test_checkin_requires_note_and_does_not_persist(self):
        with self.assertRaises(ValueError):
            goal_check_in({"id": 1, "title": "Goal", "target": 5}, "no")
        result = goal_check_in({"id": 1, "title": "Goal", "target": 5}, "Completed module one", 2)
        self.assertFalse(result["persisted"])

    def test_snapshot_comparison_reports_additions(self):
        result = compare_goal_snapshots([], [{"id": 1, "title": "Goal", "target": 5}])
        self.assertEqual(result["changes"][0]["change"], "added")

class ContactLogTests(SimpleTestCase):
    def test_interaction_requires_summary_and_date(self):
        with self.assertRaises(ValueError):
            validate_interaction({"summary": ""})
        with self.assertRaises(ValueError):
            validate_interaction({"summary": "Called recruiter"})

    def test_timeline_sorts_by_date(self):
        result = interaction_timeline([
            {"id": 2, "summary": "Second", "occurred_on": "2026-02-01"},
            {"id": 1, "summary": "First", "occurred_on": "2026-01-01"},
        ])
        self.assertEqual([row["id"] for row in result], [1, 2])

    def test_summary_counts_action_required(self):
        result = interaction_summary([{"id": 1, "summary": "Need to reply", "occurred_on": "2026-01-01",
                                       "outcome": "action_required"}])
        self.assertEqual(result["action_required_count"], 1)

    def test_next_step_queue_includes_follow_up(self):
        result = next_step_queue([{"id": 1, "summary": "Interview", "occurred_on": "2026-01-01",
                                   "next_step": "Send thank-you note"}])
        self.assertEqual(result[0]["next_step"], "Send thank-you note")

    def test_gap_validation_and_reporting(self):
        rows = [{"id": 1, "summary": "First", "occurred_on": "2026-01-01"},
                {"id": 2, "summary": "Second", "occurred_on": "2026-02-01"}]
        self.assertEqual(len(interaction_gaps(rows, 21)), 1)
        with self.assertRaises(ValueError):
            interaction_gaps(rows, 0)

    def test_redaction_hides_private_notes_by_default(self):
        event = {"summary": "Private", "occurred_on": "2026-01-01", "private_notes": "secret"}
        self.assertEqual(redact_interaction(event)["private_notes"], "[REDACTED]")
        self.assertEqual(redact_interaction(event, True)["private_notes"], "secret")
