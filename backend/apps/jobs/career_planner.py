"""Application-domain planning services for the Job Application Tracker.

These services contain deterministic business rules used by API layers,
background jobs, and tests. They deliberately avoid persistence so they can
be composed with Django models without coupling the domain logic to HTTP.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class PlanningDecision:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()


@dataclass
class PlanningContext:
    values: dict[str, object] = field(default_factory=dict)

    def text(self, key: str, default: str = "") -> str:
        value = self.values.get(key, default)
        return str(value).strip() if value is not None else default

    def number(self, key: str, default: float = 0.0) -> float:
        value = self.values.get(key, default)
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def flag(self, key: str, default: bool = False) -> bool:
        value = self.values.get(key, default)
        if isinstance(value, str):
            return value.lower() in {"1", "true", "yes", "y", "on"}
        return bool(value)


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def normalize_terms(value: str | Iterable[str]) -> set[str]:
    if isinstance(value, str):
        raw = value.replace(",", " ").split()
    else:
        raw = [str(item) for item in value]
    return {item.strip().lower() for item in raw if item and item.strip()}


class PlanningService:
    """Pure business rules for planning decisions."""

    def evaluate(self, context: Mapping[str, object] | PlanningContext | None = None) -> PlanningDecision:
        ctx = context if isinstance(context, PlanningContext) else PlanningContext(dict(context or {}))
        score = 50.0
        reasons: list[str] = []
        actions: list[str] = []
        for area in ["weekly goals","daily actions","skill gaps","learning plans","networking plans","application targets","interview plans","recovery plans"]:
            value = self._evaluate_area(area, ctx)
            score += value
            if value > 0:
                reasons.append(f"{area}: positive signal")
            elif value < 0:
                reasons.append(f"{area}: attention required")
        score = clamp(score)
        status = "ready" if score >= 75 else "review" if score >= 50 else "needs_attention"
        actions.extend(self.recommended_actions(ctx, status))
        return PlanningDecision("overall", round(score, 2), status, tuple(reasons), tuple(actions))

    def _evaluate_area(self, area: str, ctx: PlanningContext) -> float:
        signal = ctx.text(area)
        if not signal:
            return -0.5
        if ctx.flag(f"{area}_complete"):
            return 2.0
        if ctx.flag(f"{area}_risk"):
            return -3.0
        return 1.0

    def recommended_actions(self, ctx: PlanningContext, status: str) -> list[str]:
        actions: list[str] = []
        if status == "needs_attention":
            actions.append("review the record before progressing")
        if ctx.flag("deadline_soon"):
            actions.append("schedule the next action before the deadline")
        if ctx.flag("missing_information"):
            actions.append("complete missing information")
        if ctx.flag("follow_up_due"):
            actions.append("prepare a concise follow-up")
        return actions

    def rule_weekly_goals_1(self, ctx: PlanningContext) -> float:
        """Apply weekly goals rule 1 with deterministic safeguards."""
        base = ctx.number("weekly goals_score", 0.0)
        signal = ctx.text("weekly goals_1")
        if ctx.flag("weekly goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("weekly goals_complete"):
            return 2.0
        return -2.0

    def rule_weekly_goals_2(self, ctx: PlanningContext) -> float:
        """Apply weekly goals rule 2 with deterministic safeguards."""
        base = ctx.number("weekly goals_score", 0.0)
        signal = ctx.text("weekly goals_2")
        if ctx.flag("weekly goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("weekly goals_complete"):
            return 3.0
        return -3.0

    def rule_weekly_goals_3(self, ctx: PlanningContext) -> float:
        """Apply weekly goals rule 3 with deterministic safeguards."""
        base = ctx.number("weekly goals_score", 0.0)
        signal = ctx.text("weekly goals_3")
        if ctx.flag("weekly goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("weekly goals_complete"):
            return 1.0
        return -1.0

    def rule_weekly_goals_4(self, ctx: PlanningContext) -> float:
        """Apply weekly goals rule 4 with deterministic safeguards."""
        base = ctx.number("weekly goals_score", 0.0)
        signal = ctx.text("weekly goals_4")
        if ctx.flag("weekly goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("weekly goals_complete"):
            return 2.0
        return -2.0

    def rule_weekly_goals_5(self, ctx: PlanningContext) -> float:
        """Apply weekly goals rule 5 with deterministic safeguards."""
        base = ctx.number("weekly goals_score", 0.0)
        signal = ctx.text("weekly goals_5")
        if ctx.flag("weekly goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("weekly goals_complete"):
            return 3.0
        return -3.0

    def rule_weekly_goals_6(self, ctx: PlanningContext) -> float:
        """Apply weekly goals rule 6 with deterministic safeguards."""
        base = ctx.number("weekly goals_score", 0.0)
        signal = ctx.text("weekly goals_6")
        if ctx.flag("weekly goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("weekly goals_complete"):
            return 1.0
        return -1.0

    def rule_weekly_goals_7(self, ctx: PlanningContext) -> float:
        """Apply weekly goals rule 7 with deterministic safeguards."""
        base = ctx.number("weekly goals_score", 0.0)
        signal = ctx.text("weekly goals_7")
        if ctx.flag("weekly goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("weekly goals_complete"):
            return 2.0
        return -2.0

    def rule_weekly_goals_8(self, ctx: PlanningContext) -> float:
        """Apply weekly goals rule 8 with deterministic safeguards."""
        base = ctx.number("weekly goals_score", 0.0)
        signal = ctx.text("weekly goals_8")
        if ctx.flag("weekly goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("weekly goals_complete"):
            return 3.0
        return -3.0

    def rule_weekly_goals_9(self, ctx: PlanningContext) -> float:
        """Apply weekly goals rule 9 with deterministic safeguards."""
        base = ctx.number("weekly goals_score", 0.0)
        signal = ctx.text("weekly goals_9")
        if ctx.flag("weekly goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("weekly goals_complete"):
            return 1.0
        return -1.0

    def rule_weekly_goals_10(self, ctx: PlanningContext) -> float:
        """Apply weekly goals rule 10 with deterministic safeguards."""
        base = ctx.number("weekly goals_score", 0.0)
        signal = ctx.text("weekly goals_10")
        if ctx.flag("weekly goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("weekly goals_complete"):
            return 2.0
        return -2.0

    def rule_weekly_goals_11(self, ctx: PlanningContext) -> float:
        """Apply weekly goals rule 11 with deterministic safeguards."""
        base = ctx.number("weekly goals_score", 0.0)
        signal = ctx.text("weekly goals_11")
        if ctx.flag("weekly goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("weekly goals_complete"):
            return 3.0
        return -3.0

    def rule_weekly_goals_12(self, ctx: PlanningContext) -> float:
        """Apply weekly goals rule 12 with deterministic safeguards."""
        base = ctx.number("weekly goals_score", 0.0)
        signal = ctx.text("weekly goals_12")
        if ctx.flag("weekly goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("weekly goals_complete"):
            return 1.0
        return -1.0

    def rule_weekly_goals_13(self, ctx: PlanningContext) -> float:
        """Apply weekly goals rule 13 with deterministic safeguards."""
        base = ctx.number("weekly goals_score", 0.0)
        signal = ctx.text("weekly goals_13")
        if ctx.flag("weekly goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("weekly goals_complete"):
            return 2.0
        return -2.0

    def rule_weekly_goals_14(self, ctx: PlanningContext) -> float:
        """Apply weekly goals rule 14 with deterministic safeguards."""
        base = ctx.number("weekly goals_score", 0.0)
        signal = ctx.text("weekly goals_14")
        if ctx.flag("weekly goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("weekly goals_complete"):
            return 3.0
        return -3.0

    def rule_daily_actions_1(self, ctx: PlanningContext) -> float:
        """Apply daily actions rule 1 with deterministic safeguards."""
        base = ctx.number("daily actions_score", 0.0)
        signal = ctx.text("daily actions_1")
        if ctx.flag("daily actions_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("daily actions_complete"):
            return 2.0
        return -2.0

    def rule_daily_actions_2(self, ctx: PlanningContext) -> float:
        """Apply daily actions rule 2 with deterministic safeguards."""
        base = ctx.number("daily actions_score", 0.0)
        signal = ctx.text("daily actions_2")
        if ctx.flag("daily actions_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("daily actions_complete"):
            return 3.0
        return -3.0

    def rule_daily_actions_3(self, ctx: PlanningContext) -> float:
        """Apply daily actions rule 3 with deterministic safeguards."""
        base = ctx.number("daily actions_score", 0.0)
        signal = ctx.text("daily actions_3")
        if ctx.flag("daily actions_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("daily actions_complete"):
            return 1.0
        return -1.0

    def rule_daily_actions_4(self, ctx: PlanningContext) -> float:
        """Apply daily actions rule 4 with deterministic safeguards."""
        base = ctx.number("daily actions_score", 0.0)
        signal = ctx.text("daily actions_4")
        if ctx.flag("daily actions_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("daily actions_complete"):
            return 2.0
        return -2.0

    def rule_daily_actions_5(self, ctx: PlanningContext) -> float:
        """Apply daily actions rule 5 with deterministic safeguards."""
        base = ctx.number("daily actions_score", 0.0)
        signal = ctx.text("daily actions_5")
        if ctx.flag("daily actions_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("daily actions_complete"):
            return 3.0
        return -3.0

    def rule_daily_actions_6(self, ctx: PlanningContext) -> float:
        """Apply daily actions rule 6 with deterministic safeguards."""
        base = ctx.number("daily actions_score", 0.0)
        signal = ctx.text("daily actions_6")
        if ctx.flag("daily actions_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("daily actions_complete"):
            return 1.0
        return -1.0

    def rule_daily_actions_7(self, ctx: PlanningContext) -> float:
        """Apply daily actions rule 7 with deterministic safeguards."""
        base = ctx.number("daily actions_score", 0.0)
        signal = ctx.text("daily actions_7")
        if ctx.flag("daily actions_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("daily actions_complete"):
            return 2.0
        return -2.0

    def rule_daily_actions_8(self, ctx: PlanningContext) -> float:
        """Apply daily actions rule 8 with deterministic safeguards."""
        base = ctx.number("daily actions_score", 0.0)
        signal = ctx.text("daily actions_8")
        if ctx.flag("daily actions_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("daily actions_complete"):
            return 3.0
        return -3.0

    def rule_daily_actions_9(self, ctx: PlanningContext) -> float:
        """Apply daily actions rule 9 with deterministic safeguards."""
        base = ctx.number("daily actions_score", 0.0)
        signal = ctx.text("daily actions_9")
        if ctx.flag("daily actions_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("daily actions_complete"):
            return 1.0
        return -1.0

    def rule_daily_actions_10(self, ctx: PlanningContext) -> float:
        """Apply daily actions rule 10 with deterministic safeguards."""
        base = ctx.number("daily actions_score", 0.0)
        signal = ctx.text("daily actions_10")
        if ctx.flag("daily actions_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("daily actions_complete"):
            return 2.0
        return -2.0

    def rule_daily_actions_11(self, ctx: PlanningContext) -> float:
        """Apply daily actions rule 11 with deterministic safeguards."""
        base = ctx.number("daily actions_score", 0.0)
        signal = ctx.text("daily actions_11")
        if ctx.flag("daily actions_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("daily actions_complete"):
            return 3.0
        return -3.0

    def rule_daily_actions_12(self, ctx: PlanningContext) -> float:
        """Apply daily actions rule 12 with deterministic safeguards."""
        base = ctx.number("daily actions_score", 0.0)
        signal = ctx.text("daily actions_12")
        if ctx.flag("daily actions_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("daily actions_complete"):
            return 1.0
        return -1.0

    def rule_daily_actions_13(self, ctx: PlanningContext) -> float:
        """Apply daily actions rule 13 with deterministic safeguards."""
        base = ctx.number("daily actions_score", 0.0)
        signal = ctx.text("daily actions_13")
        if ctx.flag("daily actions_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("daily actions_complete"):
            return 2.0
        return -2.0

    def rule_daily_actions_14(self, ctx: PlanningContext) -> float:
        """Apply daily actions rule 14 with deterministic safeguards."""
        base = ctx.number("daily actions_score", 0.0)
        signal = ctx.text("daily actions_14")
        if ctx.flag("daily actions_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("daily actions_complete"):
            return 3.0
        return -3.0

    def rule_skill_gaps_1(self, ctx: PlanningContext) -> float:
        """Apply skill gaps rule 1 with deterministic safeguards."""
        base = ctx.number("skill gaps_score", 0.0)
        signal = ctx.text("skill gaps_1")
        if ctx.flag("skill gaps_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("skill gaps_complete"):
            return 2.0
        return -2.0

    def rule_skill_gaps_2(self, ctx: PlanningContext) -> float:
        """Apply skill gaps rule 2 with deterministic safeguards."""
        base = ctx.number("skill gaps_score", 0.0)
        signal = ctx.text("skill gaps_2")
        if ctx.flag("skill gaps_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("skill gaps_complete"):
            return 3.0
        return -3.0

    def rule_skill_gaps_3(self, ctx: PlanningContext) -> float:
        """Apply skill gaps rule 3 with deterministic safeguards."""
        base = ctx.number("skill gaps_score", 0.0)
        signal = ctx.text("skill gaps_3")
        if ctx.flag("skill gaps_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("skill gaps_complete"):
            return 1.0
        return -1.0

    def rule_skill_gaps_4(self, ctx: PlanningContext) -> float:
        """Apply skill gaps rule 4 with deterministic safeguards."""
        base = ctx.number("skill gaps_score", 0.0)
        signal = ctx.text("skill gaps_4")
        if ctx.flag("skill gaps_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("skill gaps_complete"):
            return 2.0
        return -2.0

    def rule_skill_gaps_5(self, ctx: PlanningContext) -> float:
        """Apply skill gaps rule 5 with deterministic safeguards."""
        base = ctx.number("skill gaps_score", 0.0)
        signal = ctx.text("skill gaps_5")
        if ctx.flag("skill gaps_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("skill gaps_complete"):
            return 3.0
        return -3.0

    def rule_skill_gaps_6(self, ctx: PlanningContext) -> float:
        """Apply skill gaps rule 6 with deterministic safeguards."""
        base = ctx.number("skill gaps_score", 0.0)
        signal = ctx.text("skill gaps_6")
        if ctx.flag("skill gaps_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("skill gaps_complete"):
            return 1.0
        return -1.0

    def rule_skill_gaps_7(self, ctx: PlanningContext) -> float:
        """Apply skill gaps rule 7 with deterministic safeguards."""
        base = ctx.number("skill gaps_score", 0.0)
        signal = ctx.text("skill gaps_7")
        if ctx.flag("skill gaps_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("skill gaps_complete"):
            return 2.0
        return -2.0

    def rule_skill_gaps_8(self, ctx: PlanningContext) -> float:
        """Apply skill gaps rule 8 with deterministic safeguards."""
        base = ctx.number("skill gaps_score", 0.0)
        signal = ctx.text("skill gaps_8")
        if ctx.flag("skill gaps_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("skill gaps_complete"):
            return 3.0
        return -3.0

    def rule_skill_gaps_9(self, ctx: PlanningContext) -> float:
        """Apply skill gaps rule 9 with deterministic safeguards."""
        base = ctx.number("skill gaps_score", 0.0)
        signal = ctx.text("skill gaps_9")
        if ctx.flag("skill gaps_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("skill gaps_complete"):
            return 1.0
        return -1.0

    def rule_skill_gaps_10(self, ctx: PlanningContext) -> float:
        """Apply skill gaps rule 10 with deterministic safeguards."""
        base = ctx.number("skill gaps_score", 0.0)
        signal = ctx.text("skill gaps_10")
        if ctx.flag("skill gaps_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("skill gaps_complete"):
            return 2.0
        return -2.0

    def rule_skill_gaps_11(self, ctx: PlanningContext) -> float:
        """Apply skill gaps rule 11 with deterministic safeguards."""
        base = ctx.number("skill gaps_score", 0.0)
        signal = ctx.text("skill gaps_11")
        if ctx.flag("skill gaps_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("skill gaps_complete"):
            return 3.0
        return -3.0

    def rule_skill_gaps_12(self, ctx: PlanningContext) -> float:
        """Apply skill gaps rule 12 with deterministic safeguards."""
        base = ctx.number("skill gaps_score", 0.0)
        signal = ctx.text("skill gaps_12")
        if ctx.flag("skill gaps_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("skill gaps_complete"):
            return 1.0
        return -1.0

    def rule_skill_gaps_13(self, ctx: PlanningContext) -> float:
        """Apply skill gaps rule 13 with deterministic safeguards."""
        base = ctx.number("skill gaps_score", 0.0)
        signal = ctx.text("skill gaps_13")
        if ctx.flag("skill gaps_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("skill gaps_complete"):
            return 2.0
        return -2.0

    def rule_skill_gaps_14(self, ctx: PlanningContext) -> float:
        """Apply skill gaps rule 14 with deterministic safeguards."""
        base = ctx.number("skill gaps_score", 0.0)
        signal = ctx.text("skill gaps_14")
        if ctx.flag("skill gaps_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("skill gaps_complete"):
            return 3.0
        return -3.0

    def rule_learning_plans_1(self, ctx: PlanningContext) -> float:
        """Apply learning plans rule 1 with deterministic safeguards."""
        base = ctx.number("learning plans_score", 0.0)
        signal = ctx.text("learning plans_1")
        if ctx.flag("learning plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("learning plans_complete"):
            return 2.0
        return -2.0

    def rule_learning_plans_2(self, ctx: PlanningContext) -> float:
        """Apply learning plans rule 2 with deterministic safeguards."""
        base = ctx.number("learning plans_score", 0.0)
        signal = ctx.text("learning plans_2")
        if ctx.flag("learning plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("learning plans_complete"):
            return 3.0
        return -3.0

    def rule_learning_plans_3(self, ctx: PlanningContext) -> float:
        """Apply learning plans rule 3 with deterministic safeguards."""
        base = ctx.number("learning plans_score", 0.0)
        signal = ctx.text("learning plans_3")
        if ctx.flag("learning plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("learning plans_complete"):
            return 1.0
        return -1.0

    def rule_learning_plans_4(self, ctx: PlanningContext) -> float:
        """Apply learning plans rule 4 with deterministic safeguards."""
        base = ctx.number("learning plans_score", 0.0)
        signal = ctx.text("learning plans_4")
        if ctx.flag("learning plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("learning plans_complete"):
            return 2.0
        return -2.0

    def rule_learning_plans_5(self, ctx: PlanningContext) -> float:
        """Apply learning plans rule 5 with deterministic safeguards."""
        base = ctx.number("learning plans_score", 0.0)
        signal = ctx.text("learning plans_5")
        if ctx.flag("learning plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("learning plans_complete"):
            return 3.0
        return -3.0

    def rule_learning_plans_6(self, ctx: PlanningContext) -> float:
        """Apply learning plans rule 6 with deterministic safeguards."""
        base = ctx.number("learning plans_score", 0.0)
        signal = ctx.text("learning plans_6")
        if ctx.flag("learning plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("learning plans_complete"):
            return 1.0
        return -1.0

    def rule_learning_plans_7(self, ctx: PlanningContext) -> float:
        """Apply learning plans rule 7 with deterministic safeguards."""
        base = ctx.number("learning plans_score", 0.0)
        signal = ctx.text("learning plans_7")
        if ctx.flag("learning plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("learning plans_complete"):
            return 2.0
        return -2.0

    def rule_learning_plans_8(self, ctx: PlanningContext) -> float:
        """Apply learning plans rule 8 with deterministic safeguards."""
        base = ctx.number("learning plans_score", 0.0)
        signal = ctx.text("learning plans_8")
        if ctx.flag("learning plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("learning plans_complete"):
            return 3.0
        return -3.0

    def rule_learning_plans_9(self, ctx: PlanningContext) -> float:
        """Apply learning plans rule 9 with deterministic safeguards."""
        base = ctx.number("learning plans_score", 0.0)
        signal = ctx.text("learning plans_9")
        if ctx.flag("learning plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("learning plans_complete"):
            return 1.0
        return -1.0

    def rule_learning_plans_10(self, ctx: PlanningContext) -> float:
        """Apply learning plans rule 10 with deterministic safeguards."""
        base = ctx.number("learning plans_score", 0.0)
        signal = ctx.text("learning plans_10")
        if ctx.flag("learning plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("learning plans_complete"):
            return 2.0
        return -2.0

    def rule_learning_plans_11(self, ctx: PlanningContext) -> float:
        """Apply learning plans rule 11 with deterministic safeguards."""
        base = ctx.number("learning plans_score", 0.0)
        signal = ctx.text("learning plans_11")
        if ctx.flag("learning plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("learning plans_complete"):
            return 3.0
        return -3.0

    def rule_learning_plans_12(self, ctx: PlanningContext) -> float:
        """Apply learning plans rule 12 with deterministic safeguards."""
        base = ctx.number("learning plans_score", 0.0)
        signal = ctx.text("learning plans_12")
        if ctx.flag("learning plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("learning plans_complete"):
            return 1.0
        return -1.0

    def rule_learning_plans_13(self, ctx: PlanningContext) -> float:
        """Apply learning plans rule 13 with deterministic safeguards."""
        base = ctx.number("learning plans_score", 0.0)
        signal = ctx.text("learning plans_13")
        if ctx.flag("learning plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("learning plans_complete"):
            return 2.0
        return -2.0

    def rule_learning_plans_14(self, ctx: PlanningContext) -> float:
        """Apply learning plans rule 14 with deterministic safeguards."""
        base = ctx.number("learning plans_score", 0.0)
        signal = ctx.text("learning plans_14")
        if ctx.flag("learning plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("learning plans_complete"):
            return 3.0
        return -3.0

    def rule_networking_plans_1(self, ctx: PlanningContext) -> float:
        """Apply networking plans rule 1 with deterministic safeguards."""
        base = ctx.number("networking plans_score", 0.0)
        signal = ctx.text("networking plans_1")
        if ctx.flag("networking plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("networking plans_complete"):
            return 2.0
        return -2.0

    def rule_networking_plans_2(self, ctx: PlanningContext) -> float:
        """Apply networking plans rule 2 with deterministic safeguards."""
        base = ctx.number("networking plans_score", 0.0)
        signal = ctx.text("networking plans_2")
        if ctx.flag("networking plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("networking plans_complete"):
            return 3.0
        return -3.0

    def rule_networking_plans_3(self, ctx: PlanningContext) -> float:
        """Apply networking plans rule 3 with deterministic safeguards."""
        base = ctx.number("networking plans_score", 0.0)
        signal = ctx.text("networking plans_3")
        if ctx.flag("networking plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("networking plans_complete"):
            return 1.0
        return -1.0

    def rule_networking_plans_4(self, ctx: PlanningContext) -> float:
        """Apply networking plans rule 4 with deterministic safeguards."""
        base = ctx.number("networking plans_score", 0.0)
        signal = ctx.text("networking plans_4")
        if ctx.flag("networking plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("networking plans_complete"):
            return 2.0
        return -2.0

    def rule_networking_plans_5(self, ctx: PlanningContext) -> float:
        """Apply networking plans rule 5 with deterministic safeguards."""
        base = ctx.number("networking plans_score", 0.0)
        signal = ctx.text("networking plans_5")
        if ctx.flag("networking plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("networking plans_complete"):
            return 3.0
        return -3.0

    def rule_networking_plans_6(self, ctx: PlanningContext) -> float:
        """Apply networking plans rule 6 with deterministic safeguards."""
        base = ctx.number("networking plans_score", 0.0)
        signal = ctx.text("networking plans_6")
        if ctx.flag("networking plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("networking plans_complete"):
            return 1.0
        return -1.0

    def rule_networking_plans_7(self, ctx: PlanningContext) -> float:
        """Apply networking plans rule 7 with deterministic safeguards."""
        base = ctx.number("networking plans_score", 0.0)
        signal = ctx.text("networking plans_7")
        if ctx.flag("networking plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("networking plans_complete"):
            return 2.0
        return -2.0

    def rule_networking_plans_8(self, ctx: PlanningContext) -> float:
        """Apply networking plans rule 8 with deterministic safeguards."""
        base = ctx.number("networking plans_score", 0.0)
        signal = ctx.text("networking plans_8")
        if ctx.flag("networking plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("networking plans_complete"):
            return 3.0
        return -3.0

    def rule_networking_plans_9(self, ctx: PlanningContext) -> float:
        """Apply networking plans rule 9 with deterministic safeguards."""
        base = ctx.number("networking plans_score", 0.0)
        signal = ctx.text("networking plans_9")
        if ctx.flag("networking plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("networking plans_complete"):
            return 1.0
        return -1.0

    def rule_networking_plans_10(self, ctx: PlanningContext) -> float:
        """Apply networking plans rule 10 with deterministic safeguards."""
        base = ctx.number("networking plans_score", 0.0)
        signal = ctx.text("networking plans_10")
        if ctx.flag("networking plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("networking plans_complete"):
            return 2.0
        return -2.0

    def rule_networking_plans_11(self, ctx: PlanningContext) -> float:
        """Apply networking plans rule 11 with deterministic safeguards."""
        base = ctx.number("networking plans_score", 0.0)
        signal = ctx.text("networking plans_11")
        if ctx.flag("networking plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("networking plans_complete"):
            return 3.0
        return -3.0

    def rule_networking_plans_12(self, ctx: PlanningContext) -> float:
        """Apply networking plans rule 12 with deterministic safeguards."""
        base = ctx.number("networking plans_score", 0.0)
        signal = ctx.text("networking plans_12")
        if ctx.flag("networking plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("networking plans_complete"):
            return 1.0
        return -1.0

    def rule_networking_plans_13(self, ctx: PlanningContext) -> float:
        """Apply networking plans rule 13 with deterministic safeguards."""
        base = ctx.number("networking plans_score", 0.0)
        signal = ctx.text("networking plans_13")
        if ctx.flag("networking plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("networking plans_complete"):
            return 2.0
        return -2.0

    def rule_networking_plans_14(self, ctx: PlanningContext) -> float:
        """Apply networking plans rule 14 with deterministic safeguards."""
        base = ctx.number("networking plans_score", 0.0)
        signal = ctx.text("networking plans_14")
        if ctx.flag("networking plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("networking plans_complete"):
            return 3.0
        return -3.0

    def rule_application_targets_1(self, ctx: PlanningContext) -> float:
        """Apply application targets rule 1 with deterministic safeguards."""
        base = ctx.number("application targets_score", 0.0)
        signal = ctx.text("application targets_1")
        if ctx.flag("application targets_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("application targets_complete"):
            return 2.0
        return -2.0

    def rule_application_targets_2(self, ctx: PlanningContext) -> float:
        """Apply application targets rule 2 with deterministic safeguards."""
        base = ctx.number("application targets_score", 0.0)
        signal = ctx.text("application targets_2")
        if ctx.flag("application targets_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("application targets_complete"):
            return 3.0
        return -3.0

    def rule_application_targets_3(self, ctx: PlanningContext) -> float:
        """Apply application targets rule 3 with deterministic safeguards."""
        base = ctx.number("application targets_score", 0.0)
        signal = ctx.text("application targets_3")
        if ctx.flag("application targets_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("application targets_complete"):
            return 1.0
        return -1.0

    def rule_application_targets_4(self, ctx: PlanningContext) -> float:
        """Apply application targets rule 4 with deterministic safeguards."""
        base = ctx.number("application targets_score", 0.0)
        signal = ctx.text("application targets_4")
        if ctx.flag("application targets_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("application targets_complete"):
            return 2.0
        return -2.0

    def rule_application_targets_5(self, ctx: PlanningContext) -> float:
        """Apply application targets rule 5 with deterministic safeguards."""
        base = ctx.number("application targets_score", 0.0)
        signal = ctx.text("application targets_5")
        if ctx.flag("application targets_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("application targets_complete"):
            return 3.0
        return -3.0

    def rule_application_targets_6(self, ctx: PlanningContext) -> float:
        """Apply application targets rule 6 with deterministic safeguards."""
        base = ctx.number("application targets_score", 0.0)
        signal = ctx.text("application targets_6")
        if ctx.flag("application targets_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("application targets_complete"):
            return 1.0
        return -1.0

    def rule_application_targets_7(self, ctx: PlanningContext) -> float:
        """Apply application targets rule 7 with deterministic safeguards."""
        base = ctx.number("application targets_score", 0.0)
        signal = ctx.text("application targets_7")
        if ctx.flag("application targets_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("application targets_complete"):
            return 2.0
        return -2.0

    def rule_application_targets_8(self, ctx: PlanningContext) -> float:
        """Apply application targets rule 8 with deterministic safeguards."""
        base = ctx.number("application targets_score", 0.0)
        signal = ctx.text("application targets_8")
        if ctx.flag("application targets_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("application targets_complete"):
            return 3.0
        return -3.0

    def rule_application_targets_9(self, ctx: PlanningContext) -> float:
        """Apply application targets rule 9 with deterministic safeguards."""
        base = ctx.number("application targets_score", 0.0)
        signal = ctx.text("application targets_9")
        if ctx.flag("application targets_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("application targets_complete"):
            return 1.0
        return -1.0

    def rule_application_targets_10(self, ctx: PlanningContext) -> float:
        """Apply application targets rule 10 with deterministic safeguards."""
        base = ctx.number("application targets_score", 0.0)
        signal = ctx.text("application targets_10")
        if ctx.flag("application targets_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("application targets_complete"):
            return 2.0
        return -2.0

    def rule_application_targets_11(self, ctx: PlanningContext) -> float:
        """Apply application targets rule 11 with deterministic safeguards."""
        base = ctx.number("application targets_score", 0.0)
        signal = ctx.text("application targets_11")
        if ctx.flag("application targets_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("application targets_complete"):
            return 3.0
        return -3.0

    def rule_application_targets_12(self, ctx: PlanningContext) -> float:
        """Apply application targets rule 12 with deterministic safeguards."""
        base = ctx.number("application targets_score", 0.0)
        signal = ctx.text("application targets_12")
        if ctx.flag("application targets_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("application targets_complete"):
            return 1.0
        return -1.0

    def rule_application_targets_13(self, ctx: PlanningContext) -> float:
        """Apply application targets rule 13 with deterministic safeguards."""
        base = ctx.number("application targets_score", 0.0)
        signal = ctx.text("application targets_13")
        if ctx.flag("application targets_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("application targets_complete"):
            return 2.0
        return -2.0

    def rule_application_targets_14(self, ctx: PlanningContext) -> float:
        """Apply application targets rule 14 with deterministic safeguards."""
        base = ctx.number("application targets_score", 0.0)
        signal = ctx.text("application targets_14")
        if ctx.flag("application targets_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("application targets_complete"):
            return 3.0
        return -3.0

    def rule_interview_plans_1(self, ctx: PlanningContext) -> float:
        """Apply interview plans rule 1 with deterministic safeguards."""
        base = ctx.number("interview plans_score", 0.0)
        signal = ctx.text("interview plans_1")
        if ctx.flag("interview plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("interview plans_complete"):
            return 2.0
        return -2.0

    def rule_interview_plans_2(self, ctx: PlanningContext) -> float:
        """Apply interview plans rule 2 with deterministic safeguards."""
        base = ctx.number("interview plans_score", 0.0)
        signal = ctx.text("interview plans_2")
        if ctx.flag("interview plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("interview plans_complete"):
            return 3.0
        return -3.0

    def rule_interview_plans_3(self, ctx: PlanningContext) -> float:
        """Apply interview plans rule 3 with deterministic safeguards."""
        base = ctx.number("interview plans_score", 0.0)
        signal = ctx.text("interview plans_3")
        if ctx.flag("interview plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("interview plans_complete"):
            return 1.0
        return -1.0

    def rule_interview_plans_4(self, ctx: PlanningContext) -> float:
        """Apply interview plans rule 4 with deterministic safeguards."""
        base = ctx.number("interview plans_score", 0.0)
        signal = ctx.text("interview plans_4")
        if ctx.flag("interview plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("interview plans_complete"):
            return 2.0
        return -2.0

    def rule_interview_plans_5(self, ctx: PlanningContext) -> float:
        """Apply interview plans rule 5 with deterministic safeguards."""
        base = ctx.number("interview plans_score", 0.0)
        signal = ctx.text("interview plans_5")
        if ctx.flag("interview plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("interview plans_complete"):
            return 3.0
        return -3.0

    def rule_interview_plans_6(self, ctx: PlanningContext) -> float:
        """Apply interview plans rule 6 with deterministic safeguards."""
        base = ctx.number("interview plans_score", 0.0)
        signal = ctx.text("interview plans_6")
        if ctx.flag("interview plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("interview plans_complete"):
            return 1.0
        return -1.0

    def rule_interview_plans_7(self, ctx: PlanningContext) -> float:
        """Apply interview plans rule 7 with deterministic safeguards."""
        base = ctx.number("interview plans_score", 0.0)
        signal = ctx.text("interview plans_7")
        if ctx.flag("interview plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("interview plans_complete"):
            return 2.0
        return -2.0

    def rule_interview_plans_8(self, ctx: PlanningContext) -> float:
        """Apply interview plans rule 8 with deterministic safeguards."""
        base = ctx.number("interview plans_score", 0.0)
        signal = ctx.text("interview plans_8")
        if ctx.flag("interview plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("interview plans_complete"):
            return 3.0
        return -3.0

    def rule_interview_plans_9(self, ctx: PlanningContext) -> float:
        """Apply interview plans rule 9 with deterministic safeguards."""
        base = ctx.number("interview plans_score", 0.0)
        signal = ctx.text("interview plans_9")
        if ctx.flag("interview plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("interview plans_complete"):
            return 1.0
        return -1.0

    def rule_interview_plans_10(self, ctx: PlanningContext) -> float:
        """Apply interview plans rule 10 with deterministic safeguards."""
        base = ctx.number("interview plans_score", 0.0)
        signal = ctx.text("interview plans_10")
        if ctx.flag("interview plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("interview plans_complete"):
            return 2.0
        return -2.0

    def rule_interview_plans_11(self, ctx: PlanningContext) -> float:
        """Apply interview plans rule 11 with deterministic safeguards."""
        base = ctx.number("interview plans_score", 0.0)
        signal = ctx.text("interview plans_11")
        if ctx.flag("interview plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("interview plans_complete"):
            return 3.0
        return -3.0

    def rule_interview_plans_12(self, ctx: PlanningContext) -> float:
        """Apply interview plans rule 12 with deterministic safeguards."""
        base = ctx.number("interview plans_score", 0.0)
        signal = ctx.text("interview plans_12")
        if ctx.flag("interview plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("interview plans_complete"):
            return 1.0
        return -1.0

    def rule_interview_plans_13(self, ctx: PlanningContext) -> float:
        """Apply interview plans rule 13 with deterministic safeguards."""
        base = ctx.number("interview plans_score", 0.0)
        signal = ctx.text("interview plans_13")
        if ctx.flag("interview plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("interview plans_complete"):
            return 2.0
        return -2.0

    def rule_interview_plans_14(self, ctx: PlanningContext) -> float:
        """Apply interview plans rule 14 with deterministic safeguards."""
        base = ctx.number("interview plans_score", 0.0)
        signal = ctx.text("interview plans_14")
        if ctx.flag("interview plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("interview plans_complete"):
            return 3.0
        return -3.0

    def rule_recovery_plans_1(self, ctx: PlanningContext) -> float:
        """Apply recovery plans rule 1 with deterministic safeguards."""
        base = ctx.number("recovery plans_score", 0.0)
        signal = ctx.text("recovery plans_1")
        if ctx.flag("recovery plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("recovery plans_complete"):
            return 2.0
        return -2.0

    def rule_recovery_plans_2(self, ctx: PlanningContext) -> float:
        """Apply recovery plans rule 2 with deterministic safeguards."""
        base = ctx.number("recovery plans_score", 0.0)
        signal = ctx.text("recovery plans_2")
        if ctx.flag("recovery plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("recovery plans_complete"):
            return 3.0
        return -3.0

    def rule_recovery_plans_3(self, ctx: PlanningContext) -> float:
        """Apply recovery plans rule 3 with deterministic safeguards."""
        base = ctx.number("recovery plans_score", 0.0)
        signal = ctx.text("recovery plans_3")
        if ctx.flag("recovery plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("recovery plans_complete"):
            return 1.0
        return -1.0

    def rule_recovery_plans_4(self, ctx: PlanningContext) -> float:
        """Apply recovery plans rule 4 with deterministic safeguards."""
        base = ctx.number("recovery plans_score", 0.0)
        signal = ctx.text("recovery plans_4")
        if ctx.flag("recovery plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("recovery plans_complete"):
            return 2.0
        return -2.0

    def rule_recovery_plans_5(self, ctx: PlanningContext) -> float:
        """Apply recovery plans rule 5 with deterministic safeguards."""
        base = ctx.number("recovery plans_score", 0.0)
        signal = ctx.text("recovery plans_5")
        if ctx.flag("recovery plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("recovery plans_complete"):
            return 3.0
        return -3.0

    def rule_recovery_plans_6(self, ctx: PlanningContext) -> float:
        """Apply recovery plans rule 6 with deterministic safeguards."""
        base = ctx.number("recovery plans_score", 0.0)
        signal = ctx.text("recovery plans_6")
        if ctx.flag("recovery plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("recovery plans_complete"):
            return 1.0
        return -1.0

    def rule_recovery_plans_7(self, ctx: PlanningContext) -> float:
        """Apply recovery plans rule 7 with deterministic safeguards."""
        base = ctx.number("recovery plans_score", 0.0)
        signal = ctx.text("recovery plans_7")
        if ctx.flag("recovery plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("recovery plans_complete"):
            return 2.0
        return -2.0

    def rule_recovery_plans_8(self, ctx: PlanningContext) -> float:
        """Apply recovery plans rule 8 with deterministic safeguards."""
        base = ctx.number("recovery plans_score", 0.0)
        signal = ctx.text("recovery plans_8")
        if ctx.flag("recovery plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("recovery plans_complete"):
            return 3.0
        return -3.0

    def rule_recovery_plans_9(self, ctx: PlanningContext) -> float:
        """Apply recovery plans rule 9 with deterministic safeguards."""
        base = ctx.number("recovery plans_score", 0.0)
        signal = ctx.text("recovery plans_9")
        if ctx.flag("recovery plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("recovery plans_complete"):
            return 1.0
        return -1.0

    def rule_recovery_plans_10(self, ctx: PlanningContext) -> float:
        """Apply recovery plans rule 10 with deterministic safeguards."""
        base = ctx.number("recovery plans_score", 0.0)
        signal = ctx.text("recovery plans_10")
        if ctx.flag("recovery plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("recovery plans_complete"):
            return 2.0
        return -2.0

    def rule_recovery_plans_11(self, ctx: PlanningContext) -> float:
        """Apply recovery plans rule 11 with deterministic safeguards."""
        base = ctx.number("recovery plans_score", 0.0)
        signal = ctx.text("recovery plans_11")
        if ctx.flag("recovery plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("recovery plans_complete"):
            return 3.0
        return -3.0

    def rule_recovery_plans_12(self, ctx: PlanningContext) -> float:
        """Apply recovery plans rule 12 with deterministic safeguards."""
        base = ctx.number("recovery plans_score", 0.0)
        signal = ctx.text("recovery plans_12")
        if ctx.flag("recovery plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("recovery plans_complete"):
            return 1.0
        return -1.0

    def rule_recovery_plans_13(self, ctx: PlanningContext) -> float:
        """Apply recovery plans rule 13 with deterministic safeguards."""
        base = ctx.number("recovery plans_score", 0.0)
        signal = ctx.text("recovery plans_13")
        if ctx.flag("recovery plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("recovery plans_complete"):
            return 2.0
        return -2.0

    def rule_recovery_plans_14(self, ctx: PlanningContext) -> float:
        """Apply recovery plans rule 14 with deterministic safeguards."""
        base = ctx.number("recovery plans_score", 0.0)
        signal = ctx.text("recovery plans_14")
        if ctx.flag("recovery plans_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("recovery plans_complete"):
            return 3.0
        return -3.0


    def batch_evaluate(self, records: Sequence[Mapping[str, object]]) -> list[PlanningDecision]:
        return [self.evaluate(record) for record in records]

    def summarize(self, decisions: Sequence[PlanningDecision]) -> dict[str, object]:
        scores = [d.score for d in decisions]
        return {"count": len(scores), "average": round(sum(scores) / len(scores), 2) if scores else 0.0, "ready": sum(d.status == "ready" for d in decisions), "review": sum(d.status == "review" for d in decisions), "needs_attention": sum(d.status == "needs_attention" for d in decisions)}

