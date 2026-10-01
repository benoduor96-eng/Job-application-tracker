"""Deterministic job-fit analysis based on stored career and job-description data."""
from dataclasses import dataclass
from decimal import Decimal
import re
from .models import CareerProfile, JobApplication, JobDescription

@dataclass(frozen=True)
class FitResult:
    score: int
    required_matches: list
    required_gaps: list
    preferred_matches: list
    role_match: bool
    location_match: bool
    salary_match: bool
    recommendations: list

    def to_dict(self):
        return {
            "score": self.score,
            "required_matches": self.required_matches,
            "required_gaps": self.required_gaps,
            "preferred_matches": self.preferred_matches,
            "role_match": self.role_match,
            "location_match": self.location_match,
            "salary_match": self.salary_match,
            "recommendations": self.recommendations,
        }

class JobFitAnalyzer:
    def __init__(self, user):
        self.user = user

    @staticmethod
    def _norm(value):
        return re.sub(r"[^a-z0-9+#.]+", " ", str(value or "").lower()).strip()

    @classmethod
    def _skills(cls, values):
        return {cls._norm(value) for value in (values or []) if cls._norm(value)}

    def _profile(self):
        try:
            return self.user.career_profile
        except CareerProfile.DoesNotExist:
            return None

    def analyze(self, application):
        if application.user_id != self.user.id:
            raise PermissionError("Application does not belong to this user")
        try:
            description = application.job_description
        except JobDescription.DoesNotExist:
            return FitResult(0, [], [], [], False, False, False, ["Add a job description before running fit analysis."])
        profile = self._profile()
        profile_skills = self._skills(profile.skills if profile else [])
        required = self._skills(description.required_skills)
        preferred = self._skills(description.preferred_skills)
        required_matches = sorted(required & profile_skills)
        required_gaps = sorted(required - profile_skills)
        preferred_matches = sorted(preferred & profile_skills)
        role_match = self._role_match(application, profile, description)
        location_match = self._location_match(application, profile)
        salary_match = self._salary_match(application, profile, description)
        required_score = 45 if not required else round(45 * len(required_matches) / len(required))
        preferred_score = 20 if not preferred else round(20 * len(preferred_matches) / len(preferred))
        score = min(100, required_score + preferred_score + (15 if role_match else 0) + (10 if location_match else 0) + (10 if salary_match else 0))
        recommendations = []
        if required_gaps: recommendations.append("Review missing required skills: " + ", ".join(required_gaps[:8]))
        if not role_match: recommendations.append("Check whether the role matches your preferred roles.")
        if not location_match: recommendations.append("Review the role location and your work preferences.")
        if not salary_match: recommendations.append("Compare the posted range with your salary expectations.")
        if not recommendations: recommendations.append("Profile and job description signals are aligned.")
        return FitResult(score, required_matches, required_gaps, preferred_matches, role_match, location_match, salary_match, recommendations)

    def _role_match(self, application, profile, description):
        roles = [self._norm(x) for x in (profile.preferred_roles if profile else [])]
        if not roles: return True
        target = self._norm(description.title or application.role)
        return any(role in target or target in role for role in roles)

    def _location_match(self, application, profile):
        if not profile: return True
        if profile.work_preference in {"remote", "flexible"}: return True
        locations = [self._norm(x) for x in (profile.preferred_locations or [])]
        if not locations or not application.location: return True
        location = self._norm(application.location)
        return any(value in location or location in value for value in locations)

    @staticmethod
    def _salary_match(application, profile, description):
        if not profile or profile.minimum_salary is None: return True
        high = description.salary_max or application.salary_max
        return high is None or Decimal(str(high)) >= Decimal(str(profile.minimum_salary))
