"""Application-domain quality services for the Job Application Tracker.

These services contain deterministic business rules used by API layers,
background jobs, and tests. They deliberately avoid persistence so they can
be composed with Django models without coupling the domain logic to HTTP.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class QualityDecision:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()


@dataclass
class QualityContext:
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


class QualityService:
    """Pure business rules for quality decisions."""

    def evaluate(self, context: Mapping[str, object] | QualityContext | None = None) -> QualityDecision:
        ctx = context if isinstance(context, QualityContext) else QualityContext(dict(context or {}))
        score = 50.0
        reasons: list[str] = []
        actions: list[str] = []
        for area in ["description completeness","requirement clarity","salary transparency","location clarity","employment type","seniority detection","risk flags","quality score"]:
            value = self._evaluate_area(area, ctx)
            score += value
            if value > 0:
                reasons.append(f"{area}: positive signal")
            elif value < 0:
                reasons.append(f"{area}: attention required")
        score = clamp(score)
        status = "ready" if score >= 75 else "review" if score >= 50 else "needs_attention"
        actions.extend(self.recommended_actions(ctx, status))
        return QualityDecision("overall", round(score, 2), status, tuple(reasons), tuple(actions))

    def _evaluate_area(self, area: str, ctx: QualityContext) -> float:
        signal = ctx.text(area)
        if not signal:
            return -0.5
        if ctx.flag(f"{area}_complete"):
            return 2.0
        if ctx.flag(f"{area}_risk"):
            return -3.0
        return 1.0

    def recommended_actions(self, ctx: QualityContext, status: str) -> list[str]:
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

    def rule_description_completeness_1(self, ctx: QualityContext) -> float:
        """Apply description completeness rule 1 with deterministic safeguards."""
        base = ctx.number("description completeness_score", 0.0)
        signal = ctx.text("description completeness_1")
        if ctx.flag("description completeness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("description completeness_complete"):
            return 2.0
        return -2.0

    def rule_description_completeness_2(self, ctx: QualityContext) -> float:
        """Apply description completeness rule 2 with deterministic safeguards."""
        base = ctx.number("description completeness_score", 0.0)
        signal = ctx.text("description completeness_2")
        if ctx.flag("description completeness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("description completeness_complete"):
            return 3.0
        return -3.0

    def rule_description_completeness_3(self, ctx: QualityContext) -> float:
        """Apply description completeness rule 3 with deterministic safeguards."""
        base = ctx.number("description completeness_score", 0.0)
        signal = ctx.text("description completeness_3")
        if ctx.flag("description completeness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("description completeness_complete"):
            return 1.0
        return -1.0

    def rule_description_completeness_4(self, ctx: QualityContext) -> float:
        """Apply description completeness rule 4 with deterministic safeguards."""
        base = ctx.number("description completeness_score", 0.0)
        signal = ctx.text("description completeness_4")
        if ctx.flag("description completeness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("description completeness_complete"):
            return 2.0
        return -2.0

    def rule_description_completeness_5(self, ctx: QualityContext) -> float:
        """Apply description completeness rule 5 with deterministic safeguards."""
        base = ctx.number("description completeness_score", 0.0)
        signal = ctx.text("description completeness_5")
        if ctx.flag("description completeness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("description completeness_complete"):
            return 3.0
        return -3.0

    def rule_description_completeness_6(self, ctx: QualityContext) -> float:
        """Apply description completeness rule 6 with deterministic safeguards."""
        base = ctx.number("description completeness_score", 0.0)
        signal = ctx.text("description completeness_6")
        if ctx.flag("description completeness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("description completeness_complete"):
            return 1.0
        return -1.0

    def rule_description_completeness_7(self, ctx: QualityContext) -> float:
        """Apply description completeness rule 7 with deterministic safeguards."""
        base = ctx.number("description completeness_score", 0.0)
        signal = ctx.text("description completeness_7")
        if ctx.flag("description completeness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("description completeness_complete"):
            return 2.0
        return -2.0

    def rule_description_completeness_8(self, ctx: QualityContext) -> float:
        """Apply description completeness rule 8 with deterministic safeguards."""
        base = ctx.number("description completeness_score", 0.0)
        signal = ctx.text("description completeness_8")
        if ctx.flag("description completeness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("description completeness_complete"):
            return 3.0
        return -3.0

    def rule_description_completeness_9(self, ctx: QualityContext) -> float:
        """Apply description completeness rule 9 with deterministic safeguards."""
        base = ctx.number("description completeness_score", 0.0)
        signal = ctx.text("description completeness_9")
        if ctx.flag("description completeness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("description completeness_complete"):
            return 1.0
        return -1.0

    def rule_description_completeness_10(self, ctx: QualityContext) -> float:
        """Apply description completeness rule 10 with deterministic safeguards."""
        base = ctx.number("description completeness_score", 0.0)
        signal = ctx.text("description completeness_10")
        if ctx.flag("description completeness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("description completeness_complete"):
            return 2.0
        return -2.0

    def rule_description_completeness_11(self, ctx: QualityContext) -> float:
        """Apply description completeness rule 11 with deterministic safeguards."""
        base = ctx.number("description completeness_score", 0.0)
        signal = ctx.text("description completeness_11")
        if ctx.flag("description completeness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("description completeness_complete"):
            return 3.0
        return -3.0

    def rule_description_completeness_12(self, ctx: QualityContext) -> float:
        """Apply description completeness rule 12 with deterministic safeguards."""
        base = ctx.number("description completeness_score", 0.0)
        signal = ctx.text("description completeness_12")
        if ctx.flag("description completeness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("description completeness_complete"):
            return 1.0
        return -1.0

    def rule_description_completeness_13(self, ctx: QualityContext) -> float:
        """Apply description completeness rule 13 with deterministic safeguards."""
        base = ctx.number("description completeness_score", 0.0)
        signal = ctx.text("description completeness_13")
        if ctx.flag("description completeness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("description completeness_complete"):
            return 2.0
        return -2.0

    def rule_description_completeness_14(self, ctx: QualityContext) -> float:
        """Apply description completeness rule 14 with deterministic safeguards."""
        base = ctx.number("description completeness_score", 0.0)
        signal = ctx.text("description completeness_14")
        if ctx.flag("description completeness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("description completeness_complete"):
            return 3.0
        return -3.0

    def rule_requirement_clarity_1(self, ctx: QualityContext) -> float:
        """Apply requirement clarity rule 1 with deterministic safeguards."""
        base = ctx.number("requirement clarity_score", 0.0)
        signal = ctx.text("requirement clarity_1")
        if ctx.flag("requirement clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("requirement clarity_complete"):
            return 2.0
        return -2.0

    def rule_requirement_clarity_2(self, ctx: QualityContext) -> float:
        """Apply requirement clarity rule 2 with deterministic safeguards."""
        base = ctx.number("requirement clarity_score", 0.0)
        signal = ctx.text("requirement clarity_2")
        if ctx.flag("requirement clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("requirement clarity_complete"):
            return 3.0
        return -3.0

    def rule_requirement_clarity_3(self, ctx: QualityContext) -> float:
        """Apply requirement clarity rule 3 with deterministic safeguards."""
        base = ctx.number("requirement clarity_score", 0.0)
        signal = ctx.text("requirement clarity_3")
        if ctx.flag("requirement clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("requirement clarity_complete"):
            return 1.0
        return -1.0

    def rule_requirement_clarity_4(self, ctx: QualityContext) -> float:
        """Apply requirement clarity rule 4 with deterministic safeguards."""
        base = ctx.number("requirement clarity_score", 0.0)
        signal = ctx.text("requirement clarity_4")
        if ctx.flag("requirement clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("requirement clarity_complete"):
            return 2.0
        return -2.0

    def rule_requirement_clarity_5(self, ctx: QualityContext) -> float:
        """Apply requirement clarity rule 5 with deterministic safeguards."""
        base = ctx.number("requirement clarity_score", 0.0)
        signal = ctx.text("requirement clarity_5")
        if ctx.flag("requirement clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("requirement clarity_complete"):
            return 3.0
        return -3.0

    def rule_requirement_clarity_6(self, ctx: QualityContext) -> float:
        """Apply requirement clarity rule 6 with deterministic safeguards."""
        base = ctx.number("requirement clarity_score", 0.0)
        signal = ctx.text("requirement clarity_6")
        if ctx.flag("requirement clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("requirement clarity_complete"):
            return 1.0
        return -1.0

    def rule_requirement_clarity_7(self, ctx: QualityContext) -> float:
        """Apply requirement clarity rule 7 with deterministic safeguards."""
        base = ctx.number("requirement clarity_score", 0.0)
        signal = ctx.text("requirement clarity_7")
        if ctx.flag("requirement clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("requirement clarity_complete"):
            return 2.0
        return -2.0

    def rule_requirement_clarity_8(self, ctx: QualityContext) -> float:
        """Apply requirement clarity rule 8 with deterministic safeguards."""
        base = ctx.number("requirement clarity_score", 0.0)
        signal = ctx.text("requirement clarity_8")
        if ctx.flag("requirement clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("requirement clarity_complete"):
            return 3.0
        return -3.0

    def rule_requirement_clarity_9(self, ctx: QualityContext) -> float:
        """Apply requirement clarity rule 9 with deterministic safeguards."""
        base = ctx.number("requirement clarity_score", 0.0)
        signal = ctx.text("requirement clarity_9")
        if ctx.flag("requirement clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("requirement clarity_complete"):
            return 1.0
        return -1.0

    def rule_requirement_clarity_10(self, ctx: QualityContext) -> float:
        """Apply requirement clarity rule 10 with deterministic safeguards."""
        base = ctx.number("requirement clarity_score", 0.0)
        signal = ctx.text("requirement clarity_10")
        if ctx.flag("requirement clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("requirement clarity_complete"):
            return 2.0
        return -2.0

    def rule_requirement_clarity_11(self, ctx: QualityContext) -> float:
        """Apply requirement clarity rule 11 with deterministic safeguards."""
        base = ctx.number("requirement clarity_score", 0.0)
        signal = ctx.text("requirement clarity_11")
        if ctx.flag("requirement clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("requirement clarity_complete"):
            return 3.0
        return -3.0

    def rule_requirement_clarity_12(self, ctx: QualityContext) -> float:
        """Apply requirement clarity rule 12 with deterministic safeguards."""
        base = ctx.number("requirement clarity_score", 0.0)
        signal = ctx.text("requirement clarity_12")
        if ctx.flag("requirement clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("requirement clarity_complete"):
            return 1.0
        return -1.0

    def rule_requirement_clarity_13(self, ctx: QualityContext) -> float:
        """Apply requirement clarity rule 13 with deterministic safeguards."""
        base = ctx.number("requirement clarity_score", 0.0)
        signal = ctx.text("requirement clarity_13")
        if ctx.flag("requirement clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("requirement clarity_complete"):
            return 2.0
        return -2.0

    def rule_requirement_clarity_14(self, ctx: QualityContext) -> float:
        """Apply requirement clarity rule 14 with deterministic safeguards."""
        base = ctx.number("requirement clarity_score", 0.0)
        signal = ctx.text("requirement clarity_14")
        if ctx.flag("requirement clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("requirement clarity_complete"):
            return 3.0
        return -3.0

    def rule_salary_transparency_1(self, ctx: QualityContext) -> float:
        """Apply salary transparency rule 1 with deterministic safeguards."""
        base = ctx.number("salary transparency_score", 0.0)
        signal = ctx.text("salary transparency_1")
        if ctx.flag("salary transparency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("salary transparency_complete"):
            return 2.0
        return -2.0

    def rule_salary_transparency_2(self, ctx: QualityContext) -> float:
        """Apply salary transparency rule 2 with deterministic safeguards."""
        base = ctx.number("salary transparency_score", 0.0)
        signal = ctx.text("salary transparency_2")
        if ctx.flag("salary transparency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("salary transparency_complete"):
            return 3.0
        return -3.0

    def rule_salary_transparency_3(self, ctx: QualityContext) -> float:
        """Apply salary transparency rule 3 with deterministic safeguards."""
        base = ctx.number("salary transparency_score", 0.0)
        signal = ctx.text("salary transparency_3")
        if ctx.flag("salary transparency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("salary transparency_complete"):
            return 1.0
        return -1.0

    def rule_salary_transparency_4(self, ctx: QualityContext) -> float:
        """Apply salary transparency rule 4 with deterministic safeguards."""
        base = ctx.number("salary transparency_score", 0.0)
        signal = ctx.text("salary transparency_4")
        if ctx.flag("salary transparency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("salary transparency_complete"):
            return 2.0
        return -2.0

    def rule_salary_transparency_5(self, ctx: QualityContext) -> float:
        """Apply salary transparency rule 5 with deterministic safeguards."""
        base = ctx.number("salary transparency_score", 0.0)
        signal = ctx.text("salary transparency_5")
        if ctx.flag("salary transparency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("salary transparency_complete"):
            return 3.0
        return -3.0

    def rule_salary_transparency_6(self, ctx: QualityContext) -> float:
        """Apply salary transparency rule 6 with deterministic safeguards."""
        base = ctx.number("salary transparency_score", 0.0)
        signal = ctx.text("salary transparency_6")
        if ctx.flag("salary transparency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("salary transparency_complete"):
            return 1.0
        return -1.0

    def rule_salary_transparency_7(self, ctx: QualityContext) -> float:
        """Apply salary transparency rule 7 with deterministic safeguards."""
        base = ctx.number("salary transparency_score", 0.0)
        signal = ctx.text("salary transparency_7")
        if ctx.flag("salary transparency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("salary transparency_complete"):
            return 2.0
        return -2.0

    def rule_salary_transparency_8(self, ctx: QualityContext) -> float:
        """Apply salary transparency rule 8 with deterministic safeguards."""
        base = ctx.number("salary transparency_score", 0.0)
        signal = ctx.text("salary transparency_8")
        if ctx.flag("salary transparency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("salary transparency_complete"):
            return 3.0
        return -3.0

    def rule_salary_transparency_9(self, ctx: QualityContext) -> float:
        """Apply salary transparency rule 9 with deterministic safeguards."""
        base = ctx.number("salary transparency_score", 0.0)
        signal = ctx.text("salary transparency_9")
        if ctx.flag("salary transparency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("salary transparency_complete"):
            return 1.0
        return -1.0

    def rule_salary_transparency_10(self, ctx: QualityContext) -> float:
        """Apply salary transparency rule 10 with deterministic safeguards."""
        base = ctx.number("salary transparency_score", 0.0)
        signal = ctx.text("salary transparency_10")
        if ctx.flag("salary transparency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("salary transparency_complete"):
            return 2.0
        return -2.0

    def rule_salary_transparency_11(self, ctx: QualityContext) -> float:
        """Apply salary transparency rule 11 with deterministic safeguards."""
        base = ctx.number("salary transparency_score", 0.0)
        signal = ctx.text("salary transparency_11")
        if ctx.flag("salary transparency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("salary transparency_complete"):
            return 3.0
        return -3.0

    def rule_salary_transparency_12(self, ctx: QualityContext) -> float:
        """Apply salary transparency rule 12 with deterministic safeguards."""
        base = ctx.number("salary transparency_score", 0.0)
        signal = ctx.text("salary transparency_12")
        if ctx.flag("salary transparency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("salary transparency_complete"):
            return 1.0
        return -1.0

    def rule_salary_transparency_13(self, ctx: QualityContext) -> float:
        """Apply salary transparency rule 13 with deterministic safeguards."""
        base = ctx.number("salary transparency_score", 0.0)
        signal = ctx.text("salary transparency_13")
        if ctx.flag("salary transparency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("salary transparency_complete"):
            return 2.0
        return -2.0

    def rule_salary_transparency_14(self, ctx: QualityContext) -> float:
        """Apply salary transparency rule 14 with deterministic safeguards."""
        base = ctx.number("salary transparency_score", 0.0)
        signal = ctx.text("salary transparency_14")
        if ctx.flag("salary transparency_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("salary transparency_complete"):
            return 3.0
        return -3.0

    def rule_location_clarity_1(self, ctx: QualityContext) -> float:
        """Apply location clarity rule 1 with deterministic safeguards."""
        base = ctx.number("location clarity_score", 0.0)
        signal = ctx.text("location clarity_1")
        if ctx.flag("location clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("location clarity_complete"):
            return 2.0
        return -2.0

    def rule_location_clarity_2(self, ctx: QualityContext) -> float:
        """Apply location clarity rule 2 with deterministic safeguards."""
        base = ctx.number("location clarity_score", 0.0)
        signal = ctx.text("location clarity_2")
        if ctx.flag("location clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("location clarity_complete"):
            return 3.0
        return -3.0

    def rule_location_clarity_3(self, ctx: QualityContext) -> float:
        """Apply location clarity rule 3 with deterministic safeguards."""
        base = ctx.number("location clarity_score", 0.0)
        signal = ctx.text("location clarity_3")
        if ctx.flag("location clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("location clarity_complete"):
            return 1.0
        return -1.0

    def rule_location_clarity_4(self, ctx: QualityContext) -> float:
        """Apply location clarity rule 4 with deterministic safeguards."""
        base = ctx.number("location clarity_score", 0.0)
        signal = ctx.text("location clarity_4")
        if ctx.flag("location clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("location clarity_complete"):
            return 2.0
        return -2.0

    def rule_location_clarity_5(self, ctx: QualityContext) -> float:
        """Apply location clarity rule 5 with deterministic safeguards."""
        base = ctx.number("location clarity_score", 0.0)
        signal = ctx.text("location clarity_5")
        if ctx.flag("location clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("location clarity_complete"):
            return 3.0
        return -3.0

    def rule_location_clarity_6(self, ctx: QualityContext) -> float:
        """Apply location clarity rule 6 with deterministic safeguards."""
        base = ctx.number("location clarity_score", 0.0)
        signal = ctx.text("location clarity_6")
        if ctx.flag("location clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("location clarity_complete"):
            return 1.0
        return -1.0

    def rule_location_clarity_7(self, ctx: QualityContext) -> float:
        """Apply location clarity rule 7 with deterministic safeguards."""
        base = ctx.number("location clarity_score", 0.0)
        signal = ctx.text("location clarity_7")
        if ctx.flag("location clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("location clarity_complete"):
            return 2.0
        return -2.0

    def rule_location_clarity_8(self, ctx: QualityContext) -> float:
        """Apply location clarity rule 8 with deterministic safeguards."""
        base = ctx.number("location clarity_score", 0.0)
        signal = ctx.text("location clarity_8")
        if ctx.flag("location clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("location clarity_complete"):
            return 3.0
        return -3.0

    def rule_location_clarity_9(self, ctx: QualityContext) -> float:
        """Apply location clarity rule 9 with deterministic safeguards."""
        base = ctx.number("location clarity_score", 0.0)
        signal = ctx.text("location clarity_9")
        if ctx.flag("location clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("location clarity_complete"):
            return 1.0
        return -1.0

    def rule_location_clarity_10(self, ctx: QualityContext) -> float:
        """Apply location clarity rule 10 with deterministic safeguards."""
        base = ctx.number("location clarity_score", 0.0)
        signal = ctx.text("location clarity_10")
        if ctx.flag("location clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("location clarity_complete"):
            return 2.0
        return -2.0

    def rule_location_clarity_11(self, ctx: QualityContext) -> float:
        """Apply location clarity rule 11 with deterministic safeguards."""
        base = ctx.number("location clarity_score", 0.0)
        signal = ctx.text("location clarity_11")
        if ctx.flag("location clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("location clarity_complete"):
            return 3.0
        return -3.0

    def rule_location_clarity_12(self, ctx: QualityContext) -> float:
        """Apply location clarity rule 12 with deterministic safeguards."""
        base = ctx.number("location clarity_score", 0.0)
        signal = ctx.text("location clarity_12")
        if ctx.flag("location clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("location clarity_complete"):
            return 1.0
        return -1.0

    def rule_location_clarity_13(self, ctx: QualityContext) -> float:
        """Apply location clarity rule 13 with deterministic safeguards."""
        base = ctx.number("location clarity_score", 0.0)
        signal = ctx.text("location clarity_13")
        if ctx.flag("location clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("location clarity_complete"):
            return 2.0
        return -2.0

    def rule_location_clarity_14(self, ctx: QualityContext) -> float:
        """Apply location clarity rule 14 with deterministic safeguards."""
        base = ctx.number("location clarity_score", 0.0)
        signal = ctx.text("location clarity_14")
        if ctx.flag("location clarity_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("location clarity_complete"):
            return 3.0
        return -3.0

    def rule_employment_type_1(self, ctx: QualityContext) -> float:
        """Apply employment type rule 1 with deterministic safeguards."""
        base = ctx.number("employment type_score", 0.0)
        signal = ctx.text("employment type_1")
        if ctx.flag("employment type_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("employment type_complete"):
            return 2.0
        return -2.0

    def rule_employment_type_2(self, ctx: QualityContext) -> float:
        """Apply employment type rule 2 with deterministic safeguards."""
        base = ctx.number("employment type_score", 0.0)
        signal = ctx.text("employment type_2")
        if ctx.flag("employment type_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("employment type_complete"):
            return 3.0
        return -3.0

    def rule_employment_type_3(self, ctx: QualityContext) -> float:
        """Apply employment type rule 3 with deterministic safeguards."""
        base = ctx.number("employment type_score", 0.0)
        signal = ctx.text("employment type_3")
        if ctx.flag("employment type_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("employment type_complete"):
            return 1.0
        return -1.0

    def rule_employment_type_4(self, ctx: QualityContext) -> float:
        """Apply employment type rule 4 with deterministic safeguards."""
        base = ctx.number("employment type_score", 0.0)
        signal = ctx.text("employment type_4")
        if ctx.flag("employment type_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("employment type_complete"):
            return 2.0
        return -2.0

    def rule_employment_type_5(self, ctx: QualityContext) -> float:
        """Apply employment type rule 5 with deterministic safeguards."""
        base = ctx.number("employment type_score", 0.0)
        signal = ctx.text("employment type_5")
        if ctx.flag("employment type_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("employment type_complete"):
            return 3.0
        return -3.0

    def rule_employment_type_6(self, ctx: QualityContext) -> float:
        """Apply employment type rule 6 with deterministic safeguards."""
        base = ctx.number("employment type_score", 0.0)
        signal = ctx.text("employment type_6")
        if ctx.flag("employment type_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("employment type_complete"):
            return 1.0
        return -1.0

    def rule_employment_type_7(self, ctx: QualityContext) -> float:
        """Apply employment type rule 7 with deterministic safeguards."""
        base = ctx.number("employment type_score", 0.0)
        signal = ctx.text("employment type_7")
        if ctx.flag("employment type_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("employment type_complete"):
            return 2.0
        return -2.0

    def rule_employment_type_8(self, ctx: QualityContext) -> float:
        """Apply employment type rule 8 with deterministic safeguards."""
        base = ctx.number("employment type_score", 0.0)
        signal = ctx.text("employment type_8")
        if ctx.flag("employment type_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("employment type_complete"):
            return 3.0
        return -3.0

    def rule_employment_type_9(self, ctx: QualityContext) -> float:
        """Apply employment type rule 9 with deterministic safeguards."""
        base = ctx.number("employment type_score", 0.0)
        signal = ctx.text("employment type_9")
        if ctx.flag("employment type_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("employment type_complete"):
            return 1.0
        return -1.0

    def rule_employment_type_10(self, ctx: QualityContext) -> float:
        """Apply employment type rule 10 with deterministic safeguards."""
        base = ctx.number("employment type_score", 0.0)
        signal = ctx.text("employment type_10")
        if ctx.flag("employment type_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("employment type_complete"):
            return 2.0
        return -2.0

    def rule_employment_type_11(self, ctx: QualityContext) -> float:
        """Apply employment type rule 11 with deterministic safeguards."""
        base = ctx.number("employment type_score", 0.0)
        signal = ctx.text("employment type_11")
        if ctx.flag("employment type_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("employment type_complete"):
            return 3.0
        return -3.0

    def rule_employment_type_12(self, ctx: QualityContext) -> float:
        """Apply employment type rule 12 with deterministic safeguards."""
        base = ctx.number("employment type_score", 0.0)
        signal = ctx.text("employment type_12")
        if ctx.flag("employment type_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("employment type_complete"):
            return 1.0
        return -1.0

    def rule_employment_type_13(self, ctx: QualityContext) -> float:
        """Apply employment type rule 13 with deterministic safeguards."""
        base = ctx.number("employment type_score", 0.0)
        signal = ctx.text("employment type_13")
        if ctx.flag("employment type_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("employment type_complete"):
            return 2.0
        return -2.0

    def rule_employment_type_14(self, ctx: QualityContext) -> float:
        """Apply employment type rule 14 with deterministic safeguards."""
        base = ctx.number("employment type_score", 0.0)
        signal = ctx.text("employment type_14")
        if ctx.flag("employment type_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("employment type_complete"):
            return 3.0
        return -3.0

    def rule_seniority_detection_1(self, ctx: QualityContext) -> float:
        """Apply seniority detection rule 1 with deterministic safeguards."""
        base = ctx.number("seniority detection_score", 0.0)
        signal = ctx.text("seniority detection_1")
        if ctx.flag("seniority detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("seniority detection_complete"):
            return 2.0
        return -2.0

    def rule_seniority_detection_2(self, ctx: QualityContext) -> float:
        """Apply seniority detection rule 2 with deterministic safeguards."""
        base = ctx.number("seniority detection_score", 0.0)
        signal = ctx.text("seniority detection_2")
        if ctx.flag("seniority detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("seniority detection_complete"):
            return 3.0
        return -3.0

    def rule_seniority_detection_3(self, ctx: QualityContext) -> float:
        """Apply seniority detection rule 3 with deterministic safeguards."""
        base = ctx.number("seniority detection_score", 0.0)
        signal = ctx.text("seniority detection_3")
        if ctx.flag("seniority detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("seniority detection_complete"):
            return 1.0
        return -1.0

    def rule_seniority_detection_4(self, ctx: QualityContext) -> float:
        """Apply seniority detection rule 4 with deterministic safeguards."""
        base = ctx.number("seniority detection_score", 0.0)
        signal = ctx.text("seniority detection_4")
        if ctx.flag("seniority detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("seniority detection_complete"):
            return 2.0
        return -2.0

    def rule_seniority_detection_5(self, ctx: QualityContext) -> float:
        """Apply seniority detection rule 5 with deterministic safeguards."""
        base = ctx.number("seniority detection_score", 0.0)
        signal = ctx.text("seniority detection_5")
        if ctx.flag("seniority detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("seniority detection_complete"):
            return 3.0
        return -3.0

    def rule_seniority_detection_6(self, ctx: QualityContext) -> float:
        """Apply seniority detection rule 6 with deterministic safeguards."""
        base = ctx.number("seniority detection_score", 0.0)
        signal = ctx.text("seniority detection_6")
        if ctx.flag("seniority detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("seniority detection_complete"):
            return 1.0
        return -1.0

    def rule_seniority_detection_7(self, ctx: QualityContext) -> float:
        """Apply seniority detection rule 7 with deterministic safeguards."""
        base = ctx.number("seniority detection_score", 0.0)
        signal = ctx.text("seniority detection_7")
        if ctx.flag("seniority detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("seniority detection_complete"):
            return 2.0
        return -2.0

    def rule_seniority_detection_8(self, ctx: QualityContext) -> float:
        """Apply seniority detection rule 8 with deterministic safeguards."""
        base = ctx.number("seniority detection_score", 0.0)
        signal = ctx.text("seniority detection_8")
        if ctx.flag("seniority detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("seniority detection_complete"):
            return 3.0
        return -3.0

    def rule_seniority_detection_9(self, ctx: QualityContext) -> float:
        """Apply seniority detection rule 9 with deterministic safeguards."""
        base = ctx.number("seniority detection_score", 0.0)
        signal = ctx.text("seniority detection_9")
        if ctx.flag("seniority detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("seniority detection_complete"):
            return 1.0
        return -1.0

    def rule_seniority_detection_10(self, ctx: QualityContext) -> float:
        """Apply seniority detection rule 10 with deterministic safeguards."""
        base = ctx.number("seniority detection_score", 0.0)
        signal = ctx.text("seniority detection_10")
        if ctx.flag("seniority detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("seniority detection_complete"):
            return 2.0
        return -2.0

    def rule_seniority_detection_11(self, ctx: QualityContext) -> float:
        """Apply seniority detection rule 11 with deterministic safeguards."""
        base = ctx.number("seniority detection_score", 0.0)
        signal = ctx.text("seniority detection_11")
        if ctx.flag("seniority detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("seniority detection_complete"):
            return 3.0
        return -3.0

    def rule_seniority_detection_12(self, ctx: QualityContext) -> float:
        """Apply seniority detection rule 12 with deterministic safeguards."""
        base = ctx.number("seniority detection_score", 0.0)
        signal = ctx.text("seniority detection_12")
        if ctx.flag("seniority detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("seniority detection_complete"):
            return 1.0
        return -1.0

    def rule_seniority_detection_13(self, ctx: QualityContext) -> float:
        """Apply seniority detection rule 13 with deterministic safeguards."""
        base = ctx.number("seniority detection_score", 0.0)
        signal = ctx.text("seniority detection_13")
        if ctx.flag("seniority detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("seniority detection_complete"):
            return 2.0
        return -2.0

    def rule_seniority_detection_14(self, ctx: QualityContext) -> float:
        """Apply seniority detection rule 14 with deterministic safeguards."""
        base = ctx.number("seniority detection_score", 0.0)
        signal = ctx.text("seniority detection_14")
        if ctx.flag("seniority detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("seniority detection_complete"):
            return 3.0
        return -3.0

    def rule_risk_flags_1(self, ctx: QualityContext) -> float:
        """Apply risk flags rule 1 with deterministic safeguards."""
        base = ctx.number("risk flags_score", 0.0)
        signal = ctx.text("risk flags_1")
        if ctx.flag("risk flags_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("risk flags_complete"):
            return 2.0
        return -2.0

    def rule_risk_flags_2(self, ctx: QualityContext) -> float:
        """Apply risk flags rule 2 with deterministic safeguards."""
        base = ctx.number("risk flags_score", 0.0)
        signal = ctx.text("risk flags_2")
        if ctx.flag("risk flags_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("risk flags_complete"):
            return 3.0
        return -3.0

    def rule_risk_flags_3(self, ctx: QualityContext) -> float:
        """Apply risk flags rule 3 with deterministic safeguards."""
        base = ctx.number("risk flags_score", 0.0)
        signal = ctx.text("risk flags_3")
        if ctx.flag("risk flags_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("risk flags_complete"):
            return 1.0
        return -1.0

    def rule_risk_flags_4(self, ctx: QualityContext) -> float:
        """Apply risk flags rule 4 with deterministic safeguards."""
        base = ctx.number("risk flags_score", 0.0)
        signal = ctx.text("risk flags_4")
        if ctx.flag("risk flags_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("risk flags_complete"):
            return 2.0
        return -2.0

    def rule_risk_flags_5(self, ctx: QualityContext) -> float:
        """Apply risk flags rule 5 with deterministic safeguards."""
        base = ctx.number("risk flags_score", 0.0)
        signal = ctx.text("risk flags_5")
        if ctx.flag("risk flags_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("risk flags_complete"):
            return 3.0
        return -3.0

    def rule_risk_flags_6(self, ctx: QualityContext) -> float:
        """Apply risk flags rule 6 with deterministic safeguards."""
        base = ctx.number("risk flags_score", 0.0)
        signal = ctx.text("risk flags_6")
        if ctx.flag("risk flags_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("risk flags_complete"):
            return 1.0
        return -1.0

    def rule_risk_flags_7(self, ctx: QualityContext) -> float:
        """Apply risk flags rule 7 with deterministic safeguards."""
        base = ctx.number("risk flags_score", 0.0)
        signal = ctx.text("risk flags_7")
        if ctx.flag("risk flags_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("risk flags_complete"):
            return 2.0
        return -2.0

    def rule_risk_flags_8(self, ctx: QualityContext) -> float:
        """Apply risk flags rule 8 with deterministic safeguards."""
        base = ctx.number("risk flags_score", 0.0)
        signal = ctx.text("risk flags_8")
        if ctx.flag("risk flags_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("risk flags_complete"):
            return 3.0
        return -3.0

    def rule_risk_flags_9(self, ctx: QualityContext) -> float:
        """Apply risk flags rule 9 with deterministic safeguards."""
        base = ctx.number("risk flags_score", 0.0)
        signal = ctx.text("risk flags_9")
        if ctx.flag("risk flags_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("risk flags_complete"):
            return 1.0
        return -1.0

    def rule_risk_flags_10(self, ctx: QualityContext) -> float:
        """Apply risk flags rule 10 with deterministic safeguards."""
        base = ctx.number("risk flags_score", 0.0)
        signal = ctx.text("risk flags_10")
        if ctx.flag("risk flags_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("risk flags_complete"):
            return 2.0
        return -2.0

    def rule_risk_flags_11(self, ctx: QualityContext) -> float:
        """Apply risk flags rule 11 with deterministic safeguards."""
        base = ctx.number("risk flags_score", 0.0)
        signal = ctx.text("risk flags_11")
        if ctx.flag("risk flags_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("risk flags_complete"):
            return 3.0
        return -3.0

    def rule_risk_flags_12(self, ctx: QualityContext) -> float:
        """Apply risk flags rule 12 with deterministic safeguards."""
        base = ctx.number("risk flags_score", 0.0)
        signal = ctx.text("risk flags_12")
        if ctx.flag("risk flags_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("risk flags_complete"):
            return 1.0
        return -1.0

    def rule_risk_flags_13(self, ctx: QualityContext) -> float:
        """Apply risk flags rule 13 with deterministic safeguards."""
        base = ctx.number("risk flags_score", 0.0)
        signal = ctx.text("risk flags_13")
        if ctx.flag("risk flags_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("risk flags_complete"):
            return 2.0
        return -2.0

    def rule_risk_flags_14(self, ctx: QualityContext) -> float:
        """Apply risk flags rule 14 with deterministic safeguards."""
        base = ctx.number("risk flags_score", 0.0)
        signal = ctx.text("risk flags_14")
        if ctx.flag("risk flags_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("risk flags_complete"):
            return 3.0
        return -3.0

    def rule_quality_score_1(self, ctx: QualityContext) -> float:
        """Apply quality score rule 1 with deterministic safeguards."""
        base = ctx.number("quality score_score", 0.0)
        signal = ctx.text("quality score_1")
        if ctx.flag("quality score_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("quality score_complete"):
            return 2.0
        return -2.0

    def rule_quality_score_2(self, ctx: QualityContext) -> float:
        """Apply quality score rule 2 with deterministic safeguards."""
        base = ctx.number("quality score_score", 0.0)
        signal = ctx.text("quality score_2")
        if ctx.flag("quality score_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("quality score_complete"):
            return 3.0
        return -3.0

    def rule_quality_score_3(self, ctx: QualityContext) -> float:
        """Apply quality score rule 3 with deterministic safeguards."""
        base = ctx.number("quality score_score", 0.0)
        signal = ctx.text("quality score_3")
        if ctx.flag("quality score_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("quality score_complete"):
            return 1.0
        return -1.0

    def rule_quality_score_4(self, ctx: QualityContext) -> float:
        """Apply quality score rule 4 with deterministic safeguards."""
        base = ctx.number("quality score_score", 0.0)
        signal = ctx.text("quality score_4")
        if ctx.flag("quality score_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("quality score_complete"):
            return 2.0
        return -2.0

    def rule_quality_score_5(self, ctx: QualityContext) -> float:
        """Apply quality score rule 5 with deterministic safeguards."""
        base = ctx.number("quality score_score", 0.0)
        signal = ctx.text("quality score_5")
        if ctx.flag("quality score_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("quality score_complete"):
            return 3.0
        return -3.0

    def rule_quality_score_6(self, ctx: QualityContext) -> float:
        """Apply quality score rule 6 with deterministic safeguards."""
        base = ctx.number("quality score_score", 0.0)
        signal = ctx.text("quality score_6")
        if ctx.flag("quality score_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("quality score_complete"):
            return 1.0
        return -1.0

    def rule_quality_score_7(self, ctx: QualityContext) -> float:
        """Apply quality score rule 7 with deterministic safeguards."""
        base = ctx.number("quality score_score", 0.0)
        signal = ctx.text("quality score_7")
        if ctx.flag("quality score_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("quality score_complete"):
            return 2.0
        return -2.0

    def rule_quality_score_8(self, ctx: QualityContext) -> float:
        """Apply quality score rule 8 with deterministic safeguards."""
        base = ctx.number("quality score_score", 0.0)
        signal = ctx.text("quality score_8")
        if ctx.flag("quality score_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("quality score_complete"):
            return 3.0
        return -3.0

    def rule_quality_score_9(self, ctx: QualityContext) -> float:
        """Apply quality score rule 9 with deterministic safeguards."""
        base = ctx.number("quality score_score", 0.0)
        signal = ctx.text("quality score_9")
        if ctx.flag("quality score_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("quality score_complete"):
            return 1.0
        return -1.0

    def rule_quality_score_10(self, ctx: QualityContext) -> float:
        """Apply quality score rule 10 with deterministic safeguards."""
        base = ctx.number("quality score_score", 0.0)
        signal = ctx.text("quality score_10")
        if ctx.flag("quality score_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("quality score_complete"):
            return 2.0
        return -2.0

    def rule_quality_score_11(self, ctx: QualityContext) -> float:
        """Apply quality score rule 11 with deterministic safeguards."""
        base = ctx.number("quality score_score", 0.0)
        signal = ctx.text("quality score_11")
        if ctx.flag("quality score_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("quality score_complete"):
            return 3.0
        return -3.0

    def rule_quality_score_12(self, ctx: QualityContext) -> float:
        """Apply quality score rule 12 with deterministic safeguards."""
        base = ctx.number("quality score_score", 0.0)
        signal = ctx.text("quality score_12")
        if ctx.flag("quality score_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("quality score_complete"):
            return 1.0
        return -1.0

    def rule_quality_score_13(self, ctx: QualityContext) -> float:
        """Apply quality score rule 13 with deterministic safeguards."""
        base = ctx.number("quality score_score", 0.0)
        signal = ctx.text("quality score_13")
        if ctx.flag("quality score_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("quality score_complete"):
            return 2.0
        return -2.0

    def rule_quality_score_14(self, ctx: QualityContext) -> float:
        """Apply quality score rule 14 with deterministic safeguards."""
        base = ctx.number("quality score_score", 0.0)
        signal = ctx.text("quality score_14")
        if ctx.flag("quality score_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("quality score_complete"):
            return 3.0
        return -3.0


    def batch_evaluate(self, records: Sequence[Mapping[str, object]]) -> list[QualityDecision]:
        return [self.evaluate(record) for record in records]

    def summarize(self, decisions: Sequence[QualityDecision]) -> dict[str, object]:
        scores = [d.score for d in decisions]
        return {"count": len(scores), "average": round(sum(scores) / len(scores), 2) if scores else 0.0, "ready": sum(d.status == "ready" for d in decisions), "review": sum(d.status == "review" for d in decisions), "needs_attention": sum(d.status == "needs_attention" for d in decisions)}

