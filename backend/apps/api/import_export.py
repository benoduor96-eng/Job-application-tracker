import csv
import io
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.jobs.models import JobApplication


FIELDS = [
    "company", "role", "location", "job_url", "status",
    "salary_min", "salary_max", "applied_date", "next_action",
    "next_action_date", "notes",
]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_applications(request):
    applications = JobApplication.objects.filter(user=request.user)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=FIELDS)
    writer.writeheader()
    for application in applications.iterator():
        writer.writerow({field: getattr(application, field) for field in FIELDS})
    response = HttpResponse(output.getvalue(), content_type="text/csv")
    response.data = [
        {field: getattr(application, field) for field in FIELDS}
        for application in applications
    ]
    response["Content-Disposition"] = 'attachment; filename="job-applications.csv"'
    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def import_applications(request):
    uploaded = request.FILES.get("file")
    if not uploaded:
        return Response({"detail": "CSV file is required."}, status=400)
    decoded = uploaded.read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))
    missing = [field for field in FIELDS if field not in (reader.fieldnames or [])]
    if missing:
        return Response({"detail": "Missing columns.", "columns": missing}, status=400)
    created = 0
    errors = []
    for line, row in enumerate(reader, start=2):
        try:
            nullable_fields = {"salary_min", "salary_max", "applied_date", "next_action_date"}
            data = {
                field: (row.get(field) or None if field in nullable_fields else row.get(field) or "")
                for field in FIELDS
            }
            data["user"] = request.user
            JobApplication.objects.create(**data)
            created += 1
        except Exception as exc:
            errors.append({"line": line, "error": str(exc)})
    return Response({"created": created, "errors": errors})
