"""Regression tests for planning, resume targeting, and safe import preview services."""
from datetime import date
from django.test import SimpleTestCase
from apps.jobs.career_planning import (
    build_week_plan, capacity_for_day, compare_week_plans, effort_estimate,
    normalize_goal_payload, prioritize_tasks, task_backlog_report,
    validate_task, weekly_goal_progress, workload_recommendations,
)
from apps.jobs.resume_targeting import (
    compare_resume_to_job, evidence_inventory, extract_skills, keyword_frequency,
    normalize_text, parse_required_and_preferred, rank_resume_variants,
    resume_completeness_report, sanitize_job_description, tailor_summary_guidance,
)
from apps.jobs.import_validation import (
    csv_export, import_statistics, map_headers, parse_csv, parse_json_records,
    preview_import, validate_row, validate_rows,
)

class CareerPlanningTests(SimpleTestCase):
    def test_task_validation_rejects_unknown_type(self):
        with self.assertRaises(ValueError):
            validate_task({"type": "invented"})

    def test_task_validation_normalizes_defaults_and_limits_text(self):
        result = validate_task({"type": "apply", "title": "  Apply  ", "notes": "n" * 5000})
        self.assertEqual(result["title"], "Apply")
        self.assertEqual(len(result["notes"]), 2000)
        self.assertEqual(result["estimated_minutes"], 20)

    def test_daily_capacity_reports_overload(self):
        result = capacity_for_day([
            {"id": 1, "type": "apply", "due_date": "2026-01-01"},
            {"id": 2, "type": "interview_prep", "due_date": "2026-01-01"},
        ], daily_minutes=30, target_date=date(2026, 1, 1))
        self.assertTrue(result["is_over_capacity"])
        self.assertEqual(result["over_capacity_minutes"], 20)

    def test_prioritization_puts_overdue_first(self):
        tasks = [{"id": 1, "title": "later", "due_date": "2026-02-10"},
                 {"id": 2, "title": "overdue", "due_date": "2026-02-01", "priority": "low"}]
        result = prioritize_tasks(tasks, today=date(2026, 2, 5))
        self.assertEqual(result[0]["id"], 2)
        self.assertTrue(result[0]["overdue"])

    def test_week_plan_respects_capacity_and_deadlines(self):
        result = build_week_plan([
            {"id": 1, "type": "apply", "due_date": "2026-01-05"},
            {"id": 2, "type": "interview_prep", "due_date": "2025-12-31"},
        ], daily_capacity={"2026-01-05": 30}, start_date=date(2026, 1, 5), days=2)
        self.assertEqual(result["scheduled_count"], 1)
        self.assertEqual(result["unscheduled_count"], 1)
        self.assertEqual(result["schedule"][0]["minutes"], 20)

    def test_week_plan_rejects_too_many_days(self):
        with self.assertRaises(ValueError):
            build_week_plan([], days=32)

    def test_weekly_goals_count_only_completed_tasks(self):
        result = weekly_goal_progress([
            {"type": "apply", "due_date": "2026-01-05", "completed": True},
            {"type": "apply", "due_date": "2026-01-06", "completed": False},
            {"type": "network", "due_date": "2026-01-06", "completed": True},
        ], {"applications": 1, "networking": 1}, start_date=date(2026, 1, 6))
        self.assertTrue(result["goals"]["applications"]["complete"])
        self.assertTrue(result["goals"]["networking"]["complete"])

    def test_effort_estimate_has_transparent_components(self):
        result = effort_estimate(4, minutes_per_application=30, networking_events=2, interview_count=1)
        self.assertEqual(result["application_minutes"], 120)
        self.assertEqual(result["networking_minutes"], 30)
        self.assertEqual(result["interview_prep_minutes"], 30)
        self.assertEqual(result["total_minutes"], 180)

    def test_backlog_and_recommendations(self):
        result = task_backlog_report([
            {"id": 1, "type": "apply", "due_date": "2026-01-01"},
            {"id": 2, "type": "network", "due_date": "2026-01-10", "completed": True},
        ], today=date(2026, 1, 5))
        self.assertEqual(result["overdue"], 1)
        self.assertEqual(workload_recommendations(result)[0]["code"], "review_overdue")

    def test_goal_payload_rejects_unknown_and_negative_fields(self):
        with self.assertRaises(ValueError):
            normalize_goal_payload({"applications": 2, "admin": True})
        with self.assertRaises(ValueError):
            normalize_goal_payload({"applications": -1})

    def test_plan_comparison_does_not_claim_quality(self):
        result = compare_week_plans({"schedule": [], "unscheduled_count": 2},
                                    {"schedule": [{"tasks": [{"id": 1}], "minutes": 20, "capacity": 60}],
                                     "unscheduled_count": 1})
        self.assertTrue(result["better_capacity_fit"])
        self.assertIn("not job-search quality", result["warning"])

class ResumeTargetingTests(SimpleTestCase):
    def test_aliases_are_normalized(self):
        self.assertEqual(normalize_text("JS & ML"), "javascript and machine learning")

    def test_skill_extraction_finds_bounded_terms(self):
        result = extract_skills("Python, Django, PostgreSQL and REST API design.")
        self.assertIn("python", result)
        self.assertIn("django", result)
        self.assertIn("postgresql", result)
        self.assertIn("rest api", result)

    def test_comparison_reports_missing_and_matched_skills(self):
        result = compare_resume_to_job(
            "I built a Python Django service and used PostgreSQL for data storage.",
            "Required skills: Python, Django, PostgreSQL, Docker, Kubernetes.")
        self.assertIn("python", result["matched_skills"])
        self.assertIn("docker", result["missing_job_skills"])
        self.assertTrue(result["recommendations"])

    def test_comparison_requires_both_documents(self):
        with self.assertRaises(ValueError):
            compare_resume_to_job("", "Python required")

    def test_rank_variants_handles_empty_variant_and_ties(self):
        result = rank_resume_variants([
            {"id": "b", "text": "Python and Django"},
            {"id": "a", "text": "Python and Django"},
            {"id": "empty", "text": ""},
        ], "Python and Django")
        self.assertEqual(result[0]["id"], "a")
        self.assertFalse(result[-1]["valid"])

    def test_evidence_inventory_warns_mentions_are_not_verified(self):
        result = evidence_inventory("Python experience", "Python and Docker")
        self.assertEqual(result["mentioned_count"], 1)
        self.assertIn("not evidence of proficiency", result["note"])

    def test_guidance_does_not_recommend_fabrication(self):
        result = tailor_summary_guidance("Python", "Python Django Docker", max_suggestions=3)
        self.assertTrue(any(item["kind"] == "verify_before_adding" for item in result))

    def test_required_and_preferred_sections_are_heuristic(self):
        result = parse_required_and_preferred(
            "Required qualifications:\\n- Python\\nPreferred qualifications:\\n- Kubernetes")
        self.assertIn("Python", result["required"])
        self.assertIn("Kubernetes", result["preferred"])
        self.assertIn("heuristic", result["warning"])

    def test_resume_completeness_reports_missing_sections(self):
        result = resume_completeness_report({"email": "x@example.test", "summary": "Analyst"})
        self.assertIn("experience", result["missing_sections"])
        self.assertGreater(result["completeness_percent"], 0)

    def test_keyword_frequency_validates_limit(self):
        self.assertEqual(keyword_frequency("python python django", 2)[0]["keyword"], "python")
        with self.assertRaises(ValueError):
            keyword_frequency("python", 0)

    def test_job_description_sanitization_bounds_input(self):
        self.assertEqual(sanitize_job_description("  Hello  ", 10), "Hello")
        with self.assertRaises(ValueError):
            sanitize_job_description("x", 0)

class ImportValidationTests(SimpleTestCase):
    def test_header_mapping_supports_common_aliases(self):
        result = map_headers(["Employer", "Job Title", "Application Status"])
        self.assertEqual(result["mapping"]["company"], 0)
        self.assertEqual(result["mapping"]["role"], 1)
        self.assertEqual(result["mapping"]["status"], 2)
        self.assertNotIn("company", result["missing_required"])

    def test_valid_row_normalizes_status_and_salary(self):
        result = validate_row({"Employer": "Acme", "Job Title": "Analyst", "Status": "APPLIED",
                               "Salary From": "50,000", "Salary To": "70000"})
        self.assertTrue(result["valid"])
        self.assertEqual(result["status"], "applied")
        self.assertEqual(result["salary_min"], "50000.00")

    def test_invalid_row_reports_multiple_field_errors(self):
        result = validate_row({"company": "", "role": "", "status": "mystery",
                               "applied_date": "tomorrow", "salary_min": "lots"})
        self.assertFalse(result["valid"])
        self.assertGreaterEqual(len(result["errors"]), 4)

    def test_salary_range_inversion_is_rejected(self):
        result = validate_row({"company": "A", "role": "B", "salary_min": 90000, "salary_max": 50000})
        self.assertIn("inverted_range", [error["code"] for error in result["errors"]])

    def test_csv_parser_returns_mapping_and_validation(self):
        report = parse_csv("Employer,Job Title,Status\\nAcme,Analyst,applied\\n,Engineer,saved")
        self.assertEqual(report["format"], "csv")
        self.assertEqual(report["row_count"], 2)
        self.assertEqual(report["valid_count"], 1)
        self.assertTrue(report["header_mapping"]["mapping"])

    def test_csv_requires_headers_and_content(self):
        with self.assertRaises(ValueError):
            parse_csv("")
        with self.assertRaises(ValueError):
            parse_csv("")

    def test_json_parser_accepts_application_wrappers(self):
        report = parse_json_records('{"applications":[{"company":"A","role":"B"}]}')
        self.assertEqual(report["valid_count"], 1)
        self.assertEqual(report["format"], "json")

    def test_json_parser_rejects_non_object_lists(self):
        with self.assertRaises(ValueError):
            parse_json_records("[1,2,3]")

    def test_duplicate_rows_are_flagged_without_automatic_deduplication(self):
        report = validate_rows([{"company":"A","role":"B"}, {"company":"A","role":"B"}])
        self.assertEqual(len(report["duplicate_warnings"]), 1)
        self.assertEqual(report["row_count"], 2)

    def test_preview_never_persists_and_can_skip_duplicates(self):
        rows = [{"company":"A","role":"B"}, {"company":"A","role":"B"}]
        result = preview_import(rows, mode="skip_duplicates")
        self.assertEqual(result["accepted_count"], 1)
        self.assertEqual(result["skipped_count"], 1)
        self.assertFalse(result["persistence_performed"])

    def test_preview_rejects_unknown_mode(self):
        with self.assertRaises(ValueError):
            preview_import([], mode="merge_everything")

    def test_csv_export_prevents_formula_injection(self):
        result = csv_export([{"company":"=IMPORTXML('x')","role":"Analyst"}])
        self.assertIn("'=IMPORTXML", result)

    def test_export_rejects_unknown_fields(self):
        with self.assertRaises(ValueError):
            csv_export([], fields=["password"])

    def test_import_statistics_summarizes_error_codes(self):
        report = validate_rows([{"company":"","role":""}])
        stats = import_statistics(report)
        self.assertEqual(stats["invalid"], 1)
        self.assertEqual(stats["top_error"], "required")

    def test_maximum_rows_is_bounded(self):
        report = validate_rows([{"company":str(i),"role":"Role"} for i in range(5)], maximum=2)
        self.assertEqual(report["row_count"], 2)
        self.assertTrue(report["truncated"])
        with self.assertRaises(ValueError):
            validate_rows([], maximum=6000)
