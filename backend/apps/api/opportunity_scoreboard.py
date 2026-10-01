from collections import Counter

from django.db.models import Count
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.models import JobApplication, JobDescription


STATUS_WEIGHT = {
    "saved": 20,
    "applied": 45,
    "screening": 60,
    "interview": 75,
    "offer": 95,
    "rejected": 0,
    "withdrawn": 0,
}


def _score(application, descriptions):
    score = STATUS_WEIGHT.get(application.status, 10)
    signals = []
    if application.applied_date:
        score += 5
        signals.append("Application date recorded")
    if application.next_action_date:
        score += 8
        signals.append("Next action scheduled")
    if application.job_url:
        score += 3
        signals.append("Job source link saved")
    if application.notes:
        score += 4
        signals.append("Notes captured")
    if application.salary_min or application.salary_max:
        score += 4
        signals.append("Compensation data captured")
    if application.status in {"interview", "offer"}:
        score += 8
        signals.append("Late-stage pipeline")
    score = min(score, 100)

    description = descriptions.get(application.id)
    if description:
        required = set(str(x).lower() for x in (description.required_skills or []))
        preferred = set(str(x).lower() for x in (description.preferred_skills or []))
        if required:
            score += min(10, len(required))
            signals.append("Job requirements analyzed")
        if preferred:
            score += min(5, len(preferred) // 2 + 1)
            signals.append("Preferred skills analyzed")
        score = min(score, 100)
    return score, signals


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def opportunity_scoreboard(request):
    applications = JobApplication.objects.filter(user=request.user).order_by("-updated_at")
    descriptions = {d.application_id: d for d in JobDescription.objects.filter(user=request.user, application__isnull=False)}
    rows = []
    for application in applications:
        score, signals = _score(application, descriptions)
        rows.append({
            "id": application.id,
            "company": application.company,
            "role": application.role,
            "status": application.status,
            "score": score,
            "signals": signals,
            "updated_at": application.updated_at,
        })
    rows.sort(key=lambda row: (-row["score"], row["company"].lower(), row["role"].lower()))
    distribution = Counter(
        "high" if r["score"] >= 75 else "medium" if r["score"] >= 50 else "low"
        for r in rows
    )
    return Response({
        "generated_at": timezone.now(),
        "total": len(rows),
        "distribution": dict(distribution),
        "average_score": round(sum(r["score"] for r in rows) / len(rows), 1) if rows else 0,
        "opportunities": rows[:50],
    })
