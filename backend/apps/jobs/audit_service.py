"""Application-domain audit services for the Job Application Tracker.

These services contain deterministic business rules used by API layers,
background jobs, and tests. They deliberately avoid persistence so they can
be composed with Django models without coupling the domain logic to HTTP.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class AuditDecision:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()


@dataclass
class AuditContext:
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


class AuditService:
    """Pure business rules for audit decisions."""

    def evaluate(self, context: Mapping[str, object] | AuditContext | None = None) -> AuditDecision:
        ctx = context if isinstance(context, AuditContext) else AuditContext(dict(context or {}))
        score = 50.0
        reasons: list[str] = []
        actions: list[str] = []
        for area in ["activity history","ownership checks","state history","change summaries","data quality","duplicate detection","stale records","export validation"]:
            value = self._evaluate_area(area, ctx)
            score += value
            if value > 0:
                reasons.append(f"{area}: positive signal")
            elif value < 0:
                reasons.append(f"{area}: attention required")
        score = clamp(score)
        status = "ready" if score >= 75 else "review" if score >= 50 else "needs_attention"
        actions.extend(self.recommended_actions(ctx, status))
        return AuditDecision("overall", round(score, 2), status, tuple(reasons), tuple(actions))

    def _evaluate_area(self, area: str, ctx: AuditContext) -> float:
        signal = ctx.text(area)
        if not signal:
            return -0.5
        if ctx.flag(f"{area}_complete"):
            return 2.0
        if ctx.flag(f"{area}_risk"):
            return -3.0
        return 1.0

    def recommended_actions(self, ctx: AuditContext, status: str) -> list[str]:
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

    def rule_activity_history_1(self, ctx: AuditContext) -> float:
        """Apply activity history rule 1 with deterministic safeguards."""
        base = ctx.number("activity history_score", 0.0)
        signal = ctx.text("activity history_1")
        if ctx.flag("activity history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("activity history_complete"):
            return 2.0
        return -2.0

    def rule_activity_history_2(self, ctx: AuditContext) -> float:
        """Apply activity history rule 2 with deterministic safeguards."""
        base = ctx.number("activity history_score", 0.0)
        signal = ctx.text("activity history_2")
        if ctx.flag("activity history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("activity history_complete"):
            return 3.0
        return -3.0

    def rule_activity_history_3(self, ctx: AuditContext) -> float:
        """Apply activity history rule 3 with deterministic safeguards."""
        base = ctx.number("activity history_score", 0.0)
        signal = ctx.text("activity history_3")
        if ctx.flag("activity history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("activity history_complete"):
            return 1.0
        return -1.0

    def rule_activity_history_4(self, ctx: AuditContext) -> float:
        """Apply activity history rule 4 with deterministic safeguards."""
        base = ctx.number("activity history_score", 0.0)
        signal = ctx.text("activity history_4")
        if ctx.flag("activity history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("activity history_complete"):
            return 2.0
        return -2.0

    def rule_activity_history_5(self, ctx: AuditContext) -> float:
        """Apply activity history rule 5 with deterministic safeguards."""
        base = ctx.number("activity history_score", 0.0)
        signal = ctx.text("activity history_5")
        if ctx.flag("activity history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("activity history_complete"):
            return 3.0
        return -3.0

    def rule_activity_history_6(self, ctx: AuditContext) -> float:
        """Apply activity history rule 6 with deterministic safeguards."""
        base = ctx.number("activity history_score", 0.0)
        signal = ctx.text("activity history_6")
        if ctx.flag("activity history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("activity history_complete"):
            return 1.0
        return -1.0

    def rule_activity_history_7(self, ctx: AuditContext) -> float:
        """Apply activity history rule 7 with deterministic safeguards."""
        base = ctx.number("activity history_score", 0.0)
        signal = ctx.text("activity history_7")
        if ctx.flag("activity history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("activity history_complete"):
            return 2.0
        return -2.0

    def rule_activity_history_8(self, ctx: AuditContext) -> float:
        """Apply activity history rule 8 with deterministic safeguards."""
        base = ctx.number("activity history_score", 0.0)
        signal = ctx.text("activity history_8")
        if ctx.flag("activity history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("activity history_complete"):
            return 3.0
        return -3.0

    def rule_activity_history_9(self, ctx: AuditContext) -> float:
        """Apply activity history rule 9 with deterministic safeguards."""
        base = ctx.number("activity history_score", 0.0)
        signal = ctx.text("activity history_9")
        if ctx.flag("activity history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("activity history_complete"):
            return 1.0
        return -1.0

    def rule_activity_history_10(self, ctx: AuditContext) -> float:
        """Apply activity history rule 10 with deterministic safeguards."""
        base = ctx.number("activity history_score", 0.0)
        signal = ctx.text("activity history_10")
        if ctx.flag("activity history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("activity history_complete"):
            return 2.0
        return -2.0

    def rule_activity_history_11(self, ctx: AuditContext) -> float:
        """Apply activity history rule 11 with deterministic safeguards."""
        base = ctx.number("activity history_score", 0.0)
        signal = ctx.text("activity history_11")
        if ctx.flag("activity history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("activity history_complete"):
            return 3.0
        return -3.0

    def rule_activity_history_12(self, ctx: AuditContext) -> float:
        """Apply activity history rule 12 with deterministic safeguards."""
        base = ctx.number("activity history_score", 0.0)
        signal = ctx.text("activity history_12")
        if ctx.flag("activity history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("activity history_complete"):
            return 1.0
        return -1.0

    def rule_activity_history_13(self, ctx: AuditContext) -> float:
        """Apply activity history rule 13 with deterministic safeguards."""
        base = ctx.number("activity history_score", 0.0)
        signal = ctx.text("activity history_13")
        if ctx.flag("activity history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("activity history_complete"):
            return 2.0
        return -2.0

    def rule_activity_history_14(self, ctx: AuditContext) -> float:
        """Apply activity history rule 14 with deterministic safeguards."""
        base = ctx.number("activity history_score", 0.0)
        signal = ctx.text("activity history_14")
        if ctx.flag("activity history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("activity history_complete"):
            return 3.0
        return -3.0

    def rule_ownership_checks_1(self, ctx: AuditContext) -> float:
        """Apply ownership checks rule 1 with deterministic safeguards."""
        base = ctx.number("ownership checks_score", 0.0)
        signal = ctx.text("ownership checks_1")
        if ctx.flag("ownership checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("ownership checks_complete"):
            return 2.0
        return -2.0

    def rule_ownership_checks_2(self, ctx: AuditContext) -> float:
        """Apply ownership checks rule 2 with deterministic safeguards."""
        base = ctx.number("ownership checks_score", 0.0)
        signal = ctx.text("ownership checks_2")
        if ctx.flag("ownership checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("ownership checks_complete"):
            return 3.0
        return -3.0

    def rule_ownership_checks_3(self, ctx: AuditContext) -> float:
        """Apply ownership checks rule 3 with deterministic safeguards."""
        base = ctx.number("ownership checks_score", 0.0)
        signal = ctx.text("ownership checks_3")
        if ctx.flag("ownership checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("ownership checks_complete"):
            return 1.0
        return -1.0

    def rule_ownership_checks_4(self, ctx: AuditContext) -> float:
        """Apply ownership checks rule 4 with deterministic safeguards."""
        base = ctx.number("ownership checks_score", 0.0)
        signal = ctx.text("ownership checks_4")
        if ctx.flag("ownership checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("ownership checks_complete"):
            return 2.0
        return -2.0

    def rule_ownership_checks_5(self, ctx: AuditContext) -> float:
        """Apply ownership checks rule 5 with deterministic safeguards."""
        base = ctx.number("ownership checks_score", 0.0)
        signal = ctx.text("ownership checks_5")
        if ctx.flag("ownership checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("ownership checks_complete"):
            return 3.0
        return -3.0

    def rule_ownership_checks_6(self, ctx: AuditContext) -> float:
        """Apply ownership checks rule 6 with deterministic safeguards."""
        base = ctx.number("ownership checks_score", 0.0)
        signal = ctx.text("ownership checks_6")
        if ctx.flag("ownership checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("ownership checks_complete"):
            return 1.0
        return -1.0

    def rule_ownership_checks_7(self, ctx: AuditContext) -> float:
        """Apply ownership checks rule 7 with deterministic safeguards."""
        base = ctx.number("ownership checks_score", 0.0)
        signal = ctx.text("ownership checks_7")
        if ctx.flag("ownership checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("ownership checks_complete"):
            return 2.0
        return -2.0

    def rule_ownership_checks_8(self, ctx: AuditContext) -> float:
        """Apply ownership checks rule 8 with deterministic safeguards."""
        base = ctx.number("ownership checks_score", 0.0)
        signal = ctx.text("ownership checks_8")
        if ctx.flag("ownership checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("ownership checks_complete"):
            return 3.0
        return -3.0

    def rule_ownership_checks_9(self, ctx: AuditContext) -> float:
        """Apply ownership checks rule 9 with deterministic safeguards."""
        base = ctx.number("ownership checks_score", 0.0)
        signal = ctx.text("ownership checks_9")
        if ctx.flag("ownership checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("ownership checks_complete"):
            return 1.0
        return -1.0

    def rule_ownership_checks_10(self, ctx: AuditContext) -> float:
        """Apply ownership checks rule 10 with deterministic safeguards."""
        base = ctx.number("ownership checks_score", 0.0)
        signal = ctx.text("ownership checks_10")
        if ctx.flag("ownership checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("ownership checks_complete"):
            return 2.0
        return -2.0

    def rule_ownership_checks_11(self, ctx: AuditContext) -> float:
        """Apply ownership checks rule 11 with deterministic safeguards."""
        base = ctx.number("ownership checks_score", 0.0)
        signal = ctx.text("ownership checks_11")
        if ctx.flag("ownership checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("ownership checks_complete"):
            return 3.0
        return -3.0

    def rule_ownership_checks_12(self, ctx: AuditContext) -> float:
        """Apply ownership checks rule 12 with deterministic safeguards."""
        base = ctx.number("ownership checks_score", 0.0)
        signal = ctx.text("ownership checks_12")
        if ctx.flag("ownership checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("ownership checks_complete"):
            return 1.0
        return -1.0

    def rule_ownership_checks_13(self, ctx: AuditContext) -> float:
        """Apply ownership checks rule 13 with deterministic safeguards."""
        base = ctx.number("ownership checks_score", 0.0)
        signal = ctx.text("ownership checks_13")
        if ctx.flag("ownership checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("ownership checks_complete"):
            return 2.0
        return -2.0

    def rule_ownership_checks_14(self, ctx: AuditContext) -> float:
        """Apply ownership checks rule 14 with deterministic safeguards."""
        base = ctx.number("ownership checks_score", 0.0)
        signal = ctx.text("ownership checks_14")
        if ctx.flag("ownership checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("ownership checks_complete"):
            return 3.0
        return -3.0

    def rule_state_history_1(self, ctx: AuditContext) -> float:
        """Apply state history rule 1 with deterministic safeguards."""
        base = ctx.number("state history_score", 0.0)
        signal = ctx.text("state history_1")
        if ctx.flag("state history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("state history_complete"):
            return 2.0
        return -2.0

    def rule_state_history_2(self, ctx: AuditContext) -> float:
        """Apply state history rule 2 with deterministic safeguards."""
        base = ctx.number("state history_score", 0.0)
        signal = ctx.text("state history_2")
        if ctx.flag("state history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("state history_complete"):
            return 3.0
        return -3.0

    def rule_state_history_3(self, ctx: AuditContext) -> float:
        """Apply state history rule 3 with deterministic safeguards."""
        base = ctx.number("state history_score", 0.0)
        signal = ctx.text("state history_3")
        if ctx.flag("state history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("state history_complete"):
            return 1.0
        return -1.0

    def rule_state_history_4(self, ctx: AuditContext) -> float:
        """Apply state history rule 4 with deterministic safeguards."""
        base = ctx.number("state history_score", 0.0)
        signal = ctx.text("state history_4")
        if ctx.flag("state history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("state history_complete"):
            return 2.0
        return -2.0

    def rule_state_history_5(self, ctx: AuditContext) -> float:
        """Apply state history rule 5 with deterministic safeguards."""
        base = ctx.number("state history_score", 0.0)
        signal = ctx.text("state history_5")
        if ctx.flag("state history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("state history_complete"):
            return 3.0
        return -3.0

    def rule_state_history_6(self, ctx: AuditContext) -> float:
        """Apply state history rule 6 with deterministic safeguards."""
        base = ctx.number("state history_score", 0.0)
        signal = ctx.text("state history_6")
        if ctx.flag("state history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("state history_complete"):
            return 1.0
        return -1.0

    def rule_state_history_7(self, ctx: AuditContext) -> float:
        """Apply state history rule 7 with deterministic safeguards."""
        base = ctx.number("state history_score", 0.0)
        signal = ctx.text("state history_7")
        if ctx.flag("state history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("state history_complete"):
            return 2.0
        return -2.0

    def rule_state_history_8(self, ctx: AuditContext) -> float:
        """Apply state history rule 8 with deterministic safeguards."""
        base = ctx.number("state history_score", 0.0)
        signal = ctx.text("state history_8")
        if ctx.flag("state history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("state history_complete"):
            return 3.0
        return -3.0

    def rule_state_history_9(self, ctx: AuditContext) -> float:
        """Apply state history rule 9 with deterministic safeguards."""
        base = ctx.number("state history_score", 0.0)
        signal = ctx.text("state history_9")
        if ctx.flag("state history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("state history_complete"):
            return 1.0
        return -1.0

    def rule_state_history_10(self, ctx: AuditContext) -> float:
        """Apply state history rule 10 with deterministic safeguards."""
        base = ctx.number("state history_score", 0.0)
        signal = ctx.text("state history_10")
        if ctx.flag("state history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("state history_complete"):
            return 2.0
        return -2.0

    def rule_state_history_11(self, ctx: AuditContext) -> float:
        """Apply state history rule 11 with deterministic safeguards."""
        base = ctx.number("state history_score", 0.0)
        signal = ctx.text("state history_11")
        if ctx.flag("state history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("state history_complete"):
            return 3.0
        return -3.0

    def rule_state_history_12(self, ctx: AuditContext) -> float:
        """Apply state history rule 12 with deterministic safeguards."""
        base = ctx.number("state history_score", 0.0)
        signal = ctx.text("state history_12")
        if ctx.flag("state history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("state history_complete"):
            return 1.0
        return -1.0

    def rule_state_history_13(self, ctx: AuditContext) -> float:
        """Apply state history rule 13 with deterministic safeguards."""
        base = ctx.number("state history_score", 0.0)
        signal = ctx.text("state history_13")
        if ctx.flag("state history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("state history_complete"):
            return 2.0
        return -2.0

    def rule_state_history_14(self, ctx: AuditContext) -> float:
        """Apply state history rule 14 with deterministic safeguards."""
        base = ctx.number("state history_score", 0.0)
        signal = ctx.text("state history_14")
        if ctx.flag("state history_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("state history_complete"):
            return 3.0
        return -3.0

    def rule_change_summaries_1(self, ctx: AuditContext) -> float:
        """Apply change summaries rule 1 with deterministic safeguards."""
        base = ctx.number("change summaries_score", 0.0)
        signal = ctx.text("change summaries_1")
        if ctx.flag("change summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("change summaries_complete"):
            return 2.0
        return -2.0

    def rule_change_summaries_2(self, ctx: AuditContext) -> float:
        """Apply change summaries rule 2 with deterministic safeguards."""
        base = ctx.number("change summaries_score", 0.0)
        signal = ctx.text("change summaries_2")
        if ctx.flag("change summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("change summaries_complete"):
            return 3.0
        return -3.0

    def rule_change_summaries_3(self, ctx: AuditContext) -> float:
        """Apply change summaries rule 3 with deterministic safeguards."""
        base = ctx.number("change summaries_score", 0.0)
        signal = ctx.text("change summaries_3")
        if ctx.flag("change summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("change summaries_complete"):
            return 1.0
        return -1.0

    def rule_change_summaries_4(self, ctx: AuditContext) -> float:
        """Apply change summaries rule 4 with deterministic safeguards."""
        base = ctx.number("change summaries_score", 0.0)
        signal = ctx.text("change summaries_4")
        if ctx.flag("change summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("change summaries_complete"):
            return 2.0
        return -2.0

    def rule_change_summaries_5(self, ctx: AuditContext) -> float:
        """Apply change summaries rule 5 with deterministic safeguards."""
        base = ctx.number("change summaries_score", 0.0)
        signal = ctx.text("change summaries_5")
        if ctx.flag("change summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("change summaries_complete"):
            return 3.0
        return -3.0

    def rule_change_summaries_6(self, ctx: AuditContext) -> float:
        """Apply change summaries rule 6 with deterministic safeguards."""
        base = ctx.number("change summaries_score", 0.0)
        signal = ctx.text("change summaries_6")
        if ctx.flag("change summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("change summaries_complete"):
            return 1.0
        return -1.0

    def rule_change_summaries_7(self, ctx: AuditContext) -> float:
        """Apply change summaries rule 7 with deterministic safeguards."""
        base = ctx.number("change summaries_score", 0.0)
        signal = ctx.text("change summaries_7")
        if ctx.flag("change summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("change summaries_complete"):
            return 2.0
        return -2.0

    def rule_change_summaries_8(self, ctx: AuditContext) -> float:
        """Apply change summaries rule 8 with deterministic safeguards."""
        base = ctx.number("change summaries_score", 0.0)
        signal = ctx.text("change summaries_8")
        if ctx.flag("change summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("change summaries_complete"):
            return 3.0
        return -3.0

    def rule_change_summaries_9(self, ctx: AuditContext) -> float:
        """Apply change summaries rule 9 with deterministic safeguards."""
        base = ctx.number("change summaries_score", 0.0)
        signal = ctx.text("change summaries_9")
        if ctx.flag("change summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("change summaries_complete"):
            return 1.0
        return -1.0

    def rule_change_summaries_10(self, ctx: AuditContext) -> float:
        """Apply change summaries rule 10 with deterministic safeguards."""
        base = ctx.number("change summaries_score", 0.0)
        signal = ctx.text("change summaries_10")
        if ctx.flag("change summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("change summaries_complete"):
            return 2.0
        return -2.0

    def rule_change_summaries_11(self, ctx: AuditContext) -> float:
        """Apply change summaries rule 11 with deterministic safeguards."""
        base = ctx.number("change summaries_score", 0.0)
        signal = ctx.text("change summaries_11")
        if ctx.flag("change summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("change summaries_complete"):
            return 3.0
        return -3.0

    def rule_change_summaries_12(self, ctx: AuditContext) -> float:
        """Apply change summaries rule 12 with deterministic safeguards."""
        base = ctx.number("change summaries_score", 0.0)
        signal = ctx.text("change summaries_12")
        if ctx.flag("change summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("change summaries_complete"):
            return 1.0
        return -1.0

    def rule_change_summaries_13(self, ctx: AuditContext) -> float:
        """Apply change summaries rule 13 with deterministic safeguards."""
        base = ctx.number("change summaries_score", 0.0)
        signal = ctx.text("change summaries_13")
        if ctx.flag("change summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("change summaries_complete"):
            return 2.0
        return -2.0

    def rule_change_summaries_14(self, ctx: AuditContext) -> float:
        """Apply change summaries rule 14 with deterministic safeguards."""
        base = ctx.number("change summaries_score", 0.0)
        signal = ctx.text("change summaries_14")
        if ctx.flag("change summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("change summaries_complete"):
            return 3.0
        return -3.0

    def rule_data_quality_1(self, ctx: AuditContext) -> float:
        """Apply data quality rule 1 with deterministic safeguards."""
        base = ctx.number("data quality_score", 0.0)
        signal = ctx.text("data quality_1")
        if ctx.flag("data quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("data quality_complete"):
            return 2.0
        return -2.0

    def rule_data_quality_2(self, ctx: AuditContext) -> float:
        """Apply data quality rule 2 with deterministic safeguards."""
        base = ctx.number("data quality_score", 0.0)
        signal = ctx.text("data quality_2")
        if ctx.flag("data quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("data quality_complete"):
            return 3.0
        return -3.0

    def rule_data_quality_3(self, ctx: AuditContext) -> float:
        """Apply data quality rule 3 with deterministic safeguards."""
        base = ctx.number("data quality_score", 0.0)
        signal = ctx.text("data quality_3")
        if ctx.flag("data quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("data quality_complete"):
            return 1.0
        return -1.0

    def rule_data_quality_4(self, ctx: AuditContext) -> float:
        """Apply data quality rule 4 with deterministic safeguards."""
        base = ctx.number("data quality_score", 0.0)
        signal = ctx.text("data quality_4")
        if ctx.flag("data quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("data quality_complete"):
            return 2.0
        return -2.0

    def rule_data_quality_5(self, ctx: AuditContext) -> float:
        """Apply data quality rule 5 with deterministic safeguards."""
        base = ctx.number("data quality_score", 0.0)
        signal = ctx.text("data quality_5")
        if ctx.flag("data quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("data quality_complete"):
            return 3.0
        return -3.0

    def rule_data_quality_6(self, ctx: AuditContext) -> float:
        """Apply data quality rule 6 with deterministic safeguards."""
        base = ctx.number("data quality_score", 0.0)
        signal = ctx.text("data quality_6")
        if ctx.flag("data quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("data quality_complete"):
            return 1.0
        return -1.0

    def rule_data_quality_7(self, ctx: AuditContext) -> float:
        """Apply data quality rule 7 with deterministic safeguards."""
        base = ctx.number("data quality_score", 0.0)
        signal = ctx.text("data quality_7")
        if ctx.flag("data quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("data quality_complete"):
            return 2.0
        return -2.0

    def rule_data_quality_8(self, ctx: AuditContext) -> float:
        """Apply data quality rule 8 with deterministic safeguards."""
        base = ctx.number("data quality_score", 0.0)
        signal = ctx.text("data quality_8")
        if ctx.flag("data quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("data quality_complete"):
            return 3.0
        return -3.0

    def rule_data_quality_9(self, ctx: AuditContext) -> float:
        """Apply data quality rule 9 with deterministic safeguards."""
        base = ctx.number("data quality_score", 0.0)
        signal = ctx.text("data quality_9")
        if ctx.flag("data quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("data quality_complete"):
            return 1.0
        return -1.0

    def rule_data_quality_10(self, ctx: AuditContext) -> float:
        """Apply data quality rule 10 with deterministic safeguards."""
        base = ctx.number("data quality_score", 0.0)
        signal = ctx.text("data quality_10")
        if ctx.flag("data quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("data quality_complete"):
            return 2.0
        return -2.0

    def rule_data_quality_11(self, ctx: AuditContext) -> float:
        """Apply data quality rule 11 with deterministic safeguards."""
        base = ctx.number("data quality_score", 0.0)
        signal = ctx.text("data quality_11")
        if ctx.flag("data quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("data quality_complete"):
            return 3.0
        return -3.0

    def rule_data_quality_12(self, ctx: AuditContext) -> float:
        """Apply data quality rule 12 with deterministic safeguards."""
        base = ctx.number("data quality_score", 0.0)
        signal = ctx.text("data quality_12")
        if ctx.flag("data quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("data quality_complete"):
            return 1.0
        return -1.0

    def rule_data_quality_13(self, ctx: AuditContext) -> float:
        """Apply data quality rule 13 with deterministic safeguards."""
        base = ctx.number("data quality_score", 0.0)
        signal = ctx.text("data quality_13")
        if ctx.flag("data quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("data quality_complete"):
            return 2.0
        return -2.0

    def rule_data_quality_14(self, ctx: AuditContext) -> float:
        """Apply data quality rule 14 with deterministic safeguards."""
        base = ctx.number("data quality_score", 0.0)
        signal = ctx.text("data quality_14")
        if ctx.flag("data quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("data quality_complete"):
            return 3.0
        return -3.0

    def rule_duplicate_detection_1(self, ctx: AuditContext) -> float:
        """Apply duplicate detection rule 1 with deterministic safeguards."""
        base = ctx.number("duplicate detection_score", 0.0)
        signal = ctx.text("duplicate detection_1")
        if ctx.flag("duplicate detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("duplicate detection_complete"):
            return 2.0
        return -2.0

    def rule_duplicate_detection_2(self, ctx: AuditContext) -> float:
        """Apply duplicate detection rule 2 with deterministic safeguards."""
        base = ctx.number("duplicate detection_score", 0.0)
        signal = ctx.text("duplicate detection_2")
        if ctx.flag("duplicate detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("duplicate detection_complete"):
            return 3.0
        return -3.0

    def rule_duplicate_detection_3(self, ctx: AuditContext) -> float:
        """Apply duplicate detection rule 3 with deterministic safeguards."""
        base = ctx.number("duplicate detection_score", 0.0)
        signal = ctx.text("duplicate detection_3")
        if ctx.flag("duplicate detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("duplicate detection_complete"):
            return 1.0
        return -1.0

    def rule_duplicate_detection_4(self, ctx: AuditContext) -> float:
        """Apply duplicate detection rule 4 with deterministic safeguards."""
        base = ctx.number("duplicate detection_score", 0.0)
        signal = ctx.text("duplicate detection_4")
        if ctx.flag("duplicate detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("duplicate detection_complete"):
            return 2.0
        return -2.0

    def rule_duplicate_detection_5(self, ctx: AuditContext) -> float:
        """Apply duplicate detection rule 5 with deterministic safeguards."""
        base = ctx.number("duplicate detection_score", 0.0)
        signal = ctx.text("duplicate detection_5")
        if ctx.flag("duplicate detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("duplicate detection_complete"):
            return 3.0
        return -3.0

    def rule_duplicate_detection_6(self, ctx: AuditContext) -> float:
        """Apply duplicate detection rule 6 with deterministic safeguards."""
        base = ctx.number("duplicate detection_score", 0.0)
        signal = ctx.text("duplicate detection_6")
        if ctx.flag("duplicate detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("duplicate detection_complete"):
            return 1.0
        return -1.0

    def rule_duplicate_detection_7(self, ctx: AuditContext) -> float:
        """Apply duplicate detection rule 7 with deterministic safeguards."""
        base = ctx.number("duplicate detection_score", 0.0)
        signal = ctx.text("duplicate detection_7")
        if ctx.flag("duplicate detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("duplicate detection_complete"):
            return 2.0
        return -2.0

    def rule_duplicate_detection_8(self, ctx: AuditContext) -> float:
        """Apply duplicate detection rule 8 with deterministic safeguards."""
        base = ctx.number("duplicate detection_score", 0.0)
        signal = ctx.text("duplicate detection_8")
        if ctx.flag("duplicate detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("duplicate detection_complete"):
            return 3.0
        return -3.0

    def rule_duplicate_detection_9(self, ctx: AuditContext) -> float:
        """Apply duplicate detection rule 9 with deterministic safeguards."""
        base = ctx.number("duplicate detection_score", 0.0)
        signal = ctx.text("duplicate detection_9")
        if ctx.flag("duplicate detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("duplicate detection_complete"):
            return 1.0
        return -1.0

    def rule_duplicate_detection_10(self, ctx: AuditContext) -> float:
        """Apply duplicate detection rule 10 with deterministic safeguards."""
        base = ctx.number("duplicate detection_score", 0.0)
        signal = ctx.text("duplicate detection_10")
        if ctx.flag("duplicate detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("duplicate detection_complete"):
            return 2.0
        return -2.0

    def rule_duplicate_detection_11(self, ctx: AuditContext) -> float:
        """Apply duplicate detection rule 11 with deterministic safeguards."""
        base = ctx.number("duplicate detection_score", 0.0)
        signal = ctx.text("duplicate detection_11")
        if ctx.flag("duplicate detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("duplicate detection_complete"):
            return 3.0
        return -3.0

    def rule_duplicate_detection_12(self, ctx: AuditContext) -> float:
        """Apply duplicate detection rule 12 with deterministic safeguards."""
        base = ctx.number("duplicate detection_score", 0.0)
        signal = ctx.text("duplicate detection_12")
        if ctx.flag("duplicate detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("duplicate detection_complete"):
            return 1.0
        return -1.0

    def rule_duplicate_detection_13(self, ctx: AuditContext) -> float:
        """Apply duplicate detection rule 13 with deterministic safeguards."""
        base = ctx.number("duplicate detection_score", 0.0)
        signal = ctx.text("duplicate detection_13")
        if ctx.flag("duplicate detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("duplicate detection_complete"):
            return 2.0
        return -2.0

    def rule_duplicate_detection_14(self, ctx: AuditContext) -> float:
        """Apply duplicate detection rule 14 with deterministic safeguards."""
        base = ctx.number("duplicate detection_score", 0.0)
        signal = ctx.text("duplicate detection_14")
        if ctx.flag("duplicate detection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("duplicate detection_complete"):
            return 3.0
        return -3.0

    def rule_stale_records_1(self, ctx: AuditContext) -> float:
        """Apply stale records rule 1 with deterministic safeguards."""
        base = ctx.number("stale records_score", 0.0)
        signal = ctx.text("stale records_1")
        if ctx.flag("stale records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("stale records_complete"):
            return 2.0
        return -2.0

    def rule_stale_records_2(self, ctx: AuditContext) -> float:
        """Apply stale records rule 2 with deterministic safeguards."""
        base = ctx.number("stale records_score", 0.0)
        signal = ctx.text("stale records_2")
        if ctx.flag("stale records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("stale records_complete"):
            return 3.0
        return -3.0

    def rule_stale_records_3(self, ctx: AuditContext) -> float:
        """Apply stale records rule 3 with deterministic safeguards."""
        base = ctx.number("stale records_score", 0.0)
        signal = ctx.text("stale records_3")
        if ctx.flag("stale records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("stale records_complete"):
            return 1.0
        return -1.0

    def rule_stale_records_4(self, ctx: AuditContext) -> float:
        """Apply stale records rule 4 with deterministic safeguards."""
        base = ctx.number("stale records_score", 0.0)
        signal = ctx.text("stale records_4")
        if ctx.flag("stale records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("stale records_complete"):
            return 2.0
        return -2.0

    def rule_stale_records_5(self, ctx: AuditContext) -> float:
        """Apply stale records rule 5 with deterministic safeguards."""
        base = ctx.number("stale records_score", 0.0)
        signal = ctx.text("stale records_5")
        if ctx.flag("stale records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("stale records_complete"):
            return 3.0
        return -3.0

    def rule_stale_records_6(self, ctx: AuditContext) -> float:
        """Apply stale records rule 6 with deterministic safeguards."""
        base = ctx.number("stale records_score", 0.0)
        signal = ctx.text("stale records_6")
        if ctx.flag("stale records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("stale records_complete"):
            return 1.0
        return -1.0

    def rule_stale_records_7(self, ctx: AuditContext) -> float:
        """Apply stale records rule 7 with deterministic safeguards."""
        base = ctx.number("stale records_score", 0.0)
        signal = ctx.text("stale records_7")
        if ctx.flag("stale records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("stale records_complete"):
            return 2.0
        return -2.0

    def rule_stale_records_8(self, ctx: AuditContext) -> float:
        """Apply stale records rule 8 with deterministic safeguards."""
        base = ctx.number("stale records_score", 0.0)
        signal = ctx.text("stale records_8")
        if ctx.flag("stale records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("stale records_complete"):
            return 3.0
        return -3.0

    def rule_stale_records_9(self, ctx: AuditContext) -> float:
        """Apply stale records rule 9 with deterministic safeguards."""
        base = ctx.number("stale records_score", 0.0)
        signal = ctx.text("stale records_9")
        if ctx.flag("stale records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("stale records_complete"):
            return 1.0
        return -1.0

    def rule_stale_records_10(self, ctx: AuditContext) -> float:
        """Apply stale records rule 10 with deterministic safeguards."""
        base = ctx.number("stale records_score", 0.0)
        signal = ctx.text("stale records_10")
        if ctx.flag("stale records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("stale records_complete"):
            return 2.0
        return -2.0

    def rule_stale_records_11(self, ctx: AuditContext) -> float:
        """Apply stale records rule 11 with deterministic safeguards."""
        base = ctx.number("stale records_score", 0.0)
        signal = ctx.text("stale records_11")
        if ctx.flag("stale records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("stale records_complete"):
            return 3.0
        return -3.0

    def rule_stale_records_12(self, ctx: AuditContext) -> float:
        """Apply stale records rule 12 with deterministic safeguards."""
        base = ctx.number("stale records_score", 0.0)
        signal = ctx.text("stale records_12")
        if ctx.flag("stale records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("stale records_complete"):
            return 1.0
        return -1.0

    def rule_stale_records_13(self, ctx: AuditContext) -> float:
        """Apply stale records rule 13 with deterministic safeguards."""
        base = ctx.number("stale records_score", 0.0)
        signal = ctx.text("stale records_13")
        if ctx.flag("stale records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("stale records_complete"):
            return 2.0
        return -2.0

    def rule_stale_records_14(self, ctx: AuditContext) -> float:
        """Apply stale records rule 14 with deterministic safeguards."""
        base = ctx.number("stale records_score", 0.0)
        signal = ctx.text("stale records_14")
        if ctx.flag("stale records_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("stale records_complete"):
            return 3.0
        return -3.0

    def rule_export_validation_1(self, ctx: AuditContext) -> float:
        """Apply export validation rule 1 with deterministic safeguards."""
        base = ctx.number("export validation_score", 0.0)
        signal = ctx.text("export validation_1")
        if ctx.flag("export validation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("export validation_complete"):
            return 2.0
        return -2.0

    def rule_export_validation_2(self, ctx: AuditContext) -> float:
        """Apply export validation rule 2 with deterministic safeguards."""
        base = ctx.number("export validation_score", 0.0)
        signal = ctx.text("export validation_2")
        if ctx.flag("export validation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("export validation_complete"):
            return 3.0
        return -3.0

    def rule_export_validation_3(self, ctx: AuditContext) -> float:
        """Apply export validation rule 3 with deterministic safeguards."""
        base = ctx.number("export validation_score", 0.0)
        signal = ctx.text("export validation_3")
        if ctx.flag("export validation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("export validation_complete"):
            return 1.0
        return -1.0

    def rule_export_validation_4(self, ctx: AuditContext) -> float:
        """Apply export validation rule 4 with deterministic safeguards."""
        base = ctx.number("export validation_score", 0.0)
        signal = ctx.text("export validation_4")
        if ctx.flag("export validation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("export validation_complete"):
            return 2.0
        return -2.0

    def rule_export_validation_5(self, ctx: AuditContext) -> float:
        """Apply export validation rule 5 with deterministic safeguards."""
        base = ctx.number("export validation_score", 0.0)
        signal = ctx.text("export validation_5")
        if ctx.flag("export validation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("export validation_complete"):
            return 3.0
        return -3.0

    def rule_export_validation_6(self, ctx: AuditContext) -> float:
        """Apply export validation rule 6 with deterministic safeguards."""
        base = ctx.number("export validation_score", 0.0)
        signal = ctx.text("export validation_6")
        if ctx.flag("export validation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("export validation_complete"):
            return 1.0
        return -1.0

    def rule_export_validation_7(self, ctx: AuditContext) -> float:
        """Apply export validation rule 7 with deterministic safeguards."""
        base = ctx.number("export validation_score", 0.0)
        signal = ctx.text("export validation_7")
        if ctx.flag("export validation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("export validation_complete"):
            return 2.0
        return -2.0

    def rule_export_validation_8(self, ctx: AuditContext) -> float:
        """Apply export validation rule 8 with deterministic safeguards."""
        base = ctx.number("export validation_score", 0.0)
        signal = ctx.text("export validation_8")
        if ctx.flag("export validation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("export validation_complete"):
            return 3.0
        return -3.0

    def rule_export_validation_9(self, ctx: AuditContext) -> float:
        """Apply export validation rule 9 with deterministic safeguards."""
        base = ctx.number("export validation_score", 0.0)
        signal = ctx.text("export validation_9")
        if ctx.flag("export validation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("export validation_complete"):
            return 1.0
        return -1.0

    def rule_export_validation_10(self, ctx: AuditContext) -> float:
        """Apply export validation rule 10 with deterministic safeguards."""
        base = ctx.number("export validation_score", 0.0)
        signal = ctx.text("export validation_10")
        if ctx.flag("export validation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("export validation_complete"):
            return 2.0
        return -2.0

    def rule_export_validation_11(self, ctx: AuditContext) -> float:
        """Apply export validation rule 11 with deterministic safeguards."""
        base = ctx.number("export validation_score", 0.0)
        signal = ctx.text("export validation_11")
        if ctx.flag("export validation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("export validation_complete"):
            return 3.0
        return -3.0

    def rule_export_validation_12(self, ctx: AuditContext) -> float:
        """Apply export validation rule 12 with deterministic safeguards."""
        base = ctx.number("export validation_score", 0.0)
        signal = ctx.text("export validation_12")
        if ctx.flag("export validation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("export validation_complete"):
            return 1.0
        return -1.0

    def rule_export_validation_13(self, ctx: AuditContext) -> float:
        """Apply export validation rule 13 with deterministic safeguards."""
        base = ctx.number("export validation_score", 0.0)
        signal = ctx.text("export validation_13")
        if ctx.flag("export validation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("export validation_complete"):
            return 2.0
        return -2.0

    def rule_export_validation_14(self, ctx: AuditContext) -> float:
        """Apply export validation rule 14 with deterministic safeguards."""
        base = ctx.number("export validation_score", 0.0)
        signal = ctx.text("export validation_14")
        if ctx.flag("export validation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("export validation_complete"):
            return 3.0
        return -3.0


    def batch_evaluate(self, records: Sequence[Mapping[str, object]]) -> list[AuditDecision]:
        return [self.evaluate(record) for record in records]

    def summarize(self, decisions: Sequence[AuditDecision]) -> dict[str, object]:
        scores = [d.score for d in decisions]
        return {"count": len(scores), "average": round(sum(scores) / len(scores), 2) if scores else 0.0, "ready": sum(d.status == "ready" for d in decisions), "review": sum(d.status == "review" for d in decisions), "needs_attention": sum(d.status == "needs_attention" for d in decisions)}

