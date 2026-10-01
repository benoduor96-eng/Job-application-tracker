from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncWeek
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.models import JobApplication, Interview, CareerTask

STATUS_LABELS = {"saved":"Saved","applied":"Applied","screening":"Screening","interview":"Interview","offer":"Offer","rejected":"Rejected","withdrawn":"Withdrawn"}

def _applications(request):
    return JobApplication.objects.filter(user=request.user)

def _week_start(value):
    return value - timedelta(days=value.weekday())

def _safe_percent(numerator, denominator):
    return round((numerator / denominator) * 100, 1) if denominator else 0.0

def _weekly_series(queryset, weeks=12):
    today = timezone.localdate()
    start = _week_start(today) - timedelta(weeks=weeks - 1)
    rows = queryset.filter(applied_date__gte=start).annotate(period=TruncWeek("applied_date")).values("period").annotate(total=Count("id")).order_by("period")
    lookup = {}
    for row in rows:
        key = row["period"].date() if hasattr(row["period"], "date") else row["period"]
        lookup[key] = row["total"]
    return [{"week": (start + timedelta(weeks=i)).isoformat(), "label": (start + timedelta(weeks=i)).strftime("%d %b"), "applications": lookup.get(start + timedelta(weeks=i), 0)} for i in range(weeks)]

def _status_matrix(queryset):
    rows = queryset.values("status").annotate(total=Count("id"))
    counts = {row["status"]: row["total"] for row in rows}
    total = sum(counts.values())
    return [{"status": key, "label": STATUS_LABELS[key], "count": counts.get(key, 0), "share": _safe_percent(counts.get(key, 0), total)} for key in STATUS_LABELS]

def _response_summary(queryset):
    total = queryset.count()
    applied = queryset.filter(applied_date__isnull=False).count()
    interviews = queryset.filter(status="interview").count()
    offers = queryset.filter(status="offer").count()
    return {"total": total, "applied": applied, "active": queryset.filter(status__in=["applied","screening","interview","offer"]).count(), "interviews": interviews, "offers": offers, "rejected": queryset.filter(status="rejected").count(), "application_to_interview": _safe_percent(interviews, applied), "application_to_offer": _safe_percent(offers, applied), "interview_to_offer": _safe_percent(offers, interviews)}

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_performance(request):
    queryset = _applications(request)
    weeks = max(4, min(int(request.query_params.get("weeks", 12)), 26))
    return Response({"generated_at": timezone.now(), "period_weeks": weeks, "weekly": _weekly_series(queryset, weeks), "statuses": _status_matrix(queryset), "responses": _response_summary(queryset)})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_activity(request):
    today = timezone.localdate()
    horizon = today + timedelta(days=30)
    interviews = Interview.objects.filter(application__user=request.user, scheduled_date__date__gte=today, scheduled_date__date__lte=horizon).select_related("application").order_by("scheduled_date")[:20]
    tasks = CareerTask.objects.filter(user=request.user, status__in=["todo","in_progress"], due_date__date__gte=today, due_date__date__lte=horizon).select_related("application").order_by("due_date")[:20]
    next_application = _applications(request).filter(next_action_date__gte=today, next_action_date__lte=horizon).order_by("next_action_date").values("id","company","role","next_action","next_action_date").first()
    return Response({"upcoming_interviews":[{"id":i.id,"company":i.application.company,"role":i.application.role,"type":i.get_interview_type_display(),"date":i.scheduled_date,"outcome":i.outcome} for i in interviews], "upcoming_tasks":[{"id":t.id,"title":t.title,"priority":t.priority,"status":t.status,"due":t.due_date,"company":t.application.company if t.application else "General"} for t in tasks], "next_application": next_application})
