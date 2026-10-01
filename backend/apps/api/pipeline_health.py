from collections import Counter, defaultdict
from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.models import JobApplication, Interview, CareerContact


def _apps(request):
    return JobApplication.objects.filter(user=request.user)


def _days_since(value, today):
    return (today - value).days if value else None


def _follow_up_bucket(days):
    if days is None:
        return "never"
    if days <= 2:
        return "recent"
    if days <= 7:
        return "this_week"
    if days <= 21:
        return "this_month"
    return "older"


def _contact_summary(request):
    today = timezone.localdate()
    contacts = CareerContact.objects.filter(user=request.user)
    buckets = Counter()
    companies = defaultdict(int)
    for contact in contacts:
        bucket = _follow_up_bucket(_days_since(contact.last_contacted_at.date(), today) if contact.last_contacted_at else None)
        buckets[bucket] += 1
        if contact.company:
            companies[contact.company] += 1
    return {
        "total": contacts.count(),
        "with_email": contacts.exclude(email="").count(),
        "with_follow_up": contacts.filter(next_follow_up__isnull=False).count(),
        "follow_up_buckets": dict(buckets),
        "top_companies": sorted(
            [{"company": name, "contacts": count} for name, count in companies.items()],
            key=lambda row: (-row["contacts"], row["company"].lower()),
        )[:12],
    }


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pipeline_risk(request):
    today = timezone.localdate()
    applications = _apps(request).select_related()
    rows = []
    for item in applications:
        if item.status in {"rejected", "withdrawn"}:
            continue
        age = _days_since(item.updated_at.date(), today)
        follow_up_age = _days_since(item.next_action_date, today) if item.next_action_date else None
        risk = 0
        reasons = []
        if age is not None and age >= 21:
            risk += 35
            reasons.append("No recent pipeline update")
        elif age is not None and age >= 14:
            risk += 20
            reasons.append("Pipeline record is getting stale")
        if follow_up_age is not None and follow_up_age > 0:
            risk += min(40, 15 + follow_up_age)
            reasons.append("Next action is overdue")
        if item.status == "interview" and not item.next_action_date:
            risk += 20
            reasons.append("Interview stage has no next action")
        if item.status == "applied" and not item.next_action_date:
            risk += 10
            reasons.append("Applied stage has no follow-up date")
        if risk:
            rows.append({"id": item.id, "company": item.company, "role": item.role, "status": item.status, "risk": min(risk, 100), "reasons": reasons, "updated_at": item.updated_at, "next_action_date": item.next_action_date})
    rows.sort(key=lambda row: (-row["risk"], row["company"].lower()))
    return Response({"generated_at": timezone.now(), "total_risk_items": len(rows), "items": rows[:50]})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pipeline_health(request):
    applications = _apps(request)
    total = applications.count()
    active = applications.filter(status__in=["applied","screening","interview","offer"]).count()
    with_actions = applications.filter(next_action_date__isnull=False).count()
    stale = sum(1 for item in applications.filter(status__in=["applied","screening","interview","offer"]) if (timezone.localdate() - item.updated_at.date()).days >= 14)
    return Response({"total": total, "active": active, "with_next_action": with_actions, "stale_active": stale, "action_coverage": round(with_actions / total * 100, 1) if total else 0})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def relationship_health(request):
    summary = _contact_summary(request)
    interviews = Interview.objects.filter(application__user=request.user).count()
    applications_with_contacts = _apps(request).filter(contacts__isnull=False).distinct().count()
    summary.update({"interviews": interviews, "applications_with_contacts": applications_with_contacts})
    return Response(summary)
