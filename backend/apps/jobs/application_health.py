from dataclasses import dataclass

from django.utils import timezone

from .interview_readiness import InterviewReadinessService
from .job_fit import JobFitAnalyzer
from .models import CareerTask, JobApplication


@dataclass
class ApplicationHealth:
    application_id: int
    company: str
    role: str
    status: str
    fit_score: int
    readiness_score: int
    action_count: int
    overdue_actions: int
    health_score: int
    signals: list[str]

    def to_dict(self):
        return {
            "application_id": self.application_id,
            "company": self.company,
            "role": self.role,
            "status": self.status,
            "fit_score": self.fit_score,
            "readiness_score": self.readiness_score,
            "action_count": self.action_count,
            "overdue_actions": self.overdue_actions,
            "health_score": self.health_score,
            "signals": self.signals,
        }


class ApplicationHealthService:
    ACTIVE_STATUSES = {"applied", "screening", "interview", "offer"}

    def __init__(self, user):
        self.user = user
        self.readiness = InterviewReadinessService(user)

    def analyze(self, application_id):
        app = JobApplication.objects.filter(
            id=application_id, user=self.user
        ).first()
        if not app:
            return None

        fit = JobFitAnalyzer(self.user).analyze(app)
        readiness = self.readiness.analyze(application_id)

        tasks = CareerTask.objects.filter(
            user=self.user,
            application=app,
            status__in=["todo", "in_progress"],
        )
        overdue = tasks.filter(due_date__lt=timezone.now()).count()

        fit_score = fit.score if fit else 0
        readiness_score = readiness.score if readiness else 0
        action_count = tasks.count()

        components = [fit_score]
        if app.status in {"screening", "interview", "offer"}:
            components.append(readiness_score)
        else:
            components.append(100 if readiness is None else readiness_score)

        action_score = 100 if not overdue else max(0, 100 - overdue * 20)
        components.append(action_score)
        health = round(sum(components) / len(components))

        signals = []
        if fit_score < 60:
            signals.append("Review role fit and missing requirements.")
        if readiness and readiness_score < 60:
            signals.append("More interview preparation is needed.")
        if overdue:
            signals.append(f"{overdue} overdue action(s) need attention.")
        if not signals:
            signals.append("No immediate risk signals detected.")

        return ApplicationHealth(
            application_id=app.id,
            company=app.company,
            role=app.role,
            status=app.status,
            fit_score=fit_score,
            readiness_score=readiness_score,
            action_count=action_count,
            overdue_actions=overdue,
            health_score=health,
            signals=signals,
        )

    def summary(self, limit=25):
        applications = JobApplication.objects.filter(
            user=self.user, status__in=self.ACTIVE_STATUSES
        ).order_by("-updated_at")[:limit]
        results = [self.analyze(app.id) for app in applications]
        results = [item for item in results if item]
        scores = [item.health_score for item in results]
        return {
            "count": len(results),
            "average_health": round(sum(scores) / len(scores), 2) if scores else 0,
            "healthy": sum(item.health_score >= 80 for item in results),
            "attention_needed": sum(item.health_score < 60 for item in results),
            "applications": [item.to_dict() for item in results],
        }


# Pure reporting helpers used by import previews, maintenance screens, and tests.
# They never mutate the input records or write to the database.
from datetime import date, datetime
from typing import Iterable, Mapping

CLOSED_STATUSES = {"rejected", "withdrawn", "archived", "closed", "hired", "accepted"}
KNOWN_STATUSES = {"saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn", "archived", "hired", "accepted"}


def _health_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except (TypeError, ValueError):
        return None


def inspect_application(record: Mapping, today: date | None = None) -> dict:
    row = dict(record)
    today = today or date.today()
    issues = []
    for field in ("company", "role"):
        if not str(row.get(field) or "").strip():
            issues.append({"code": f"missing_{field}", "field": field, "severity": "high"})
    status = str(row.get("status") or "").strip().lower()
    if status not in KNOWN_STATUSES:
        issues.append({"code": "unknown_status", "field": "status", "severity": "high"})
    url = str(row.get("job_url") or "").strip()
    if url and not url.lower().startswith(("https://", "http://")):
        issues.append({"code": "invalid_job_url", "field": "job_url", "severity": "medium"})
    health = "needs_attention" if any(item["severity"] == "high" for item in issues) else ("review_recommended" if issues else "looks_complete")
    return {"application_id": row.get("id"), "health": health, "issue_count": len(issues),
            "issues": issues, "status": status or None,
            "note": "Inspection only; no application fields were changed."}


def application_health_report(records: Iterable[Mapping], today: date | None = None) -> dict:
    inspected = [inspect_application(row, today=today) for row in records]
    counts = {key: sum(item["health"] == key for item in inspected)
              for key in ("looks_complete", "review_recommended", "needs_attention")}
    return {"record_count": len(inspected), "by_health": counts, "records": inspected,
            "automatic_changes_performed": False}


def stale_record_report(records: Iterable[Mapping], stale_days: int = 30, today: date | None = None) -> dict:
    if not isinstance(stale_days, int) or isinstance(stale_days, bool) or not 1 <= stale_days <= 3650:
        raise ValueError("stale_days must be between 1 and 3650")
    today = today or date.today()
    stale, closed = [], []
    for record in records:
        row = dict(record)
        status = str(row.get("status") or "").strip().lower()
        if status in CLOSED_STATUSES:
            closed.append(row.get("id"))
            continue
        updated = _health_date(row.get("updated_at") or row.get("updated") or row.get("created_at"))
        if updated is None:
            continue
        age = (today - updated).days
        if age >= stale_days:
            stale.append({"id": row.get("id"), "status": status, "age_days": age,
                          "updated_at": updated.isoformat(), "review_suggestion": "Review status and next action."})
    stale.sort(key=lambda item: (-item["age_days"], str(item["id"])))
    return {"stale_count": len(stale), "stale_records": stale,
            "closed_record_ids": closed, "stale_days": stale_days,
            "automatic_changes_performed": False}


def maintenance_plan(records: Iterable[Mapping], today: date | None = None) -> dict:
    rows = list(records)
    tasks = []
    for record in rows:
        inspection = inspect_application(record, today=today)
        for issue in inspection["issues"]:
            tasks.append({"application_id": record.get("id"), "code": issue["code"],
                          "severity": issue["severity"], "suggested_action": f"Review {issue['field']}."})
    severity_order = {"high": 0, "medium": 1, "low": 2}
    tasks.sort(key=lambda item: (severity_order[item["severity"]], str(item["application_id"]), item["code"]))
    return {"record_count": len(rows), "task_count": len(tasks), "tasks": tasks,
            "automatic_changes_performed": False}


def completeness_by_status(records: Iterable[Mapping]) -> list[dict]:
    groups = {}
    for record in records:
        row = dict(record)
        status = str(row.get("status") or "unknown").strip().lower() or "unknown"
        required = ("company", "role")
        present = sum(bool(str(row.get(field) or "").strip()) for field in required)
        groups.setdefault(status, {"status": status, "records": 0, "complete_fields": 0, "required_fields": 0})
        groups[status]["records"] += 1
        groups[status]["complete_fields"] += present
        groups[status]["required_fields"] += len(required)
    return [{**item, "completeness_percent": round(100 * item["complete_fields"] / item["required_fields"], 1)
             if item["required_fields"] else 100}
            for _, item in sorted(groups.items())]
