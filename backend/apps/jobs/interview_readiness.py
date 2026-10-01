from dataclasses import dataclass
from django.utils import timezone

from .models import CareerTask, Interview, JobApplication


@dataclass
class ReadinessResult:
    application_id: int
    score: int
    interview_count: int
    completed_interviews: int
    pending_tasks: int
    overdue_tasks: int
    has_notes: bool
    has_job_description: bool
    recommendations: list[str]

    def to_dict(self):
        return {
            "application_id": self.application_id,
            "score": self.score,
            "interview_count": self.interview_count,
            "completed_interviews": self.completed_interviews,
            "pending_tasks": self.pending_tasks,
            "overdue_tasks": self.overdue_tasks,
            "has_notes": self.has_notes,
            "has_job_description": self.has_job_description,
            "recommendations": self.recommendations,
        }


class InterviewReadinessService:
    def __init__(self, user):
        self.user = user

    def analyze(self, application_id):
        app = JobApplication.objects.filter(id=application_id, user=self.user).first()
        if not app:
            return None

        now = timezone.now()
        interviews = Interview.objects.filter(application=app)
        tasks = CareerTask.objects.filter(user=self.user, application=app)
        completed = interviews.filter(outcome="passed").count()
        pending_tasks = tasks.filter(status__in=["todo", "in_progress"]).count()
        overdue = tasks.filter(
            status__in=["todo", "in_progress"], due_date__lt=now
        ).count()

        score = 0
        if interviews.exists():
            score += 25
        if completed:
            score += 15
        if app.notes.strip():
            score += 15
        if hasattr(app, "job_description"):
            score += 20
        if pending_tasks == 0:
            score += 15
        elif pending_tasks <= 2:
            score += 10
        if overdue == 0:
            score += 10

        recommendations = []
        if not interviews.exists():
            recommendations.append("Add the scheduled interview details.")
        if not app.notes.strip():
            recommendations.append("Record role-specific preparation notes.")
        if not hasattr(app, "job_description"):
            recommendations.append("Attach a job description to identify role requirements.")
        if pending_tasks:
            recommendations.append(f"Review {pending_tasks} open preparation task(s).")
        if overdue:
            recommendations.append(f"Resolve {overdue} overdue preparation task(s).")
        if completed:
            recommendations.append("Use previous interview outcomes and feedback to refine preparation.")

        return ReadinessResult(
            application_id=app.id,
            score=min(score, 100),
            interview_count=interviews.count(),
            completed_interviews=completed,
            pending_tasks=pending_tasks,
            overdue_tasks=overdue,
            has_notes=bool(app.notes.strip()),
            has_job_description=hasattr(app, "job_description"),
            recommendations=recommendations,
        )

    def summary(self, limit=50):
        applications = JobApplication.objects.filter(
            user=self.user, status__in=["screening", "interview", "offer"]
        ).order_by("-updated_at")[:limit]
        results = [self.analyze(app.id) for app in applications]
        results = [r for r in results if r]
        scores = [r.score for r in results]
        return {
            "count": len(results),
            "average_score": round(sum(scores) / len(scores), 2) if scores else 0,
            "ready": sum(r.score >= 80 for r in results),
            "needs_preparation": sum(r.score < 60 for r in results),
            "applications": [r.to_dict() for r in results],
        }
