from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, timedelta
from difflib import SequenceMatcher
from decimal import Decimal
from typing import Iterable, Sequence

from django.db.models import Count, Q
from django.utils import timezone

from .models import CareerTask, JobApplication


COMMON_SKILLS = {
    "python", "javascript", "typescript", "java", "sql", "postgresql", "mysql",
    "django", "fastapi", "flask", "react", "vue", "angular", "node", "node.js",
    "docker", "kubernetes", "aws", "azure", "gcp", "git", "github", "linux",
    "terraform", "ansible", "spark", "pandas", "numpy", "scikit-learn",
    "machine learning", "deep learning", "computer vision", "nlp", "data analysis",
    "data annotation", "quality assurance", "project management", "sales",
    "customer service", "communication", "excel", "power bi", "tableau",
}


@dataclass(frozen=True)
class Keyword:
    value: str
    weight: float = 1.0
    category: str = "general"


@dataclass
class JobDescriptionProfile:
    raw_text: str
    normalized_text: str
    skills: list[str] = field(default_factory=list)
    keywords: list[Keyword] = field(default_factory=list)
    seniority: str | None = None
    work_mode: str | None = None
    employment_type: str | None = None
    location: str | None = None
    salary_min: Decimal | None = None
    salary_max: Decimal | None = None


class TextNormalizer:
    STOPWORDS = {
        "the", "and", "for", "with", "from", "that", "this", "are", "you",
        "your", "our", "will", "have", "has", "into", "about", "job", "role",
        "work", "team", "they", "their", "who", "what", "when", "where",
        "how", "all", "any", "can", "not", "but", "was", "were", "been",
        "its", "than", "then", "also", "using", "use", "more", "other",
    }

    @classmethod
    def normalize(cls, text: str) -> str:
        value = (text or "").lower()
        value = re.sub(r"https?://\S+", " ", value)
        value = re.sub(r"[^a-z0-9+#.\-\s]", " ", value)
        value = re.sub(r"\s+", " ", value)
        return value.strip()

    @classmethod
    def tokens(cls, text: str) -> list[str]:
        normalized = cls.normalize(text)
        return [token for token in normalized.split()
                if token not in cls.STOPWORDS and len(token) > 1]

    @classmethod
    def frequencies(cls, text: str) -> Counter:
        return Counter(cls.tokens(text))


class JobDescriptionParser:
    """Extract structured search signals from plain-text job descriptions."""

    SENIORITY_PATTERNS = [
        ("executive", r"\b(chief|vp|vice president|director|head of)\b"),
        ("senior", r"\b(senior|sr\.?|lead|principal|staff)\b"),
        ("mid", r"\b(mid[- ]level|intermediate)\b"),
        ("junior", r"\b(junior|jr\.?|entry[- ]level|graduate)\b"),
        ("internship", r"\b(intern|internship|trainee)\b"),
    ]
    WORK_MODE_PATTERNS = [
        ("remote", r"\b(remote|work from home|distributed)\b"),
        ("hybrid", r"\b(hybrid|flexible location)\b"),
        ("onsite", r"\b(on[- ]site|in[- ]office|office based)\b"),
    ]
    EMPLOYMENT_PATTERNS = [
        ("full_time", r"\b(full[- ]time|permanent)\b"),
        ("part_time", r"\b(part[- ]time)\b"),
        ("contract", r"\b(contract|contractor)\b"),
        ("internship", r"\b(intern|internship)\b"),
        ("freelance", r"\b(freelance|freelancer)\b"),
    ]

    @classmethod
    def parse(cls, text: str) -> JobDescriptionProfile:
        normalized = TextNormalizer.normalize(text)
        profile = JobDescriptionProfile(raw_text=text, normalized_text=normalized)
        profile.skills = cls.extract_skills(normalized)
        profile.keywords = cls.extract_keywords(normalized, profile.skills)
        profile.seniority = cls.extract_first(normalized, cls.SENIORITY_PATTERNS)
        profile.work_mode = cls.extract_first(normalized, cls.WORK_MODE_PATTERNS)
        profile.employment_type = cls.extract_first(normalized, cls.EMPLOYMENT_PATTERNS)
        profile.location = cls.extract_location(text)
        profile.salary_min, profile.salary_max = cls.extract_salary(normalized)
        return profile

    @staticmethod
    def extract_first(text: str, patterns: Sequence[tuple[str, str]]) -> str | None:
        for value, pattern in patterns:
            if re.search(pattern, text):
                return value
        return None

    @classmethod
    def extract_skills(cls, text: str) -> list[str]:
        found = []
        for skill in sorted(COMMON_SKILLS, key=len, reverse=True):
            if re.search(rf"(?<![\w+#.]){re.escape(skill)}(?![\w+#.])", text):
                found.append(skill)
        return sorted(set(found))

    @classmethod
    def extract_keywords(cls, text: str, skills: Sequence[str]) -> list[Keyword]:
        frequencies = TextNormalizer.frequencies(text)
        skill_set = set(skills)
        candidates = []
        for word, count in frequencies.most_common(100):
            if word in skill_set:
                continue
            if count >= 2 and len(word) >= 4:
                candidates.append(Keyword(word, min(3.0, 1.0 + count / 5), "keyword"))
        candidates.extend(Keyword(skill, 3.0, "skill") for skill in skills)
        return sorted(candidates, key=lambda item: (-item.weight, item.value))

    @staticmethod
    def extract_location(text: str) -> str | None:
        patterns = [
            r"(?:location|located in|based in)\s*[:\-]?\s*([A-Za-z][A-Za-z .,'\-]{2,60})",
            r"(?:office|position)\s+(?:in|at)\s+([A-Za-z][A-Za-z .,'\-]{2,60})",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                return re.sub(r"\s+", " ", match.group(1)).strip(" .,-")
        return None

    @staticmethod
    def extract_salary(text: str) -> tuple[Decimal | None, Decimal | None]:
        numbers = []
        for match in re.finditer(
            r"(?:[$£€]\s*)?(\d{1,3}(?:[,\s]\d{3})?(?:\.\d+)?)\s*(k|m)?",
            text, flags=re.IGNORECASE,
        ):
            raw, suffix = match.groups()
            try:
                value = Decimal(raw.replace(",", "").replace(" ", ""))
            except Exception:
                continue
            multiplier = (Decimal("1000") if (suffix or "").lower() == "k"
                          else Decimal("1000000") if (suffix or "").lower() == "m"
                          else Decimal("1"))
            value *= multiplier
            if 10000 <= value <= 10000000:
                numbers.append(value)
        return (min(numbers), max(numbers)) if numbers else (None, None)


class KeywordMatchService:
    """Compare candidate skills or resume text with a parsed job profile."""

    def __init__(self, profile: JobDescriptionProfile):
        self.profile = profile

    def match_skills(self, candidate_skills: Iterable[str]) -> dict:
        normalized = {TextNormalizer.normalize(skill) for skill in candidate_skills}
        required = set(self.profile.skills)
        matched = sorted(required & normalized)
        missing = sorted(required - normalized)
        score = len(matched) / len(required) * 100 if required else 100.0
        return {"required": sorted(required), "matched": matched,
                "missing": missing, "score": round(score, 2)}

    def match_text(self, resume_text: str) -> dict:
        text = TextNormalizer.normalize(resume_text)
        required = [item for item in self.profile.keywords if item.category == "skill"]
        matches = [item.value for item in required if item.value in text]
        missing = [item.value for item in required if item.value not in text]
        weighted_total = sum(item.weight for item in required) or 1
        weighted_match = sum(item.weight for item in required if item.value in text)
        return {"matched": matches, "missing": missing,
                "score": round(weighted_match / weighted_total * 100, 2)}


class ApplicationScoringService:
    """Produce transparent application-fit scores with explicit reasons."""

    def __init__(self, user):
        self.user = user

    def score(self, application: JobApplication,
              candidate_skills: Iterable[str] | None = None) -> dict:
        if application.user_id != self.user.id:
            raise PermissionError("Application belongs to another user.")
        points = 0.0
        reasons = []
        status_points = {"saved": 5, "applied": 15, "screening": 25,
                         "interview": 40, "offer": 60, "rejected": 0, "withdrawn": 0}
        status_value = status_points.get(application.status, 0)
        points += min(status_value, 60)
        reasons.append(f"Pipeline stage contributes {status_value} points.")
        priority_points = max(0, 15 - (application.priority - 1) * 3)
        points += priority_points
        reasons.append(f"Priority contributes {priority_points} points.")
        if application.job_url:
            points += 5
            reasons.append("Job posting URL is recorded.")
        if application.next_action and application.next_action_date:
            points += 10
            reasons.append("A dated next action is scheduled.")
        if application.recruiter_name or application.recruiter_email:
            points += 5
            reasons.append("Recruiter contact information is recorded.")
        if application.applied_date:
            age = (timezone.localdate() - application.applied_date).days
            if 0 <= age <= 14:
                points += 5
                reasons.append("Application is recent.")
        if candidate_skills is not None and application.requirements:
            profile = JobDescriptionParser.parse(application.requirements)
            match = KeywordMatchService(profile).match_skills(candidate_skills)
            skill_points = match["score"] * 0.20
            points += skill_points
            reasons.append(f"Requirement skill match contributes {skill_points:.1f} points.")
        return {"score": round(min(points, 100.0), 2), "maximum": 100.0,
                "reasons": reasons, "status": application.status,
                "priority": application.priority}

    def rank(self, applications: Iterable[JobApplication], candidate_skills=None):
        scored = [{"application": app, "score": self.score(app, candidate_skills)}
                  for app in applications]
        return sorted(scored, key=lambda item: item["score"]["score"], reverse=True)


class FollowUpPlanner:
    """Create practical next actions without sending external messages."""

    DEFAULT_ACTIONS = {
        "saved": ("Review job requirements", 2),
        "applied": ("Follow up with recruiter", 7),
        "screening": ("Prepare screening notes", 2),
        "interview": ("Prepare for next interview", 2),
        "offer": ("Review offer details", 3),
    }

    def __init__(self, user):
        self.user = user

    def plan_for_application(self, application, replace_existing=False):
        if application.user_id != self.user.id:
            raise PermissionError("Application belongs to another user.")
        if application.status in {"rejected", "withdrawn"}:
            return None
        if application.next_action_date and not replace_existing:
            return None
        action, days = self.DEFAULT_ACTIONS.get(application.status, ("Review application", 7))
        return CareerTask.objects.create(
            user=self.user, application=application, title=action,
            task_type="follow_up",
            priority=2 if application.status in {"screening", "interview"} else 3,
            due_date=timezone.localdate() + timedelta(days=days),
        )

    def plan_missing_followups(self, limit=50):
        applications = JobApplication.objects.filter(
            user=self.user,
            status__in=["saved", "applied", "screening", "interview", "offer"],
            next_action_date__isnull=True,
        ).order_by("-priority", "-updated_at")[:limit]
        return [task for app in applications
                if (task := self.plan_for_application(app)) is not None]


class InterviewPreparationService:
    """Build structured preparation checklists from interview type."""

    CHECKLISTS = {
        "phone": [
            "Review the job description.",
            "Prepare a 60-second introduction.",
            "Confirm availability and work authorization details.",
            "Prepare three questions for the recruiter.",
        ],
        "technical": [
            "Review the core technologies named in the job description.",
            "Practice explaining recent technical projects.",
            "Prepare examples of debugging and trade-off decisions.",
            "Review system constraints and testing strategy.",
        ],
        "system_design": [
            "Clarify requirements before proposing architecture.",
            "Review scaling, caching and data-storage trade-offs.",
            "Practice API and data-model design.",
            "Prepare to discuss observability and failure handling.",
        ],
        "behavioral": [
            "Prepare concise STAR examples.",
            "Choose examples demonstrating ownership and collaboration.",
            "Prepare an example of resolving disagreement.",
            "Prepare an example of learning from a mistake.",
        ],
        "panel": [
            "Review the responsibilities of each interviewer where known.",
            "Prepare concise answers for multiple audiences.",
            "Practice maintaining a clear thread when questions change.",
            "Prepare questions for each function represented on the panel.",
        ],
        "final": [
            "Review the complete interview history.",
            "Prepare questions about expectations and success measures.",
            "Clarify compensation and start-date questions you may need to ask.",
            "Prepare a concise closing statement.",
        ],
    }

    @classmethod
    def checklist(cls, interview_type: str) -> list[str]:
        return list(cls.CHECKLISTS.get(interview_type, cls.CHECKLISTS["phone"]))

    @classmethod
    def progress(cls, interview_type: str, completed_items: Iterable[str]) -> dict:
        items = cls.checklist(interview_type)
        completed = set(completed_items)
        done = sum(1 for item in items if item in completed)
        return {"total": len(items), "completed": done, "remaining": len(items) - done,
                "percent": round(done / len(items) * 100, 2) if items else 100.0}


class DuplicateDetectionService:
    """Find likely duplicate applications using normalized similarity."""

    def __init__(self, user):
        self.user = user

    @staticmethod
    def normalize(value: str) -> str:
        value = TextNormalizer.normalize(value)
        value = re.sub(r"\b(inc|incorporated|ltd|limited|llc|corp|corporation)\b", "", value)
        return re.sub(r"\s+", " ", value).strip()

    def similarity(self, left: JobApplication, right: JobApplication) -> float:
        company = SequenceMatcher(None, self.normalize(left.company),
                                  self.normalize(right.company)).ratio()
        role = SequenceMatcher(None, self.normalize(left.role),
                               self.normalize(right.role)).ratio()
        return round(company * 0.45 + role * 0.55, 4)

    def candidates(self, application, threshold=0.78):
        if application.user_id != self.user.id:
            raise PermissionError("Application belongs to another user.")
        candidates = JobApplication.objects.filter(user=self.user).exclude(pk=application.pk)
        results = []
        for candidate in candidates:
            score = self.similarity(application, candidate)
            if score >= threshold:
                results.append({"application": candidate, "similarity": score})
        return sorted(results, key=lambda row: row["similarity"], reverse=True)


class SearchQueryService:
    """Parse compact filters for command-center searches."""

    PREFIXES = {"status": "status", "mode": "work_mode", "priority": "priority",
                "company": "company", "location": "location"}

    def __init__(self, user):
        self.user = user

    def parse(self, expression: str) -> dict:
        result = {"text": "", "filters": {}}
        free_text = []
        for token in (expression or "").split():
            if ":" not in token:
                free_text.append(token)
                continue
            key, value = token.split(":", 1)
            key, value = key.lower().strip(), value.strip()
            if key in self.PREFIXES and value:
                result["filters"][self.PREFIXES[key]] = value
            else:
                free_text.append(token)
        result["text"] = " ".join(free_text)
        return result

    def execute(self, expression: str):
        parsed = self.parse(expression)
        qs = JobApplication.objects.filter(user=self.user)
        filters = parsed["filters"]
        if filters.get("status"):
            qs = qs.filter(status=filters["status"])
        if filters.get("mode"):
            qs = qs.filter(work_mode=filters["mode"])
        if filters.get("priority"):
            qs = qs.filter(priority=filters["priority"])
        if filters.get("company"):
            qs = qs.filter(company__icontains=filters["company"])
        if filters.get("location"):
            qs = qs.filter(location__icontains=filters["location"])
        if parsed["text"]:
            text = parsed["text"]
            qs = qs.filter(Q(company__icontains=text) | Q(role__icontains=text)
                           | Q(notes__icontains=text))
        return qs


class ResponseTimeService:
    """Measure elapsed time between applications and interview milestones."""

    def __init__(self, user):
        self.user = user

    def application_age(self, application):
        if application.user_id != self.user.id:
            raise PermissionError("Application belongs to another user.")
        if not application.applied_date:
            return None
        return max(0, (timezone.localdate() - application.applied_date).days)

    def interview_lead_time(self, application):
        if application.user_id != self.user.id:
            raise PermissionError("Application belongs to another user.")
        if not application.applied_date:
            return None
        values = []
        for interview in application.interviews.filter(scheduled_date__isnull=False):
            values.append(max(0, (interview.scheduled_date.date() -
                                  application.applied_date).days))
        return min(values) if values else None

    def summary(self):
        applications = JobApplication.objects.filter(user=self.user, applied_date__isnull=False)
        ages = [self.application_age(app) for app in applications]
        ages = [age for age in ages if age is not None]
        lead_times = []
        for application in applications:
            value = self.interview_lead_time(application)
            if value is not None:
                lead_times.append(value)
        return {
            "tracked_applications": len(ages),
            "average_application_age": round(sum(ages) / len(ages), 2) if ages else 0,
            "fastest_interview_days": min(lead_times) if lead_times else None,
            "average_interview_lead_time": (
                round(sum(lead_times) / len(lead_times), 2) if lead_times else None
            ),
        }


class WorkloadService:
    """Balance open tasks across priority and due-date buckets."""

    def __init__(self, user):
        self.user = user

    def buckets(self):
        today = timezone.localdate()
        tasks = CareerCareerTask.objects.filter(user=self.user, is_completed=False)
        return {
            "overdue": tasks.filter(due_date__lt=today).count(),
            "today": tasks.filter(due_date=today).count(),
            "next_7_days": tasks.filter(
                due_date__gt=today, due_date__lte=today + timedelta(days=7)
            ).count(),
            "later": tasks.filter(due_date__gt=today + timedelta(days=7)).count(),
            "unscheduled": tasks.filter(due_date__isnull=True).count(),
        }

    def priority_distribution(self):
        return list(
            Task.objects.filter(user=self.user, is_completed=False)
            .values("priority").annotate(total=Count("id")).order_by("priority")
        )

    def health(self):
        buckets = self.buckets()
        urgent = sum(row["total"] for row in self.priority_distribution()
                     if row["priority"] in (1, 2))
        open_count = sum(buckets.values())
        if not open_count:
            status = "clear"
        elif buckets["overdue"] / open_count > 0.35:
            status = "overloaded"
        elif urgent / open_count > 0.5:
            status = "high_priority"
        else:
            status = "manageable"
        return {"status": status, "open": open_count, "urgent": urgent, "buckets": buckets}


class ApplicationLifecycleService:
    """Coordinate common multi-model workflows explicitly."""

    def __init__(self, user):
        self.user = user

    def prepare_new_application(self, company_name, role, source=None, **fields):
        from .services import ActivityService, CompanyService
        company, _ = CompanyService(self.user).get_or_create_from_application(company_name)
        application = JobApplication.objects.create(
            user=self.user, company=company.name, company_record=company,
            source=source, role=role, **fields,
        )
        ActivityService.record(
            self.user, "created",
            f"Created application lifecycle record for {company.name}", application,
        )
        return application

    def close_application(self, application, status, note=""):
        if application.user_id != self.user.id:
            raise PermissionError("Application belongs to another user.")
        if status not in {"offer", "rejected", "withdrawn"}:
            raise ValueError("Closing status must be offer, rejected or withdrawn.")
        from .services import StatusService
        return StatusService(self.user).transition(application, status, note=note)

    def reopen_from_rejection(self, application):
        if application.user_id != self.user.id:
            raise PermissionError("Application belongs to another user.")
        if application.status != "rejected":
            raise ValueError("Only rejected applications can be reopened.")
        from .services import StatusService
        return StatusService(self.user).transition(
            application, "applied", reason="Reopened for continued tracking"
        )


def build_job_profile(text: str) -> JobDescriptionProfile:
    return JobDescriptionParser.parse(text)


def compare_candidate_to_job(candidate_text: str, job_text: str) -> dict:
    profile = JobDescriptionParser.parse(job_text)
    return {
        "job_profile": profile,
        "keyword_match": KeywordMatchService(profile).match_text(candidate_text),
        "candidate_tokens": len(TextNormalizer.tokens(candidate_text)),
        "job_tokens": len(TextNormalizer.tokens(job_text)),
    }
