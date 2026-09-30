"""Interview preparation domain services."""
from dataclasses import dataclass
from datetime import timedelta
from typing import Iterable

from django.utils import timezone

from apps.jobs.models import Interview, JobApplication


@dataclass(frozen=True)
class InterviewQuestion:
    category: str
    question: str
    purpose: str
    preparation_hint: str


QUESTION_BANK = (
    InterviewQuestion("behavioral", "Tell me about a project you are proud of.",
                       "Understand ownership and communication.",
                       "Prepare a concise situation, action, and result."),
    InterviewQuestion("behavioral", "Describe a difficult problem you solved.",
                       "Explore problem solving.",
                       "Focus on constraints, trade-offs, and measurable outcome."),
    InterviewQuestion("technical", "How would you design a reliable API?",
                       "Explore engineering fundamentals.",
                       "Discuss validation, observability, failure handling, and tests."),
    InterviewQuestion("technical", "How do you approach debugging a production issue?",
                       "Explore operational reasoning.",
                       "Explain reproduction, evidence, isolation, mitigation, and follow-up."),
    InterviewQuestion("role", "Why are you interested in this role?",
                       "Understand role alignment.",
                       "Connect the responsibilities to your documented experience."),
    InterviewQuestion("role", "What would you prioritize in your first 30 days?",
                       "Explore planning.",
                       "Use the job description and distinguish learning from delivery."),
    InterviewQuestion("questions", "What questions do you have for the team?",
                       "Assess preparation.",
                       "Prepare questions about success measures, collaboration, and workflow."),
)


def questions_for_application(application: JobApplication) -> list[InterviewQuestion]:
    role = (application.role or "").lower()
    questions = list(QUESTION_BANK)
    if "data" in role or "ai" in role:
        questions.extend([
            InterviewQuestion("domain", "How would you validate a dataset before use?",
                               "Explore data quality reasoning.",
                               "Discuss schema checks, sampling, provenance, and edge cases."),
            InterviewQuestion("domain", "How would you measure annotation consistency?",
                               "Explore quality methodology.",
                               "Discuss guidelines, agreement measures, review, and feedback loops."),
        ])
    if "backend" in role or "software" in role or "engineer" in role:
        questions.extend([
            InterviewQuestion("technical", "How would you investigate a slow database query?",
                               "Explore performance reasoning.",
                               "Discuss query plans, indexes, cardinality, and measured changes."),
            InterviewQuestion("technical", "How do you decide what belongs in a service layer?",
                               "Explore architecture judgment.",
                               "Explain separation of concerns and testability."),
        ])
    return questions


def upcoming_interviews(user, days: int = 30) -> list[Interview]:
    end = timezone.now() + timedelta(days=max(1, days))
    return list(
        Interview.objects.filter(
            application__user=user,
            scheduled_date__gte=timezone.now(),
            scheduled_date__lte=end,
        ).select_related("application").order_by("scheduled_date")
    )


def interview_readiness(application: JobApplication) -> dict:
    interviews = list(application.interviews.order_by("scheduled_date"))
    upcoming = [item for item in interviews if item.scheduled_date >= timezone.now()]
    completed = [item for item in interviews if item.completed_date]
    questions = questions_for_application(application)
    return {
        "application_id": application.id,
        "interview_count": len(interviews),
        "upcoming_count": len(upcoming),
        "completed_count": len(completed),
        "question_count": len(questions),
        "has_feedback": any(bool(item.feedback) for item in completed),
        "has_interviewer": any(bool(item.interviewer_name) for item in interviews),
        "recommended_actions": _recommended_actions(interviews, questions),
    }


def _recommended_actions(interviews: Iterable[Interview],
                         questions: Iterable[InterviewQuestion]) -> list[str]:
    items = list(interviews)
    actions = []
    if not items:
        actions.append("Confirm interview schedule and format.")
    if items and not any(item.interviewer_name for item in items):
        actions.append("Record interviewer names and roles when available.")
    if items and not any(item.notes for item in items):
        actions.append("Prepare concise notes about the role and company.")
    if len(list(questions)) < 5:
        actions.append("Add role-specific questions before the interview.")
    actions.append("Prepare two questions to ask the interview team.")
    return actions
