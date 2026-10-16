"""Authenticated endpoints for workflow preview, reminders, and explainable priority."""
from datetime import date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.application_lifecycle import LifecycleError, plan_bulk_transition
from apps.jobs.import_pipeline import listing_fingerprint, preview_import
from apps.jobs.models import CareerTask, Interview, JobApplication
from apps.jobs.recommendation_engine import rank_applications
from apps.jobs.reminder_engine import (
    ReminderInputError, combine_reminders, plan_application_reminders,
    plan_interview_reminders, plan_task_reminders, reminder_summary,
)
from apps.jobs.workflow_rules import RuleValidationError, evaluate_rules, summarize_rule_set


def _positive_int(value, default, maximum):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return default
    if number < 1:
        return default
    return min(number, maximum)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def workflow_preview(request):
    """Evaluate caller-owned rule definitions against a supplied context; no side effects."""
    rules = request.data.get("rules", [])
    event = request.data.get("event")
    context = request.data.get("context", {})
    if not isinstance(rules, list) or not isinstance(context, dict):
        return Response({"detail": "rules must be a list and context must be an object."}, status=400)
    try:
        plans = evaluate_rules(rules, event, context)
        summary = summarize_rule_set(rules)
    except RuleValidationError as exc:
        return Response({"detail": str(exc)}, status=400)
    return Response({"event": event, "plans": plans, "summary": summary,
                     "execution_mode": "preview_only"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def lifecycle_transition_preview(request):
    """Preflight status changes for this user's applications without saving them."""
    ids = request.data.get("application_ids", [])
    target = request.data.get("target_status")
    reopen_ids = request.data.get("reopen_ids", [])
    if not isinstance(ids, list) or not 1 <= len(ids) <= 200:
        return Response({"detail": "application_ids must contain 1 to 200 ids."}, status=400)
    if not isinstance(reopen_ids, list):
        return Response({"detail": "reopen_ids must be a list."}, status=400)
    rows = list(JobApplication.objects.filter(user=request.user, id__in=ids).values("id", "status"))
    found = {row["id"] for row in rows}
    missing = [{"id": item, "reason": "Not found or not owned by the current user."}
               for item in ids if item not in found]
    try:
        plan = plan_bulk_transition(rows, target, reopen_ids=reopen_ids)
    except LifecycleError as exc:
        return Response({"detail": str(exc)}, status=400)
    plan["rejected"].extend(missing)
    plan["requested"] = len(ids)
    plan["ready_to_commit"] = not plan["rejected"]
    return Response({**plan, "execution_mode": "preview_only"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reminder_inbox(request):
    """Build a consolidated reminder inbox from the signed-in user's own records."""
    horizon = _positive_int(request.query_params.get("days"), 14, 90)
    today_text = request.query_params.get("today")
    try:
        today = date.fromisoformat(today_text) if today_text else date.today()
    except ValueError:
        return Response({"detail": "today must use YYYY-MM-DD."}, status=400)
    applications = list(JobApplication.objects.filter(user=request.user).values(
        "id", "company", "role", "status", "next_action", "next_action_date"))
    interviews = list(Interview.objects.filter(application__user=request.user).values(
        "id", "interview_type", "outcome", "scheduled_date",
        "application__company", "application__role"))
    interviews = [{
        "id": row["id"], "interview_type": row["interview_type"], "outcome": row["outcome"],
        "scheduled_date": row["scheduled_date"], "company": row["application__company"],
        "role": row["application__role"],
    } for row in interviews]
    tasks = list(CareerTask.objects.filter(user=request.user).values(
        "id", "title", "status", "due_date", "priority"))
    for task in tasks:
        task["completed"] = task["status"] in {"done", "cancelled"}
    try:
        groups = (
            plan_application_reminders(applications, owner_id=request.user.pk, today=today, horizon_days=horizon),
            plan_interview_reminders(interviews, owner_id=request.user.pk, today=today, horizon_days=horizon),
            plan_task_reminders(tasks, owner_id=request.user.pk, today=today, horizon_days=horizon),
        )
        reminders = combine_reminders(*groups)
    except (ReminderInputError, TypeError, ValueError) as exc:
        return Response({"detail": str(exc)}, status=400)
    return Response({"today": today.isoformat(), "horizon_days": horizon,
                     "summary": reminder_summary(reminders), "reminders": reminders})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def priority_queue(request):
    """Rank active applications using transparent, deterministic weighted rules."""
    limit = _positive_int(request.query_params.get("limit"), 50, 200)
    applications = list(JobApplication.objects.filter(user=request.user).values(
        "id", "company", "role", "location", "status", "salary_min", "salary_max",
        "next_action_date", "updated_at", "created_at", "applied_date", "next_action"))
    try:
        profile_obj = request.user.career_profile
        profile = {"minimum_salary": profile_obj.minimum_salary,
                   "target_salary": profile_obj.target_salary}
    except Exception:
        profile = {}
    ranked = rank_applications(applications, profile=profile, limit=limit)
    by_id = {item["id"]: item for item in applications}
    for item in ranked:
        item["company"] = by_id.get(item["application_id"], {}).get("company", "")
        item["role"] = by_id.get(item["application_id"], {}).get("role", "")
    return Response({"count": len(ranked), "items": ranked,
                     "method": "transparent-weighted-rules-v1"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def import_preview(request):
    """Validate candidate import rows and detect duplicates against the user's records."""
    rows = request.data.get("rows")
    if not isinstance(rows, list):
        return Response({"detail": "rows must be a list of job objects."}, status=400)
    if len(rows) > 5000:
        return Response({"detail": "At most 5000 rows can be previewed."}, status=400)
    existing = list(JobApplication.objects.filter(user=request.user).values(
        "company", "role", "job_url"))
    fingerprints = [listing_fingerprint(item) for item in existing]
    preview = preview_import(rows, existing_fingerprints=fingerprints)
    return Response(preview.as_dict())
