"""Authenticated HTTP adapters for the career platform's pure domain services."""
from django.utils.dateparse import parse_date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.analytics_cohorts import (
    analytics_quality_report, company_rollup, funnel_summary, outcome_summary,
    response_lag_summary, salary_band_summary, source_performance, weekly_application_counts,
    weekly_cohort_retention,
)
from apps.jobs.duplicate_resolution import duplicate_report
from apps.jobs.privacy_lifecycle import build_retention_report
from apps.jobs.search_language import SearchSyntaxError, explain_query, rank_records
from apps.jobs.models import (
    ApplicationActivity, CareerContact, CareerTask, Interview, JobApplication, Resume,
)

MAX_ANALYTICS_ROWS = 5000


def _applications_for_user(user):
    return list(JobApplication.objects.filter(user=user).values(
        "id", "company", "role", "location", "job_url", "status", "salary_min", "salary_max",
        "applied_date", "next_action_date", "next_action", "notes", "created_at", "updated_at"
    )[:MAX_ANALYTICS_ROWS])


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def advanced_application_search(request):
    """Search only the caller's records using the validated search language."""
    query = request.query_params.get("q", "")
    try:
        explanation = explain_query(query)
        records = _applications_for_user(request.user)
        ranked = rank_records(records, query)
    except (SearchSyntaxError, TypeError, ValueError) as exc:
        return Response({"detail": str(exc)}, status=400)
    return Response({"query": explanation, "count": len(ranked), "items": ranked,
                     "limit": MAX_ANALYTICS_ROWS})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def duplicate_review(request):
    """Return duplicate candidates for the current user's own application records."""
    records = _applications_for_user(request.user)[:1000]
    try:
        threshold = float(request.query_params.get("threshold", ".55"))
        limit = int(request.query_params.get("limit", "500"))
        if not 0 <= threshold <= 1:
            raise ValueError("threshold must be between 0 and 1")
        if not 1 <= limit <= 2000:
            raise ValueError("limit must be between 1 and 2000")
        report = duplicate_report(records)
        report["pairs"] = [item for item in report["pairs"] if item["score"] >= threshold][:limit]
        report["threshold"] = threshold
        report["truncated"] = JobApplication.objects.filter(user=request.user).count() > 1000
        report["warning"] = "Candidates are suggestions only. No records were merged or deleted."
    except (TypeError, ValueError) as exc:
        return Response({"detail": str(exc)}, status=400)
    return Response(report)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cohort_analytics(request):
    """Return bounded analytics from the authenticated user's application snapshot."""
    try:
        weeks = int(request.query_params.get("weeks", "12"))
        periods = int(request.query_params.get("periods", "8"))
        if not 1 <= weeks <= 104:
            raise ValueError("weeks must be between 1 and 104")
        if not 1 <= periods <= 52:
            raise ValueError("periods must be between 1 and 52")
    except (TypeError, ValueError) as exc:
        return Response({"detail": str(exc)}, status=400)
    rows = _applications_for_user(request.user)
    return Response({
        "count": len(rows),
        "funnel": funnel_summary(rows),
        "outcomes": outcome_summary(rows),
        "weekly_applications": weekly_application_counts(rows, weeks=weeks),
        "weekly_cohorts": weekly_cohort_retention(rows, periods=periods),
        "companies": company_rollup(rows),
        "salary_bands": salary_band_summary(rows),
        "source_performance": source_performance(rows),
        "response_lag": response_lag_summary(rows),
        "quality": analytics_quality_report(rows),
        "truncated": JobApplication.objects.filter(user=request.user).count() > MAX_ANALYTICS_ROWS,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retention_preview(request):
    """Report on retention eligibility without deleting or changing any records."""
    rows = []
    for model_name, queryset in (
        ("application", JobApplication.objects.filter(user=request.user).values("id", "created_at")),
        ("resume", Resume.objects.filter(user=request.user).values("id", "created_at")),
        ("contact", CareerContact.objects.filter(user=request.user).values("id", "created_at")),
        ("notification", CareerTask.objects.filter(user=request.user).values("id", "created_at")),
        ("audit_event", ApplicationActivity.objects.filter(user=request.user).values("id", "created_at")),
        ("notification", Interview.objects.filter(application__user=request.user).values("id", "created_at")),
    ):
        rows.extend({"record_type": model_name, **item} for item in queryset[:MAX_ANALYTICS_ROWS])
    report = build_retention_report(rows)
    report["policy_note"] = "Preview only; no records were deleted. Confirm applicable retention requirements before any destructive action."
    return Response(report)
