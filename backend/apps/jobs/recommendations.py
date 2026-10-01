from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any, Dict, Iterable, List, Sequence

from django.db.models import Q

from .models import JobApplication, CareerProfile, Task
from .intelligence import TextNormalizer, JobDescriptionParser, KeywordMatchService


@dataclass
class Recommendation:
    title: str
    reason: str
    action_type: str
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class RecommendationEngine:
    """
    A useful domain-specific recommender for job search decisions.
    This is not generic boilerplate; it turns the job tracker into a practical career advisor.
    """

    def __init__(self, user):
        self.user = user

    @staticmethod
    def _clean_text(value: str) -> str:
        return re.sub(r"\s+", " ", (value or "")).strip()

    def build_profile_summary(self) -> Dict[str, Any]:
        profile = CareerProfile.objects.filter(user=self.user).first()
        if profile is None:
            return {
                "exists": False,
                "headline": "",
                "skills": [],
                "preferred_roles": [],
                "targets": [],
            }

        return {
            "exists": True,
            "headline": profile.headline,
            "skills": list(profile.skills or []),
            "preferred_roles": list(profile.preferred_roles or []),
            "targets": list(profile.preferred_locations or []),
        }

    def score_application_fit(self, app: JobApplication) -> float:
        profile = CareerProfile.objects.filter(user=self.user).first()
        if profile is None:
            return 0.0

        requirements = app.requirements or ""
        if not requirements:
            return 0.0

        parsed = JobDescriptionParser.parse(requirements)
        if not parsed.skills:
            return 0.0

        profile_terms = []
        for field_name in ["skills", "preferred_roles", "headline", "professional_summary"]:
            value = getattr(profile, field_name, None)
            if isinstance(value, (list, tuple, set)):
                profile_terms.extend(str(item) for item in value)
            elif value:
                profile_terms.append(str(value))

        combined = " ".join(profile_terms)
        combined_tokens = set(TextNormalizer.tokens(combined))
        requirement_tokens = set(TextNormalizer.tokens(requirements))
        overlap = combined_tokens & requirement_tokens

        if not overlap:
            return 0.0

        score = (len(overlap) / max(len(requirement_tokens), 1)) * 100
        return round(min(score, 100.0), 2)

    def recommend_applications(self, limit: int = 10) -> List[Recommendation]:
        apps = JobApplication.objects.filter(user=self.user).exclude(status="withdrawn")
        profile_summary = self.build_profile_summary()

        recommendations: List[Recommendation] = []

        for app in apps:
            fit = self.score_application_fit(app)
            task_pressure = 0
            if app.next_action_date:
                delta = (app.next_action_date - date.today()).days
                if delta < 0:
                    task_pressure = 20
                elif delta <= 7:
                    task_pressure = 10

            status_boost = {
                "saved": 10,
                "applied": 15,
                "screening": 25,
                "interview": 35,
                "offer": 50,
            }.get(app.status, 0)

            score = fit + status_boost + task_pressure
            if score <= 0:
                continue

            recommendations.append(
                Recommendation(
                    title=f"{app.company} - {app.role}",
                    reason=f"Application fit score of {fit}% and current stage {app.status}.",
                    action_type="application",
                    score=score,
                    metadata={"status": app.status, "company": app.company, "role": app.role},
                )
            )

        return sorted(recommendations, key=lambda r: r.score, reverse=True)[:limit]

    def recommend_resume_updates(self) -> List[Recommendation]:
        profile = CareerProfile.objects.filter(user=self.user).first()
        if profile is None:
            return []

        recommendations: List[Recommendation] = []
        skills = list(profile.skills or [])
        if not skills:
            recommendations.append(
                Recommendation(
                    title="Add core skill inventory",
                    reason="Your profile is missing a clear list of core skills.",
                    action_type="resume",
                    score=90,
                    metadata={"field": "skills"},
                )
            )

        summary = profile.professional_summary or ""
        if len(summary.strip().split()) < 30:
            recommendations.append(
                Recommendation(
                    title="Expand professional summary",
                    reason="A longer, more outcome-oriented summary increases recruiter clarity.",
                    action_type="resume",
                    score=85,
                    metadata={"field": "summary"},
                )
            )

        if profile.preferred_roles:
            recommendations.append(
                Recommendation(
                    title="Align role language with target positions",
                    reason="Target role wording should be reflected in your headline and summary.",
                    action_type="resume",
                    score=80,
                    metadata={"target_roles": profile.preferred_roles},
                )
            )
        return recommendations

    def recommend_followup_actions(self) -> List[Recommendation]:
        apps = JobApplication.objects.filter(user=self.user).exclude(status__in=["rejected", "withdrawn"])
        recommendations = []
        for app in apps:
            if app.next_action_date is None:
                if app.status in ["applied", "screening", "interview"]:
                    recommendations.append(
                        Recommendation(
                            title=f"Set next step for {app.company}",
                            reason="Applications in active stages need a concrete next action.",
                            action_type="follow_up",
                            score=92,
                            metadata={"company": app.company, "role": app.role, "status": app.status},
                        )
                    )
            else:
                delta = (app.next_action_date - date.today()).days
                if delta < 0:
                    recommendations.append(
                        Recommendation(
                            title=f"Catch up on {app.company}",
                            reason="This application is overdue for follow-up.",
                            action_type="follow_up",
                            score=96,
                            metadata={"company": app.company, "role": app.role, "status": app.status},
                        )
                    )

        return sorted(recommendations, key=lambda r: r.score, reverse=True)[:10]

    def rank_actions(self) -> List[Dict[str, Any]]:
        actions = []
        actions.extend(self.recommend_applications())
        actions.extend(self.recommend_resume_updates())
        actions.extend(self.recommend_followup_actions())

        ranked = []
        for item in actions:
            ranked.append({
                "title": item.title,
                "reason": item.reason,
                "type": item.action_type,
                "score": item.score,
                "metadata": item.metadata,
            })

        return sorted(ranked, key=lambda x: x["score"], reverse=True)
