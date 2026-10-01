from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any, Dict, List

from .models import JobApplication, CareerProfile, Task


@dataclass
class StrategyStep:
    title: str
    rationale: str
    due_in_days: int
    focus_area: str


class PortfolioStrategyService:
    """
    Converts the job tracker into a deliberate career strategy engine,
    with weekly actions and milestone sequencing.
    """

    def __init__(self, user):
        self.user = user

    def build_strategy(self) -> List[StrategyStep]:
        profile = CareerProfile.objects.filter(user=self.user).first()
        applications = JobApplication.objects.filter(user=self.user)

        steps = [
            StrategyStep(
                title="Audit current profile against target titles",
                rationale="Your profile should reflect real role positioning, not just generic resume text.",
                due_in_days=3,
                focus_area="profile",
            ),
            StrategyStep(
                title="Prioritize top-fit applications",
                rationale="Focus attention on applications with the strongest alignment to the job description.",
                due_in_days=5,
                focus_area="applications",
            ),
            StrategyStep(
                title="Prepare tailored evidence for each role",
                rationale="Each application should include project examples that match the target role.",
                due_in_days=7,
                focus_area="experience",
            ),
            StrategyStep(
                title="Clean up overdue tasks",
                rationale="Follow-up tasks and missed reminders slow momentum and reduce response quality.",
                due_in_days=2,
                focus_area="operations",
            ),
            StrategyStep(
                title="Review interview preparation needs",
                rationale="Interview improvement is measurable and should be treated as a pipeline stage, not a guess.",
                due_in_days=8,
                focus_area="interview",
            ),
        ]

        if applications.filter(status="offer").exists():
            steps.insert(0, StrategyStep(
                title="Review offer decision criteria",
                rationale="A live offer should trigger a structured comparison against your target market.",
                due_in_days=2,
                focus_area="negotiation",
            ))

        if profile and profile.skills:
            steps.insert(1, StrategyStep(
                title="Close skill gaps that matter most",
                rationale="Target the most important missing skills based on your profile and target roles.",
                due_in_days=4,
                focus_area="skills",
            ))

        return steps

    def monthly_plan(self, month_offset: int = 0) -> Dict[str, Any]:
        today = date.today()
        start = today.replace(day=1) + timedelta(days=month_offset * 30)
        steps = self.build_strategy()

        return {
            "month_start": start.isoformat(),
            "strategy_steps": [
                {
                    "title": step.title,
                    "rationale": step.rationale,
                    "due_in_days": step.due_in_days,
                    "focus_area": step.focus_area,
                }
                for step in steps
            ],
        }
