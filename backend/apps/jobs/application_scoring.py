"""Application-domain scoring services for the Job Application Tracker.

These services contain deterministic business rules used by API layers,
background jobs, and tests. They deliberately avoid persistence so they can
be composed with Django models without coupling the domain logic to HTTP.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class ScoringDecision:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()


@dataclass
class ScoringContext:
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


class ScoringService:
    """Pure business rules for scoring decisions."""

    def evaluate(self, context: Mapping[str, object] | ScoringContext | None = None) -> ScoringDecision:
        ctx = context if isinstance(context, ScoringContext) else ScoringContext(dict(context or {}))
        score = 50.0
        reasons: list[str] = []
        actions: list[str] = []
        for area in ["role fit","skill match","salary fit","location fit","seniority fit","application freshness","company preference","follow-up urgency"]:
            value = self._evaluate_area(area, ctx)
            score += value
            if value > 0:
                reasons.append(f"{area}: positive signal")
            elif value < 0:
                reasons.append(f"{area}: attention required")
        score = clamp(score)
        status = "ready" if score >= 75 else "review" if score >= 50 else "needs_attention"
        actions.extend(self.recommended_actions(ctx, status))
        return ScoringDecision("overall", round(score, 2), status, tuple(reasons), tuple(actions))

    def _evaluate_area(self, area: str, ctx: ScoringContext) -> float:
        signal = ctx.text(area)
        if not signal:
            return -0.5
        if ctx.flag(f"{area}_complete"):
            return 2.0
        if ctx.flag(f"{area}_risk"):
            return -3.0
        return 1.0

    def recommended_actions(self, ctx: ScoringContext, status: str) -> list[str]:
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

    def rule_role_fit_1(self, ctx: ScoringContext) -> float:
        """Apply role fit rule 1 with deterministic safeguards."""
        base = ctx.number("role fit_score", 0.0)
        signal = ctx.text("role fit_1")
        if ctx.flag("role fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("role fit_complete"):
            return 2.0
        return -2.0

    def rule_role_fit_2(self, ctx: ScoringContext) -> float:
        """Apply role fit rule 2 with deterministic safeguards."""
        base = ctx.number("role fit_score", 0.0)
        signal = ctx.text("role fit_2")
        if ctx.flag("role fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("role fit_complete"):
            return 3.0
        return -3.0

    def rule_role_fit_3(self, ctx: ScoringContext) -> float:
        """Apply role fit rule 3 with deterministic safeguards."""
        base = ctx.number("role fit_score", 0.0)
        signal = ctx.text("role fit_3")
        if ctx.flag("role fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("role fit_complete"):
            return 1.0
        return -1.0

    def rule_role_fit_4(self, ctx: ScoringContext) -> float:
        """Apply role fit rule 4 with deterministic safeguards."""
        base = ctx.number("role fit_score", 0.0)
        signal = ctx.text("role fit_4")
        if ctx.flag("role fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("role fit_complete"):
            return 2.0
        return -2.0

    def rule_role_fit_5(self, ctx: ScoringContext) -> float:
        """Apply role fit rule 5 with deterministic safeguards."""
        base = ctx.number("role fit_score", 0.0)
        signal = ctx.text("role fit_5")
        if ctx.flag("role fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("role fit_complete"):
            return 3.0
        return -3.0

    def rule_role_fit_6(self, ctx: ScoringContext) -> float:
        """Apply role fit rule 6 with deterministic safeguards."""
        base = ctx.number("role fit_score", 0.0)
        signal = ctx.text("role fit_6")
        if ctx.flag("role fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("role fit_complete"):
            return 1.0
        return -1.0

    def rule_role_fit_7(self, ctx: ScoringContext) -> float:
        """Apply role fit rule 7 with deterministic safeguards."""
        base = ctx.number("role fit_score", 0.0)
        signal = ctx.text("role fit_7")
        if ctx.flag("role fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("role fit_complete"):
            return 2.0
        return -2.0

    def rule_role_fit_8(self, ctx: ScoringContext) -> float:
        """Apply role fit rule 8 with deterministic safeguards."""
        base = ctx.number("role fit_score", 0.0)
        signal = ctx.text("role fit_8")
        if ctx.flag("role fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("role fit_complete"):
            return 3.0
        return -3.0

    def rule_role_fit_9(self, ctx: ScoringContext) -> float:
        """Apply role fit rule 9 with deterministic safeguards."""
        base = ctx.number("role fit_score", 0.0)
        signal = ctx.text("role fit_9")
        if ctx.flag("role fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("role fit_complete"):
            return 1.0
        return -1.0

    def rule_role_fit_10(self, ctx: ScoringContext) -> float:
        """Apply role fit rule 10 with deterministic safeguards."""
        base = ctx.number("role fit_score", 0.0)
        signal = ctx.text("role fit_10")
        if ctx.flag("role fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("role fit_complete"):
            return 2.0
        return -2.0

    def rule_role_fit_11(self, ctx: ScoringContext) -> float:
        """Apply role fit rule 11 with deterministic safeguards."""
        base = ctx.number("role fit_score", 0.0)
        signal = ctx.text("role fit_11")
        if ctx.flag("role fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("role fit_complete"):
            return 3.0
        return -3.0

    def rule_role_fit_12(self, ctx: ScoringContext) -> float:
        """Apply role fit rule 12 with deterministic safeguards."""
        base = ctx.number("role fit_score", 0.0)
        signal = ctx.text("role fit_12")
        if ctx.flag("role fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("role fit_complete"):
            return 1.0
        return -1.0

    def rule_role_fit_13(self, ctx: ScoringContext) -> float:
        """Apply role fit rule 13 with deterministic safeguards."""
        base = ctx.number("role fit_score", 0.0)
        signal = ctx.text("role fit_13")
        if ctx.flag("role fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("role fit_complete"):
            return 2.0
        return -2.0

    def rule_role_fit_14(self, ctx: ScoringContext) -> float:
        """Apply role fit rule 14 with deterministic safeguards."""
        base = ctx.number("role fit_score", 0.0)
        signal = ctx.text("role fit_14")
        if ctx.flag("role fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("role fit_complete"):
            return 3.0
        return -3.0

    def rule_skill_match_1(self, ctx: ScoringContext) -> float:
        """Apply skill match rule 1 with deterministic safeguards."""
        base = ctx.number("skill match_score", 0.0)
        signal = ctx.text("skill match_1")
        if ctx.flag("skill match_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("skill match_complete"):
            return 2.0
        return -2.0

    def rule_skill_match_2(self, ctx: ScoringContext) -> float:
        """Apply skill match rule 2 with deterministic safeguards."""
        base = ctx.number("skill match_score", 0.0)
        signal = ctx.text("skill match_2")
        if ctx.flag("skill match_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("skill match_complete"):
            return 3.0
        return -3.0

    def rule_skill_match_3(self, ctx: ScoringContext) -> float:
        """Apply skill match rule 3 with deterministic safeguards."""
        base = ctx.number("skill match_score", 0.0)
        signal = ctx.text("skill match_3")
        if ctx.flag("skill match_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("skill match_complete"):
            return 1.0
        return -1.0

    def rule_skill_match_4(self, ctx: ScoringContext) -> float:
        """Apply skill match rule 4 with deterministic safeguards."""
        base = ctx.number("skill match_score", 0.0)
        signal = ctx.text("skill match_4")
        if ctx.flag("skill match_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("skill match_complete"):
            return 2.0
        return -2.0

    def rule_skill_match_5(self, ctx: ScoringContext) -> float:
        """Apply skill match rule 5 with deterministic safeguards."""
        base = ctx.number("skill match_score", 0.0)
        signal = ctx.text("skill match_5")
        if ctx.flag("skill match_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("skill match_complete"):
            return 3.0
        return -3.0

    def rule_skill_match_6(self, ctx: ScoringContext) -> float:
        """Apply skill match rule 6 with deterministic safeguards."""
        base = ctx.number("skill match_score", 0.0)
        signal = ctx.text("skill match_6")
        if ctx.flag("skill match_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("skill match_complete"):
            return 1.0
        return -1.0

    def rule_skill_match_7(self, ctx: ScoringContext) -> float:
        """Apply skill match rule 7 with deterministic safeguards."""
        base = ctx.number("skill match_score", 0.0)
        signal = ctx.text("skill match_7")
        if ctx.flag("skill match_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("skill match_complete"):
            return 2.0
        return -2.0

    def rule_skill_match_8(self, ctx: ScoringContext) -> float:
        """Apply skill match rule 8 with deterministic safeguards."""
        base = ctx.number("skill match_score", 0.0)
        signal = ctx.text("skill match_8")
        if ctx.flag("skill match_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("skill match_complete"):
            return 3.0
        return -3.0

    def rule_skill_match_9(self, ctx: ScoringContext) -> float:
        """Apply skill match rule 9 with deterministic safeguards."""
        base = ctx.number("skill match_score", 0.0)
        signal = ctx.text("skill match_9")
        if ctx.flag("skill match_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("skill match_complete"):
            return 1.0
        return -1.0

    def rule_skill_match_10(self, ctx: ScoringContext) -> float:
        """Apply skill match rule 10 with deterministic safeguards."""
        base = ctx.number("skill match_score", 0.0)
        signal = ctx.text("skill match_10")
        if ctx.flag("skill match_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("skill match_complete"):
            return 2.0
        return -2.0

    def rule_skill_match_11(self, ctx: ScoringContext) -> float:
        """Apply skill match rule 11 with deterministic safeguards."""
        base = ctx.number("skill match_score", 0.0)
        signal = ctx.text("skill match_11")
        if ctx.flag("skill match_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("skill match_complete"):
            return 3.0
        return -3.0

    def rule_skill_match_12(self, ctx: ScoringContext) -> float:
        """Apply skill match rule 12 with deterministic safeguards."""
        base = ctx.number("skill match_score", 0.0)
        signal = ctx.text("skill match_12")
        if ctx.flag("skill match_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("skill match_complete"):
            return 1.0
        return -1.0

    def rule_skill_match_13(self, ctx: ScoringContext) -> float:
        """Apply skill match rule 13 with deterministic safeguards."""
        base = ctx.number("skill match_score", 0.0)
        signal = ctx.text("skill match_13")
        if ctx.flag("skill match_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("skill match_complete"):
            return 2.0
        return -2.0

    def rule_skill_match_14(self, ctx: ScoringContext) -> float:
        """Apply skill match rule 14 with deterministic safeguards."""
        base = ctx.number("skill match_score", 0.0)
        signal = ctx.text("skill match_14")
        if ctx.flag("skill match_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("skill match_complete"):
            return 3.0
        return -3.0

    def rule_salary_fit_1(self, ctx: ScoringContext) -> float:
        """Apply salary fit rule 1 with deterministic safeguards."""
        base = ctx.number("salary fit_score", 0.0)
        signal = ctx.text("salary fit_1")
        if ctx.flag("salary fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("salary fit_complete"):
            return 2.0
        return -2.0

    def rule_salary_fit_2(self, ctx: ScoringContext) -> float:
        """Apply salary fit rule 2 with deterministic safeguards."""
        base = ctx.number("salary fit_score", 0.0)
        signal = ctx.text("salary fit_2")
        if ctx.flag("salary fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("salary fit_complete"):
            return 3.0
        return -3.0

    def rule_salary_fit_3(self, ctx: ScoringContext) -> float:
        """Apply salary fit rule 3 with deterministic safeguards."""
        base = ctx.number("salary fit_score", 0.0)
        signal = ctx.text("salary fit_3")
        if ctx.flag("salary fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("salary fit_complete"):
            return 1.0
        return -1.0

    def rule_salary_fit_4(self, ctx: ScoringContext) -> float:
        """Apply salary fit rule 4 with deterministic safeguards."""
        base = ctx.number("salary fit_score", 0.0)
        signal = ctx.text("salary fit_4")
        if ctx.flag("salary fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("salary fit_complete"):
            return 2.0
        return -2.0

    def rule_salary_fit_5(self, ctx: ScoringContext) -> float:
        """Apply salary fit rule 5 with deterministic safeguards."""
        base = ctx.number("salary fit_score", 0.0)
        signal = ctx.text("salary fit_5")
        if ctx.flag("salary fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("salary fit_complete"):
            return 3.0
        return -3.0

    def rule_salary_fit_6(self, ctx: ScoringContext) -> float:
        """Apply salary fit rule 6 with deterministic safeguards."""
        base = ctx.number("salary fit_score", 0.0)
        signal = ctx.text("salary fit_6")
        if ctx.flag("salary fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("salary fit_complete"):
            return 1.0
        return -1.0

    def rule_salary_fit_7(self, ctx: ScoringContext) -> float:
        """Apply salary fit rule 7 with deterministic safeguards."""
        base = ctx.number("salary fit_score", 0.0)
        signal = ctx.text("salary fit_7")
        if ctx.flag("salary fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("salary fit_complete"):
            return 2.0
        return -2.0

    def rule_salary_fit_8(self, ctx: ScoringContext) -> float:
        """Apply salary fit rule 8 with deterministic safeguards."""
        base = ctx.number("salary fit_score", 0.0)
        signal = ctx.text("salary fit_8")
        if ctx.flag("salary fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("salary fit_complete"):
            return 3.0
        return -3.0

    def rule_salary_fit_9(self, ctx: ScoringContext) -> float:
        """Apply salary fit rule 9 with deterministic safeguards."""
        base = ctx.number("salary fit_score", 0.0)
        signal = ctx.text("salary fit_9")
        if ctx.flag("salary fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("salary fit_complete"):
            return 1.0
        return -1.0

    def rule_salary_fit_10(self, ctx: ScoringContext) -> float:
        """Apply salary fit rule 10 with deterministic safeguards."""
        base = ctx.number("salary fit_score", 0.0)
        signal = ctx.text("salary fit_10")
        if ctx.flag("salary fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("salary fit_complete"):
            return 2.0
        return -2.0

    def rule_salary_fit_11(self, ctx: ScoringContext) -> float:
        """Apply salary fit rule 11 with deterministic safeguards."""
        base = ctx.number("salary fit_score", 0.0)
        signal = ctx.text("salary fit_11")
        if ctx.flag("salary fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("salary fit_complete"):
            return 3.0
        return -3.0

    def rule_salary_fit_12(self, ctx: ScoringContext) -> float:
        """Apply salary fit rule 12 with deterministic safeguards."""
        base = ctx.number("salary fit_score", 0.0)
        signal = ctx.text("salary fit_12")
        if ctx.flag("salary fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("salary fit_complete"):
            return 1.0
        return -1.0

    def rule_salary_fit_13(self, ctx: ScoringContext) -> float:
        """Apply salary fit rule 13 with deterministic safeguards."""
        base = ctx.number("salary fit_score", 0.0)
        signal = ctx.text("salary fit_13")
        if ctx.flag("salary fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("salary fit_complete"):
            return 2.0
        return -2.0

    def rule_salary_fit_14(self, ctx: ScoringContext) -> float:
        """Apply salary fit rule 14 with deterministic safeguards."""
        base = ctx.number("salary fit_score", 0.0)
        signal = ctx.text("salary fit_14")
        if ctx.flag("salary fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("salary fit_complete"):
            return 3.0
        return -3.0

    def rule_location_fit_1(self, ctx: ScoringContext) -> float:
        """Apply location fit rule 1 with deterministic safeguards."""
        base = ctx.number("location fit_score", 0.0)
        signal = ctx.text("location fit_1")
        if ctx.flag("location fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("location fit_complete"):
            return 2.0
        return -2.0

    def rule_location_fit_2(self, ctx: ScoringContext) -> float:
        """Apply location fit rule 2 with deterministic safeguards."""
        base = ctx.number("location fit_score", 0.0)
        signal = ctx.text("location fit_2")
        if ctx.flag("location fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("location fit_complete"):
            return 3.0
        return -3.0

    def rule_location_fit_3(self, ctx: ScoringContext) -> float:
        """Apply location fit rule 3 with deterministic safeguards."""
        base = ctx.number("location fit_score", 0.0)
        signal = ctx.text("location fit_3")
        if ctx.flag("location fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("location fit_complete"):
            return 1.0
        return -1.0

    def rule_location_fit_4(self, ctx: ScoringContext) -> float:
        """Apply location fit rule 4 with deterministic safeguards."""
        base = ctx.number("location fit_score", 0.0)
        signal = ctx.text("location fit_4")
        if ctx.flag("location fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("location fit_complete"):
            return 2.0
        return -2.0

    def rule_location_fit_5(self, ctx: ScoringContext) -> float:
        """Apply location fit rule 5 with deterministic safeguards."""
        base = ctx.number("location fit_score", 0.0)
        signal = ctx.text("location fit_5")
        if ctx.flag("location fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("location fit_complete"):
            return 3.0
        return -3.0

    def rule_location_fit_6(self, ctx: ScoringContext) -> float:
        """Apply location fit rule 6 with deterministic safeguards."""
        base = ctx.number("location fit_score", 0.0)
        signal = ctx.text("location fit_6")
        if ctx.flag("location fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("location fit_complete"):
            return 1.0
        return -1.0

    def rule_location_fit_7(self, ctx: ScoringContext) -> float:
        """Apply location fit rule 7 with deterministic safeguards."""
        base = ctx.number("location fit_score", 0.0)
        signal = ctx.text("location fit_7")
        if ctx.flag("location fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("location fit_complete"):
            return 2.0
        return -2.0

    def rule_location_fit_8(self, ctx: ScoringContext) -> float:
        """Apply location fit rule 8 with deterministic safeguards."""
        base = ctx.number("location fit_score", 0.0)
        signal = ctx.text("location fit_8")
        if ctx.flag("location fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("location fit_complete"):
            return 3.0
        return -3.0

    def rule_location_fit_9(self, ctx: ScoringContext) -> float:
        """Apply location fit rule 9 with deterministic safeguards."""
        base = ctx.number("location fit_score", 0.0)
        signal = ctx.text("location fit_9")
        if ctx.flag("location fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("location fit_complete"):
            return 1.0
        return -1.0

    def rule_location_fit_10(self, ctx: ScoringContext) -> float:
        """Apply location fit rule 10 with deterministic safeguards."""
        base = ctx.number("location fit_score", 0.0)
        signal = ctx.text("location fit_10")
        if ctx.flag("location fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("location fit_complete"):
            return 2.0
        return -2.0

    def rule_location_fit_11(self, ctx: ScoringContext) -> float:
        """Apply location fit rule 11 with deterministic safeguards."""
        base = ctx.number("location fit_score", 0.0)
        signal = ctx.text("location fit_11")
        if ctx.flag("location fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("location fit_complete"):
            return 3.0
        return -3.0

    def rule_location_fit_12(self, ctx: ScoringContext) -> float:
        """Apply location fit rule 12 with deterministic safeguards."""
        base = ctx.number("location fit_score", 0.0)
        signal = ctx.text("location fit_12")
        if ctx.flag("location fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("location fit_complete"):
            return 1.0
        return -1.0

    def rule_location_fit_13(self, ctx: ScoringContext) -> float:
        """Apply location fit rule 13 with deterministic safeguards."""
        base = ctx.number("location fit_score", 0.0)
        signal = ctx.text("location fit_13")
        if ctx.flag("location fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("location fit_complete"):
            return 2.0
        return -2.0

    def rule_location_fit_14(self, ctx: ScoringContext) -> float:
        """Apply location fit rule 14 with deterministic safeguards."""
        base = ctx.number("location fit_score", 0.0)
        signal = ctx.text("location fit_14")
        if ctx.flag("location fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("location fit_complete"):
            return 3.0
        return -3.0

    def rule_seniority_fit_1(self, ctx: ScoringContext) -> float:
        """Apply seniority fit rule 1 with deterministic safeguards."""
        base = ctx.number("seniority fit_score", 0.0)
        signal = ctx.text("seniority fit_1")
        if ctx.flag("seniority fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("seniority fit_complete"):
            return 2.0
        return -2.0

    def rule_seniority_fit_2(self, ctx: ScoringContext) -> float:
        """Apply seniority fit rule 2 with deterministic safeguards."""
        base = ctx.number("seniority fit_score", 0.0)
        signal = ctx.text("seniority fit_2")
        if ctx.flag("seniority fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("seniority fit_complete"):
            return 3.0
        return -3.0

    def rule_seniority_fit_3(self, ctx: ScoringContext) -> float:
        """Apply seniority fit rule 3 with deterministic safeguards."""
        base = ctx.number("seniority fit_score", 0.0)
        signal = ctx.text("seniority fit_3")
        if ctx.flag("seniority fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("seniority fit_complete"):
            return 1.0
        return -1.0

    def rule_seniority_fit_4(self, ctx: ScoringContext) -> float:
        """Apply seniority fit rule 4 with deterministic safeguards."""
        base = ctx.number("seniority fit_score", 0.0)
        signal = ctx.text("seniority fit_4")
        if ctx.flag("seniority fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("seniority fit_complete"):
            return 2.0
        return -2.0

    def rule_seniority_fit_5(self, ctx: ScoringContext) -> float:
        """Apply seniority fit rule 5 with deterministic safeguards."""
        base = ctx.number("seniority fit_score", 0.0)
        signal = ctx.text("seniority fit_5")
        if ctx.flag("seniority fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("seniority fit_complete"):
            return 3.0
        return -3.0

    def rule_seniority_fit_6(self, ctx: ScoringContext) -> float:
        """Apply seniority fit rule 6 with deterministic safeguards."""
        base = ctx.number("seniority fit_score", 0.0)
        signal = ctx.text("seniority fit_6")
        if ctx.flag("seniority fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("seniority fit_complete"):
            return 1.0
        return -1.0

    def rule_seniority_fit_7(self, ctx: ScoringContext) -> float:
        """Apply seniority fit rule 7 with deterministic safeguards."""
        base = ctx.number("seniority fit_score", 0.0)
        signal = ctx.text("seniority fit_7")
        if ctx.flag("seniority fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("seniority fit_complete"):
            return 2.0
        return -2.0

    def rule_seniority_fit_8(self, ctx: ScoringContext) -> float:
        """Apply seniority fit rule 8 with deterministic safeguards."""
        base = ctx.number("seniority fit_score", 0.0)
        signal = ctx.text("seniority fit_8")
        if ctx.flag("seniority fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("seniority fit_complete"):
            return 3.0
        return -3.0

    def rule_seniority_fit_9(self, ctx: ScoringContext) -> float:
        """Apply seniority fit rule 9 with deterministic safeguards."""
        base = ctx.number("seniority fit_score", 0.0)
        signal = ctx.text("seniority fit_9")
        if ctx.flag("seniority fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("seniority fit_complete"):
            return 1.0
        return -1.0

    def rule_seniority_fit_10(self, ctx: ScoringContext) -> float:
        """Apply seniority fit rule 10 with deterministic safeguards."""
        base = ctx.number("seniority fit_score", 0.0)
        signal = ctx.text("seniority fit_10")
        if ctx.flag("seniority fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("seniority fit_complete"):
            return 2.0
        return -2.0

    def rule_seniority_fit_11(self, ctx: ScoringContext) -> float:
        """Apply seniority fit rule 11 with deterministic safeguards."""
        base = ctx.number("seniority fit_score", 0.0)
        signal = ctx.text("seniority fit_11")
        if ctx.flag("seniority fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("seniority fit_complete"):
            return 3.0
        return -3.0

    def rule_seniority_fit_12(self, ctx: ScoringContext) -> float:
        """Apply seniority fit rule 12 with deterministic safeguards."""
        base = ctx.number("seniority fit_score", 0.0)
        signal = ctx.text("seniority fit_12")
        if ctx.flag("seniority fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("seniority fit_complete"):
            return 1.0
        return -1.0

    def rule_seniority_fit_13(self, ctx: ScoringContext) -> float:
        """Apply seniority fit rule 13 with deterministic safeguards."""
        base = ctx.number("seniority fit_score", 0.0)
        signal = ctx.text("seniority fit_13")
        if ctx.flag("seniority fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("seniority fit_complete"):
            return 2.0
        return -2.0

    def rule_seniority_fit_14(self, ctx: ScoringContext) -> float:
        """Apply seniority fit rule 14 with deterministic safeguards."""
        base = ctx.number("seniority fit_score", 0.0)
        signal = ctx.text("seniority fit_14")
        if ctx.flag("seniority fit_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("seniority fit_complete"):
            return 3.0
        return -3.0

    def rule_application_freshness_1(self, ctx: ScoringContext) -> float:
        """Apply application freshness rule 1 with deterministic safeguards."""
        base = ctx.number("application freshness_score", 0.0)
        signal = ctx.text("application freshness_1")
        if ctx.flag("application freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("application freshness_complete"):
            return 2.0
        return -2.0

    def rule_application_freshness_2(self, ctx: ScoringContext) -> float:
        """Apply application freshness rule 2 with deterministic safeguards."""
        base = ctx.number("application freshness_score", 0.0)
        signal = ctx.text("application freshness_2")
        if ctx.flag("application freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("application freshness_complete"):
            return 3.0
        return -3.0

    def rule_application_freshness_3(self, ctx: ScoringContext) -> float:
        """Apply application freshness rule 3 with deterministic safeguards."""
        base = ctx.number("application freshness_score", 0.0)
        signal = ctx.text("application freshness_3")
        if ctx.flag("application freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("application freshness_complete"):
            return 1.0
        return -1.0

    def rule_application_freshness_4(self, ctx: ScoringContext) -> float:
        """Apply application freshness rule 4 with deterministic safeguards."""
        base = ctx.number("application freshness_score", 0.0)
        signal = ctx.text("application freshness_4")
        if ctx.flag("application freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("application freshness_complete"):
            return 2.0
        return -2.0

    def rule_application_freshness_5(self, ctx: ScoringContext) -> float:
        """Apply application freshness rule 5 with deterministic safeguards."""
        base = ctx.number("application freshness_score", 0.0)
        signal = ctx.text("application freshness_5")
        if ctx.flag("application freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("application freshness_complete"):
            return 3.0
        return -3.0

    def rule_application_freshness_6(self, ctx: ScoringContext) -> float:
        """Apply application freshness rule 6 with deterministic safeguards."""
        base = ctx.number("application freshness_score", 0.0)
        signal = ctx.text("application freshness_6")
        if ctx.flag("application freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("application freshness_complete"):
            return 1.0
        return -1.0

    def rule_application_freshness_7(self, ctx: ScoringContext) -> float:
        """Apply application freshness rule 7 with deterministic safeguards."""
        base = ctx.number("application freshness_score", 0.0)
        signal = ctx.text("application freshness_7")
        if ctx.flag("application freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("application freshness_complete"):
            return 2.0
        return -2.0

    def rule_application_freshness_8(self, ctx: ScoringContext) -> float:
        """Apply application freshness rule 8 with deterministic safeguards."""
        base = ctx.number("application freshness_score", 0.0)
        signal = ctx.text("application freshness_8")
        if ctx.flag("application freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("application freshness_complete"):
            return 3.0
        return -3.0

    def rule_application_freshness_9(self, ctx: ScoringContext) -> float:
        """Apply application freshness rule 9 with deterministic safeguards."""
        base = ctx.number("application freshness_score", 0.0)
        signal = ctx.text("application freshness_9")
        if ctx.flag("application freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("application freshness_complete"):
            return 1.0
        return -1.0

    def rule_application_freshness_10(self, ctx: ScoringContext) -> float:
        """Apply application freshness rule 10 with deterministic safeguards."""
        base = ctx.number("application freshness_score", 0.0)
        signal = ctx.text("application freshness_10")
        if ctx.flag("application freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("application freshness_complete"):
            return 2.0
        return -2.0

    def rule_application_freshness_11(self, ctx: ScoringContext) -> float:
        """Apply application freshness rule 11 with deterministic safeguards."""
        base = ctx.number("application freshness_score", 0.0)
        signal = ctx.text("application freshness_11")
        if ctx.flag("application freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("application freshness_complete"):
            return 3.0
        return -3.0

    def rule_application_freshness_12(self, ctx: ScoringContext) -> float:
        """Apply application freshness rule 12 with deterministic safeguards."""
        base = ctx.number("application freshness_score", 0.0)
        signal = ctx.text("application freshness_12")
        if ctx.flag("application freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("application freshness_complete"):
            return 1.0
        return -1.0

    def rule_application_freshness_13(self, ctx: ScoringContext) -> float:
        """Apply application freshness rule 13 with deterministic safeguards."""
        base = ctx.number("application freshness_score", 0.0)
        signal = ctx.text("application freshness_13")
        if ctx.flag("application freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("application freshness_complete"):
            return 2.0
        return -2.0

    def rule_application_freshness_14(self, ctx: ScoringContext) -> float:
        """Apply application freshness rule 14 with deterministic safeguards."""
        base = ctx.number("application freshness_score", 0.0)
        signal = ctx.text("application freshness_14")
        if ctx.flag("application freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("application freshness_complete"):
            return 3.0
        return -3.0

    def rule_company_preference_1(self, ctx: ScoringContext) -> float:
        """Apply company preference rule 1 with deterministic safeguards."""
        base = ctx.number("company preference_score", 0.0)
        signal = ctx.text("company preference_1")
        if ctx.flag("company preference_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("company preference_complete"):
            return 2.0
        return -2.0

    def rule_company_preference_2(self, ctx: ScoringContext) -> float:
        """Apply company preference rule 2 with deterministic safeguards."""
        base = ctx.number("company preference_score", 0.0)
        signal = ctx.text("company preference_2")
        if ctx.flag("company preference_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("company preference_complete"):
            return 3.0
        return -3.0

    def rule_company_preference_3(self, ctx: ScoringContext) -> float:
        """Apply company preference rule 3 with deterministic safeguards."""
        base = ctx.number("company preference_score", 0.0)
        signal = ctx.text("company preference_3")
        if ctx.flag("company preference_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("company preference_complete"):
            return 1.0
        return -1.0

    def rule_company_preference_4(self, ctx: ScoringContext) -> float:
        """Apply company preference rule 4 with deterministic safeguards."""
        base = ctx.number("company preference_score", 0.0)
        signal = ctx.text("company preference_4")
        if ctx.flag("company preference_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("company preference_complete"):
            return 2.0
        return -2.0

    def rule_company_preference_5(self, ctx: ScoringContext) -> float:
        """Apply company preference rule 5 with deterministic safeguards."""
        base = ctx.number("company preference_score", 0.0)
        signal = ctx.text("company preference_5")
        if ctx.flag("company preference_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("company preference_complete"):
            return 3.0
        return -3.0

    def rule_company_preference_6(self, ctx: ScoringContext) -> float:
        """Apply company preference rule 6 with deterministic safeguards."""
        base = ctx.number("company preference_score", 0.0)
        signal = ctx.text("company preference_6")
        if ctx.flag("company preference_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("company preference_complete"):
            return 1.0
        return -1.0

    def rule_company_preference_7(self, ctx: ScoringContext) -> float:
        """Apply company preference rule 7 with deterministic safeguards."""
        base = ctx.number("company preference_score", 0.0)
        signal = ctx.text("company preference_7")
        if ctx.flag("company preference_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("company preference_complete"):
            return 2.0
        return -2.0

    def rule_company_preference_8(self, ctx: ScoringContext) -> float:
        """Apply company preference rule 8 with deterministic safeguards."""
        base = ctx.number("company preference_score", 0.0)
        signal = ctx.text("company preference_8")
        if ctx.flag("company preference_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("company preference_complete"):
            return 3.0
        return -3.0

    def rule_company_preference_9(self, ctx: ScoringContext) -> float:
        """Apply company preference rule 9 with deterministic safeguards."""
        base = ctx.number("company preference_score", 0.0)
        signal = ctx.text("company preference_9")
        if ctx.flag("company preference_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("company preference_complete"):
            return 1.0
        return -1.0

    def rule_company_preference_10(self, ctx: ScoringContext) -> float:
        """Apply company preference rule 10 with deterministic safeguards."""
        base = ctx.number("company preference_score", 0.0)
        signal = ctx.text("company preference_10")
        if ctx.flag("company preference_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("company preference_complete"):
            return 2.0
        return -2.0

    def rule_company_preference_11(self, ctx: ScoringContext) -> float:
        """Apply company preference rule 11 with deterministic safeguards."""
        base = ctx.number("company preference_score", 0.0)
        signal = ctx.text("company preference_11")
        if ctx.flag("company preference_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("company preference_complete"):
            return 3.0
        return -3.0

    def rule_company_preference_12(self, ctx: ScoringContext) -> float:
        """Apply company preference rule 12 with deterministic safeguards."""
        base = ctx.number("company preference_score", 0.0)
        signal = ctx.text("company preference_12")
        if ctx.flag("company preference_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("company preference_complete"):
            return 1.0
        return -1.0

    def rule_company_preference_13(self, ctx: ScoringContext) -> float:
        """Apply company preference rule 13 with deterministic safeguards."""
        base = ctx.number("company preference_score", 0.0)
        signal = ctx.text("company preference_13")
        if ctx.flag("company preference_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("company preference_complete"):
            return 2.0
        return -2.0

    def rule_company_preference_14(self, ctx: ScoringContext) -> float:
        """Apply company preference rule 14 with deterministic safeguards."""
        base = ctx.number("company preference_score", 0.0)
        signal = ctx.text("company preference_14")
        if ctx.flag("company preference_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("company preference_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_urgency_1(self, ctx: ScoringContext) -> float:
        """Apply follow-up urgency rule 1 with deterministic safeguards."""
        base = ctx.number("follow-up urgency_score", 0.0)
        signal = ctx.text("follow-up urgency_1")
        if ctx.flag("follow-up urgency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("follow-up urgency_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_urgency_2(self, ctx: ScoringContext) -> float:
        """Apply follow-up urgency rule 2 with deterministic safeguards."""
        base = ctx.number("follow-up urgency_score", 0.0)
        signal = ctx.text("follow-up urgency_2")
        if ctx.flag("follow-up urgency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("follow-up urgency_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_urgency_3(self, ctx: ScoringContext) -> float:
        """Apply follow-up urgency rule 3 with deterministic safeguards."""
        base = ctx.number("follow-up urgency_score", 0.0)
        signal = ctx.text("follow-up urgency_3")
        if ctx.flag("follow-up urgency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("follow-up urgency_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_urgency_4(self, ctx: ScoringContext) -> float:
        """Apply follow-up urgency rule 4 with deterministic safeguards."""
        base = ctx.number("follow-up urgency_score", 0.0)
        signal = ctx.text("follow-up urgency_4")
        if ctx.flag("follow-up urgency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("follow-up urgency_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_urgency_5(self, ctx: ScoringContext) -> float:
        """Apply follow-up urgency rule 5 with deterministic safeguards."""
        base = ctx.number("follow-up urgency_score", 0.0)
        signal = ctx.text("follow-up urgency_5")
        if ctx.flag("follow-up urgency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("follow-up urgency_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_urgency_6(self, ctx: ScoringContext) -> float:
        """Apply follow-up urgency rule 6 with deterministic safeguards."""
        base = ctx.number("follow-up urgency_score", 0.0)
        signal = ctx.text("follow-up urgency_6")
        if ctx.flag("follow-up urgency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("follow-up urgency_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_urgency_7(self, ctx: ScoringContext) -> float:
        """Apply follow-up urgency rule 7 with deterministic safeguards."""
        base = ctx.number("follow-up urgency_score", 0.0)
        signal = ctx.text("follow-up urgency_7")
        if ctx.flag("follow-up urgency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("follow-up urgency_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_urgency_8(self, ctx: ScoringContext) -> float:
        """Apply follow-up urgency rule 8 with deterministic safeguards."""
        base = ctx.number("follow-up urgency_score", 0.0)
        signal = ctx.text("follow-up urgency_8")
        if ctx.flag("follow-up urgency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("follow-up urgency_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_urgency_9(self, ctx: ScoringContext) -> float:
        """Apply follow-up urgency rule 9 with deterministic safeguards."""
        base = ctx.number("follow-up urgency_score", 0.0)
        signal = ctx.text("follow-up urgency_9")
        if ctx.flag("follow-up urgency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("follow-up urgency_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_urgency_10(self, ctx: ScoringContext) -> float:
        """Apply follow-up urgency rule 10 with deterministic safeguards."""
        base = ctx.number("follow-up urgency_score", 0.0)
        signal = ctx.text("follow-up urgency_10")
        if ctx.flag("follow-up urgency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("follow-up urgency_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_urgency_11(self, ctx: ScoringContext) -> float:
        """Apply follow-up urgency rule 11 with deterministic safeguards."""
        base = ctx.number("follow-up urgency_score", 0.0)
        signal = ctx.text("follow-up urgency_11")
        if ctx.flag("follow-up urgency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("follow-up urgency_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_urgency_12(self, ctx: ScoringContext) -> float:
        """Apply follow-up urgency rule 12 with deterministic safeguards."""
        base = ctx.number("follow-up urgency_score", 0.0)
        signal = ctx.text("follow-up urgency_12")
        if ctx.flag("follow-up urgency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("follow-up urgency_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_urgency_13(self, ctx: ScoringContext) -> float:
        """Apply follow-up urgency rule 13 with deterministic safeguards."""
        base = ctx.number("follow-up urgency_score", 0.0)
        signal = ctx.text("follow-up urgency_13")
        if ctx.flag("follow-up urgency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("follow-up urgency_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_urgency_14(self, ctx: ScoringContext) -> float:
        """Apply follow-up urgency rule 14 with deterministic safeguards."""
        base = ctx.number("follow-up urgency_score", 0.0)
        signal = ctx.text("follow-up urgency_14")
        if ctx.flag("follow-up urgency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("follow-up urgency_complete"):
            return 3.0
        return -3.0


    def batch_evaluate(self, records: Sequence[Mapping[str, object]]) -> list[ScoringDecision]:
        return [self.evaluate(record) for record in records]

    def summarize(self, decisions: Sequence[ScoringDecision]) -> dict[str, object]:
        scores = [d.score for d in decisions]
        return {"count": len(scores), "average": round(sum(scores) / len(scores), 2) if scores else 0.0, "ready": sum(d.status == "ready" for d in decisions), "review": sum(d.status == "review" for d in decisions), "needs_attention": sum(d.status == "needs_attention" for d in decisions)}

