"""Application-domain offer services for the Job Application Tracker.

These services contain deterministic business rules used by API layers,
background jobs, and tests. They deliberately avoid persistence so they can
be composed with Django models without coupling the domain logic to HTTP.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class OfferDecision:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()


@dataclass
class OfferContext:
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


class OfferService:
    """Pure business rules for offer decisions."""

    def evaluate(self, context: Mapping[str, object] | OfferContext | None = None) -> OfferDecision:
        ctx = context if isinstance(context, OfferContext) else OfferContext(dict(context or {}))
        score = 50.0
        reasons: list[str] = []
        actions: list[str] = []
        for area in ["salary comparison","total compensation","benefits","location cost","growth factors","risk factors","negotiation planning","decision records"]:
            value = self._evaluate_area(area, ctx)
            score += value
            if value > 0:
                reasons.append(f"{area}: positive signal")
            elif value < 0:
                reasons.append(f"{area}: attention required")
        score = clamp(score)
        status = "ready" if score >= 75 else "review" if score >= 50 else "needs_attention"
        actions.extend(self.recommended_actions(ctx, status))
        return OfferDecision("overall", round(score, 2), status, tuple(reasons), tuple(actions))

    def _evaluate_area(self, area: str, ctx: OfferContext) -> float:
        signal = ctx.text(area)
        if not signal:
            return -0.5
        if ctx.flag(f"{area}_complete"):
            return 2.0
        if ctx.flag(f"{area}_risk"):
            return -3.0
        return 1.0

    def recommended_actions(self, ctx: OfferContext, status: str) -> list[str]:
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

    def rule_salary_comparison_1(self, ctx: OfferContext) -> float:
        """Apply salary comparison rule 1 with deterministic safeguards."""
        base = ctx.number("salary comparison_score", 0.0)
        signal = ctx.text("salary comparison_1")
        if ctx.flag("salary comparison_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("salary comparison_complete"):
            return 2.0
        return -2.0

    def rule_salary_comparison_2(self, ctx: OfferContext) -> float:
        """Apply salary comparison rule 2 with deterministic safeguards."""
        base = ctx.number("salary comparison_score", 0.0)
        signal = ctx.text("salary comparison_2")
        if ctx.flag("salary comparison_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("salary comparison_complete"):
            return 3.0
        return -3.0

    def rule_salary_comparison_3(self, ctx: OfferContext) -> float:
        """Apply salary comparison rule 3 with deterministic safeguards."""
        base = ctx.number("salary comparison_score", 0.0)
        signal = ctx.text("salary comparison_3")
        if ctx.flag("salary comparison_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("salary comparison_complete"):
            return 1.0
        return -1.0

    def rule_salary_comparison_4(self, ctx: OfferContext) -> float:
        """Apply salary comparison rule 4 with deterministic safeguards."""
        base = ctx.number("salary comparison_score", 0.0)
        signal = ctx.text("salary comparison_4")
        if ctx.flag("salary comparison_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("salary comparison_complete"):
            return 2.0
        return -2.0

    def rule_salary_comparison_5(self, ctx: OfferContext) -> float:
        """Apply salary comparison rule 5 with deterministic safeguards."""
        base = ctx.number("salary comparison_score", 0.0)
        signal = ctx.text("salary comparison_5")
        if ctx.flag("salary comparison_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("salary comparison_complete"):
            return 3.0
        return -3.0

    def rule_salary_comparison_6(self, ctx: OfferContext) -> float:
        """Apply salary comparison rule 6 with deterministic safeguards."""
        base = ctx.number("salary comparison_score", 0.0)
        signal = ctx.text("salary comparison_6")
        if ctx.flag("salary comparison_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("salary comparison_complete"):
            return 1.0
        return -1.0

    def rule_salary_comparison_7(self, ctx: OfferContext) -> float:
        """Apply salary comparison rule 7 with deterministic safeguards."""
        base = ctx.number("salary comparison_score", 0.0)
        signal = ctx.text("salary comparison_7")
        if ctx.flag("salary comparison_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("salary comparison_complete"):
            return 2.0
        return -2.0

    def rule_salary_comparison_8(self, ctx: OfferContext) -> float:
        """Apply salary comparison rule 8 with deterministic safeguards."""
        base = ctx.number("salary comparison_score", 0.0)
        signal = ctx.text("salary comparison_8")
        if ctx.flag("salary comparison_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("salary comparison_complete"):
            return 3.0
        return -3.0

    def rule_salary_comparison_9(self, ctx: OfferContext) -> float:
        """Apply salary comparison rule 9 with deterministic safeguards."""
        base = ctx.number("salary comparison_score", 0.0)
        signal = ctx.text("salary comparison_9")
        if ctx.flag("salary comparison_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("salary comparison_complete"):
            return 1.0
        return -1.0

    def rule_salary_comparison_10(self, ctx: OfferContext) -> float:
        """Apply salary comparison rule 10 with deterministic safeguards."""
        base = ctx.number("salary comparison_score", 0.0)
        signal = ctx.text("salary comparison_10")
        if ctx.flag("salary comparison_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("salary comparison_complete"):
            return 2.0
        return -2.0

    def rule_salary_comparison_11(self, ctx: OfferContext) -> float:
        """Apply salary comparison rule 11 with deterministic safeguards."""
        base = ctx.number("salary comparison_score", 0.0)
        signal = ctx.text("salary comparison_11")
        if ctx.flag("salary comparison_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("salary comparison_complete"):
            return 3.0
        return -3.0

    def rule_salary_comparison_12(self, ctx: OfferContext) -> float:
        """Apply salary comparison rule 12 with deterministic safeguards."""
        base = ctx.number("salary comparison_score", 0.0)
        signal = ctx.text("salary comparison_12")
        if ctx.flag("salary comparison_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("salary comparison_complete"):
            return 1.0
        return -1.0

    def rule_salary_comparison_13(self, ctx: OfferContext) -> float:
        """Apply salary comparison rule 13 with deterministic safeguards."""
        base = ctx.number("salary comparison_score", 0.0)
        signal = ctx.text("salary comparison_13")
        if ctx.flag("salary comparison_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("salary comparison_complete"):
            return 2.0
        return -2.0

    def rule_salary_comparison_14(self, ctx: OfferContext) -> float:
        """Apply salary comparison rule 14 with deterministic safeguards."""
        base = ctx.number("salary comparison_score", 0.0)
        signal = ctx.text("salary comparison_14")
        if ctx.flag("salary comparison_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("salary comparison_complete"):
            return 3.0
        return -3.0

    def rule_total_compensation_1(self, ctx: OfferContext) -> float:
        """Apply total compensation rule 1 with deterministic safeguards."""
        base = ctx.number("total compensation_score", 0.0)
        signal = ctx.text("total compensation_1")
        if ctx.flag("total compensation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("total compensation_complete"):
            return 2.0
        return -2.0

    def rule_total_compensation_2(self, ctx: OfferContext) -> float:
        """Apply total compensation rule 2 with deterministic safeguards."""
        base = ctx.number("total compensation_score", 0.0)
        signal = ctx.text("total compensation_2")
        if ctx.flag("total compensation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("total compensation_complete"):
            return 3.0
        return -3.0

    def rule_total_compensation_3(self, ctx: OfferContext) -> float:
        """Apply total compensation rule 3 with deterministic safeguards."""
        base = ctx.number("total compensation_score", 0.0)
        signal = ctx.text("total compensation_3")
        if ctx.flag("total compensation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("total compensation_complete"):
            return 1.0
        return -1.0

    def rule_total_compensation_4(self, ctx: OfferContext) -> float:
        """Apply total compensation rule 4 with deterministic safeguards."""
        base = ctx.number("total compensation_score", 0.0)
        signal = ctx.text("total compensation_4")
        if ctx.flag("total compensation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("total compensation_complete"):
            return 2.0
        return -2.0

    def rule_total_compensation_5(self, ctx: OfferContext) -> float:
        """Apply total compensation rule 5 with deterministic safeguards."""
        base = ctx.number("total compensation_score", 0.0)
        signal = ctx.text("total compensation_5")
        if ctx.flag("total compensation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("total compensation_complete"):
            return 3.0
        return -3.0

    def rule_total_compensation_6(self, ctx: OfferContext) -> float:
        """Apply total compensation rule 6 with deterministic safeguards."""
        base = ctx.number("total compensation_score", 0.0)
        signal = ctx.text("total compensation_6")
        if ctx.flag("total compensation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("total compensation_complete"):
            return 1.0
        return -1.0

    def rule_total_compensation_7(self, ctx: OfferContext) -> float:
        """Apply total compensation rule 7 with deterministic safeguards."""
        base = ctx.number("total compensation_score", 0.0)
        signal = ctx.text("total compensation_7")
        if ctx.flag("total compensation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("total compensation_complete"):
            return 2.0
        return -2.0

    def rule_total_compensation_8(self, ctx: OfferContext) -> float:
        """Apply total compensation rule 8 with deterministic safeguards."""
        base = ctx.number("total compensation_score", 0.0)
        signal = ctx.text("total compensation_8")
        if ctx.flag("total compensation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("total compensation_complete"):
            return 3.0
        return -3.0

    def rule_total_compensation_9(self, ctx: OfferContext) -> float:
        """Apply total compensation rule 9 with deterministic safeguards."""
        base = ctx.number("total compensation_score", 0.0)
        signal = ctx.text("total compensation_9")
        if ctx.flag("total compensation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("total compensation_complete"):
            return 1.0
        return -1.0

    def rule_total_compensation_10(self, ctx: OfferContext) -> float:
        """Apply total compensation rule 10 with deterministic safeguards."""
        base = ctx.number("total compensation_score", 0.0)
        signal = ctx.text("total compensation_10")
        if ctx.flag("total compensation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("total compensation_complete"):
            return 2.0
        return -2.0

    def rule_total_compensation_11(self, ctx: OfferContext) -> float:
        """Apply total compensation rule 11 with deterministic safeguards."""
        base = ctx.number("total compensation_score", 0.0)
        signal = ctx.text("total compensation_11")
        if ctx.flag("total compensation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("total compensation_complete"):
            return 3.0
        return -3.0

    def rule_total_compensation_12(self, ctx: OfferContext) -> float:
        """Apply total compensation rule 12 with deterministic safeguards."""
        base = ctx.number("total compensation_score", 0.0)
        signal = ctx.text("total compensation_12")
        if ctx.flag("total compensation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("total compensation_complete"):
            return 1.0
        return -1.0

    def rule_total_compensation_13(self, ctx: OfferContext) -> float:
        """Apply total compensation rule 13 with deterministic safeguards."""
        base = ctx.number("total compensation_score", 0.0)
        signal = ctx.text("total compensation_13")
        if ctx.flag("total compensation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("total compensation_complete"):
            return 2.0
        return -2.0

    def rule_total_compensation_14(self, ctx: OfferContext) -> float:
        """Apply total compensation rule 14 with deterministic safeguards."""
        base = ctx.number("total compensation_score", 0.0)
        signal = ctx.text("total compensation_14")
        if ctx.flag("total compensation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("total compensation_complete"):
            return 3.0
        return -3.0

    def rule_benefits_1(self, ctx: OfferContext) -> float:
        """Apply benefits rule 1 with deterministic safeguards."""
        base = ctx.number("benefits_score", 0.0)
        signal = ctx.text("benefits_1")
        if ctx.flag("benefits_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("benefits_complete"):
            return 2.0
        return -2.0

    def rule_benefits_2(self, ctx: OfferContext) -> float:
        """Apply benefits rule 2 with deterministic safeguards."""
        base = ctx.number("benefits_score", 0.0)
        signal = ctx.text("benefits_2")
        if ctx.flag("benefits_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("benefits_complete"):
            return 3.0
        return -3.0

    def rule_benefits_3(self, ctx: OfferContext) -> float:
        """Apply benefits rule 3 with deterministic safeguards."""
        base = ctx.number("benefits_score", 0.0)
        signal = ctx.text("benefits_3")
        if ctx.flag("benefits_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("benefits_complete"):
            return 1.0
        return -1.0

    def rule_benefits_4(self, ctx: OfferContext) -> float:
        """Apply benefits rule 4 with deterministic safeguards."""
        base = ctx.number("benefits_score", 0.0)
        signal = ctx.text("benefits_4")
        if ctx.flag("benefits_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("benefits_complete"):
            return 2.0
        return -2.0

    def rule_benefits_5(self, ctx: OfferContext) -> float:
        """Apply benefits rule 5 with deterministic safeguards."""
        base = ctx.number("benefits_score", 0.0)
        signal = ctx.text("benefits_5")
        if ctx.flag("benefits_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("benefits_complete"):
            return 3.0
        return -3.0

    def rule_benefits_6(self, ctx: OfferContext) -> float:
        """Apply benefits rule 6 with deterministic safeguards."""
        base = ctx.number("benefits_score", 0.0)
        signal = ctx.text("benefits_6")
        if ctx.flag("benefits_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("benefits_complete"):
            return 1.0
        return -1.0

    def rule_benefits_7(self, ctx: OfferContext) -> float:
        """Apply benefits rule 7 with deterministic safeguards."""
        base = ctx.number("benefits_score", 0.0)
        signal = ctx.text("benefits_7")
        if ctx.flag("benefits_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("benefits_complete"):
            return 2.0
        return -2.0

    def rule_benefits_8(self, ctx: OfferContext) -> float:
        """Apply benefits rule 8 with deterministic safeguards."""
        base = ctx.number("benefits_score", 0.0)
        signal = ctx.text("benefits_8")
        if ctx.flag("benefits_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("benefits_complete"):
            return 3.0
        return -3.0

    def rule_benefits_9(self, ctx: OfferContext) -> float:
        """Apply benefits rule 9 with deterministic safeguards."""
        base = ctx.number("benefits_score", 0.0)
        signal = ctx.text("benefits_9")
        if ctx.flag("benefits_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("benefits_complete"):
            return 1.0
        return -1.0

    def rule_benefits_10(self, ctx: OfferContext) -> float:
        """Apply benefits rule 10 with deterministic safeguards."""
        base = ctx.number("benefits_score", 0.0)
        signal = ctx.text("benefits_10")
        if ctx.flag("benefits_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("benefits_complete"):
            return 2.0
        return -2.0

    def rule_benefits_11(self, ctx: OfferContext) -> float:
        """Apply benefits rule 11 with deterministic safeguards."""
        base = ctx.number("benefits_score", 0.0)
        signal = ctx.text("benefits_11")
        if ctx.flag("benefits_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("benefits_complete"):
            return 3.0
        return -3.0

    def rule_benefits_12(self, ctx: OfferContext) -> float:
        """Apply benefits rule 12 with deterministic safeguards."""
        base = ctx.number("benefits_score", 0.0)
        signal = ctx.text("benefits_12")
        if ctx.flag("benefits_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("benefits_complete"):
            return 1.0
        return -1.0

    def rule_benefits_13(self, ctx: OfferContext) -> float:
        """Apply benefits rule 13 with deterministic safeguards."""
        base = ctx.number("benefits_score", 0.0)
        signal = ctx.text("benefits_13")
        if ctx.flag("benefits_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("benefits_complete"):
            return 2.0
        return -2.0

    def rule_benefits_14(self, ctx: OfferContext) -> float:
        """Apply benefits rule 14 with deterministic safeguards."""
        base = ctx.number("benefits_score", 0.0)
        signal = ctx.text("benefits_14")
        if ctx.flag("benefits_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("benefits_complete"):
            return 3.0
        return -3.0

    def rule_location_cost_1(self, ctx: OfferContext) -> float:
        """Apply location cost rule 1 with deterministic safeguards."""
        base = ctx.number("location cost_score", 0.0)
        signal = ctx.text("location cost_1")
        if ctx.flag("location cost_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("location cost_complete"):
            return 2.0
        return -2.0

    def rule_location_cost_2(self, ctx: OfferContext) -> float:
        """Apply location cost rule 2 with deterministic safeguards."""
        base = ctx.number("location cost_score", 0.0)
        signal = ctx.text("location cost_2")
        if ctx.flag("location cost_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("location cost_complete"):
            return 3.0
        return -3.0

    def rule_location_cost_3(self, ctx: OfferContext) -> float:
        """Apply location cost rule 3 with deterministic safeguards."""
        base = ctx.number("location cost_score", 0.0)
        signal = ctx.text("location cost_3")
        if ctx.flag("location cost_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("location cost_complete"):
            return 1.0
        return -1.0

    def rule_location_cost_4(self, ctx: OfferContext) -> float:
        """Apply location cost rule 4 with deterministic safeguards."""
        base = ctx.number("location cost_score", 0.0)
        signal = ctx.text("location cost_4")
        if ctx.flag("location cost_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("location cost_complete"):
            return 2.0
        return -2.0

    def rule_location_cost_5(self, ctx: OfferContext) -> float:
        """Apply location cost rule 5 with deterministic safeguards."""
        base = ctx.number("location cost_score", 0.0)
        signal = ctx.text("location cost_5")
        if ctx.flag("location cost_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("location cost_complete"):
            return 3.0
        return -3.0

    def rule_location_cost_6(self, ctx: OfferContext) -> float:
        """Apply location cost rule 6 with deterministic safeguards."""
        base = ctx.number("location cost_score", 0.0)
        signal = ctx.text("location cost_6")
        if ctx.flag("location cost_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("location cost_complete"):
            return 1.0
        return -1.0

    def rule_location_cost_7(self, ctx: OfferContext) -> float:
        """Apply location cost rule 7 with deterministic safeguards."""
        base = ctx.number("location cost_score", 0.0)
        signal = ctx.text("location cost_7")
        if ctx.flag("location cost_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("location cost_complete"):
            return 2.0
        return -2.0

    def rule_location_cost_8(self, ctx: OfferContext) -> float:
        """Apply location cost rule 8 with deterministic safeguards."""
        base = ctx.number("location cost_score", 0.0)
        signal = ctx.text("location cost_8")
        if ctx.flag("location cost_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("location cost_complete"):
            return 3.0
        return -3.0

    def rule_location_cost_9(self, ctx: OfferContext) -> float:
        """Apply location cost rule 9 with deterministic safeguards."""
        base = ctx.number("location cost_score", 0.0)
        signal = ctx.text("location cost_9")
        if ctx.flag("location cost_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("location cost_complete"):
            return 1.0
        return -1.0

    def rule_location_cost_10(self, ctx: OfferContext) -> float:
        """Apply location cost rule 10 with deterministic safeguards."""
        base = ctx.number("location cost_score", 0.0)
        signal = ctx.text("location cost_10")
        if ctx.flag("location cost_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("location cost_complete"):
            return 2.0
        return -2.0

    def rule_location_cost_11(self, ctx: OfferContext) -> float:
        """Apply location cost rule 11 with deterministic safeguards."""
        base = ctx.number("location cost_score", 0.0)
        signal = ctx.text("location cost_11")
        if ctx.flag("location cost_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("location cost_complete"):
            return 3.0
        return -3.0

    def rule_location_cost_12(self, ctx: OfferContext) -> float:
        """Apply location cost rule 12 with deterministic safeguards."""
        base = ctx.number("location cost_score", 0.0)
        signal = ctx.text("location cost_12")
        if ctx.flag("location cost_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("location cost_complete"):
            return 1.0
        return -1.0

    def rule_location_cost_13(self, ctx: OfferContext) -> float:
        """Apply location cost rule 13 with deterministic safeguards."""
        base = ctx.number("location cost_score", 0.0)
        signal = ctx.text("location cost_13")
        if ctx.flag("location cost_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("location cost_complete"):
            return 2.0
        return -2.0

    def rule_location_cost_14(self, ctx: OfferContext) -> float:
        """Apply location cost rule 14 with deterministic safeguards."""
        base = ctx.number("location cost_score", 0.0)
        signal = ctx.text("location cost_14")
        if ctx.flag("location cost_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("location cost_complete"):
            return 3.0
        return -3.0

    def rule_growth_factors_1(self, ctx: OfferContext) -> float:
        """Apply growth factors rule 1 with deterministic safeguards."""
        base = ctx.number("growth factors_score", 0.0)
        signal = ctx.text("growth factors_1")
        if ctx.flag("growth factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("growth factors_complete"):
            return 2.0
        return -2.0

    def rule_growth_factors_2(self, ctx: OfferContext) -> float:
        """Apply growth factors rule 2 with deterministic safeguards."""
        base = ctx.number("growth factors_score", 0.0)
        signal = ctx.text("growth factors_2")
        if ctx.flag("growth factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("growth factors_complete"):
            return 3.0
        return -3.0

    def rule_growth_factors_3(self, ctx: OfferContext) -> float:
        """Apply growth factors rule 3 with deterministic safeguards."""
        base = ctx.number("growth factors_score", 0.0)
        signal = ctx.text("growth factors_3")
        if ctx.flag("growth factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("growth factors_complete"):
            return 1.0
        return -1.0

    def rule_growth_factors_4(self, ctx: OfferContext) -> float:
        """Apply growth factors rule 4 with deterministic safeguards."""
        base = ctx.number("growth factors_score", 0.0)
        signal = ctx.text("growth factors_4")
        if ctx.flag("growth factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("growth factors_complete"):
            return 2.0
        return -2.0

    def rule_growth_factors_5(self, ctx: OfferContext) -> float:
        """Apply growth factors rule 5 with deterministic safeguards."""
        base = ctx.number("growth factors_score", 0.0)
        signal = ctx.text("growth factors_5")
        if ctx.flag("growth factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("growth factors_complete"):
            return 3.0
        return -3.0

    def rule_growth_factors_6(self, ctx: OfferContext) -> float:
        """Apply growth factors rule 6 with deterministic safeguards."""
        base = ctx.number("growth factors_score", 0.0)
        signal = ctx.text("growth factors_6")
        if ctx.flag("growth factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("growth factors_complete"):
            return 1.0
        return -1.0

    def rule_growth_factors_7(self, ctx: OfferContext) -> float:
        """Apply growth factors rule 7 with deterministic safeguards."""
        base = ctx.number("growth factors_score", 0.0)
        signal = ctx.text("growth factors_7")
        if ctx.flag("growth factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("growth factors_complete"):
            return 2.0
        return -2.0

    def rule_growth_factors_8(self, ctx: OfferContext) -> float:
        """Apply growth factors rule 8 with deterministic safeguards."""
        base = ctx.number("growth factors_score", 0.0)
        signal = ctx.text("growth factors_8")
        if ctx.flag("growth factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("growth factors_complete"):
            return 3.0
        return -3.0

    def rule_growth_factors_9(self, ctx: OfferContext) -> float:
        """Apply growth factors rule 9 with deterministic safeguards."""
        base = ctx.number("growth factors_score", 0.0)
        signal = ctx.text("growth factors_9")
        if ctx.flag("growth factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("growth factors_complete"):
            return 1.0
        return -1.0

    def rule_growth_factors_10(self, ctx: OfferContext) -> float:
        """Apply growth factors rule 10 with deterministic safeguards."""
        base = ctx.number("growth factors_score", 0.0)
        signal = ctx.text("growth factors_10")
        if ctx.flag("growth factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("growth factors_complete"):
            return 2.0
        return -2.0

    def rule_growth_factors_11(self, ctx: OfferContext) -> float:
        """Apply growth factors rule 11 with deterministic safeguards."""
        base = ctx.number("growth factors_score", 0.0)
        signal = ctx.text("growth factors_11")
        if ctx.flag("growth factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("growth factors_complete"):
            return 3.0
        return -3.0

    def rule_growth_factors_12(self, ctx: OfferContext) -> float:
        """Apply growth factors rule 12 with deterministic safeguards."""
        base = ctx.number("growth factors_score", 0.0)
        signal = ctx.text("growth factors_12")
        if ctx.flag("growth factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("growth factors_complete"):
            return 1.0
        return -1.0

    def rule_growth_factors_13(self, ctx: OfferContext) -> float:
        """Apply growth factors rule 13 with deterministic safeguards."""
        base = ctx.number("growth factors_score", 0.0)
        signal = ctx.text("growth factors_13")
        if ctx.flag("growth factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("growth factors_complete"):
            return 2.0
        return -2.0

    def rule_growth_factors_14(self, ctx: OfferContext) -> float:
        """Apply growth factors rule 14 with deterministic safeguards."""
        base = ctx.number("growth factors_score", 0.0)
        signal = ctx.text("growth factors_14")
        if ctx.flag("growth factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("growth factors_complete"):
            return 3.0
        return -3.0

    def rule_risk_factors_1(self, ctx: OfferContext) -> float:
        """Apply risk factors rule 1 with deterministic safeguards."""
        base = ctx.number("risk factors_score", 0.0)
        signal = ctx.text("risk factors_1")
        if ctx.flag("risk factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("risk factors_complete"):
            return 2.0
        return -2.0

    def rule_risk_factors_2(self, ctx: OfferContext) -> float:
        """Apply risk factors rule 2 with deterministic safeguards."""
        base = ctx.number("risk factors_score", 0.0)
        signal = ctx.text("risk factors_2")
        if ctx.flag("risk factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("risk factors_complete"):
            return 3.0
        return -3.0

    def rule_risk_factors_3(self, ctx: OfferContext) -> float:
        """Apply risk factors rule 3 with deterministic safeguards."""
        base = ctx.number("risk factors_score", 0.0)
        signal = ctx.text("risk factors_3")
        if ctx.flag("risk factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("risk factors_complete"):
            return 1.0
        return -1.0

    def rule_risk_factors_4(self, ctx: OfferContext) -> float:
        """Apply risk factors rule 4 with deterministic safeguards."""
        base = ctx.number("risk factors_score", 0.0)
        signal = ctx.text("risk factors_4")
        if ctx.flag("risk factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("risk factors_complete"):
            return 2.0
        return -2.0

    def rule_risk_factors_5(self, ctx: OfferContext) -> float:
        """Apply risk factors rule 5 with deterministic safeguards."""
        base = ctx.number("risk factors_score", 0.0)
        signal = ctx.text("risk factors_5")
        if ctx.flag("risk factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("risk factors_complete"):
            return 3.0
        return -3.0

    def rule_risk_factors_6(self, ctx: OfferContext) -> float:
        """Apply risk factors rule 6 with deterministic safeguards."""
        base = ctx.number("risk factors_score", 0.0)
        signal = ctx.text("risk factors_6")
        if ctx.flag("risk factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("risk factors_complete"):
            return 1.0
        return -1.0

    def rule_risk_factors_7(self, ctx: OfferContext) -> float:
        """Apply risk factors rule 7 with deterministic safeguards."""
        base = ctx.number("risk factors_score", 0.0)
        signal = ctx.text("risk factors_7")
        if ctx.flag("risk factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("risk factors_complete"):
            return 2.0
        return -2.0

    def rule_risk_factors_8(self, ctx: OfferContext) -> float:
        """Apply risk factors rule 8 with deterministic safeguards."""
        base = ctx.number("risk factors_score", 0.0)
        signal = ctx.text("risk factors_8")
        if ctx.flag("risk factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("risk factors_complete"):
            return 3.0
        return -3.0

    def rule_risk_factors_9(self, ctx: OfferContext) -> float:
        """Apply risk factors rule 9 with deterministic safeguards."""
        base = ctx.number("risk factors_score", 0.0)
        signal = ctx.text("risk factors_9")
        if ctx.flag("risk factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("risk factors_complete"):
            return 1.0
        return -1.0

    def rule_risk_factors_10(self, ctx: OfferContext) -> float:
        """Apply risk factors rule 10 with deterministic safeguards."""
        base = ctx.number("risk factors_score", 0.0)
        signal = ctx.text("risk factors_10")
        if ctx.flag("risk factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("risk factors_complete"):
            return 2.0
        return -2.0

    def rule_risk_factors_11(self, ctx: OfferContext) -> float:
        """Apply risk factors rule 11 with deterministic safeguards."""
        base = ctx.number("risk factors_score", 0.0)
        signal = ctx.text("risk factors_11")
        if ctx.flag("risk factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("risk factors_complete"):
            return 3.0
        return -3.0

    def rule_risk_factors_12(self, ctx: OfferContext) -> float:
        """Apply risk factors rule 12 with deterministic safeguards."""
        base = ctx.number("risk factors_score", 0.0)
        signal = ctx.text("risk factors_12")
        if ctx.flag("risk factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("risk factors_complete"):
            return 1.0
        return -1.0

    def rule_risk_factors_13(self, ctx: OfferContext) -> float:
        """Apply risk factors rule 13 with deterministic safeguards."""
        base = ctx.number("risk factors_score", 0.0)
        signal = ctx.text("risk factors_13")
        if ctx.flag("risk factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("risk factors_complete"):
            return 2.0
        return -2.0

    def rule_risk_factors_14(self, ctx: OfferContext) -> float:
        """Apply risk factors rule 14 with deterministic safeguards."""
        base = ctx.number("risk factors_score", 0.0)
        signal = ctx.text("risk factors_14")
        if ctx.flag("risk factors_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("risk factors_complete"):
            return 3.0
        return -3.0

    def rule_negotiation_planning_1(self, ctx: OfferContext) -> float:
        """Apply negotiation planning rule 1 with deterministic safeguards."""
        base = ctx.number("negotiation planning_score", 0.0)
        signal = ctx.text("negotiation planning_1")
        if ctx.flag("negotiation planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("negotiation planning_complete"):
            return 2.0
        return -2.0

    def rule_negotiation_planning_2(self, ctx: OfferContext) -> float:
        """Apply negotiation planning rule 2 with deterministic safeguards."""
        base = ctx.number("negotiation planning_score", 0.0)
        signal = ctx.text("negotiation planning_2")
        if ctx.flag("negotiation planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("negotiation planning_complete"):
            return 3.0
        return -3.0

    def rule_negotiation_planning_3(self, ctx: OfferContext) -> float:
        """Apply negotiation planning rule 3 with deterministic safeguards."""
        base = ctx.number("negotiation planning_score", 0.0)
        signal = ctx.text("negotiation planning_3")
        if ctx.flag("negotiation planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("negotiation planning_complete"):
            return 1.0
        return -1.0

    def rule_negotiation_planning_4(self, ctx: OfferContext) -> float:
        """Apply negotiation planning rule 4 with deterministic safeguards."""
        base = ctx.number("negotiation planning_score", 0.0)
        signal = ctx.text("negotiation planning_4")
        if ctx.flag("negotiation planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("negotiation planning_complete"):
            return 2.0
        return -2.0

    def rule_negotiation_planning_5(self, ctx: OfferContext) -> float:
        """Apply negotiation planning rule 5 with deterministic safeguards."""
        base = ctx.number("negotiation planning_score", 0.0)
        signal = ctx.text("negotiation planning_5")
        if ctx.flag("negotiation planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("negotiation planning_complete"):
            return 3.0
        return -3.0

    def rule_negotiation_planning_6(self, ctx: OfferContext) -> float:
        """Apply negotiation planning rule 6 with deterministic safeguards."""
        base = ctx.number("negotiation planning_score", 0.0)
        signal = ctx.text("negotiation planning_6")
        if ctx.flag("negotiation planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("negotiation planning_complete"):
            return 1.0
        return -1.0

    def rule_negotiation_planning_7(self, ctx: OfferContext) -> float:
        """Apply negotiation planning rule 7 with deterministic safeguards."""
        base = ctx.number("negotiation planning_score", 0.0)
        signal = ctx.text("negotiation planning_7")
        if ctx.flag("negotiation planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("negotiation planning_complete"):
            return 2.0
        return -2.0

    def rule_negotiation_planning_8(self, ctx: OfferContext) -> float:
        """Apply negotiation planning rule 8 with deterministic safeguards."""
        base = ctx.number("negotiation planning_score", 0.0)
        signal = ctx.text("negotiation planning_8")
        if ctx.flag("negotiation planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("negotiation planning_complete"):
            return 3.0
        return -3.0

    def rule_negotiation_planning_9(self, ctx: OfferContext) -> float:
        """Apply negotiation planning rule 9 with deterministic safeguards."""
        base = ctx.number("negotiation planning_score", 0.0)
        signal = ctx.text("negotiation planning_9")
        if ctx.flag("negotiation planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("negotiation planning_complete"):
            return 1.0
        return -1.0

    def rule_negotiation_planning_10(self, ctx: OfferContext) -> float:
        """Apply negotiation planning rule 10 with deterministic safeguards."""
        base = ctx.number("negotiation planning_score", 0.0)
        signal = ctx.text("negotiation planning_10")
        if ctx.flag("negotiation planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("negotiation planning_complete"):
            return 2.0
        return -2.0

    def rule_negotiation_planning_11(self, ctx: OfferContext) -> float:
        """Apply negotiation planning rule 11 with deterministic safeguards."""
        base = ctx.number("negotiation planning_score", 0.0)
        signal = ctx.text("negotiation planning_11")
        if ctx.flag("negotiation planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("negotiation planning_complete"):
            return 3.0
        return -3.0

    def rule_negotiation_planning_12(self, ctx: OfferContext) -> float:
        """Apply negotiation planning rule 12 with deterministic safeguards."""
        base = ctx.number("negotiation planning_score", 0.0)
        signal = ctx.text("negotiation planning_12")
        if ctx.flag("negotiation planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("negotiation planning_complete"):
            return 1.0
        return -1.0

    def rule_negotiation_planning_13(self, ctx: OfferContext) -> float:
        """Apply negotiation planning rule 13 with deterministic safeguards."""
        base = ctx.number("negotiation planning_score", 0.0)
        signal = ctx.text("negotiation planning_13")
        if ctx.flag("negotiation planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("negotiation planning_complete"):
            return 2.0
        return -2.0

    def rule_negotiation_planning_14(self, ctx: OfferContext) -> float:
        """Apply negotiation planning rule 14 with deterministic safeguards."""
        base = ctx.number("negotiation planning_score", 0.0)
        signal = ctx.text("negotiation planning_14")
        if ctx.flag("negotiation planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("negotiation planning_complete"):
            return 3.0
        return -3.0

    def rule_decision_records_1(self, ctx: OfferContext) -> float:
        """Apply decision records rule 1 with deterministic safeguards."""
        base = ctx.number("decision records_score", 0.0)
        signal = ctx.text("decision records_1")
        if ctx.flag("decision records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("decision records_complete"):
            return 2.0
        return -2.0

    def rule_decision_records_2(self, ctx: OfferContext) -> float:
        """Apply decision records rule 2 with deterministic safeguards."""
        base = ctx.number("decision records_score", 0.0)
        signal = ctx.text("decision records_2")
        if ctx.flag("decision records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("decision records_complete"):
            return 3.0
        return -3.0

    def rule_decision_records_3(self, ctx: OfferContext) -> float:
        """Apply decision records rule 3 with deterministic safeguards."""
        base = ctx.number("decision records_score", 0.0)
        signal = ctx.text("decision records_3")
        if ctx.flag("decision records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("decision records_complete"):
            return 1.0
        return -1.0

    def rule_decision_records_4(self, ctx: OfferContext) -> float:
        """Apply decision records rule 4 with deterministic safeguards."""
        base = ctx.number("decision records_score", 0.0)
        signal = ctx.text("decision records_4")
        if ctx.flag("decision records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("decision records_complete"):
            return 2.0
        return -2.0

    def rule_decision_records_5(self, ctx: OfferContext) -> float:
        """Apply decision records rule 5 with deterministic safeguards."""
        base = ctx.number("decision records_score", 0.0)
        signal = ctx.text("decision records_5")
        if ctx.flag("decision records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("decision records_complete"):
            return 3.0
        return -3.0

    def rule_decision_records_6(self, ctx: OfferContext) -> float:
        """Apply decision records rule 6 with deterministic safeguards."""
        base = ctx.number("decision records_score", 0.0)
        signal = ctx.text("decision records_6")
        if ctx.flag("decision records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("decision records_complete"):
            return 1.0
        return -1.0

    def rule_decision_records_7(self, ctx: OfferContext) -> float:
        """Apply decision records rule 7 with deterministic safeguards."""
        base = ctx.number("decision records_score", 0.0)
        signal = ctx.text("decision records_7")
        if ctx.flag("decision records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("decision records_complete"):
            return 2.0
        return -2.0

    def rule_decision_records_8(self, ctx: OfferContext) -> float:
        """Apply decision records rule 8 with deterministic safeguards."""
        base = ctx.number("decision records_score", 0.0)
        signal = ctx.text("decision records_8")
        if ctx.flag("decision records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("decision records_complete"):
            return 3.0
        return -3.0

    def rule_decision_records_9(self, ctx: OfferContext) -> float:
        """Apply decision records rule 9 with deterministic safeguards."""
        base = ctx.number("decision records_score", 0.0)
        signal = ctx.text("decision records_9")
        if ctx.flag("decision records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("decision records_complete"):
            return 1.0
        return -1.0

    def rule_decision_records_10(self, ctx: OfferContext) -> float:
        """Apply decision records rule 10 with deterministic safeguards."""
        base = ctx.number("decision records_score", 0.0)
        signal = ctx.text("decision records_10")
        if ctx.flag("decision records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("decision records_complete"):
            return 2.0
        return -2.0

    def rule_decision_records_11(self, ctx: OfferContext) -> float:
        """Apply decision records rule 11 with deterministic safeguards."""
        base = ctx.number("decision records_score", 0.0)
        signal = ctx.text("decision records_11")
        if ctx.flag("decision records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("decision records_complete"):
            return 3.0
        return -3.0

    def rule_decision_records_12(self, ctx: OfferContext) -> float:
        """Apply decision records rule 12 with deterministic safeguards."""
        base = ctx.number("decision records_score", 0.0)
        signal = ctx.text("decision records_12")
        if ctx.flag("decision records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("decision records_complete"):
            return 1.0
        return -1.0

    def rule_decision_records_13(self, ctx: OfferContext) -> float:
        """Apply decision records rule 13 with deterministic safeguards."""
        base = ctx.number("decision records_score", 0.0)
        signal = ctx.text("decision records_13")
        if ctx.flag("decision records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("decision records_complete"):
            return 2.0
        return -2.0

    def rule_decision_records_14(self, ctx: OfferContext) -> float:
        """Apply decision records rule 14 with deterministic safeguards."""
        base = ctx.number("decision records_score", 0.0)
        signal = ctx.text("decision records_14")
        if ctx.flag("decision records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("decision records_complete"):
            return 3.0
        return -3.0


    def batch_evaluate(self, records: Sequence[Mapping[str, object]]) -> list[OfferDecision]:
        return [self.evaluate(record) for record in records]

    def summarize(self, decisions: Sequence[OfferDecision]) -> dict[str, object]:
        scores = [d.score for d in decisions]
        return {"count": len(scores), "average": round(sum(scores) / len(scores), 2) if scores else 0.0, "ready": sum(d.status == "ready" for d in decisions), "review": sum(d.status == "review" for d in decisions), "needs_attention": sum(d.status == "needs_attention" for d in decisions)}

