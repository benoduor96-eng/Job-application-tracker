"""Regression tests for the platform expansion's pure domain services."""
from datetime import date, datetime, timezone
from django.test import SimpleTestCase

from apps.jobs.analytics_cohorts import (
    analytics_quality_report, company_rollup, funnel_summary, outcome_summary,
    response_lag_summary, salary_band_summary, source_performance, weekly_application_counts,
    weekly_cohort_retention,
)
from apps.jobs.duplicate_resolution import (
    build_merge_preview, canonical_job_url, compare_records, find_duplicate_candidates,
    normalize_company, normalize_role,
)
from apps.jobs.privacy_lifecycle import (
    build_retention_report, classify_personal_data_keys, export_manifest,
    expiry_timestamp, redact_mapping, retention_decision, sanitize_export,
    validate_export_request,
)
from apps.jobs.search_language import (
    SearchSyntaxError, autocomplete_suggestions, explain_query, filter_records,
    matches_search, parse_search_query, rank_records,
)
from apps.jobs.workflow_policy import (
    InvalidTransition, TransitionReasonRequired, follow_up_sla, next_actions_for_status,
    plan_bulk_transition, prioritize_follow_ups, status_summary, transition_decision,
    transition_history_is_consistent, transition_matrix, validate_transition,
)

class WorkflowPolicyTests(SimpleTestCase):
    def test_valid_and_invalid_transitions_are_explained(self):
        self.assertTrue(transition_decision("applied", "interview").allowed)
        decision = transition_decision("saved", "offer")
        self.assertFalse(decision.allowed)
        self.assertTrue(decision.blockers)

    def test_reopening_requires_reason(self):
        with self.assertRaises(TransitionReasonRequired):
            validate_transition("rejected", "applied")
        self.assertIsNotNone(validate_transition("rejected", "applied", "Employer reopened role"))

    def test_unsupported_status_is_rejected(self):
        with self.assertRaises(InvalidTransition):
            validate_transition("applied", "made_up")

    def test_transition_matrix_is_deterministic_and_complete(self):
        matrix = transition_matrix()
        self.assertEqual(len(matrix), 7 * 6)
        self.assertEqual(matrix, transition_matrix())

    def test_bulk_transition_reports_partial_failures_without_mutating(self):
        result = plan_bulk_transition([
            {"id": 1, "status": "applied"}, {"id": 2, "status": "saved"},
            {"id": "bad", "status": "applied"},
        ], "interview")
        self.assertEqual([row["id"] for row in result["accepted"]], [1])
        self.assertEqual(len(result["rejected"]), 2)
        self.assertFalse(result["ready"])

    def test_follow_up_sla_uses_status_and_overrides(self):
        result = follow_up_sla("applied", date(2026, 1, 1), today=date(2026, 1, 12))
        self.assertEqual(result["due_date"], "2026-01-08")
        self.assertTrue(result["overdue"])
        self.assertIsNone(follow_up_sla("rejected", date(2026, 1, 1))["due_date"])

    def test_prioritization_orders_old_overdue_items_first(self):
        rows = [{"id": 1, "due_date": "2026-01-09", "priority": "low"},
                {"id": 2, "due_date": "2026-01-01", "priority": "medium"},
                {"id": 3, "due_date": "2026-01-09", "priority": "urgent"}]
        result = prioritize_follow_ups(rows, today=date(2026, 1, 10))
        self.assertEqual([row["id"] for row in result], [2, 3, 1])

    def test_status_summary_includes_zero_categories_and_unknown_rows(self):
        result = status_summary([{"status": "applied"}, {"status": "applied"}, {"status": "oops"}])
        self.assertEqual(result["counts"]["offer"], 0)
        self.assertEqual(result["invalid_rows"], 1)
        self.assertEqual(result["total"], 2)

    def test_history_chain_detects_discontinuity(self):
        events = [{"source": "saved", "target": "applied"},
                  {"source": "interview", "target": "offer"}]
        result = transition_history_is_consistent(events, initial_status="saved")
        self.assertFalse(result["consistent"])
        self.assertEqual(result["errors"][0]["error"], "source_does_not_match_previous_target")

    def test_status_actions_are_useful_and_validate_input(self):
        self.assertIn("Confirm the time and format", next_actions_for_status("interview"))
        with self.assertRaises(ValueError):
            next_actions_for_status("unknown")

class DuplicateResolutionTests(SimpleTestCase):
    def test_normalization_handles_company_suffix_and_title_alias(self):
        self.assertEqual(normalize_company("Example, Inc."), "example")
        self.assertEqual(normalize_role("Sr Eng"), "senior engineer")

    def test_url_canonicalization_removes_tracking_parameters(self):
        self.assertEqual(canonical_job_url("http://www.example.com/jobs/1?utm_source=x"),
                         "https://example.com/jobs/1")

    def test_url_schemes_are_not_treated_as_job_urls(self):
        self.assertEqual(canonical_job_url("file:///etc/passwd"), "")

    def test_matching_records_receive_explainable_high_score(self):
        left = {"id": 1, "company": "Acme Ltd", "role": "Senior Engineer",
                "job_url": "https://jobs.example/1", "location": "Remote",
                "applied_date": "2026-01-01"}
        right = {"id": 2, "company": "Acme", "role": "Sr Engineer",
                 "job_url": "https://jobs.example/1?utm_source=mail", "location": "Remote",
                 "applied_date": "2026-01-02"}
        result = compare_records(left, right)
        self.assertGreaterEqual(result.score, .86)
        self.assertEqual(result.confidence, "high")
        self.assertIn("job_url", [feature.name for feature in result.features])

    def test_candidate_pairing_skips_same_identifier_and_sorts(self):
        rows = [{"id": 1, "company": "Acme", "role": "Analyst"},
                {"id": 1, "company": "Acme", "role": "Analyst"},
                {"id": 2, "company": "Acme", "role": "Analyst"}]
        result = find_duplicate_candidates(rows, threshold=.2)
        self.assertTrue(all(item["left_id"] != item["right_id"] for item in result))
        with self.assertRaises(ValueError):
            find_duplicate_candidates(rows, threshold=1.5)

    def test_merge_preview_keeps_conflicts_for_review(self):
        result = build_merge_preview({"id": 1, "company": "Acme", "notes": "first"},
                                     {"id": 2, "company": "Other", "notes": "second"})
        self.assertTrue(result["requires_review"])
        self.assertEqual(result["proposed_values"]["company"], "Acme")
        self.assertEqual(len(result["conflicts"]), 2)
        self.assertIn("No records were changed", result["warning"])

class SearchLanguageTests(SimpleTestCase):
    def setUp(self):
        self.rows = [
            {"id": 1, "company": "Acme", "role": "Data Analyst", "location": "Remote",
             "status": "interview", "notes": "SQL Python", "applied_date": "2026-01-05",
             "salary_min": 70000, "updated_at": "2026-01-07"},
            {"id": 2, "company": "Globex", "role": "Support Engineer", "location": "Nairobi",
             "status": "applied", "notes": "Customer service", "applied_date": "2025-12-01",
             "salary_min": 40000, "updated_at": "2025-12-02"},
        ]

    def test_plain_text_and_field_filters(self):
        self.assertEqual([row["id"] for row in filter_records(self.rows, "Python")], [1])
        self.assertEqual([row["id"] for row in filter_records(self.rows, "status:interview")], [1])
        self.assertEqual([row["id"] for row in filter_records(self.rows, "location:remote")], [1])

    def test_quotes_exclusions_dates_and_salary(self):
        self.assertTrue(matches_search(self.rows[0], '"Data Analyst"'))
        self.assertFalse(matches_search(self.rows[0], "-status:interview"))
        self.assertTrue(matches_search(self.rows[0], "after:2026-01-01 salary>=65000"))
        self.assertFalse(matches_search(self.rows[1], "before:2025-01-01"))

    def test_parser_rejects_bad_fields_dates_quotes_and_length(self):
        for query in ("password:secret", "after:tomorrow", '"unclosed'):
            with self.subTest(query=query), self.assertRaises(SearchSyntaxError):
                parse_search_query(query)
        with self.assertRaises(SearchSyntaxError):
            parse_search_query("x" * 501)

    def test_ranking_is_deterministic(self):
        result = rank_records(self.rows, "role:analyst")
        self.assertEqual([row["id"] for row in result], [1])
        self.assertGreater(result[0]["_search_score"], 0)

    def test_explanation_and_autocomplete(self):
        self.assertEqual(explain_query("company:Acme")["term_count"], 1)
        self.assertEqual(autocomplete_suggestions("ac", ["Acme", "Acadia", "Globex"]), ["Acadia", "Acme"])
        self.assertEqual(autocomplete_suggestions("a", ["Acme"], limit=0), [])

class PrivacyLifecycleTests(SimpleTestCase):
    def test_secret_redaction_is_recursive(self):
        payload = {"username": "u", "access_token": "abc", "nested": [{"password": "x", "email": "a@b.test"}]}
        result = redact_mapping(payload)
        self.assertEqual(result["access_token"], "[REDACTED]")
        self.assertEqual(result["nested"][0]["password"], "[REDACTED]")
        self.assertEqual(result["nested"][0]["email"], "[REDACTED]")
        self.assertEqual(payload["access_token"], "abc")

    def test_personal_data_can_be_retained_when_requested(self):
        self.assertEqual(redact_mapping({"email": "a@b.test"}, include_personal=True)["email"], "a@b.test")

    def test_retention_policy_never_deletes_automatically(self):
        now = datetime(2026, 2, 1, tzinfo=timezone.utc)
        row = {"id": 3, "record_type": "notification", "created_at": "2025-01-01T00:00:00Z"}
        result = retention_decision(row, now=now)
        self.assertEqual(result["action"], "eligible_for_review")
        report = build_retention_report([row], now=now)
        self.assertFalse(report["automatic_deletion_performed"])

    def test_unknown_record_type_needs_policy_review(self):
        result = retention_decision({"id": 1, "record_type": "mystery", "created_at": "2026-01-01"})
        self.assertEqual(result["action"], "review")

    def test_export_manifest_and_selection_validation(self):
        manifest = export_manifest({"applications": [{"id": 1}], "profile": {"name": "A"}})
        self.assertEqual(manifest["record_count"], 2)
        self.assertTrue(validate_export_request({"include_applications": True})["include_personal"])
        with self.assertRaises(ValueError):
            validate_export_request({"include_applications": False})
        with self.assertRaises(ValueError):
            validate_export_request({"include_passwords": True})

    def test_sanitize_export_does_not_mutate_original(self):
        payload = {"email": "person@example.test", "nested": {"api_key": "secret"}}
        sanitized = sanitize_export(payload)
        self.assertEqual(sanitized["email"], "[REDACTED]")
        self.assertEqual(sanitized["nested"]["api_key"], "[REDACTED]")
        self.assertEqual(payload["email"], "person@example.test")

    def test_classification_and_expiry_timestamp(self):
        result = classify_personal_data_keys(["email", "access_token", "company"])
        self.assertEqual(result["sensitive"], ["access_token"])
        self.assertEqual(result["personal"], ["email"])
        self.assertEqual(expiry_timestamp("2026-01-01T00:00:00Z", 7), "2026-01-08T00:00:00+00:00")

class AnalyticsCohortTests(SimpleTestCase):
    def setUp(self):
        self.rows = [
            {"id": 1, "company": "Acme", "role": "Analyst", "status": "interview",
             "applied_date": "2026-01-05", "salary_min": "50000", "salary_max": "70000", "source": "referral"},
            {"id": 2, "company": "Acme", "role": "Engineer", "status": "offer",
             "applied_date": "2026-01-06", "salary_min": "80000", "salary_max": "90000", "source": "referral"},
            {"id": 3, "company": "Globex", "role": "Support", "status": "rejected",
             "applied_date": "2026-01-07", "salary_min": "90000", "salary_max": "80000", "source": "board"},
        ]

    def test_funnel_counts_all_statuses_and_discloses_limits(self):
        result = funnel_summary(self.rows)
        self.assertEqual(result["total"], 3)
        self.assertEqual(result["by_status"]["offer"], 1)
        self.assertIn("directional", result["interpretation"])

    def test_weekly_counts_include_empty_weeks(self):
        result = weekly_application_counts(self.rows, weeks=3, today=date(2026, 1, 20))
        self.assertEqual(len(result), 3)
        self.assertEqual(sum(row["count"] for row in result), 3)

    def test_response_lag_reports_missing_and_negative_dates(self):
        result = response_lag_summary([
            {"applied_date": "2026-01-01", "first_response_date": "2026-01-05"},
            {"applied_date": "2026-01-06", "first_response_date": "2026-01-01"},
            {"applied_date": None, "first_response_date": "2026-01-01"},
        ])
        self.assertEqual(result["sample_size"], 1)
        self.assertEqual(result["mean_days"], 4)
        self.assertEqual(result["missing_or_invalid"], 2)

    def test_source_performance_marks_small_samples(self):
        result = source_performance(self.rows, minimum_sample=3)
        self.assertTrue(all(row["sample_warning"] for row in result))
        self.assertEqual(result[0]["source"], "referral")

    def test_salary_summary_excludes_inverted_ranges(self):
        result = salary_band_summary(self.rows)
        self.assertEqual(result["range_count"], 2)
        self.assertEqual(result["lowest_min"], 50000)
        self.assertIn("currency", result["currency_warning"])

    def test_company_rollup_and_limit_validation(self):
        result = company_rollup(self.rows)
        self.assertEqual(result[0]["company"], "Acme")
        with self.assertRaises(ValueError):
            company_rollup(self.rows, limit=0)

    def test_outcome_summary_uses_resolved_denominator(self):
        result = outcome_summary(self.rows)
        self.assertEqual(result["resolved"], 3)
        self.assertAlmostEqual(result["offer_rate_of_resolved_percent"], 33.33, places=2)

    def test_cohorts_are_weekly_and_only_include_requested_age(self):
        result = weekly_cohort_retention(self.rows, periods=8, today=date(2026, 1, 20))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["applications"], 3)

    def test_quality_report_flags_duplicates_and_invalid_salary(self):
        rows = self.rows + [dict(self.rows[0])]
        result = analytics_quality_report(rows)
        self.assertGreaterEqual(result["issues"]["duplicate_id"], 1)
        self.assertEqual(result["issues"]["invalid_salary_range"], 1)
