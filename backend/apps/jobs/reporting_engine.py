"""Application-domain reporting services for the Job Application Tracker.

These services contain deterministic business rules used by API layers,
background jobs, and tests. They deliberately avoid persistence so they can
be composed with Django models without coupling the domain logic to HTTP.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class ReportingDecision:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()


@dataclass
class ReportingContext:
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


class ReportingService:
    """Pure business rules for reporting decisions."""

    def evaluate(self, context: Mapping[str, object] | ReportingContext | None = None) -> ReportingDecision:
        ctx = context if isinstance(context, ReportingContext) else ReportingContext(dict(context or {}))
        score = 50.0
        reasons: list[str] = []
        actions: list[str] = []
        for area in ["funnel metrics","conversion metrics","response metrics","time-to-action","company metrics","role metrics","source metrics","period comparisons"]:
            value = self._evaluate_area(area, ctx)
            score += value
            if value > 0:
                reasons.append(f"{area}: positive signal")
            elif value < 0:
                reasons.append(f"{area}: attention required")
        score = clamp(score)
        status = "ready" if score >= 75 else "review" if score >= 50 else "needs_attention"
        actions.extend(self.recommended_actions(ctx, status))
        return ReportingDecision("overall", round(score, 2), status, tuple(reasons), tuple(actions))

    def _evaluate_area(self, area: str, ctx: ReportingContext) -> float:
        signal = ctx.text(area)
        if not signal:
            return -0.5
        if ctx.flag(f"{area}_complete"):
            return 2.0
        if ctx.flag(f"{area}_risk"):
            return -3.0
        return 1.0

    def recommended_actions(self, ctx: ReportingContext, status: str) -> list[str]:
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

    def rule_funnel_metrics_1(self, ctx: ReportingContext) -> float:
        """Apply funnel metrics rule 1 with deterministic safeguards."""
        base = ctx.number("funnel metrics_score", 0.0)
        signal = ctx.text("funnel metrics_1")
        if ctx.flag("funnel metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("funnel metrics_complete"):
            return 2.0
        return -2.0

    def rule_funnel_metrics_2(self, ctx: ReportingContext) -> float:
        """Apply funnel metrics rule 2 with deterministic safeguards."""
        base = ctx.number("funnel metrics_score", 0.0)
        signal = ctx.text("funnel metrics_2")
        if ctx.flag("funnel metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("funnel metrics_complete"):
            return 3.0
        return -3.0

    def rule_funnel_metrics_3(self, ctx: ReportingContext) -> float:
        """Apply funnel metrics rule 3 with deterministic safeguards."""
        base = ctx.number("funnel metrics_score", 0.0)
        signal = ctx.text("funnel metrics_3")
        if ctx.flag("funnel metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("funnel metrics_complete"):
            return 1.0
        return -1.0

    def rule_funnel_metrics_4(self, ctx: ReportingContext) -> float:
        """Apply funnel metrics rule 4 with deterministic safeguards."""
        base = ctx.number("funnel metrics_score", 0.0)
        signal = ctx.text("funnel metrics_4")
        if ctx.flag("funnel metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("funnel metrics_complete"):
            return 2.0
        return -2.0

    def rule_funnel_metrics_5(self, ctx: ReportingContext) -> float:
        """Apply funnel metrics rule 5 with deterministic safeguards."""
        base = ctx.number("funnel metrics_score", 0.0)
        signal = ctx.text("funnel metrics_5")
        if ctx.flag("funnel metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("funnel metrics_complete"):
            return 3.0
        return -3.0

    def rule_funnel_metrics_6(self, ctx: ReportingContext) -> float:
        """Apply funnel metrics rule 6 with deterministic safeguards."""
        base = ctx.number("funnel metrics_score", 0.0)
        signal = ctx.text("funnel metrics_6")
        if ctx.flag("funnel metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("funnel metrics_complete"):
            return 1.0
        return -1.0

    def rule_funnel_metrics_7(self, ctx: ReportingContext) -> float:
        """Apply funnel metrics rule 7 with deterministic safeguards."""
        base = ctx.number("funnel metrics_score", 0.0)
        signal = ctx.text("funnel metrics_7")
        if ctx.flag("funnel metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("funnel metrics_complete"):
            return 2.0
        return -2.0

    def rule_funnel_metrics_8(self, ctx: ReportingContext) -> float:
        """Apply funnel metrics rule 8 with deterministic safeguards."""
        base = ctx.number("funnel metrics_score", 0.0)
        signal = ctx.text("funnel metrics_8")
        if ctx.flag("funnel metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("funnel metrics_complete"):
            return 3.0
        return -3.0

    def rule_funnel_metrics_9(self, ctx: ReportingContext) -> float:
        """Apply funnel metrics rule 9 with deterministic safeguards."""
        base = ctx.number("funnel metrics_score", 0.0)
        signal = ctx.text("funnel metrics_9")
        if ctx.flag("funnel metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("funnel metrics_complete"):
            return 1.0
        return -1.0

    def rule_funnel_metrics_10(self, ctx: ReportingContext) -> float:
        """Apply funnel metrics rule 10 with deterministic safeguards."""
        base = ctx.number("funnel metrics_score", 0.0)
        signal = ctx.text("funnel metrics_10")
        if ctx.flag("funnel metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("funnel metrics_complete"):
            return 2.0
        return -2.0

    def rule_funnel_metrics_11(self, ctx: ReportingContext) -> float:
        """Apply funnel metrics rule 11 with deterministic safeguards."""
        base = ctx.number("funnel metrics_score", 0.0)
        signal = ctx.text("funnel metrics_11")
        if ctx.flag("funnel metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("funnel metrics_complete"):
            return 3.0
        return -3.0

    def rule_funnel_metrics_12(self, ctx: ReportingContext) -> float:
        """Apply funnel metrics rule 12 with deterministic safeguards."""
        base = ctx.number("funnel metrics_score", 0.0)
        signal = ctx.text("funnel metrics_12")
        if ctx.flag("funnel metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("funnel metrics_complete"):
            return 1.0
        return -1.0

    def rule_funnel_metrics_13(self, ctx: ReportingContext) -> float:
        """Apply funnel metrics rule 13 with deterministic safeguards."""
        base = ctx.number("funnel metrics_score", 0.0)
        signal = ctx.text("funnel metrics_13")
        if ctx.flag("funnel metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("funnel metrics_complete"):
            return 2.0
        return -2.0

    def rule_funnel_metrics_14(self, ctx: ReportingContext) -> float:
        """Apply funnel metrics rule 14 with deterministic safeguards."""
        base = ctx.number("funnel metrics_score", 0.0)
        signal = ctx.text("funnel metrics_14")
        if ctx.flag("funnel metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("funnel metrics_complete"):
            return 3.0
        return -3.0

    def rule_conversion_metrics_1(self, ctx: ReportingContext) -> float:
        """Apply conversion metrics rule 1 with deterministic safeguards."""
        base = ctx.number("conversion metrics_score", 0.0)
        signal = ctx.text("conversion metrics_1")
        if ctx.flag("conversion metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("conversion metrics_complete"):
            return 2.0
        return -2.0

    def rule_conversion_metrics_2(self, ctx: ReportingContext) -> float:
        """Apply conversion metrics rule 2 with deterministic safeguards."""
        base = ctx.number("conversion metrics_score", 0.0)
        signal = ctx.text("conversion metrics_2")
        if ctx.flag("conversion metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("conversion metrics_complete"):
            return 3.0
        return -3.0

    def rule_conversion_metrics_3(self, ctx: ReportingContext) -> float:
        """Apply conversion metrics rule 3 with deterministic safeguards."""
        base = ctx.number("conversion metrics_score", 0.0)
        signal = ctx.text("conversion metrics_3")
        if ctx.flag("conversion metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("conversion metrics_complete"):
            return 1.0
        return -1.0

    def rule_conversion_metrics_4(self, ctx: ReportingContext) -> float:
        """Apply conversion metrics rule 4 with deterministic safeguards."""
        base = ctx.number("conversion metrics_score", 0.0)
        signal = ctx.text("conversion metrics_4")
        if ctx.flag("conversion metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("conversion metrics_complete"):
            return 2.0
        return -2.0

    def rule_conversion_metrics_5(self, ctx: ReportingContext) -> float:
        """Apply conversion metrics rule 5 with deterministic safeguards."""
        base = ctx.number("conversion metrics_score", 0.0)
        signal = ctx.text("conversion metrics_5")
        if ctx.flag("conversion metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("conversion metrics_complete"):
            return 3.0
        return -3.0

    def rule_conversion_metrics_6(self, ctx: ReportingContext) -> float:
        """Apply conversion metrics rule 6 with deterministic safeguards."""
        base = ctx.number("conversion metrics_score", 0.0)
        signal = ctx.text("conversion metrics_6")
        if ctx.flag("conversion metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("conversion metrics_complete"):
            return 1.0
        return -1.0

    def rule_conversion_metrics_7(self, ctx: ReportingContext) -> float:
        """Apply conversion metrics rule 7 with deterministic safeguards."""
        base = ctx.number("conversion metrics_score", 0.0)
        signal = ctx.text("conversion metrics_7")
        if ctx.flag("conversion metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("conversion metrics_complete"):
            return 2.0
        return -2.0

    def rule_conversion_metrics_8(self, ctx: ReportingContext) -> float:
        """Apply conversion metrics rule 8 with deterministic safeguards."""
        base = ctx.number("conversion metrics_score", 0.0)
        signal = ctx.text("conversion metrics_8")
        if ctx.flag("conversion metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("conversion metrics_complete"):
            return 3.0
        return -3.0

    def rule_conversion_metrics_9(self, ctx: ReportingContext) -> float:
        """Apply conversion metrics rule 9 with deterministic safeguards."""
        base = ctx.number("conversion metrics_score", 0.0)
        signal = ctx.text("conversion metrics_9")
        if ctx.flag("conversion metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("conversion metrics_complete"):
            return 1.0
        return -1.0

    def rule_conversion_metrics_10(self, ctx: ReportingContext) -> float:
        """Apply conversion metrics rule 10 with deterministic safeguards."""
        base = ctx.number("conversion metrics_score", 0.0)
        signal = ctx.text("conversion metrics_10")
        if ctx.flag("conversion metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("conversion metrics_complete"):
            return 2.0
        return -2.0

    def rule_conversion_metrics_11(self, ctx: ReportingContext) -> float:
        """Apply conversion metrics rule 11 with deterministic safeguards."""
        base = ctx.number("conversion metrics_score", 0.0)
        signal = ctx.text("conversion metrics_11")
        if ctx.flag("conversion metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("conversion metrics_complete"):
            return 3.0
        return -3.0

    def rule_conversion_metrics_12(self, ctx: ReportingContext) -> float:
        """Apply conversion metrics rule 12 with deterministic safeguards."""
        base = ctx.number("conversion metrics_score", 0.0)
        signal = ctx.text("conversion metrics_12")
        if ctx.flag("conversion metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("conversion metrics_complete"):
            return 1.0
        return -1.0

    def rule_conversion_metrics_13(self, ctx: ReportingContext) -> float:
        """Apply conversion metrics rule 13 with deterministic safeguards."""
        base = ctx.number("conversion metrics_score", 0.0)
        signal = ctx.text("conversion metrics_13")
        if ctx.flag("conversion metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("conversion metrics_complete"):
            return 2.0
        return -2.0

    def rule_conversion_metrics_14(self, ctx: ReportingContext) -> float:
        """Apply conversion metrics rule 14 with deterministic safeguards."""
        base = ctx.number("conversion metrics_score", 0.0)
        signal = ctx.text("conversion metrics_14")
        if ctx.flag("conversion metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("conversion metrics_complete"):
            return 3.0
        return -3.0

    def rule_response_metrics_1(self, ctx: ReportingContext) -> float:
        """Apply response metrics rule 1 with deterministic safeguards."""
        base = ctx.number("response metrics_score", 0.0)
        signal = ctx.text("response metrics_1")
        if ctx.flag("response metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("response metrics_complete"):
            return 2.0
        return -2.0

    def rule_response_metrics_2(self, ctx: ReportingContext) -> float:
        """Apply response metrics rule 2 with deterministic safeguards."""
        base = ctx.number("response metrics_score", 0.0)
        signal = ctx.text("response metrics_2")
        if ctx.flag("response metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("response metrics_complete"):
            return 3.0
        return -3.0

    def rule_response_metrics_3(self, ctx: ReportingContext) -> float:
        """Apply response metrics rule 3 with deterministic safeguards."""
        base = ctx.number("response metrics_score", 0.0)
        signal = ctx.text("response metrics_3")
        if ctx.flag("response metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("response metrics_complete"):
            return 1.0
        return -1.0

    def rule_response_metrics_4(self, ctx: ReportingContext) -> float:
        """Apply response metrics rule 4 with deterministic safeguards."""
        base = ctx.number("response metrics_score", 0.0)
        signal = ctx.text("response metrics_4")
        if ctx.flag("response metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("response metrics_complete"):
            return 2.0
        return -2.0

    def rule_response_metrics_5(self, ctx: ReportingContext) -> float:
        """Apply response metrics rule 5 with deterministic safeguards."""
        base = ctx.number("response metrics_score", 0.0)
        signal = ctx.text("response metrics_5")
        if ctx.flag("response metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("response metrics_complete"):
            return 3.0
        return -3.0

    def rule_response_metrics_6(self, ctx: ReportingContext) -> float:
        """Apply response metrics rule 6 with deterministic safeguards."""
        base = ctx.number("response metrics_score", 0.0)
        signal = ctx.text("response metrics_6")
        if ctx.flag("response metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("response metrics_complete"):
            return 1.0
        return -1.0

    def rule_response_metrics_7(self, ctx: ReportingContext) -> float:
        """Apply response metrics rule 7 with deterministic safeguards."""
        base = ctx.number("response metrics_score", 0.0)
        signal = ctx.text("response metrics_7")
        if ctx.flag("response metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("response metrics_complete"):
            return 2.0
        return -2.0

    def rule_response_metrics_8(self, ctx: ReportingContext) -> float:
        """Apply response metrics rule 8 with deterministic safeguards."""
        base = ctx.number("response metrics_score", 0.0)
        signal = ctx.text("response metrics_8")
        if ctx.flag("response metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("response metrics_complete"):
            return 3.0
        return -3.0

    def rule_response_metrics_9(self, ctx: ReportingContext) -> float:
        """Apply response metrics rule 9 with deterministic safeguards."""
        base = ctx.number("response metrics_score", 0.0)
        signal = ctx.text("response metrics_9")
        if ctx.flag("response metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("response metrics_complete"):
            return 1.0
        return -1.0

    def rule_response_metrics_10(self, ctx: ReportingContext) -> float:
        """Apply response metrics rule 10 with deterministic safeguards."""
        base = ctx.number("response metrics_score", 0.0)
        signal = ctx.text("response metrics_10")
        if ctx.flag("response metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("response metrics_complete"):
            return 2.0
        return -2.0

    def rule_response_metrics_11(self, ctx: ReportingContext) -> float:
        """Apply response metrics rule 11 with deterministic safeguards."""
        base = ctx.number("response metrics_score", 0.0)
        signal = ctx.text("response metrics_11")
        if ctx.flag("response metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("response metrics_complete"):
            return 3.0
        return -3.0

    def rule_response_metrics_12(self, ctx: ReportingContext) -> float:
        """Apply response metrics rule 12 with deterministic safeguards."""
        base = ctx.number("response metrics_score", 0.0)
        signal = ctx.text("response metrics_12")
        if ctx.flag("response metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("response metrics_complete"):
            return 1.0
        return -1.0

    def rule_response_metrics_13(self, ctx: ReportingContext) -> float:
        """Apply response metrics rule 13 with deterministic safeguards."""
        base = ctx.number("response metrics_score", 0.0)
        signal = ctx.text("response metrics_13")
        if ctx.flag("response metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("response metrics_complete"):
            return 2.0
        return -2.0

    def rule_response_metrics_14(self, ctx: ReportingContext) -> float:
        """Apply response metrics rule 14 with deterministic safeguards."""
        base = ctx.number("response metrics_score", 0.0)
        signal = ctx.text("response metrics_14")
        if ctx.flag("response metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("response metrics_complete"):
            return 3.0
        return -3.0

    def rule_time_to_action_1(self, ctx: ReportingContext) -> float:
        """Apply time-to-action rule 1 with deterministic safeguards."""
        base = ctx.number("time-to-action_score", 0.0)
        signal = ctx.text("time-to-action_1")
        if ctx.flag("time-to-action_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("time-to-action_complete"):
            return 2.0
        return -2.0

    def rule_time_to_action_2(self, ctx: ReportingContext) -> float:
        """Apply time-to-action rule 2 with deterministic safeguards."""
        base = ctx.number("time-to-action_score", 0.0)
        signal = ctx.text("time-to-action_2")
        if ctx.flag("time-to-action_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("time-to-action_complete"):
            return 3.0
        return -3.0

    def rule_time_to_action_3(self, ctx: ReportingContext) -> float:
        """Apply time-to-action rule 3 with deterministic safeguards."""
        base = ctx.number("time-to-action_score", 0.0)
        signal = ctx.text("time-to-action_3")
        if ctx.flag("time-to-action_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("time-to-action_complete"):
            return 1.0
        return -1.0

    def rule_time_to_action_4(self, ctx: ReportingContext) -> float:
        """Apply time-to-action rule 4 with deterministic safeguards."""
        base = ctx.number("time-to-action_score", 0.0)
        signal = ctx.text("time-to-action_4")
        if ctx.flag("time-to-action_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("time-to-action_complete"):
            return 2.0
        return -2.0

    def rule_time_to_action_5(self, ctx: ReportingContext) -> float:
        """Apply time-to-action rule 5 with deterministic safeguards."""
        base = ctx.number("time-to-action_score", 0.0)
        signal = ctx.text("time-to-action_5")
        if ctx.flag("time-to-action_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("time-to-action_complete"):
            return 3.0
        return -3.0

    def rule_time_to_action_6(self, ctx: ReportingContext) -> float:
        """Apply time-to-action rule 6 with deterministic safeguards."""
        base = ctx.number("time-to-action_score", 0.0)
        signal = ctx.text("time-to-action_6")
        if ctx.flag("time-to-action_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("time-to-action_complete"):
            return 1.0
        return -1.0

    def rule_time_to_action_7(self, ctx: ReportingContext) -> float:
        """Apply time-to-action rule 7 with deterministic safeguards."""
        base = ctx.number("time-to-action_score", 0.0)
        signal = ctx.text("time-to-action_7")
        if ctx.flag("time-to-action_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("time-to-action_complete"):
            return 2.0
        return -2.0

    def rule_time_to_action_8(self, ctx: ReportingContext) -> float:
        """Apply time-to-action rule 8 with deterministic safeguards."""
        base = ctx.number("time-to-action_score", 0.0)
        signal = ctx.text("time-to-action_8")
        if ctx.flag("time-to-action_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("time-to-action_complete"):
            return 3.0
        return -3.0

    def rule_time_to_action_9(self, ctx: ReportingContext) -> float:
        """Apply time-to-action rule 9 with deterministic safeguards."""
        base = ctx.number("time-to-action_score", 0.0)
        signal = ctx.text("time-to-action_9")
        if ctx.flag("time-to-action_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("time-to-action_complete"):
            return 1.0
        return -1.0

    def rule_time_to_action_10(self, ctx: ReportingContext) -> float:
        """Apply time-to-action rule 10 with deterministic safeguards."""
        base = ctx.number("time-to-action_score", 0.0)
        signal = ctx.text("time-to-action_10")
        if ctx.flag("time-to-action_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("time-to-action_complete"):
            return 2.0
        return -2.0

    def rule_time_to_action_11(self, ctx: ReportingContext) -> float:
        """Apply time-to-action rule 11 with deterministic safeguards."""
        base = ctx.number("time-to-action_score", 0.0)
        signal = ctx.text("time-to-action_11")
        if ctx.flag("time-to-action_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("time-to-action_complete"):
            return 3.0
        return -3.0

    def rule_time_to_action_12(self, ctx: ReportingContext) -> float:
        """Apply time-to-action rule 12 with deterministic safeguards."""
        base = ctx.number("time-to-action_score", 0.0)
        signal = ctx.text("time-to-action_12")
        if ctx.flag("time-to-action_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("time-to-action_complete"):
            return 1.0
        return -1.0

    def rule_time_to_action_13(self, ctx: ReportingContext) -> float:
        """Apply time-to-action rule 13 with deterministic safeguards."""
        base = ctx.number("time-to-action_score", 0.0)
        signal = ctx.text("time-to-action_13")
        if ctx.flag("time-to-action_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("time-to-action_complete"):
            return 2.0
        return -2.0

    def rule_time_to_action_14(self, ctx: ReportingContext) -> float:
        """Apply time-to-action rule 14 with deterministic safeguards."""
        base = ctx.number("time-to-action_score", 0.0)
        signal = ctx.text("time-to-action_14")
        if ctx.flag("time-to-action_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("time-to-action_complete"):
            return 3.0
        return -3.0

    def rule_company_metrics_1(self, ctx: ReportingContext) -> float:
        """Apply company metrics rule 1 with deterministic safeguards."""
        base = ctx.number("company metrics_score", 0.0)
        signal = ctx.text("company metrics_1")
        if ctx.flag("company metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("company metrics_complete"):
            return 2.0
        return -2.0

    def rule_company_metrics_2(self, ctx: ReportingContext) -> float:
        """Apply company metrics rule 2 with deterministic safeguards."""
        base = ctx.number("company metrics_score", 0.0)
        signal = ctx.text("company metrics_2")
        if ctx.flag("company metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("company metrics_complete"):
            return 3.0
        return -3.0

    def rule_company_metrics_3(self, ctx: ReportingContext) -> float:
        """Apply company metrics rule 3 with deterministic safeguards."""
        base = ctx.number("company metrics_score", 0.0)
        signal = ctx.text("company metrics_3")
        if ctx.flag("company metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("company metrics_complete"):
            return 1.0
        return -1.0

    def rule_company_metrics_4(self, ctx: ReportingContext) -> float:
        """Apply company metrics rule 4 with deterministic safeguards."""
        base = ctx.number("company metrics_score", 0.0)
        signal = ctx.text("company metrics_4")
        if ctx.flag("company metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("company metrics_complete"):
            return 2.0
        return -2.0

    def rule_company_metrics_5(self, ctx: ReportingContext) -> float:
        """Apply company metrics rule 5 with deterministic safeguards."""
        base = ctx.number("company metrics_score", 0.0)
        signal = ctx.text("company metrics_5")
        if ctx.flag("company metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("company metrics_complete"):
            return 3.0
        return -3.0

    def rule_company_metrics_6(self, ctx: ReportingContext) -> float:
        """Apply company metrics rule 6 with deterministic safeguards."""
        base = ctx.number("company metrics_score", 0.0)
        signal = ctx.text("company metrics_6")
        if ctx.flag("company metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("company metrics_complete"):
            return 1.0
        return -1.0

    def rule_company_metrics_7(self, ctx: ReportingContext) -> float:
        """Apply company metrics rule 7 with deterministic safeguards."""
        base = ctx.number("company metrics_score", 0.0)
        signal = ctx.text("company metrics_7")
        if ctx.flag("company metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("company metrics_complete"):
            return 2.0
        return -2.0

    def rule_company_metrics_8(self, ctx: ReportingContext) -> float:
        """Apply company metrics rule 8 with deterministic safeguards."""
        base = ctx.number("company metrics_score", 0.0)
        signal = ctx.text("company metrics_8")
        if ctx.flag("company metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("company metrics_complete"):
            return 3.0
        return -3.0

    def rule_company_metrics_9(self, ctx: ReportingContext) -> float:
        """Apply company metrics rule 9 with deterministic safeguards."""
        base = ctx.number("company metrics_score", 0.0)
        signal = ctx.text("company metrics_9")
        if ctx.flag("company metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("company metrics_complete"):
            return 1.0
        return -1.0

    def rule_company_metrics_10(self, ctx: ReportingContext) -> float:
        """Apply company metrics rule 10 with deterministic safeguards."""
        base = ctx.number("company metrics_score", 0.0)
        signal = ctx.text("company metrics_10")
        if ctx.flag("company metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("company metrics_complete"):
            return 2.0
        return -2.0

    def rule_company_metrics_11(self, ctx: ReportingContext) -> float:
        """Apply company metrics rule 11 with deterministic safeguards."""
        base = ctx.number("company metrics_score", 0.0)
        signal = ctx.text("company metrics_11")
        if ctx.flag("company metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("company metrics_complete"):
            return 3.0
        return -3.0

    def rule_company_metrics_12(self, ctx: ReportingContext) -> float:
        """Apply company metrics rule 12 with deterministic safeguards."""
        base = ctx.number("company metrics_score", 0.0)
        signal = ctx.text("company metrics_12")
        if ctx.flag("company metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("company metrics_complete"):
            return 1.0
        return -1.0

    def rule_company_metrics_13(self, ctx: ReportingContext) -> float:
        """Apply company metrics rule 13 with deterministic safeguards."""
        base = ctx.number("company metrics_score", 0.0)
        signal = ctx.text("company metrics_13")
        if ctx.flag("company metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("company metrics_complete"):
            return 2.0
        return -2.0

    def rule_company_metrics_14(self, ctx: ReportingContext) -> float:
        """Apply company metrics rule 14 with deterministic safeguards."""
        base = ctx.number("company metrics_score", 0.0)
        signal = ctx.text("company metrics_14")
        if ctx.flag("company metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("company metrics_complete"):
            return 3.0
        return -3.0

    def rule_role_metrics_1(self, ctx: ReportingContext) -> float:
        """Apply role metrics rule 1 with deterministic safeguards."""
        base = ctx.number("role metrics_score", 0.0)
        signal = ctx.text("role metrics_1")
        if ctx.flag("role metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("role metrics_complete"):
            return 2.0
        return -2.0

    def rule_role_metrics_2(self, ctx: ReportingContext) -> float:
        """Apply role metrics rule 2 with deterministic safeguards."""
        base = ctx.number("role metrics_score", 0.0)
        signal = ctx.text("role metrics_2")
        if ctx.flag("role metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("role metrics_complete"):
            return 3.0
        return -3.0

    def rule_role_metrics_3(self, ctx: ReportingContext) -> float:
        """Apply role metrics rule 3 with deterministic safeguards."""
        base = ctx.number("role metrics_score", 0.0)
        signal = ctx.text("role metrics_3")
        if ctx.flag("role metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("role metrics_complete"):
            return 1.0
        return -1.0

    def rule_role_metrics_4(self, ctx: ReportingContext) -> float:
        """Apply role metrics rule 4 with deterministic safeguards."""
        base = ctx.number("role metrics_score", 0.0)
        signal = ctx.text("role metrics_4")
        if ctx.flag("role metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("role metrics_complete"):
            return 2.0
        return -2.0

    def rule_role_metrics_5(self, ctx: ReportingContext) -> float:
        """Apply role metrics rule 5 with deterministic safeguards."""
        base = ctx.number("role metrics_score", 0.0)
        signal = ctx.text("role metrics_5")
        if ctx.flag("role metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("role metrics_complete"):
            return 3.0
        return -3.0

    def rule_role_metrics_6(self, ctx: ReportingContext) -> float:
        """Apply role metrics rule 6 with deterministic safeguards."""
        base = ctx.number("role metrics_score", 0.0)
        signal = ctx.text("role metrics_6")
        if ctx.flag("role metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("role metrics_complete"):
            return 1.0
        return -1.0

    def rule_role_metrics_7(self, ctx: ReportingContext) -> float:
        """Apply role metrics rule 7 with deterministic safeguards."""
        base = ctx.number("role metrics_score", 0.0)
        signal = ctx.text("role metrics_7")
        if ctx.flag("role metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("role metrics_complete"):
            return 2.0
        return -2.0

    def rule_role_metrics_8(self, ctx: ReportingContext) -> float:
        """Apply role metrics rule 8 with deterministic safeguards."""
        base = ctx.number("role metrics_score", 0.0)
        signal = ctx.text("role metrics_8")
        if ctx.flag("role metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("role metrics_complete"):
            return 3.0
        return -3.0

    def rule_role_metrics_9(self, ctx: ReportingContext) -> float:
        """Apply role metrics rule 9 with deterministic safeguards."""
        base = ctx.number("role metrics_score", 0.0)
        signal = ctx.text("role metrics_9")
        if ctx.flag("role metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("role metrics_complete"):
            return 1.0
        return -1.0

    def rule_role_metrics_10(self, ctx: ReportingContext) -> float:
        """Apply role metrics rule 10 with deterministic safeguards."""
        base = ctx.number("role metrics_score", 0.0)
        signal = ctx.text("role metrics_10")
        if ctx.flag("role metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("role metrics_complete"):
            return 2.0
        return -2.0

    def rule_role_metrics_11(self, ctx: ReportingContext) -> float:
        """Apply role metrics rule 11 with deterministic safeguards."""
        base = ctx.number("role metrics_score", 0.0)
        signal = ctx.text("role metrics_11")
        if ctx.flag("role metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("role metrics_complete"):
            return 3.0
        return -3.0

    def rule_role_metrics_12(self, ctx: ReportingContext) -> float:
        """Apply role metrics rule 12 with deterministic safeguards."""
        base = ctx.number("role metrics_score", 0.0)
        signal = ctx.text("role metrics_12")
        if ctx.flag("role metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("role metrics_complete"):
            return 1.0
        return -1.0

    def rule_role_metrics_13(self, ctx: ReportingContext) -> float:
        """Apply role metrics rule 13 with deterministic safeguards."""
        base = ctx.number("role metrics_score", 0.0)
        signal = ctx.text("role metrics_13")
        if ctx.flag("role metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("role metrics_complete"):
            return 2.0
        return -2.0

    def rule_role_metrics_14(self, ctx: ReportingContext) -> float:
        """Apply role metrics rule 14 with deterministic safeguards."""
        base = ctx.number("role metrics_score", 0.0)
        signal = ctx.text("role metrics_14")
        if ctx.flag("role metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("role metrics_complete"):
            return 3.0
        return -3.0

    def rule_source_metrics_1(self, ctx: ReportingContext) -> float:
        """Apply source metrics rule 1 with deterministic safeguards."""
        base = ctx.number("source metrics_score", 0.0)
        signal = ctx.text("source metrics_1")
        if ctx.flag("source metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("source metrics_complete"):
            return 2.0
        return -2.0

    def rule_source_metrics_2(self, ctx: ReportingContext) -> float:
        """Apply source metrics rule 2 with deterministic safeguards."""
        base = ctx.number("source metrics_score", 0.0)
        signal = ctx.text("source metrics_2")
        if ctx.flag("source metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("source metrics_complete"):
            return 3.0
        return -3.0

    def rule_source_metrics_3(self, ctx: ReportingContext) -> float:
        """Apply source metrics rule 3 with deterministic safeguards."""
        base = ctx.number("source metrics_score", 0.0)
        signal = ctx.text("source metrics_3")
        if ctx.flag("source metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("source metrics_complete"):
            return 1.0
        return -1.0

    def rule_source_metrics_4(self, ctx: ReportingContext) -> float:
        """Apply source metrics rule 4 with deterministic safeguards."""
        base = ctx.number("source metrics_score", 0.0)
        signal = ctx.text("source metrics_4")
        if ctx.flag("source metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("source metrics_complete"):
            return 2.0
        return -2.0

    def rule_source_metrics_5(self, ctx: ReportingContext) -> float:
        """Apply source metrics rule 5 with deterministic safeguards."""
        base = ctx.number("source metrics_score", 0.0)
        signal = ctx.text("source metrics_5")
        if ctx.flag("source metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("source metrics_complete"):
            return 3.0
        return -3.0

    def rule_source_metrics_6(self, ctx: ReportingContext) -> float:
        """Apply source metrics rule 6 with deterministic safeguards."""
        base = ctx.number("source metrics_score", 0.0)
        signal = ctx.text("source metrics_6")
        if ctx.flag("source metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("source metrics_complete"):
            return 1.0
        return -1.0

    def rule_source_metrics_7(self, ctx: ReportingContext) -> float:
        """Apply source metrics rule 7 with deterministic safeguards."""
        base = ctx.number("source metrics_score", 0.0)
        signal = ctx.text("source metrics_7")
        if ctx.flag("source metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("source metrics_complete"):
            return 2.0
        return -2.0

    def rule_source_metrics_8(self, ctx: ReportingContext) -> float:
        """Apply source metrics rule 8 with deterministic safeguards."""
        base = ctx.number("source metrics_score", 0.0)
        signal = ctx.text("source metrics_8")
        if ctx.flag("source metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("source metrics_complete"):
            return 3.0
        return -3.0

    def rule_source_metrics_9(self, ctx: ReportingContext) -> float:
        """Apply source metrics rule 9 with deterministic safeguards."""
        base = ctx.number("source metrics_score", 0.0)
        signal = ctx.text("source metrics_9")
        if ctx.flag("source metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("source metrics_complete"):
            return 1.0
        return -1.0

    def rule_source_metrics_10(self, ctx: ReportingContext) -> float:
        """Apply source metrics rule 10 with deterministic safeguards."""
        base = ctx.number("source metrics_score", 0.0)
        signal = ctx.text("source metrics_10")
        if ctx.flag("source metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("source metrics_complete"):
            return 2.0
        return -2.0

    def rule_source_metrics_11(self, ctx: ReportingContext) -> float:
        """Apply source metrics rule 11 with deterministic safeguards."""
        base = ctx.number("source metrics_score", 0.0)
        signal = ctx.text("source metrics_11")
        if ctx.flag("source metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("source metrics_complete"):
            return 3.0
        return -3.0

    def rule_source_metrics_12(self, ctx: ReportingContext) -> float:
        """Apply source metrics rule 12 with deterministic safeguards."""
        base = ctx.number("source metrics_score", 0.0)
        signal = ctx.text("source metrics_12")
        if ctx.flag("source metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("source metrics_complete"):
            return 1.0
        return -1.0

    def rule_source_metrics_13(self, ctx: ReportingContext) -> float:
        """Apply source metrics rule 13 with deterministic safeguards."""
        base = ctx.number("source metrics_score", 0.0)
        signal = ctx.text("source metrics_13")
        if ctx.flag("source metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("source metrics_complete"):
            return 2.0
        return -2.0

    def rule_source_metrics_14(self, ctx: ReportingContext) -> float:
        """Apply source metrics rule 14 with deterministic safeguards."""
        base = ctx.number("source metrics_score", 0.0)
        signal = ctx.text("source metrics_14")
        if ctx.flag("source metrics_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("source metrics_complete"):
            return 3.0
        return -3.0

    def rule_period_comparisons_1(self, ctx: ReportingContext) -> float:
        """Apply period comparisons rule 1 with deterministic safeguards."""
        base = ctx.number("period comparisons_score", 0.0)
        signal = ctx.text("period comparisons_1")
        if ctx.flag("period comparisons_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("period comparisons_complete"):
            return 2.0
        return -2.0

    def rule_period_comparisons_2(self, ctx: ReportingContext) -> float:
        """Apply period comparisons rule 2 with deterministic safeguards."""
        base = ctx.number("period comparisons_score", 0.0)
        signal = ctx.text("period comparisons_2")
        if ctx.flag("period comparisons_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("period comparisons_complete"):
            return 3.0
        return -3.0

    def rule_period_comparisons_3(self, ctx: ReportingContext) -> float:
        """Apply period comparisons rule 3 with deterministic safeguards."""
        base = ctx.number("period comparisons_score", 0.0)
        signal = ctx.text("period comparisons_3")
        if ctx.flag("period comparisons_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("period comparisons_complete"):
            return 1.0
        return -1.0

    def rule_period_comparisons_4(self, ctx: ReportingContext) -> float:
        """Apply period comparisons rule 4 with deterministic safeguards."""
        base = ctx.number("period comparisons_score", 0.0)
        signal = ctx.text("period comparisons_4")
        if ctx.flag("period comparisons_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("period comparisons_complete"):
            return 2.0
        return -2.0

    def rule_period_comparisons_5(self, ctx: ReportingContext) -> float:
        """Apply period comparisons rule 5 with deterministic safeguards."""
        base = ctx.number("period comparisons_score", 0.0)
        signal = ctx.text("period comparisons_5")
        if ctx.flag("period comparisons_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("period comparisons_complete"):
            return 3.0
        return -3.0

    def rule_period_comparisons_6(self, ctx: ReportingContext) -> float:
        """Apply period comparisons rule 6 with deterministic safeguards."""
        base = ctx.number("period comparisons_score", 0.0)
        signal = ctx.text("period comparisons_6")
        if ctx.flag("period comparisons_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("period comparisons_complete"):
            return 1.0
        return -1.0

    def rule_period_comparisons_7(self, ctx: ReportingContext) -> float:
        """Apply period comparisons rule 7 with deterministic safeguards."""
        base = ctx.number("period comparisons_score", 0.0)
        signal = ctx.text("period comparisons_7")
        if ctx.flag("period comparisons_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("period comparisons_complete"):
            return 2.0
        return -2.0

    def rule_period_comparisons_8(self, ctx: ReportingContext) -> float:
        """Apply period comparisons rule 8 with deterministic safeguards."""
        base = ctx.number("period comparisons_score", 0.0)
        signal = ctx.text("period comparisons_8")
        if ctx.flag("period comparisons_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("period comparisons_complete"):
            return 3.0
        return -3.0

    def rule_period_comparisons_9(self, ctx: ReportingContext) -> float:
        """Apply period comparisons rule 9 with deterministic safeguards."""
        base = ctx.number("period comparisons_score", 0.0)
        signal = ctx.text("period comparisons_9")
        if ctx.flag("period comparisons_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("period comparisons_complete"):
            return 1.0
        return -1.0

    def rule_period_comparisons_10(self, ctx: ReportingContext) -> float:
        """Apply period comparisons rule 10 with deterministic safeguards."""
        base = ctx.number("period comparisons_score", 0.0)
        signal = ctx.text("period comparisons_10")
        if ctx.flag("period comparisons_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("period comparisons_complete"):
            return 2.0
        return -2.0

    def rule_period_comparisons_11(self, ctx: ReportingContext) -> float:
        """Apply period comparisons rule 11 with deterministic safeguards."""
        base = ctx.number("period comparisons_score", 0.0)
        signal = ctx.text("period comparisons_11")
        if ctx.flag("period comparisons_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("period comparisons_complete"):
            return 3.0
        return -3.0

    def rule_period_comparisons_12(self, ctx: ReportingContext) -> float:
        """Apply period comparisons rule 12 with deterministic safeguards."""
        base = ctx.number("period comparisons_score", 0.0)
        signal = ctx.text("period comparisons_12")
        if ctx.flag("period comparisons_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("period comparisons_complete"):
            return 1.0
        return -1.0

    def rule_period_comparisons_13(self, ctx: ReportingContext) -> float:
        """Apply period comparisons rule 13 with deterministic safeguards."""
        base = ctx.number("period comparisons_score", 0.0)
        signal = ctx.text("period comparisons_13")
        if ctx.flag("period comparisons_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("period comparisons_complete"):
            return 2.0
        return -2.0

    def rule_period_comparisons_14(self, ctx: ReportingContext) -> float:
        """Apply period comparisons rule 14 with deterministic safeguards."""
        base = ctx.number("period comparisons_score", 0.0)
        signal = ctx.text("period comparisons_14")
        if ctx.flag("period comparisons_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("period comparisons_complete"):
            return 3.0
        return -3.0


    def batch_evaluate(self, records: Sequence[Mapping[str, object]]) -> list[ReportingDecision]:
        return [self.evaluate(record) for record in records]

    def summarize(self, decisions: Sequence[ReportingDecision]) -> dict[str, object]:
        scores = [d.score for d in decisions]
        return {"count": len(scores), "average": round(sum(scores) / len(scores), 2) if scores else 0.0, "ready": sum(d.status == "ready" for d in decisions), "review": sum(d.status == "review" for d in decisions), "needs_attention": sum(d.status == "needs_attention" for d in decisions)}

