"""
Career intelligence domain services.

The module contains deterministic, testable business rules for job matching,
resume targeting, follow-up planning, and application prioritisation.
It deliberately avoids network calls so the core scoring behaviour remains
reproducible in API requests, background jobs, and automated tests.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Iterable, Sequence

from django.db.models import QuerySet

from apps.jobs.models import CareerProfile, CareerTask, JobApplication, JobDescription


DEFAULT_SKILLS = {
    "python", "django", "java", "spring", "spring boot", "javascript",
    "typescript", "react", "sql", "postgresql", "docker", "git", "rest",
    "api", "aws", "azure", "gcp", "kubernetes", "redis", "celery",
    "pytest", "junit", "linux", "html", "css", "machine learning",
    "data analysis", "communication", "leadership", "problem solving",
}


@dataclass(frozen=True)
class SkillMatch:
    skill: str
    matched: bool
    category: str = "required"
    evidence: str = ""


@dataclass(frozen=True)
class MatchResult:
    score: float
    required_score: float
    preferred_score: float
    profile_score: float
    salary_score: float
    location_score: float
    matched_required: tuple[str, ...] = ()
    missing_required: tuple[str, ...] = ()
    matched_preferred: tuple[str, ...] = ()
    recommendations: tuple[str, ...] = ()


@dataclass(frozen=True)
class FollowUpPlan:
    application_id: int
    action: str
    due_date: date
    priority: str
    reason: str


@dataclass(frozen=True)
class PipelineScore:
    application_id: int
    score: float
    urgency: str
    reasons: tuple[str, ...] = ()


def normalize_skill(value: str) -> str:
    value = re.sub(r"[^a-z0-9+#.-/ ]+", " ", value.lower())
    value = re.sub(r"\s+", " ", value).strip()
    aliases = {
        "springboot": "spring boot",
        "reactjs": "react",
        "nodejs": "node.js",
        "postgres": "postgresql",
        "py": "python",
        "js": "javascript",
        "ts": "typescript",
        "k8s": "kubernetes",
    }
    return aliases.get(value, value)


def normalize_skills(values: Iterable[str] | str | None) -> set[str]:
    if values is None:
        return set()
    if isinstance(values, str):
        values = re.split(r"[,;\n|]", values)
    result: set[str] = set()
    for value in values:
        normalized = normalize_skill(str(value))
        if normalized:
            result.add(normalized)
    return result


def extract_skills(text: str, vocabulary: Iterable[str] | None = None) -> list[str]:
    source = text.lower()
    candidates = normalize_skills(vocabulary or DEFAULT_SKILLS)
    found = []
    for skill in sorted(candidates):
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, source):
            found.append(skill)
    return found


def extract_keywords(text: str, limit: int = 30) -> list[str]:
    words = re.findall(r"[a-z][a-z0-9+#.-]{2,}", text.lower())
    stop = {
        "the", "and", "for", "with", "that", "this", "from", "your", "you",
        "our", "are", "will", "have", "has", "into", "using", "about",
        "role", "team", "work", "years", "experience", "responsible",
        "strong", "ability", "must", "should", "their", "they", "who",
    }
    frequency: dict[str, int] = {}
    for word in words:
        if word not in stop:
            frequency[word] = frequency.get(word, 0) + 1
    return [
        word for word, _ in sorted(
            frequency.items(), key=lambda item: (-item[1], item[0])
        )[:limit]
    ]


def salary_fit(
    minimum: Decimal | float | int | None,
    maximum: Decimal | float | int | None,
    target: Decimal | float | int | None,
) -> float:
    if target is None:
        return 0.5
    target = float(target)
    low = float(minimum) if minimum is not None else None
    high = float(maximum) if maximum is not None else None
    if low is None and high is None:
        return 0.5
    if low is not None and target < low:
        distance = (low - target) / max(low, 1)
        return max(0.0, 1.0 - distance * 2)
    if high is not None and target > high:
        distance = (target - high) / max(target, 1)
        return max(0.0, 1.0 - distance * 2)
    return 1.0


def location_fit(
    preferred: Sequence[str],
    job_location: str,
    work_preference: str = "flexible",
) -> float:
    location = job_location.lower()
    if work_preference == "remote" and "remote" in location:
        return 1.0
    if not preferred:
        return 0.7
    normalized = [item.lower().strip() for item in preferred if item.strip()]
    if any(item in location or location in item for item in normalized):
        return 1.0
    return 0.35


def role_fit(preferred_roles: Sequence[str], role: str) -> float:
    if not preferred_roles:
        return 0.7
    normalized_role = role.lower()
    for preferred in preferred_roles:
        tokens = [token for token in preferred.lower().split() if len(token) > 2]
        if tokens and sum(token in normalized_role for token in tokens) / len(tokens) >= 0.5:
            return 1.0
    return 0.25


class JobMatchingEngine:
    """Score a job description against a user's career profile."""

    REQUIRED_WEIGHT = 0.45
    PREFERRED_WEIGHT = 0.15
    PROFILE_WEIGHT = 0.20
    SALARY_WEIGHT = 0.10
    LOCATION_WEIGHT = 0.10

    def __init__(self, profile: CareerProfile | None = None):
        self.profile = profile

    def score(
        self,
        required_skills: Iterable[str],
        preferred_skills: Iterable[str],
        role: str = "",
        location: str = "",
        salary_min: Decimal | None = None,
        salary_max: Decimal | None = None,
    ) -> MatchResult:
        required = normalize_skills(required_skills)
        preferred = normalize_skills(preferred_skills)
        profile_skills = normalize_skills(self.profile.skills if self.profile else [])
        matched_required = tuple(sorted(required & profile_skills))
        missing_required = tuple(sorted(required - profile_skills))
        matched_preferred = tuple(sorted(preferred & profile_skills))

        required_score = len(matched_required) / len(required) if required else 1.0
        preferred_score = len(matched_preferred) / len(preferred) if preferred else 0.5
        role_score = role_fit(
            self.profile.preferred_roles if self.profile else [],
            role,
        )
        location_score = location_fit(
            self.profile.preferred_locations if self.profile else [],
            location,
            self.profile.work_preference if self.profile else "flexible",
        )
        salary_score = salary_fit(
            salary_min,
            salary_max,
            self.profile.target_salary if self.profile else None,
        )
        profile_score = role_score

        score = 100 * (
            self.REQUIRED_WEIGHT * required_score
            + self.PREFERRED_WEIGHT * preferred_score
            + self.PROFILE_WEIGHT * profile_score
            + self.SALARY_WEIGHT * salary_score
            + self.LOCATION_WEIGHT * location_score
        )

        recommendations: list[str] = []
        if missing_required:
            recommendations.append(
                "Address missing required skills: " + ", ".join(missing_required)
            )
        if preferred and not matched_preferred:
            recommendations.append("Add evidence for preferred skills in your resume.")
        if location_score < 0.5:
            recommendations.append("Review the role's location or work arrangement.")
        if salary_score < 0.5:
            recommendations.append("Review compensation expectations before applying.")
        if role_score < 0.5:
            recommendations.append("Consider whether the role matches your target roles.")

        return MatchResult(
            score=round(score, 2),
            required_score=round(required_score * 100, 2),
            preferred_score=round(preferred_score * 100, 2),
            profile_score=round(profile_score * 100, 2),
            salary_score=round(salary_score * 100, 2),
            location_score=round(location_score * 100, 2),
            matched_required=matched_required,
            missing_required=missing_required,
            matched_preferred=matched_preferred,
            recommendations=tuple(recommendations),
        )

    def score_description(self, description: JobDescription) -> MatchResult:
        return self.score(
            description.required_skills,
            description.preferred_skills,
            description.title,
            description.company,
            description.salary_min,
            description.salary_max,
        )


class ResumeTargetingService:
    """Produce deterministic resume-targeting suggestions."""

    def __init__(self, profile: CareerProfile):
        self.profile = profile

    def target_keywords(self, description: JobDescription) -> list[str]:
        profile_skills = normalize_skills(self.profile.skills)
        job_skills = normalize_skills(
            list(description.required_skills)
            + list(description.preferred_skills)
        )
        return sorted(job_skills & profile_skills)

    def missing_keywords(self, description: JobDescription) -> list[str]:
        profile_skills = normalize_skills(self.profile.skills)
        job_skills = normalize_skills(description.required_skills)
        return sorted(job_skills - profile_skills)

    def tailoring_notes(self, description: JobDescription) -> list[str]:
        notes: list[str] = []
        matched = self.target_keywords(description)
        missing = self.missing_keywords(description)
        if matched:
            notes.append("Highlight experience supporting: " + ", ".join(matched))
        if missing:
            notes.append("Only claim missing skills when you can substantiate them.")
        if description.responsibilities:
            notes.append(
                "Align experience bullets with the role's top responsibilities."
            )
        if description.extracted_keywords:
            notes.append(
                "Review job keywords: "
                + ", ".join(description.extracted_keywords[:12])
            )
        return notes


class FollowUpPlanner:
    """Generate follow-up tasks from application state."""

    DEFAULT_DELAYS = {
        "applied": 7,
        "screening": 5,
        "interview": 3,
        "offer": 2,
    }

    def __init__(self, today: date | None = None):
        self.today = today or date.today()

    def plan_for(self, application: JobApplication) -> FollowUpPlan | None:
        if application.status not in self.DEFAULT_DELAYS:
            return None
        if application.next_action_date and application.next_action_date >= self.today:
            due = application.next_action_date
        else:
            base = application.applied_date or self.today
            due = base + timedelta(days=self.DEFAULT_DELAYS[application.status])
        if application.status == "offer":
            priority = "urgent"
            action = "Review offer terms and prepare response"
        elif application.status == "interview":
            priority = "high"
            action = "Send interview follow-up"
        else:
            priority = "medium"
            action = "Check application status"
        return FollowUpPlan(
            application_id=application.id,
            action=action,
            due_date=due,
            priority=priority,
            reason=f"Application is currently in {application.status} stage.",
        )

    def create_tasks(self, applications: Iterable[JobApplication]) -> list[CareerTask]:
        tasks: list[CareerTask] = []
        for application in applications:
            plan = self.plan_for(application)
            if plan is None:
                continue
            if CareerTask.objects.filter(
                user=application.user,
                application=application,
                title=plan.action,
                status__in=["todo", "in_progress"],
            ).exists():
                continue
            tasks.append(
                CareerTask(
                    user=application.user,
                    application=application,
                    title=plan.action,
                    description=plan.reason,
                    priority=plan.priority,
                    status="todo",
                    due_date=datetime.combine(
                        plan.due_date, datetime.min.time()
                    ),
                    tags=["auto-generated", "follow-up"],
                )
            )
        return tasks


class PipelinePrioritizer:
    """Rank work items by actionable urgency without changing persisted data."""

    STATUS_BASE = {
        "offer": 100,
        "interview": 90,
        "screening": 75,
        "applied": 55,
        "saved": 30,
        "rejected": 0,
        "withdrawn": 0,
    }

    def score(self, application: JobApplication, today: date | None = None) -> PipelineScore:
        today = today or date.today()
        value = float(self.STATUS_BASE.get(application.status, 20))
        reasons: list[str] = [f"status:{application.status}"]

        if application.next_action_date:
            delta = (application.next_action_date - today).days
            if delta < 0:
                value += 25
                urgency = "overdue"
                reasons.append("next action is overdue")
            elif delta <= 2:
                value += 18
                urgency = "urgent"
                reasons.append("next action is due soon")
            elif delta <= 7:
                value += 8
                urgency = "soon"
                reasons.append("next action is due this week")
            else:
                urgency = "planned"
        else:
            urgency = "normal"

        if application.status == "offer":
            reasons.append("offer stage requires timely response")
        if application.interviews.filter(outcome="pending").exists():
            value += 10
            reasons.append("pending interview")

        return PipelineScore(
            application_id=application.id,
            score=round(value, 2),
            urgency=urgency,
            reasons=tuple(reasons),
        )

    def prioritize(self, applications: Iterable[JobApplication]) -> list[PipelineScore]:
        scores = [self.score(application) for application in applications]
        return sorted(scores, key=lambda item: item.score, reverse=True)


class JobDescriptionAnalyzer:
    """Analyze and enrich JobDescription records using local deterministic rules."""

    def analyze(self, description: JobDescription) -> JobDescription:
        skills = extract_skills(description.raw_text)
        description.extracted_keywords = extract_keywords(description.raw_text)
        existing_required = normalize_skills(description.required_skills)
        description.required_skills = sorted(existing_required or set(skills[:12]))
        description.preferred_skills = sorted(
            normalize_skills(description.preferred_skills)
        )
        description.analyzed_at = datetime.now()
        return description

    def preview(self, raw_text: str) -> dict:
        skills = extract_skills(raw_text)
        return {
            "skills": skills,
            "keywords": extract_keywords(raw_text),
            "skill_count": len(skills),
            "keyword_count": len(extract_keywords(raw_text)),
        }


class CareerDashboardService:
    """Build a compact, serializable career command center payload."""

    def __init__(self, user):
        self.user = user

    def applications(self) -> QuerySet[JobApplication]:
        return JobApplication.objects.filter(user=self.user).prefetch_related(
            "interviews"
        )

    def summary(self) -> dict:
        applications = list(self.applications())
        scores = PipelinePrioritizer().prioritize(applications)
        active = [app for app in applications if app.status not in {"rejected", "withdrawn"}]
        return {
            "total_applications": len(applications),
            "active_applications": len(active),
            "priority_items": [
                {
                    "application_id": item.application_id,
                    "score": item.score,
                    "urgency": item.urgency,
                    "reasons": list(item.reasons),
                }
                for item in scores[:10]
            ],
            "status_counts": self._status_counts(applications),
        }

    @staticmethod
    def _status_counts(applications: Iterable[JobApplication]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for application in applications:
            counts[application.status] = counts.get(application.status, 0) + 1
        return counts
