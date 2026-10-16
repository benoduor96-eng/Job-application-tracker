"""Regression tests for deterministic backend workflow engines."""
from datetime import date, datetime, timezone
import pytest

from apps.jobs.application_lifecycle import (
    LifecycleError, can_transition, follow_up_state, plan_bulk_transition,
    transition_payload, validate_transition_history,
)
from apps.jobs.import_pipeline import (
    listing_fingerprint, normalize_import_record, preview_import,
)
from apps.jobs.recommendation_engine import (
    deadline_score, explain_priority, freshness_score, rank_applications,
)
from apps.jobs.reminder_engine import (
    combine_reminders, plan_application_reminders, plan_interview_reminders,
    plan_task_reminders, reminder_summary,
)
from apps.jobs.reporting_engine import (
    build_report, company_breakdown, funnel_metrics, salary_summary,
    status_distribution, time_to_apply, weekly_activity,
)
from apps.jobs.security_controls import (
    bounded_page_size, export_limit, redact_free_text, redact_mapping,
    safe_filename, validate_sort_field,
)
from apps.jobs.workflow_rules import (
    RuleValidationError, evaluate_rules, summarize_rule_set,
)


def rule(**overrides):
    value = {
        "id": "follow-up", "name": "Follow up after application",
        "event": "application.status_changed", "enabled": True,
        "match_all": True, "priority": 10,
        "conditions": [{"field": "status", "operator": "equals", "value": "applied"}],
        "actions": [{"kind": "create_task", "parameters": {"title": "Send follow-up"}}],
    }
    value.update(overrides)
    return value


def test_rule_matches_and_action_plan_is_preview_only():
    result = evaluate_rules([rule()], "application.status_changed", {"status": "APPLIED"})
    assert len(result) == 1
    assert result[0]["actions"][0]["kind"] == "create_task"


def test_rule_event_mismatch_does_not_match():
    assert evaluate_rules([rule()], "interview.scheduled", {"status": "applied"}) == []


def test_disabled_rule_does_not_match():
    assert evaluate_rules([rule(enabled=False)], "application.status_changed", {"status": "applied"}) == []


def test_any_condition_mode_accepts_one_matching_condition():
    item = rule(match_all=False, conditions=[
        {"field": "status", "operator": "equals", "value": "offer"},
        {"field": "company", "operator": "contains", "value": "acme"},
    ])
    assert evaluate_rules([item], "application.status_changed", {"status": "saved", "company": "ACME Ltd"})


def test_rule_validation_rejects_unknown_field():
    with pytest.raises(RuleValidationError):
        evaluate_rules([rule(conditions=[{"field": "password", "operator": "equals", "value": "x"}])],
                       "application.status_changed", {})


def test_rule_validation_rejects_unknown_action():
    with pytest.raises(RuleValidationError):
        evaluate_rules([rule(actions=[{"kind": "execute_shell"}])], "application.status_changed", {})


def test_rule_priority_is_stable():
    first = rule(id="b", priority=2)
    second = rule(id="a", priority=2)
    result = evaluate_rules([first, second], "application.status_changed", {"status": "applied"})
    assert [item["rule_id"] for item in result] == ["a", "b"]


def test_rule_summary_counts_actions_and_enabled_state():
    result = summarize_rule_set([rule(), rule(id="disabled", enabled=False)])
    assert result["total"] == 2
    assert result["enabled"] == 1
    assert result["actions"]["create_task"] == 2


def test_transition_policy_blocks_rejected_reopen_without_explicit_flag():
    assert not can_transition("rejected", "applied").allowed
    assert can_transition("rejected", "applied", reopen=True).allowed


def test_transition_payload_records_change_and_confirmation():
    payload = transition_payload("applied", "withdrawn", actor_id=7, note="User confirmed")
    assert payload["changed"] is True
    assert payload["requires_confirmation"] is True
    assert payload["actor_id"] == 7


def test_bulk_transition_is_atomic_preflight_when_any_row_rejected():
    plan = plan_bulk_transition([{"id": 1, "status": "applied"},
                                 {"id": 2, "status": "rejected"}], "interview")
    assert plan["ready_to_commit"] is False
    assert len(plan["accepted"]) == 1
    assert len(plan["rejected"]) == 1


def test_bulk_transition_flags_duplicate_ids():
    plan = plan_bulk_transition([{"id": 1, "status": "applied"},
                                 {"id": 1, "status": "applied"}], "interview")
    assert len(plan["rejected"]) == 1


def test_follow_up_state_boundaries():
    today = date(2026, 10, 17)
    assert follow_up_state(None, today) == "unscheduled"
    assert follow_up_state(today, today) == "due_today"
    assert follow_up_state(date(2026, 10, 18), today) == "due_soon"
    assert follow_up_state(date(2026, 10, 1), today) == "overdue"


def test_transition_history_detects_disconnected_statuses():
    issues = validate_transition_history([
        {"from_status": "saved", "to_status": "applied"},
        {"from_status": "screening", "to_status": "interview"},
    ])
    assert any(item["issue"] == "disconnected_history" for item in issues)


def test_reminder_planner_skips_terminal_application():
    rows = [{"id": 1, "company": "Acme", "status": "applied",
             "next_action_date": "2026-10-17"},
            {"id": 2, "company": "Beta", "status": "rejected",
             "next_action_date": "2026-10-17"}]
    result = plan_application_reminders(rows, owner_id=3, today=date(2026, 10, 17))
    assert [item["object_id"] for item in result] == [1]


def test_reminder_idempotency_is_stable():
    row = {"id": 3, "status": "applied", "next_action_date": "2026-10-17"}
    a = plan_application_reminders([row], owner_id=8, today=date(2026, 10, 17))
    b = plan_application_reminders([row], owner_id=8, today=date(2026, 10, 17))
    assert a[0]["idempotency_key"] == b[0]["idempotency_key"]


def test_interview_reminder_skips_past_and_completed():
    rows = [{"id": 1, "scheduled_date": "2026-10-18", "outcome": "scheduled"},
            {"id": 2, "scheduled_date": "2026-10-16", "outcome": "scheduled"},
            {"id": 3, "scheduled_date": "2026-10-18", "outcome": "passed"}]
    result = plan_interview_reminders(rows, owner_id=1, today=date(2026, 10, 17))
    assert [item["object_id"] for item in result] == [1]


def test_task_reminders_respect_completed_status():
    rows = [{"id": 1, "title": "Practice", "due_date": "2026-10-17", "status": "todo"},
            {"id": 2, "title": "Done", "due_date": "2026-10-17", "status": "done"}]
    result = plan_task_reminders(rows, owner_id=1, today=date(2026, 10, 17))
    assert [item["object_id"] for item in result] == [1]


def test_reminder_merge_deduplicates_and_sorts_by_urgency():
    first = plan_application_reminders([{"id": 1, "status": "applied",
        "next_action_date": "2026-10-17"}], owner_id=1, today=date(2026, 10, 17))
    second = plan_application_reminders([{"id": 1, "status": "applied",
        "next_action_date": "2026-10-17"}], owner_id=1, today=date(2026, 10, 17))
    result = combine_reminders(first, second)
    assert len(result) == 1
    assert reminder_summary(result)["today"] == 1


def test_status_distribution_keeps_zero_statuses():
    result = status_distribution([{"status": "applied"}])
    assert result["counts"]["offer"] == 0
    assert result["total"] == 1


def test_funnel_metrics_zero_division_is_safe():
    result = funnel_metrics([{"status": "saved"}])
    assert result["application_to_offer_percent"] == 0.0


def test_weekly_activity_validates_window():
    with pytest.raises(ValueError):
        weekly_activity([], weeks=0)


def test_company_breakdown_groups_case_insensitively():
    result = company_breakdown([{"company": "Acme", "status": "applied"},
                                {"company": "ACME", "status": "offer"}])
    assert len(result) == 1
    assert result[0]["application_count"] == 2


def test_salary_summary_ignores_invalid_and_reversed_ranges():
    result = salary_summary([
        {"salary_min": "100", "salary_max": "200"},
        {"salary_min": "300", "salary_max": "250"},
        {"salary_min": "n/a", "salary_max": None},
    ])
    assert result["records_with_valid_ranges"] == 1
    assert result["median_range_midpoint"] == 150.0


def test_time_to_apply_ignores_negative_durations_and_reports_them():
    result = time_to_apply([
        {"created_at": "2026-10-01", "applied_date": "2026-10-04"},
        {"created_at": "2026-10-05", "applied_date": "2026-10-02"},
    ])
    assert result["average_days"] == 3.0
    assert result["invalid_date_order_count"] == 1


def test_build_report_contains_all_sections():
    result = build_report([{"status": "applied", "company": "Acme"}],
                          today=date(2026, 10, 17), weeks=2)
    assert {"status_distribution", "funnel", "weekly_activity", "companies",
            "salary", "time_to_apply"} <= set(result)


def test_priority_inactive_applications_score_zero():
    result = explain_priority({"id": 1, "status": "rejected"})
    assert result["score"] == 0
    assert result["priority"] == "inactive"


def test_priority_score_is_bounded_and_explained():
    result = explain_priority({"id": 1, "status": "interview",
        "next_action_date": "2026-10-17", "updated_at": "2026-10-17"},
        fit_score=100, preparation_score=20, today=date(2026, 10, 17))
    assert 0 <= result["score"] <= 100
    assert result["explanation"]
    assert len(result["factors"]) == 7


def test_rank_applications_is_deterministic():
    apps = [{"id": 2, "status": "applied"}, {"id": 1, "status": "applied"}]
    first = rank_applications(apps, today=date(2026, 10, 17))
    second = rank_applications(apps, today=date(2026, 10, 17))
    assert first == second


def test_deadline_and_freshness_boundaries():
    today = date(2026, 10, 17)
    assert deadline_score("2026-10-16", today=today) == 100
    assert deadline_score("2026-10-17", today=today) == 98
    assert freshness_score("2026-10-17", today=today) == 100


def test_import_requires_company_and_role():
    normalized, issues = normalize_import_record({"company": "Acme"}, 1)
    assert normalized["company"] == "Acme"
    assert any(issue.field == "role" and issue.code == "required" for issue in issues)


def test_import_rejects_unsafe_url_and_invalid_salary_range():
    _, issues = normalize_import_record({
        "company": "Acme", "role": "Engineer",
        "job_url": "https://user:pass@example.com/job",
        "salary_min": 90000, "salary_max": 80000,
    }, 1)
    codes = {issue.code for issue in issues}
    assert "invalid_url" in codes
    assert "salary_range" in codes


def test_import_preview_deduplicates_within_batch_and_existing_records():
    rows = [{"company": "Acme", "role": "Engineer", "job_url": "https://example.com/jobs/1"},
            {"company": "ACME", "role": "engineer", "job_url": "https://example.com/jobs/1"}]
    result = preview_import(rows)
    assert result.total_rows == 2
    assert len(result.accepted) == 1
    assert len(result.duplicates) == 1


def test_import_fingerprint_ignores_query_string():
    a = listing_fingerprint({"company": "Acme", "role": "Engineer",
                             "job_url": "https://example.com/jobs/1?source=a"})
    b = listing_fingerprint({"company": " ACME ", "role": " engineer ",
                             "job_url": "https://example.com/jobs/1?source=b"})
    assert a == b


def test_security_helpers_bound_pagination_and_exports():
    assert bounded_page_size(1000) == 100
    assert bounded_page_size("bad") == 25
    assert export_limit(100000) == 10000
    with pytest.raises(ValueError):
        export_limit("many")


def test_redaction_handles_nested_secret_keys_and_bearer_tokens():
    result = redact_mapping({"profile": {"api_key": "hidden", "role": "Engineer"}})
    assert result["profile"]["api_key"] == "[REDACTED]"
    assert result["profile"]["role"] == "Engineer"
    assert "Bearer [REDACTED]" in redact_free_text("Authorization: Bearer abc.def.ghi")


def test_safe_filename_removes_traversal_and_controls():
    assert safe_filename("../../my export.json") == "my-export.json"


def test_sort_validation_uses_allow_list():
    assert validate_sort_field("created_at", ["created_at", "company"], default="company") == "created_at"
    assert validate_sort_field("drop table", ["created_at", "company"], default="company") == "company"
