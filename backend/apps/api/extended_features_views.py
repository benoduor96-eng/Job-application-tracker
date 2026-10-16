"""Authenticated APIs for local career guidance, import preflight, and data export."""
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.career_assistant import build_job_fit_report, interview_question_set, resume_review
from apps.jobs.job_board_adapters import (\n    JobImportError, normalize_generic, normalize_greenhouse, normalize_lever, parse_jobs_csv,\n)
from apps.jobs.models import (
    ApplicationActivity, CareerContact, CareerProfile, CareerTask, Interview,
    JobApplication, JobDescription, Resume, SavedSearch,
)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def career_assistant_analyze(request):
    """Review candidate-provided resume text or compare it with a job description."""
    resume_text = request.data.get("resume_text", "")
    description = request.data.get("job_description", "")
    skills = request.data.get("skills", [])
    if not isinstance(resume_text, str) or not isinstance(description, str):
        return Response({"detail": "resume_text and job_description must be strings."}, status=400)
    if len(resume_text) > 50_000 or len(description) > 50_000:
        return Response({"detail": "Each text field is limited to 50,000 characters."}, status=400)
    if not isinstance(skills, list) or len(skills) > 100 or any(not isinstance(skill, str) for skill in skills):
        return Response({"detail": "skills must be a list of up to 100 strings."}, status=400)
    payload = {"resume_review": resume_review(resume_text)} if resume_text else {}
    if description:
        payload["job_fit_review"] = build_job_fit_report(skills, description)
    if not payload:
        return Response({"detail": "Provide resume_text, job_description, or both."}, status=400)
    payload["provider"] = "local-deterministic"
    payload["limitations"] = "Rule-based suggestions only; no external AI provider or hiring prediction is used."
    return Response(payload)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def career_assistant_interview_kit(request):
    """Generate a role-specific interview question set from user-provided context."""
    role, skills, count = request.data.get("role", ""), request.data.get("skills", []), request.data.get("count", 8)
    if not isinstance(role, str) or len(role) > 160:
        return Response({"detail": "role must be a string of at most 160 characters."}, status=400)
    if not isinstance(skills, list) or len(skills) > 12 or any(not isinstance(skill, str) for skill in skills):
        return Response({"detail": "skills must be a list of up to 12 strings."}, status=400)
    try:
        count = int(count)
    except (TypeError, ValueError):
        return Response({"detail": "count must be an integer."}, status=400)
    if not 1 <= count <= 20:
        return Response({"detail": "count must be between 1 and 20."}, status=400)
    return Response({"role": role or "the role", "questions": interview_question_set(role, skills, count)})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def normalize_job_import(request):
    """Validate one listing or CSV text before the client confirms persistence."""
    csv_text = request.data.get("csv")
    try:
        if csv_text is not None:
            if not isinstance(csv_text, str):
                return Response({"detail": "csv must be a string."}, status=400)
            return Response(parse_jobs_csv(csv_text))
        provider = request.data.get("provider", "generic")
        record = request.data.get("job", request.data)
        adapters = {
            "generic": normalize_generic,
            "greenhouse": normalize_greenhouse,
            "lever": normalize_lever,
        }
        if provider not in adapters:
            return Response({"detail": "provider must be generic, greenhouse, or lever."}, status=400)
        return Response({"job": adapters[provider](record)})
    except JobImportError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def personal_data_export(request):
    """Export the authenticated user's tracked career data as JSON."""
    user = request.user
    applications = JobApplication.objects.filter(user=user)
    application_ids = list(applications.values_list("id", flat=True))
    data = {
        "schema_version": 1,
        "exported_for": {"username": user.get_username()},
        "applications": list(applications.values()),
        "interviews": list(Interview.objects.filter(application_id__in=application_ids).values()),
        "contacts": list(CareerContact.objects.filter(user=user).values()),
        "career_profile": list(CareerProfile.objects.filter(user=user).values()),
        "resumes": list(Resume.objects.filter(user=user).values()),
        "tasks": list(CareerTask.objects.filter(user=user).values()),
        "job_descriptions": list(JobDescription.objects.filter(user=user).values()),
        "activities": list(ApplicationActivity.objects.filter(user=user).values()),
        "saved_searches": list(SavedSearch.objects.filter(user=user).values()),
    }
    response = HttpResponse(json.dumps(data, cls=DjangoJSONEncoder, indent=2),
                            content_type="application/json; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="job-tracker-personal-data.json"'
    response["Cache-Control"] = "no-store"
    return response
