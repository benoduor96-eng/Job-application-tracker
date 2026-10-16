"""Tests for application hygiene and evidence-based employer research."""
from datetime import date
from django.test import SimpleTestCase
from apps.jobs.application_health import (
    application_health_report, completeness_by_status, inspect_application, maintenance_plan, stale_record_report,
)
from apps.jobs.career_research import (
    checklist_progress, prioritize_verification, research_checklist, research_decision,
    research_log_entry, safe_information_request, summarize_evidence, validate_evidence,
)

class ApplicationHealthTests(SimpleTestCase):
    def test_incomplete_record_is_flagged(self):
        result = inspect_application({"id": 1, "company": "", "role": "", "status": "unknown"},
                                     today=date(2026, 1, 1))
        self.assertEqual(result["health"], "needs_attention")
        self.assertIn("missing_company", [item["code"] for item in result["issues"]])

    def test_clean_record_has_no_issues(self):
        result = inspect_application({"id": 1, "company": "Acme", "role": "Analyst", "status": "saved",
                                      "job_url": "https://example.test/job", "notes": "Interested"})
        self.assertEqual(result["health"], "looks_complete")

    def test_health_report_is_non_mutating(self):
        rows = [{"id": 1, "company": "", "role": "Analyst", "status": "saved"}]
        result = application_health_report(rows)
        self.assertFalse(result["automatic_changes_performed"])
        self.assertEqual(rows[0]["company"], "")

    def test_stale_report_excludes_closed_records(self):
        result = stale_record_report([
            {"id": 1, "status": "applied", "updated_at": "2026-01-01"},
            {"id": 2, "status": "rejected", "updated_at": "2025-01-01"},
        ], stale_days=10, today=date(2026, 2, 1))
        self.assertEqual(result["stale_count"], 1)
        self.assertEqual(result["closed_record_ids"], [2])

    def test_stale_report_validates_threshold(self):
        with self.assertRaises(ValueError):
            stale_record_report([], stale_days=0)

    def test_maintenance_plan_sorts_high_severity_first(self):
        result = maintenance_plan([{"id": 1, "status": "unknown"}])
        self.assertEqual(result["tasks"][0]["severity"], "high")
        self.assertFalse(result["automatic_changes_performed"])

    def test_completeness_is_grouped_by_status(self):
        result = completeness_by_status([
            {"status": "saved", "company": "A", "role": "B"},
            {"status": "saved", "company": "", "role": "B"},
        ])
        self.assertEqual(result[0]["records"], 2)
        self.assertEqual(result[0]["completeness_percent"], 50)

class CareerResearchTests(SimpleTestCase):
    def test_research_checklist_requires_company_and_role(self):
        with self.assertRaises(ValueError):
            research_checklist("", "Engineer")
        self.assertEqual(len(research_checklist("Acme", "Engineer")["checks"]), 8)

    def test_evidence_requires_source_and_claim(self):
        with self.assertRaises(ValueError):
            validate_evidence({"source": "site"})
        self.assertEqual(validate_evidence({"source": "official site", "claim": "Role exists"})["status"], "unverified")

    def test_evidence_summary_and_decision_are_cautious(self):
        evidence = [{"source": "site A", "claim": "Fee requested", "status": "contradicts"}]
        result = research_decision(evidence)
        self.assertEqual(result["recommendation"], "pause_and_verify")
        self.assertTrue(result["not_a_verdict"])

    def test_checklist_progress_counts_not_applicable(self):
        result = checklist_progress([{"status": "checked"}, {"status": "not_applicable"}, {"status": "blocked"}])
        self.assertEqual(result["progress_percent"], 50)
        self.assertEqual(result["blocked"], 1)

    def test_checklist_rejects_unknown_status(self):
        with self.assertRaises(ValueError):
            checklist_progress([{"status": "done"}])

    def test_log_entry_is_preview_only(self):
        result = research_log_entry("identity", "Opened official site", "Found careers page")
        self.assertFalse(result["persisted"])

    def test_prioritization_places_contradictions_first(self):
        result = prioritize_verification([
            {"source": "B", "claim": "supports", "status": "supports"},
            {"source": "A", "claim": "conflicts", "status": "contradicts"},
        ])
        self.assertEqual(result[0]["status"], "contradicts")

    def test_evidence_summary_counts_empty_input(self):
        result = summarize_evidence([])
        self.assertEqual(result["evidence_count"], 0)
        self.assertTrue(result["needs_follow_up"])

    def test_safe_information_request_never_asks_for_credentials(self):
        result = safe_information_request("privacy")
        self.assertIn("why", result["message"])
        with self.assertRaises(ValueError):
            safe_information_request("password")
