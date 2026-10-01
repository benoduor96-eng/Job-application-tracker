from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from .models import CareerProfile, JobApplication


@dataclass
class Recommendation:
    title: str
    reason: str
    action_type: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)


class RecommendationEngine:
    """Turns application and profile data into explainable next-step recommendations."""

    def __init__(self, user):
        self.user = user

    def build_profile_summary(self) -> dict[str, Any]:
        profile = CareerProfile.objects.filter(user=self.user).first()
        if not profile:
            return {"exists": False, "skills": [], "preferred_roles": [], "locations": []}
        return {"exists": True, "headline": profile.headline, "skills": list(profile.skills or []),
                "preferred_roles": list(profile.preferred_roles or []),
                "locations": list(profile.preferred_locations or [])}

    def score_application_fit(self, app: JobApplication) -> float:
        profile = CareerProfile.objects.filter(user=self.user).first()
        if not profile or not app.requirements:
            return 0.0
        profile_words = set()
        for value in [profile.headline, profile.professional_summary, *(profile.skills or []), *(profile.preferred_roles or [])]:
            profile_words.update(str(value).lower().replace(",", " ").split())
        required = set(app.requirements.lower().replace(",", " ").split())
        overlap = profile_words & required
        return round(min(100.0, len(overlap) / max(1, len(required)) * 100), 2)

    def recommend_applications(self, limit: int = 10) -> list[Recommendation]:
        results = []
        for app in JobApplication.objects.filter(user=self.user).exclude(status="withdrawn"):
            fit = self.score_application_fit(app)
            stage = {"saved": 10, "applied": 15, "screening": 25, "interview": 35, "offer": 50}.get(app.status, 0)
            urgency = 20 if app.next_action_date and app.next_action_date < date.today() else 10 if app.next_action_date and (app.next_action_date - date.today()).days <= 7 else 0
            score = fit + stage + urgency
            if score:
                results.append(Recommendation(f"{app.company} - {app.role}",
                    f"Fit {fit}% with current stage {app.status}.", "application", score,
                    {"company": app.company, "role": app.role, "status": app.status}))
        return sorted(results, key=lambda x: x.score, reverse=True)[:limit]

    def recommend_followups(self) -> list[Recommendation]:
        results = []
        for app in JobApplication.objects.filter(user=self.user).exclude(status__in=["rejected", "withdrawn"]):
            if app.next_action_date is None and app.status in ["applied", "screening", "interview"]:
                results.append(Recommendation(f"Set next step for {app.company}", "Active applications need a concrete next action.",
                    "follow_up", 92, {"application_id": app.id}))
            elif app.next_action_date and app.next_action_date < date.today():
                results.append(Recommendation(f"Follow up with {app.company}", "The planned next action is overdue.",
                    "follow_up", 96, {"application_id": app.id}))
        return sorted(results, key=lambda x: x.score, reverse=True)[:10]

    def rank_actions(self) -> list[dict[str, Any]]:
        actions = self.recommend_applications() + self.recommend_followups()
        return [{"title": a.title, "reason": a.reason, "type": a.action_type, "score": a.score, "metadata": a.metadata}
                for a in sorted(actions, key=lambda x: x.score, reverse=True)]
