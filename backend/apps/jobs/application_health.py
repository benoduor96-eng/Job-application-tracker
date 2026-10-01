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
