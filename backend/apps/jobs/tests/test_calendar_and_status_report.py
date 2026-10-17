"""Tests for calendar aggregation and application status reporting."""
from datetime import date
from django.test import SimpleTestCase
from apps.jobs.career_calendar import build_calendar, calendar_summary, daily_capacity_conflicts, normalize_calendar_event
from apps.jobs.application_status_report import outcome_audit, status_by_company, summarize_statuses, transition_counts

class CareerCalendarTests(SimpleTestCase):
    def test_event_requires_title_and_date(self):
        with self.assertRaises(ValueError):
            normalize_calendar_event({"date": "2026-01-01"})
        with self.assertRaises(ValueError):
            normalize_calendar_event({"title": "Interview"})

    def test_calendar_groups_events_by_date(self):
        result = build_calendar([
            {"id": 1, "title": "Interview", "date": "2026-01-02", "event_type": "interview"},
            {"id": 2, "title": "Follow-up", "date": "2026-01-02", "event_type": "follow_up"},
        ])
        self.assertEqual(result["event_count"], 2)
        self.assertEqual(result["days"][0]["count"], 2)
        self.assertFalse(result["calendar_invites_sent"])

    def test_calendar_filters_date_range(self):
        result = build_calendar([
            {"title": "A", "date": "2026-01-01"},
            {"title": "B", "date": "2026-02-01"},
        ], start_date=date(2026, 1, 15))
        self.assertEqual(result["event_count"], 1)

    def test_capacity_conflict_is_reported(self):
        result = daily_capacity_conflicts([
            {"title": "A", "date": "2026-01-01", "duration_minutes": 300},
            {"title": "B", "date": "2026-01-01", "duration_minutes": 240},
        ], available_minutes=480)
        self.assertEqual(result[0]["over_capacity_minutes"], 60)

    def test_summary_counts_completed_events(self):
        result = calendar_summary([{"title": "A", "date": "2026-01-01", "completed": True}])
        self.assertEqual(result["completed"], 1)

class StatusReportTests(SimpleTestCase):
    def test_status_summary_discloses_unknown_values(self):
        result = summarize_statuses([{"status": "offer"}, {"status": "mystery"}])
        self.assertEqual(result["unknown_status_records"], 1)
        self.assertEqual(result["counts"]["offer"], 1)

    def test_company_status_report_sorts_and_limits(self):
        result = status_by_company([
            {"company": "B", "status": "interview"}, {"company": "A", "status": "offer"}])
        self.assertEqual(result[0]["company"], "A")
        with self.assertRaises(ValueError):
            status_by_company([], limit=0)

    def test_transition_counts_separates_invalid_events(self):
        result = transition_counts([
            {"from_status": "applied", "to_status": "interview"},
            {"from_status": "made_up", "to_status": "offer"},
        ])
        self.assertEqual(result["transition_count"], 1)
        self.assertEqual(result["invalid_transition_events"], 1)

    def test_outcome_audit_exposes_both_denominators(self):
        result = outcome_audit([{"status": "offer"}, {"status": "rejected"}, {"status": "applied"}])
        self.assertEqual(result["resolved"], 2)
        self.assertEqual(result["offer_percent_resolved"], 50)
