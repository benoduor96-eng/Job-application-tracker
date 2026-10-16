"""Tests for reminder planning and portfolio evidence helpers."""
from datetime import date
from django.test import SimpleTestCase
from apps.jobs.application_followup import (
    rebalance_reminder_load, reminder_queue, reminder_suppression_report, suggest_follow_up,
)
from apps.jobs.career_portfolio import (
    accomplishment_entry, convert_accomplishment_to_bullet, portfolio_audit,
    portfolio_readiness, portfolio_skill_coverage, validate_portfolio_item,
)

class FollowUpTests(SimpleTestCase):
    def test_closed_and_opted_out_records_are_excluded(self):
        result = reminder_queue([
            {"id": 1, "status": "rejected", "applied_date": "2026-01-01"},
            {"id": 2, "status": "applied", "applied_date": "2026-01-01", "opted_out": True},
        ], today=date(2026, 1, 10))
        self.assertEqual(result["reminder_count"], 0)
        self.assertFalse(result["automated_messages_sent"])

    def test_suggested_date_uses_application_date_and_interval(self):
        result = suggest_follow_up({"id": 1, "status": "applied", "applied_date": "2026-01-01"},
                                   today=date(2026, 1, 5))
        self.assertEqual(result["suggested_date"], "2026-01-08")

    def test_missing_reference_date_is_not_invented(self):
        result = suggest_follow_up({"id": 1, "status": "applied"}, today=date(2026, 1, 1))
        self.assertFalse(result["eligible"])
        self.assertEqual(result["reason"], "missing_reference_date")

    def test_reminder_queue_sorts_overdue_first(self):
        result = reminder_queue([
            {"id": 1, "status": "applied", "applied_date": "2026-01-01"},
            {"id": 2, "status": "interview", "applied_date": "2026-01-09"},
        ], today=date(2026, 1, 10))
        self.assertEqual(result["reminders"][0]["id"], 1)

    def test_rebalance_obeys_daily_capacity(self):
        records = [{"id": i, "status": "applied", "next_action_date": "2026-01-01"} for i in range(1, 5)]
        result = rebalance_reminder_load(records, daily_capacity=2, today=date(2026, 1, 1))
        self.assertTrue(all(day["count"] <= 2 for day in result["schedule"]))
        self.assertFalse(result["messages_sent"])

    def test_suppression_report_counts_closed_and_opted_out(self):
        result = reminder_suppression_report([
            {"status": "rejected"}, {"status": "applied", "opted_out": True}])
        self.assertEqual(result["closed"], 1)
        self.assertEqual(result["opted_out"], 1)

class PortfolioTests(SimpleTestCase):
    def test_item_requires_title_and_safe_url(self):
        with self.assertRaises(ValueError):
            validate_portfolio_item({"title": ""})
        with self.assertRaises(ValueError):
            validate_portfolio_item({"title": "Demo", "url": "javascript:alert(1)"})

    def test_readiness_checks_confidentiality_and_evidence(self):
        result = portfolio_readiness({"title": "Demo", "description": "Example", "contribution": "Built API",
                                      "skills": ["python"], "url": "https://example.test",
                                      "confidentiality_checked": True})
        self.assertTrue(result["ready_for_review"])

    def test_skill_coverage_ignores_drafts(self):
        result = portfolio_skill_coverage([
            {"title": "Draft", "skills": ["python"], "status": "draft"},
            {"title": "Public demo", "skills": ["sql"], "status": "published"}], ["python", "sql"])
        self.assertEqual(result["uncovered_target_skills"], ["python"])

    def test_accomplishment_requires_all_core_parts(self):
        with self.assertRaises(ValueError):
            accomplishment_entry("Task", "", "Built", "Improved")
        result = accomplishment_entry("Task", "Problem", "Built", "Reduced manual work")
        self.assertFalse(result["verified"])

    def test_bullet_conversion_is_bounded_and_cautious(self):
        entry = accomplishment_entry("Task", "Problem", "Built a reporting pipeline", "Improved consistency",
                                     evidence="Public repository")
        result = convert_accomplishment_to_bullet(entry)
        self.assertIn("Built a reporting pipeline", result["bullet"])
        self.assertTrue(result["evidence_present"])

    def test_portfolio_audit_never_publishes(self):
        result = portfolio_audit([{"title": "Demo"}])
        self.assertFalse(result["automatic_publication_performed"])
        self.assertEqual(result["item_count"], 1)
