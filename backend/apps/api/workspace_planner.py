from datetime import date, timedelta
from collections import Counter, defaultdict

from django.db.models import Count, Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.models import JobApplication, CareerTask, Interview, CareerContact

STATUS_ORDER = ["saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn"]
ACTIVE_STATUSES = {"saved", "applied", "screening", "interview", "offer"}


def safe_rate(numerator, denominator):
    return round((numerator / denominator) * 100, 1) if denominator else 0


def applications_for(user):
    return JobApplication.objects.filter(user=user).prefetch_related("interviews", "contacts")


def status_counts(applications):
    counts = Counter(item.status for item in applications)
    return {status: counts.get(status, 0) for status in STATUS_ORDER}


def priority_for(application, today):
    score = 0
    reasons = []

    if application.status == "interview":
        score += 30
        reasons.append("interview stage")
    elif application.status == "offer":
        score += 35
        reasons.append("offer stage")
    elif application.status == "screening":
        score += 20
        reasons.append("active screening")

    if application.next_action_date:
        days = (application.next_action_date - today).days
        if days < 0:
            score += 40
            reasons.append("follow-up overdue")
        elif days == 0:
            score += 30
            reasons.append("follow-up due today")
        elif days <= 3:
            score += 20
            reasons.append("follow-up due soon")

    if application.applied_date and application.status in {"applied", "screening"}:
        age = (today - application.applied_date).days
        if age >= 14:
            score += 15
            reasons.append("application waiting over two weeks")

    if not application.next_action and application.status in ACTIVE_STATUSES:
        score += 10
        reasons.append("no next action recorded")

    priority = "urgent" if score >= 60 else "high" if score >= 40 else "medium" if score >= 20 else "low"
    return priority, score, reasons


def workspace_summary(user):
    today = date.today()
    applications = list(applications_for(user))
    counts = status_counts(applications)
    active = [item for item in applications if item.status in ACTIVE_STATUSES]
    overdue = [
        item for item in active
        if item.next_action_date and item.next_action_date < today
    ]
    upcoming = [
        item for item in active
        if item.next_action_date and today <= item.next_action_date <= today + timedelta(days=7)
    ]

    interview_count = Interview.objects.filter(
        application__user=user,
        scheduled_date__date__gte=today,
        scheduled_date__date__lte=today + timedelta(days=14),
    ).count()

    contact_count = CareerContact.objects.filter(
        user=user,
        next_follow_up__isnull=False,
        next_follow_up__date__lte=today + timedelta(days=7),
    ).count()

    open_tasks = CareerTask.objects.filter(user=user).exclude(
        status__in=["done", "cancelled"]
    ).count()
    completed_tasks = CareerTask.objects.filter(user=user, status="done").count()

    applied = sum(counts[name] for name in ["applied", "screening", "interview", "offer", "rejected"])
    interviews = counts["interview"] + counts["offer"]

    return {
        "generated_on": today.isoformat(),
        "total_applications": len(applications),
        "active_applications": len(active),
        "status_counts": counts,
        "conversion": {
            "applied_rate": safe_rate(applied, len(applications)),
            "interview_rate": safe_rate(interviews, applied),
            "offer_rate": safe_rate(counts["offer"], applied),
        },
        "attention": {
            "overdue_followups": len(overdue),
            "due_within_seven_days": len(upcoming),
            "upcoming_interviews": interview_count,
            "contacts_needing_followup": contact_count,
            "open_tasks": open_tasks,
            "completed_tasks": completed_tasks,
        },
    }


def priority_queue(user, limit=25):
    today = date.today()
    rows = []
    for application in applications_for(user):
        priority, score, reasons = priority_for(application, today)
        if not score:
            continue
        rows.append({
            "id": application.id,
            "company": application.company,
            "role": application.role,
            "status": application.status,
            "priority": priority,
            "score": score,
            "reasons": reasons,
            "next_action": application.next_action,
            "next_action_date": application.next_action_date.isoformat() if application.next_action_date else None,
        })
    rows.sort(key=lambda item: (-item["score"], item["next_action_date"] or "9999-12-31"))
    return rows[:limit]


def weekly_plan(user):
    today = date.today()
    end = today + timedelta(days=6)
    buckets = defaultdict(list)

    for application in applications_for(user):
        if application.next_action_date and today <= application.next_action_date <= end:
            buckets[application.next_action_date.isoformat()].append({
                "type": "application",
                "id": application.id,
                "title": application.next_action or "Follow up",
                "company": application.company,
                "role": application.role,
            })

    for task in CareerTask.objects.filter(
        user=user,
        due_date__date__gte=today,
        due_date__date__lte=end,
    ).exclude(status__in=["done", "cancelled"]):
        buckets[task.due_date.date().isoformat()].append({
            "type": "task", "id": task.id, "title": task.title, "priority": task.priority,
        })

    for interview in Interview.objects.filter(
        application__user=user,
        scheduled_date__date__gte=today,
        scheduled_date__date__lte=end,
    ).select_related("application"):
        buckets[interview.scheduled_date.date().isoformat()].append({
            "type": "interview",
            "id": interview.id,
            "title": interview.get_interview_type_display(),
            "company": interview.application.company,
            "role": interview.application.role,
        })

    days = []
    cursor = today
    while cursor <= end:
        key = cursor.isoformat()
        items = buckets.get(key, [])
        days.append({
            "date": key,
            "weekday": cursor.strftime("%A"),
            "items": items,
            "item_count": len(items),
        })
        cursor += timedelta(days=1)

    return {"start": today.isoformat(), "end": end.isoformat(), "days": days,
            "total_items": sum(day["item_count"] for day in days)}


def company_breakdown(user):
    rows = JobApplication.objects.filter(user=user).values("company").annotate(
        total=Count("id"),
        active=Count("id", filter=Q(status__in=ACTIVE_STATUSES)),
        interviews=Count("id", filter=Q(status__in=["interview", "offer"])),
        offers=Count("id", filter=Q(status="offer")),
    ).order_by("-total", "company")

    return [{
        "company": row["company"],
        "total": row["total"],
        "active": row["active"],
        "interviews": row["interviews"],
        "offers": row["offers"],
        "offer_rate": safe_rate(row["offers"], row["total"]),
    } for row in rows]


def recommendations(user):
    today = date.today()
    result = []
    applications = list(applications_for(user))

    for application in applications:
        if application.status in {"rejected", "withdrawn"}:
            continue

        priority, score, reasons = priority_for(application, today)

        if not application.next_action:
            result.append({
                "kind": "missing_action",
                "priority": "medium",
                "application_id": application.id,
                "title": "Define the next step for " + application.company,
                "detail": "Add a concrete action and target date.",
            })

        if application.next_action_date and application.next_action_date < today:
            result.append({
                "kind": "overdue",
                "priority": "high",
                "application_id": application.id,
                "title": "Review overdue follow-up at " + application.company,
                "detail": "The planned action date has passed.",
            })

        if score >= 40:
            result.append({
                "kind": "priority",
                "priority": priority,
                "application_id": application.id,
                "title": "Prioritize " + application.company + " — " + application.role,
                "detail": "; ".join(reasons),
            })

    if not applications:
        result.append({
            "kind": "onboarding", "priority": "high", "application_id": None,
            "title": "Add your first application",
            "detail": "Start the pipeline with the roles you are actively pursuing.",
        })
    return result[:30]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workspace_summary_view(request):
    return Response(workspace_summary(request.user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workspace_priority_view(request):
    try:
        limit = min(max(int(request.query_params.get("limit", 25)), 1), 100)
    except (TypeError, ValueError):
        limit = 25
    items = priority_queue(request.user, limit)
    return Response({"count": len(items), "items": items})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workspace_week_view(request):
    return Response(weekly_plan(request.user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workspace_companies_view(request):
    items = company_breakdown(request.user)
    return Response({"count": len(items), "companies": items})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workspace_recommendations_view(request):
    items = recommendations(request.user)
    return Response({"count": len(items), "recommendations": items})
