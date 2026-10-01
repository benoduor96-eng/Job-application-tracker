from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List

from .models import JobApplication, CareerProfile, CareerTask as Task
from .intelligence import TextNormalizer, JobDescriptionParser


@dataclass
class Recommendation:
    title: str
    reason: str
    action_type: str
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class RecommendationEngine:
    """Domain-specific recommendations for managing a job search."""

    def __init__(self, user):
        self.user = user

    @staticmethod
    def _clean_text(value: str) -> str:
        return re.sub(r"\s+", " ", (value or "")).strip()

    def build_profile_summary(self) -> Dict[str, Any]:
        profile = CareerProfile.objects.filter(user=self.user).first()
        if profile is None:
            return {"exists": False, "headline": "", "skills": [], "preferred_roles": [], "targets": []}
        return {
            "exists": True,
            "headline": profile.headline,
            "skills": list(profile.skills or []),
            "preferred_roles": list(profile.preferred_roles or []),
            "targets": list(profile.preferred_locations or []),
        }

    def score_application_fit(self, app: JobApplication) -> float:
        profile = CareerProfile.objects.filter(user=self.user).first()
        job_description = getattr(app, "job_description", None)\n        requirements = ""\n        if job_description is not None:\n            requirements = " ".join(job_description.required_skills or []) + " " + (job_description.raw_text or "")
        if profile is None or not requirements:
            return 0.0
        parsed = JobDescriptionParser.parse(requirements)
        if not parsed.skills:
            return 0.0
        terms = []
        for name in ("skills", "preferred_roles", "headline", "professional_summary"):
            value = getattr(profile, name, None)
            if isinstance(value, (list, tuple, set)):
                terms.extend(str(item) for item in value)
            elif value:
                terms.append(str(value))
        overlap = set(TextNormalizer.tokens(" ".join(terms))) & set(TextNormalizer.tokens(requirements))
        return round(min((len(overlap) / max(len(set(TextNormalizer.tokens(requirements))), 1)) * 100, 100.0), 2)

    def recommend_applications(self, limit: int = 10) -> List[Recommendation]:
        apps = JobApplication.objects.filter(user=self.user).exclude(status="withdrawn")
        recommendations = []
        boosts = {"saved": 10, "applied": 15, "screening": 25, "interview": 35, "offer": 50}
        for app in apps:
            fit = self.score_application_fit(app)
            pressure = 20 if app.next_action_date and (app.next_action_date - date.today()).days < 0 else 10 if app.next_action_date and (app.next_action_date - date.today()).days <= 7 else 0
            score = fit + boosts.get(app.status, 0) + pressure
            if score > 0:
                recommendations.append(Recommendation(
                    title=f"{app.company} - {app.role}",
                    reason=f"Application fit score of {fit}% and current stage {app.status}.",
                    action_type="application", score=score,
                    metadata={"status": app.status, "company": app.company, "role": app.role},
                ))
        return sorted(recommendations, key=lambda r: r.score, reverse=True)[:limit]

    def recommend_resume_updates(self) -> List[Recommendation]:
        profile = CareerProfile.objects.filter(user=self.user).first()
        if profile is None:
            return []
        recommendations = []
        if not profile.skills:
            recommendations.append(Recommendation("Add core skill inventory", "Your profile is missing a clear list of core skills.", "resume", 90, {"field": "skills"}))
        if len((profile.professional_summary or "").strip().split()) < 30:
            recommendations.append(Recommendation("Expand professional summary", "A longer, outcome-oriented summary improves recruiter clarity.", "resume", 85, {"field": "summary"}))
        return recommendations

    def recommend_followup_actions(self) -> List[Recommendation]:
        apps = JobApplication.objects.filter(user=self.user).exclude(status__in=["rejected", "withdrawn"])
        recommendations = []
        for app in apps:
            if app.next_action_date is None and app.status in ["applied", "screening", "interview"]:
                recommendations.append(Recommendation(f"Set next step for {app.company}", "Active applications need a concrete next action.", "follow_up", 92, {"company": app.company, "role": app.role, "status": app.status}))
            elif app.next_action_date and (app.next_action_date - date.today()).days < 0:
                recommendations.append(Recommendation(f"Catch up on {app.company}", "This application is overdue for follow-up.", "follow_up", 96, {"company": app.company, "role": app.role, "status": app.status}))
        return sorted(recommendations, key=lambda r: r.score, reverse=True)[:10]

    def rank_actions(self) -> List[Dict[str, Any]]:
        actions = self.recommend_applications() + self.recommend_resume_updates() + self.recommend_followup_actions()
        return sorted([
            {"title": r.title, "reason": r.reason, "type": r.action_type, "score": r.score, "metadata": r.metadata}
            for r in actions
        ], key=lambda item: item["score"], reverse=True)
