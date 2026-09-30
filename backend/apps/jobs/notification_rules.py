"""Application-domain notification services for the Job Application Tracker.

These services contain deterministic business rules used by API layers,
background jobs, and tests. They deliberately avoid persistence so they can
be composed with Django models without coupling the domain logic to HTTP.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class NotificationDecision:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()


@dataclass
class NotificationContext:
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


class NotificationService:
    """Pure business rules for notification decisions."""

    def evaluate(self, context: Mapping[str, object] | NotificationContext | None = None) -> NotificationDecision:
        ctx = context if isinstance(context, NotificationContext) else NotificationContext(dict(context or {}))
        score = 50.0
        reasons: list[str] = []
        actions: list[str] = []
        for area in ["deadline reminders","interview reminders","follow-up reminders","stale alerts","task reminders","weekly summaries","offer deadlines","search alerts"]:
            value = self._evaluate_area(area, ctx)
            score += value
            if value > 0:
                reasons.append(f"{area}: positive signal")
            elif value < 0:
                reasons.append(f"{area}: attention required")
        score = clamp(score)
        status = "ready" if score >= 75 else "review" if score >= 50 else "needs_attention"
        actions.extend(self.recommended_actions(ctx, status))
        return NotificationDecision("overall", round(score, 2), status, tuple(reasons), tuple(actions))

    def _evaluate_area(self, area: str, ctx: NotificationContext) -> float:
        signal = ctx.text(area)
        if not signal:
            return -0.5
        if ctx.flag(f"{area}_complete"):
            return 2.0
        if ctx.flag(f"{area}_risk"):
            return -3.0
        return 1.0

    def recommended_actions(self, ctx: NotificationContext, status: str) -> list[str]:
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

    def rule_deadline_reminders_1(self, ctx: NotificationContext) -> float:
        """Apply deadline reminders rule 1 with deterministic safeguards."""
        base = ctx.number("deadline reminders_score", 0.0)
        signal = ctx.text("deadline reminders_1")
        if ctx.flag("deadline reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("deadline reminders_complete"):
            return 2.0
        return -2.0

    def rule_deadline_reminders_2(self, ctx: NotificationContext) -> float:
        """Apply deadline reminders rule 2 with deterministic safeguards."""
        base = ctx.number("deadline reminders_score", 0.0)
        signal = ctx.text("deadline reminders_2")
        if ctx.flag("deadline reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("deadline reminders_complete"):
            return 3.0
        return -3.0

    def rule_deadline_reminders_3(self, ctx: NotificationContext) -> float:
        """Apply deadline reminders rule 3 with deterministic safeguards."""
        base = ctx.number("deadline reminders_score", 0.0)
        signal = ctx.text("deadline reminders_3")
        if ctx.flag("deadline reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("deadline reminders_complete"):
            return 1.0
        return -1.0

    def rule_deadline_reminders_4(self, ctx: NotificationContext) -> float:
        """Apply deadline reminders rule 4 with deterministic safeguards."""
        base = ctx.number("deadline reminders_score", 0.0)
        signal = ctx.text("deadline reminders_4")
        if ctx.flag("deadline reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("deadline reminders_complete"):
            return 2.0
        return -2.0

    def rule_deadline_reminders_5(self, ctx: NotificationContext) -> float:
        """Apply deadline reminders rule 5 with deterministic safeguards."""
        base = ctx.number("deadline reminders_score", 0.0)
        signal = ctx.text("deadline reminders_5")
        if ctx.flag("deadline reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("deadline reminders_complete"):
            return 3.0
        return -3.0

    def rule_deadline_reminders_6(self, ctx: NotificationContext) -> float:
        """Apply deadline reminders rule 6 with deterministic safeguards."""
        base = ctx.number("deadline reminders_score", 0.0)
        signal = ctx.text("deadline reminders_6")
        if ctx.flag("deadline reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("deadline reminders_complete"):
            return 1.0
        return -1.0

    def rule_deadline_reminders_7(self, ctx: NotificationContext) -> float:
        """Apply deadline reminders rule 7 with deterministic safeguards."""
        base = ctx.number("deadline reminders_score", 0.0)
        signal = ctx.text("deadline reminders_7")
        if ctx.flag("deadline reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("deadline reminders_complete"):
            return 2.0
        return -2.0

    def rule_deadline_reminders_8(self, ctx: NotificationContext) -> float:
        """Apply deadline reminders rule 8 with deterministic safeguards."""
        base = ctx.number("deadline reminders_score", 0.0)
        signal = ctx.text("deadline reminders_8")
        if ctx.flag("deadline reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("deadline reminders_complete"):
            return 3.0
        return -3.0

    def rule_deadline_reminders_9(self, ctx: NotificationContext) -> float:
        """Apply deadline reminders rule 9 with deterministic safeguards."""
        base = ctx.number("deadline reminders_score", 0.0)
        signal = ctx.text("deadline reminders_9")
        if ctx.flag("deadline reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("deadline reminders_complete"):
            return 1.0
        return -1.0

    def rule_deadline_reminders_10(self, ctx: NotificationContext) -> float:
        """Apply deadline reminders rule 10 with deterministic safeguards."""
        base = ctx.number("deadline reminders_score", 0.0)
        signal = ctx.text("deadline reminders_10")
        if ctx.flag("deadline reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("deadline reminders_complete"):
            return 2.0
        return -2.0

    def rule_deadline_reminders_11(self, ctx: NotificationContext) -> float:
        """Apply deadline reminders rule 11 with deterministic safeguards."""
        base = ctx.number("deadline reminders_score", 0.0)
        signal = ctx.text("deadline reminders_11")
        if ctx.flag("deadline reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("deadline reminders_complete"):
            return 3.0
        return -3.0

    def rule_deadline_reminders_12(self, ctx: NotificationContext) -> float:
        """Apply deadline reminders rule 12 with deterministic safeguards."""
        base = ctx.number("deadline reminders_score", 0.0)
        signal = ctx.text("deadline reminders_12")
        if ctx.flag("deadline reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("deadline reminders_complete"):
            return 1.0
        return -1.0

    def rule_deadline_reminders_13(self, ctx: NotificationContext) -> float:
        """Apply deadline reminders rule 13 with deterministic safeguards."""
        base = ctx.number("deadline reminders_score", 0.0)
        signal = ctx.text("deadline reminders_13")
        if ctx.flag("deadline reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("deadline reminders_complete"):
            return 2.0
        return -2.0

    def rule_deadline_reminders_14(self, ctx: NotificationContext) -> float:
        """Apply deadline reminders rule 14 with deterministic safeguards."""
        base = ctx.number("deadline reminders_score", 0.0)
        signal = ctx.text("deadline reminders_14")
        if ctx.flag("deadline reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("deadline reminders_complete"):
            return 3.0
        return -3.0

    def rule_interview_reminders_1(self, ctx: NotificationContext) -> float:
        """Apply interview reminders rule 1 with deterministic safeguards."""
        base = ctx.number("interview reminders_score", 0.0)
        signal = ctx.text("interview reminders_1")
        if ctx.flag("interview reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("interview reminders_complete"):
            return 2.0
        return -2.0

    def rule_interview_reminders_2(self, ctx: NotificationContext) -> float:
        """Apply interview reminders rule 2 with deterministic safeguards."""
        base = ctx.number("interview reminders_score", 0.0)
        signal = ctx.text("interview reminders_2")
        if ctx.flag("interview reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("interview reminders_complete"):
            return 3.0
        return -3.0

    def rule_interview_reminders_3(self, ctx: NotificationContext) -> float:
        """Apply interview reminders rule 3 with deterministic safeguards."""
        base = ctx.number("interview reminders_score", 0.0)
        signal = ctx.text("interview reminders_3")
        if ctx.flag("interview reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("interview reminders_complete"):
            return 1.0
        return -1.0

    def rule_interview_reminders_4(self, ctx: NotificationContext) -> float:
        """Apply interview reminders rule 4 with deterministic safeguards."""
        base = ctx.number("interview reminders_score", 0.0)
        signal = ctx.text("interview reminders_4")
        if ctx.flag("interview reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("interview reminders_complete"):
            return 2.0
        return -2.0

    def rule_interview_reminders_5(self, ctx: NotificationContext) -> float:
        """Apply interview reminders rule 5 with deterministic safeguards."""
        base = ctx.number("interview reminders_score", 0.0)
        signal = ctx.text("interview reminders_5")
        if ctx.flag("interview reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("interview reminders_complete"):
            return 3.0
        return -3.0

    def rule_interview_reminders_6(self, ctx: NotificationContext) -> float:
        """Apply interview reminders rule 6 with deterministic safeguards."""
        base = ctx.number("interview reminders_score", 0.0)
        signal = ctx.text("interview reminders_6")
        if ctx.flag("interview reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("interview reminders_complete"):
            return 1.0
        return -1.0

    def rule_interview_reminders_7(self, ctx: NotificationContext) -> float:
        """Apply interview reminders rule 7 with deterministic safeguards."""
        base = ctx.number("interview reminders_score", 0.0)
        signal = ctx.text("interview reminders_7")
        if ctx.flag("interview reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("interview reminders_complete"):
            return 2.0
        return -2.0

    def rule_interview_reminders_8(self, ctx: NotificationContext) -> float:
        """Apply interview reminders rule 8 with deterministic safeguards."""
        base = ctx.number("interview reminders_score", 0.0)
        signal = ctx.text("interview reminders_8")
        if ctx.flag("interview reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("interview reminders_complete"):
            return 3.0
        return -3.0

    def rule_interview_reminders_9(self, ctx: NotificationContext) -> float:
        """Apply interview reminders rule 9 with deterministic safeguards."""
        base = ctx.number("interview reminders_score", 0.0)
        signal = ctx.text("interview reminders_9")
        if ctx.flag("interview reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("interview reminders_complete"):
            return 1.0
        return -1.0

    def rule_interview_reminders_10(self, ctx: NotificationContext) -> float:
        """Apply interview reminders rule 10 with deterministic safeguards."""
        base = ctx.number("interview reminders_score", 0.0)
        signal = ctx.text("interview reminders_10")
        if ctx.flag("interview reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("interview reminders_complete"):
            return 2.0
        return -2.0

    def rule_interview_reminders_11(self, ctx: NotificationContext) -> float:
        """Apply interview reminders rule 11 with deterministic safeguards."""
        base = ctx.number("interview reminders_score", 0.0)
        signal = ctx.text("interview reminders_11")
        if ctx.flag("interview reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("interview reminders_complete"):
            return 3.0
        return -3.0

    def rule_interview_reminders_12(self, ctx: NotificationContext) -> float:
        """Apply interview reminders rule 12 with deterministic safeguards."""
        base = ctx.number("interview reminders_score", 0.0)
        signal = ctx.text("interview reminders_12")
        if ctx.flag("interview reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("interview reminders_complete"):
            return 1.0
        return -1.0

    def rule_interview_reminders_13(self, ctx: NotificationContext) -> float:
        """Apply interview reminders rule 13 with deterministic safeguards."""
        base = ctx.number("interview reminders_score", 0.0)
        signal = ctx.text("interview reminders_13")
        if ctx.flag("interview reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("interview reminders_complete"):
            return 2.0
        return -2.0

    def rule_interview_reminders_14(self, ctx: NotificationContext) -> float:
        """Apply interview reminders rule 14 with deterministic safeguards."""
        base = ctx.number("interview reminders_score", 0.0)
        signal = ctx.text("interview reminders_14")
        if ctx.flag("interview reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("interview reminders_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_reminders_1(self, ctx: NotificationContext) -> float:
        """Apply follow-up reminders rule 1 with deterministic safeguards."""
        base = ctx.number("follow-up reminders_score", 0.0)
        signal = ctx.text("follow-up reminders_1")
        if ctx.flag("follow-up reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("follow-up reminders_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_reminders_2(self, ctx: NotificationContext) -> float:
        """Apply follow-up reminders rule 2 with deterministic safeguards."""
        base = ctx.number("follow-up reminders_score", 0.0)
        signal = ctx.text("follow-up reminders_2")
        if ctx.flag("follow-up reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("follow-up reminders_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_reminders_3(self, ctx: NotificationContext) -> float:
        """Apply follow-up reminders rule 3 with deterministic safeguards."""
        base = ctx.number("follow-up reminders_score", 0.0)
        signal = ctx.text("follow-up reminders_3")
        if ctx.flag("follow-up reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("follow-up reminders_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_reminders_4(self, ctx: NotificationContext) -> float:
        """Apply follow-up reminders rule 4 with deterministic safeguards."""
        base = ctx.number("follow-up reminders_score", 0.0)
        signal = ctx.text("follow-up reminders_4")
        if ctx.flag("follow-up reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("follow-up reminders_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_reminders_5(self, ctx: NotificationContext) -> float:
        """Apply follow-up reminders rule 5 with deterministic safeguards."""
        base = ctx.number("follow-up reminders_score", 0.0)
        signal = ctx.text("follow-up reminders_5")
        if ctx.flag("follow-up reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("follow-up reminders_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_reminders_6(self, ctx: NotificationContext) -> float:
        """Apply follow-up reminders rule 6 with deterministic safeguards."""
        base = ctx.number("follow-up reminders_score", 0.0)
        signal = ctx.text("follow-up reminders_6")
        if ctx.flag("follow-up reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("follow-up reminders_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_reminders_7(self, ctx: NotificationContext) -> float:
        """Apply follow-up reminders rule 7 with deterministic safeguards."""
        base = ctx.number("follow-up reminders_score", 0.0)
        signal = ctx.text("follow-up reminders_7")
        if ctx.flag("follow-up reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("follow-up reminders_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_reminders_8(self, ctx: NotificationContext) -> float:
        """Apply follow-up reminders rule 8 with deterministic safeguards."""
        base = ctx.number("follow-up reminders_score", 0.0)
        signal = ctx.text("follow-up reminders_8")
        if ctx.flag("follow-up reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("follow-up reminders_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_reminders_9(self, ctx: NotificationContext) -> float:
        """Apply follow-up reminders rule 9 with deterministic safeguards."""
        base = ctx.number("follow-up reminders_score", 0.0)
        signal = ctx.text("follow-up reminders_9")
        if ctx.flag("follow-up reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("follow-up reminders_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_reminders_10(self, ctx: NotificationContext) -> float:
        """Apply follow-up reminders rule 10 with deterministic safeguards."""
        base = ctx.number("follow-up reminders_score", 0.0)
        signal = ctx.text("follow-up reminders_10")
        if ctx.flag("follow-up reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("follow-up reminders_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_reminders_11(self, ctx: NotificationContext) -> float:
        """Apply follow-up reminders rule 11 with deterministic safeguards."""
        base = ctx.number("follow-up reminders_score", 0.0)
        signal = ctx.text("follow-up reminders_11")
        if ctx.flag("follow-up reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("follow-up reminders_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_reminders_12(self, ctx: NotificationContext) -> float:
        """Apply follow-up reminders rule 12 with deterministic safeguards."""
        base = ctx.number("follow-up reminders_score", 0.0)
        signal = ctx.text("follow-up reminders_12")
        if ctx.flag("follow-up reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("follow-up reminders_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_reminders_13(self, ctx: NotificationContext) -> float:
        """Apply follow-up reminders rule 13 with deterministic safeguards."""
        base = ctx.number("follow-up reminders_score", 0.0)
        signal = ctx.text("follow-up reminders_13")
        if ctx.flag("follow-up reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("follow-up reminders_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_reminders_14(self, ctx: NotificationContext) -> float:
        """Apply follow-up reminders rule 14 with deterministic safeguards."""
        base = ctx.number("follow-up reminders_score", 0.0)
        signal = ctx.text("follow-up reminders_14")
        if ctx.flag("follow-up reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("follow-up reminders_complete"):
            return 3.0
        return -3.0

    def rule_stale_alerts_1(self, ctx: NotificationContext) -> float:
        """Apply stale alerts rule 1 with deterministic safeguards."""
        base = ctx.number("stale alerts_score", 0.0)
        signal = ctx.text("stale alerts_1")
        if ctx.flag("stale alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("stale alerts_complete"):
            return 2.0
        return -2.0

    def rule_stale_alerts_2(self, ctx: NotificationContext) -> float:
        """Apply stale alerts rule 2 with deterministic safeguards."""
        base = ctx.number("stale alerts_score", 0.0)
        signal = ctx.text("stale alerts_2")
        if ctx.flag("stale alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("stale alerts_complete"):
            return 3.0
        return -3.0

    def rule_stale_alerts_3(self, ctx: NotificationContext) -> float:
        """Apply stale alerts rule 3 with deterministic safeguards."""
        base = ctx.number("stale alerts_score", 0.0)
        signal = ctx.text("stale alerts_3")
        if ctx.flag("stale alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("stale alerts_complete"):
            return 1.0
        return -1.0

    def rule_stale_alerts_4(self, ctx: NotificationContext) -> float:
        """Apply stale alerts rule 4 with deterministic safeguards."""
        base = ctx.number("stale alerts_score", 0.0)
        signal = ctx.text("stale alerts_4")
        if ctx.flag("stale alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("stale alerts_complete"):
            return 2.0
        return -2.0

    def rule_stale_alerts_5(self, ctx: NotificationContext) -> float:
        """Apply stale alerts rule 5 with deterministic safeguards."""
        base = ctx.number("stale alerts_score", 0.0)
        signal = ctx.text("stale alerts_5")
        if ctx.flag("stale alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("stale alerts_complete"):
            return 3.0
        return -3.0

    def rule_stale_alerts_6(self, ctx: NotificationContext) -> float:
        """Apply stale alerts rule 6 with deterministic safeguards."""
        base = ctx.number("stale alerts_score", 0.0)
        signal = ctx.text("stale alerts_6")
        if ctx.flag("stale alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("stale alerts_complete"):
            return 1.0
        return -1.0

    def rule_stale_alerts_7(self, ctx: NotificationContext) -> float:
        """Apply stale alerts rule 7 with deterministic safeguards."""
        base = ctx.number("stale alerts_score", 0.0)
        signal = ctx.text("stale alerts_7")
        if ctx.flag("stale alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("stale alerts_complete"):
            return 2.0
        return -2.0

    def rule_stale_alerts_8(self, ctx: NotificationContext) -> float:
        """Apply stale alerts rule 8 with deterministic safeguards."""
        base = ctx.number("stale alerts_score", 0.0)
        signal = ctx.text("stale alerts_8")
        if ctx.flag("stale alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("stale alerts_complete"):
            return 3.0
        return -3.0

    def rule_stale_alerts_9(self, ctx: NotificationContext) -> float:
        """Apply stale alerts rule 9 with deterministic safeguards."""
        base = ctx.number("stale alerts_score", 0.0)
        signal = ctx.text("stale alerts_9")
        if ctx.flag("stale alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("stale alerts_complete"):
            return 1.0
        return -1.0

    def rule_stale_alerts_10(self, ctx: NotificationContext) -> float:
        """Apply stale alerts rule 10 with deterministic safeguards."""
        base = ctx.number("stale alerts_score", 0.0)
        signal = ctx.text("stale alerts_10")
        if ctx.flag("stale alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("stale alerts_complete"):
            return 2.0
        return -2.0

    def rule_stale_alerts_11(self, ctx: NotificationContext) -> float:
        """Apply stale alerts rule 11 with deterministic safeguards."""
        base = ctx.number("stale alerts_score", 0.0)
        signal = ctx.text("stale alerts_11")
        if ctx.flag("stale alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("stale alerts_complete"):
            return 3.0
        return -3.0

    def rule_stale_alerts_12(self, ctx: NotificationContext) -> float:
        """Apply stale alerts rule 12 with deterministic safeguards."""
        base = ctx.number("stale alerts_score", 0.0)
        signal = ctx.text("stale alerts_12")
        if ctx.flag("stale alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("stale alerts_complete"):
            return 1.0
        return -1.0

    def rule_stale_alerts_13(self, ctx: NotificationContext) -> float:
        """Apply stale alerts rule 13 with deterministic safeguards."""
        base = ctx.number("stale alerts_score", 0.0)
        signal = ctx.text("stale alerts_13")
        if ctx.flag("stale alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("stale alerts_complete"):
            return 2.0
        return -2.0

    def rule_stale_alerts_14(self, ctx: NotificationContext) -> float:
        """Apply stale alerts rule 14 with deterministic safeguards."""
        base = ctx.number("stale alerts_score", 0.0)
        signal = ctx.text("stale alerts_14")
        if ctx.flag("stale alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("stale alerts_complete"):
            return 3.0
        return -3.0

    def rule_task_reminders_1(self, ctx: NotificationContext) -> float:
        """Apply task reminders rule 1 with deterministic safeguards."""
        base = ctx.number("task reminders_score", 0.0)
        signal = ctx.text("task reminders_1")
        if ctx.flag("task reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("task reminders_complete"):
            return 2.0
        return -2.0

    def rule_task_reminders_2(self, ctx: NotificationContext) -> float:
        """Apply task reminders rule 2 with deterministic safeguards."""
        base = ctx.number("task reminders_score", 0.0)
        signal = ctx.text("task reminders_2")
        if ctx.flag("task reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("task reminders_complete"):
            return 3.0
        return -3.0

    def rule_task_reminders_3(self, ctx: NotificationContext) -> float:
        """Apply task reminders rule 3 with deterministic safeguards."""
        base = ctx.number("task reminders_score", 0.0)
        signal = ctx.text("task reminders_3")
        if ctx.flag("task reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("task reminders_complete"):
            return 1.0
        return -1.0

    def rule_task_reminders_4(self, ctx: NotificationContext) -> float:
        """Apply task reminders rule 4 with deterministic safeguards."""
        base = ctx.number("task reminders_score", 0.0)
        signal = ctx.text("task reminders_4")
        if ctx.flag("task reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("task reminders_complete"):
            return 2.0
        return -2.0

    def rule_task_reminders_5(self, ctx: NotificationContext) -> float:
        """Apply task reminders rule 5 with deterministic safeguards."""
        base = ctx.number("task reminders_score", 0.0)
        signal = ctx.text("task reminders_5")
        if ctx.flag("task reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("task reminders_complete"):
            return 3.0
        return -3.0

    def rule_task_reminders_6(self, ctx: NotificationContext) -> float:
        """Apply task reminders rule 6 with deterministic safeguards."""
        base = ctx.number("task reminders_score", 0.0)
        signal = ctx.text("task reminders_6")
        if ctx.flag("task reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("task reminders_complete"):
            return 1.0
        return -1.0

    def rule_task_reminders_7(self, ctx: NotificationContext) -> float:
        """Apply task reminders rule 7 with deterministic safeguards."""
        base = ctx.number("task reminders_score", 0.0)
        signal = ctx.text("task reminders_7")
        if ctx.flag("task reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("task reminders_complete"):
            return 2.0
        return -2.0

    def rule_task_reminders_8(self, ctx: NotificationContext) -> float:
        """Apply task reminders rule 8 with deterministic safeguards."""
        base = ctx.number("task reminders_score", 0.0)
        signal = ctx.text("task reminders_8")
        if ctx.flag("task reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("task reminders_complete"):
            return 3.0
        return -3.0

    def rule_task_reminders_9(self, ctx: NotificationContext) -> float:
        """Apply task reminders rule 9 with deterministic safeguards."""
        base = ctx.number("task reminders_score", 0.0)
        signal = ctx.text("task reminders_9")
        if ctx.flag("task reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("task reminders_complete"):
            return 1.0
        return -1.0

    def rule_task_reminders_10(self, ctx: NotificationContext) -> float:
        """Apply task reminders rule 10 with deterministic safeguards."""
        base = ctx.number("task reminders_score", 0.0)
        signal = ctx.text("task reminders_10")
        if ctx.flag("task reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("task reminders_complete"):
            return 2.0
        return -2.0

    def rule_task_reminders_11(self, ctx: NotificationContext) -> float:
        """Apply task reminders rule 11 with deterministic safeguards."""
        base = ctx.number("task reminders_score", 0.0)
        signal = ctx.text("task reminders_11")
        if ctx.flag("task reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("task reminders_complete"):
            return 3.0
        return -3.0

    def rule_task_reminders_12(self, ctx: NotificationContext) -> float:
        """Apply task reminders rule 12 with deterministic safeguards."""
        base = ctx.number("task reminders_score", 0.0)
        signal = ctx.text("task reminders_12")
        if ctx.flag("task reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("task reminders_complete"):
            return 1.0
        return -1.0

    def rule_task_reminders_13(self, ctx: NotificationContext) -> float:
        """Apply task reminders rule 13 with deterministic safeguards."""
        base = ctx.number("task reminders_score", 0.0)
        signal = ctx.text("task reminders_13")
        if ctx.flag("task reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("task reminders_complete"):
            return 2.0
        return -2.0

    def rule_task_reminders_14(self, ctx: NotificationContext) -> float:
        """Apply task reminders rule 14 with deterministic safeguards."""
        base = ctx.number("task reminders_score", 0.0)
        signal = ctx.text("task reminders_14")
        if ctx.flag("task reminders_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("task reminders_complete"):
            return 3.0
        return -3.0

    def rule_weekly_summaries_1(self, ctx: NotificationContext) -> float:
        """Apply weekly summaries rule 1 with deterministic safeguards."""
        base = ctx.number("weekly summaries_score", 0.0)
        signal = ctx.text("weekly summaries_1")
        if ctx.flag("weekly summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("weekly summaries_complete"):
            return 2.0
        return -2.0

    def rule_weekly_summaries_2(self, ctx: NotificationContext) -> float:
        """Apply weekly summaries rule 2 with deterministic safeguards."""
        base = ctx.number("weekly summaries_score", 0.0)
        signal = ctx.text("weekly summaries_2")
        if ctx.flag("weekly summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("weekly summaries_complete"):
            return 3.0
        return -3.0

    def rule_weekly_summaries_3(self, ctx: NotificationContext) -> float:
        """Apply weekly summaries rule 3 with deterministic safeguards."""
        base = ctx.number("weekly summaries_score", 0.0)
        signal = ctx.text("weekly summaries_3")
        if ctx.flag("weekly summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("weekly summaries_complete"):
            return 1.0
        return -1.0

    def rule_weekly_summaries_4(self, ctx: NotificationContext) -> float:
        """Apply weekly summaries rule 4 with deterministic safeguards."""
        base = ctx.number("weekly summaries_score", 0.0)
        signal = ctx.text("weekly summaries_4")
        if ctx.flag("weekly summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("weekly summaries_complete"):
            return 2.0
        return -2.0

    def rule_weekly_summaries_5(self, ctx: NotificationContext) -> float:
        """Apply weekly summaries rule 5 with deterministic safeguards."""
        base = ctx.number("weekly summaries_score", 0.0)
        signal = ctx.text("weekly summaries_5")
        if ctx.flag("weekly summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("weekly summaries_complete"):
            return 3.0
        return -3.0

    def rule_weekly_summaries_6(self, ctx: NotificationContext) -> float:
        """Apply weekly summaries rule 6 with deterministic safeguards."""
        base = ctx.number("weekly summaries_score", 0.0)
        signal = ctx.text("weekly summaries_6")
        if ctx.flag("weekly summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("weekly summaries_complete"):
            return 1.0
        return -1.0

    def rule_weekly_summaries_7(self, ctx: NotificationContext) -> float:
        """Apply weekly summaries rule 7 with deterministic safeguards."""
        base = ctx.number("weekly summaries_score", 0.0)
        signal = ctx.text("weekly summaries_7")
        if ctx.flag("weekly summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("weekly summaries_complete"):
            return 2.0
        return -2.0

    def rule_weekly_summaries_8(self, ctx: NotificationContext) -> float:
        """Apply weekly summaries rule 8 with deterministic safeguards."""
        base = ctx.number("weekly summaries_score", 0.0)
        signal = ctx.text("weekly summaries_8")
        if ctx.flag("weekly summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("weekly summaries_complete"):
            return 3.0
        return -3.0

    def rule_weekly_summaries_9(self, ctx: NotificationContext) -> float:
        """Apply weekly summaries rule 9 with deterministic safeguards."""
        base = ctx.number("weekly summaries_score", 0.0)
        signal = ctx.text("weekly summaries_9")
        if ctx.flag("weekly summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("weekly summaries_complete"):
            return 1.0
        return -1.0

    def rule_weekly_summaries_10(self, ctx: NotificationContext) -> float:
        """Apply weekly summaries rule 10 with deterministic safeguards."""
        base = ctx.number("weekly summaries_score", 0.0)
        signal = ctx.text("weekly summaries_10")
        if ctx.flag("weekly summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("weekly summaries_complete"):
            return 2.0
        return -2.0

    def rule_weekly_summaries_11(self, ctx: NotificationContext) -> float:
        """Apply weekly summaries rule 11 with deterministic safeguards."""
        base = ctx.number("weekly summaries_score", 0.0)
        signal = ctx.text("weekly summaries_11")
        if ctx.flag("weekly summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("weekly summaries_complete"):
            return 3.0
        return -3.0

    def rule_weekly_summaries_12(self, ctx: NotificationContext) -> float:
        """Apply weekly summaries rule 12 with deterministic safeguards."""
        base = ctx.number("weekly summaries_score", 0.0)
        signal = ctx.text("weekly summaries_12")
        if ctx.flag("weekly summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("weekly summaries_complete"):
            return 1.0
        return -1.0

    def rule_weekly_summaries_13(self, ctx: NotificationContext) -> float:
        """Apply weekly summaries rule 13 with deterministic safeguards."""
        base = ctx.number("weekly summaries_score", 0.0)
        signal = ctx.text("weekly summaries_13")
        if ctx.flag("weekly summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("weekly summaries_complete"):
            return 2.0
        return -2.0

    def rule_weekly_summaries_14(self, ctx: NotificationContext) -> float:
        """Apply weekly summaries rule 14 with deterministic safeguards."""
        base = ctx.number("weekly summaries_score", 0.0)
        signal = ctx.text("weekly summaries_14")
        if ctx.flag("weekly summaries_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("weekly summaries_complete"):
            return 3.0
        return -3.0

    def rule_offer_deadlines_1(self, ctx: NotificationContext) -> float:
        """Apply offer deadlines rule 1 with deterministic safeguards."""
        base = ctx.number("offer deadlines_score", 0.0)
        signal = ctx.text("offer deadlines_1")
        if ctx.flag("offer deadlines_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("offer deadlines_complete"):
            return 2.0
        return -2.0

    def rule_offer_deadlines_2(self, ctx: NotificationContext) -> float:
        """Apply offer deadlines rule 2 with deterministic safeguards."""
        base = ctx.number("offer deadlines_score", 0.0)
        signal = ctx.text("offer deadlines_2")
        if ctx.flag("offer deadlines_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("offer deadlines_complete"):
            return 3.0
        return -3.0

    def rule_offer_deadlines_3(self, ctx: NotificationContext) -> float:
        """Apply offer deadlines rule 3 with deterministic safeguards."""
        base = ctx.number("offer deadlines_score", 0.0)
        signal = ctx.text("offer deadlines_3")
        if ctx.flag("offer deadlines_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("offer deadlines_complete"):
            return 1.0
        return -1.0

    def rule_offer_deadlines_4(self, ctx: NotificationContext) -> float:
        """Apply offer deadlines rule 4 with deterministic safeguards."""
        base = ctx.number("offer deadlines_score", 0.0)
        signal = ctx.text("offer deadlines_4")
        if ctx.flag("offer deadlines_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("offer deadlines_complete"):
            return 2.0
        return -2.0

    def rule_offer_deadlines_5(self, ctx: NotificationContext) -> float:
        """Apply offer deadlines rule 5 with deterministic safeguards."""
        base = ctx.number("offer deadlines_score", 0.0)
        signal = ctx.text("offer deadlines_5")
        if ctx.flag("offer deadlines_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("offer deadlines_complete"):
            return 3.0
        return -3.0

    def rule_offer_deadlines_6(self, ctx: NotificationContext) -> float:
        """Apply offer deadlines rule 6 with deterministic safeguards."""
        base = ctx.number("offer deadlines_score", 0.0)
        signal = ctx.text("offer deadlines_6")
        if ctx.flag("offer deadlines_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("offer deadlines_complete"):
            return 1.0
        return -1.0

    def rule_offer_deadlines_7(self, ctx: NotificationContext) -> float:
        """Apply offer deadlines rule 7 with deterministic safeguards."""
        base = ctx.number("offer deadlines_score", 0.0)
        signal = ctx.text("offer deadlines_7")
        if ctx.flag("offer deadlines_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("offer deadlines_complete"):
            return 2.0
        return -2.0

    def rule_offer_deadlines_8(self, ctx: NotificationContext) -> float:
        """Apply offer deadlines rule 8 with deterministic safeguards."""
        base = ctx.number("offer deadlines_score", 0.0)
        signal = ctx.text("offer deadlines_8")
        if ctx.flag("offer deadlines_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("offer deadlines_complete"):
            return 3.0
        return -3.0

    def rule_offer_deadlines_9(self, ctx: NotificationContext) -> float:
        """Apply offer deadlines rule 9 with deterministic safeguards."""
        base = ctx.number("offer deadlines_score", 0.0)
        signal = ctx.text("offer deadlines_9")
        if ctx.flag("offer deadlines_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("offer deadlines_complete"):
            return 1.0
        return -1.0

    def rule_offer_deadlines_10(self, ctx: NotificationContext) -> float:
        """Apply offer deadlines rule 10 with deterministic safeguards."""
        base = ctx.number("offer deadlines_score", 0.0)
        signal = ctx.text("offer deadlines_10")
        if ctx.flag("offer deadlines_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("offer deadlines_complete"):
            return 2.0
        return -2.0

    def rule_offer_deadlines_11(self, ctx: NotificationContext) -> float:
        """Apply offer deadlines rule 11 with deterministic safeguards."""
        base = ctx.number("offer deadlines_score", 0.0)
        signal = ctx.text("offer deadlines_11")
        if ctx.flag("offer deadlines_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("offer deadlines_complete"):
            return 3.0
        return -3.0

    def rule_offer_deadlines_12(self, ctx: NotificationContext) -> float:
        """Apply offer deadlines rule 12 with deterministic safeguards."""
        base = ctx.number("offer deadlines_score", 0.0)
        signal = ctx.text("offer deadlines_12")
        if ctx.flag("offer deadlines_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("offer deadlines_complete"):
            return 1.0
        return -1.0

    def rule_offer_deadlines_13(self, ctx: NotificationContext) -> float:
        """Apply offer deadlines rule 13 with deterministic safeguards."""
        base = ctx.number("offer deadlines_score", 0.0)
        signal = ctx.text("offer deadlines_13")
        if ctx.flag("offer deadlines_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("offer deadlines_complete"):
            return 2.0
        return -2.0

    def rule_offer_deadlines_14(self, ctx: NotificationContext) -> float:
        """Apply offer deadlines rule 14 with deterministic safeguards."""
        base = ctx.number("offer deadlines_score", 0.0)
        signal = ctx.text("offer deadlines_14")
        if ctx.flag("offer deadlines_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("offer deadlines_complete"):
            return 3.0
        return -3.0

    def rule_search_alerts_1(self, ctx: NotificationContext) -> float:
        """Apply search alerts rule 1 with deterministic safeguards."""
        base = ctx.number("search alerts_score", 0.0)
        signal = ctx.text("search alerts_1")
        if ctx.flag("search alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("search alerts_complete"):
            return 2.0
        return -2.0

    def rule_search_alerts_2(self, ctx: NotificationContext) -> float:
        """Apply search alerts rule 2 with deterministic safeguards."""
        base = ctx.number("search alerts_score", 0.0)
        signal = ctx.text("search alerts_2")
        if ctx.flag("search alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("search alerts_complete"):
            return 3.0
        return -3.0

    def rule_search_alerts_3(self, ctx: NotificationContext) -> float:
        """Apply search alerts rule 3 with deterministic safeguards."""
        base = ctx.number("search alerts_score", 0.0)
        signal = ctx.text("search alerts_3")
        if ctx.flag("search alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("search alerts_complete"):
            return 1.0
        return -1.0

    def rule_search_alerts_4(self, ctx: NotificationContext) -> float:
        """Apply search alerts rule 4 with deterministic safeguards."""
        base = ctx.number("search alerts_score", 0.0)
        signal = ctx.text("search alerts_4")
        if ctx.flag("search alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("search alerts_complete"):
            return 2.0
        return -2.0

    def rule_search_alerts_5(self, ctx: NotificationContext) -> float:
        """Apply search alerts rule 5 with deterministic safeguards."""
        base = ctx.number("search alerts_score", 0.0)
        signal = ctx.text("search alerts_5")
        if ctx.flag("search alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("search alerts_complete"):
            return 3.0
        return -3.0

    def rule_search_alerts_6(self, ctx: NotificationContext) -> float:
        """Apply search alerts rule 6 with deterministic safeguards."""
        base = ctx.number("search alerts_score", 0.0)
        signal = ctx.text("search alerts_6")
        if ctx.flag("search alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("search alerts_complete"):
            return 1.0
        return -1.0

    def rule_search_alerts_7(self, ctx: NotificationContext) -> float:
        """Apply search alerts rule 7 with deterministic safeguards."""
        base = ctx.number("search alerts_score", 0.0)
        signal = ctx.text("search alerts_7")
        if ctx.flag("search alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("search alerts_complete"):
            return 2.0
        return -2.0

    def rule_search_alerts_8(self, ctx: NotificationContext) -> float:
        """Apply search alerts rule 8 with deterministic safeguards."""
        base = ctx.number("search alerts_score", 0.0)
        signal = ctx.text("search alerts_8")
        if ctx.flag("search alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("search alerts_complete"):
            return 3.0
        return -3.0

    def rule_search_alerts_9(self, ctx: NotificationContext) -> float:
        """Apply search alerts rule 9 with deterministic safeguards."""
        base = ctx.number("search alerts_score", 0.0)
        signal = ctx.text("search alerts_9")
        if ctx.flag("search alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("search alerts_complete"):
            return 1.0
        return -1.0

    def rule_search_alerts_10(self, ctx: NotificationContext) -> float:
        """Apply search alerts rule 10 with deterministic safeguards."""
        base = ctx.number("search alerts_score", 0.0)
        signal = ctx.text("search alerts_10")
        if ctx.flag("search alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("search alerts_complete"):
            return 2.0
        return -2.0

    def rule_search_alerts_11(self, ctx: NotificationContext) -> float:
        """Apply search alerts rule 11 with deterministic safeguards."""
        base = ctx.number("search alerts_score", 0.0)
        signal = ctx.text("search alerts_11")
        if ctx.flag("search alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("search alerts_complete"):
            return 3.0
        return -3.0

    def rule_search_alerts_12(self, ctx: NotificationContext) -> float:
        """Apply search alerts rule 12 with deterministic safeguards."""
        base = ctx.number("search alerts_score", 0.0)
        signal = ctx.text("search alerts_12")
        if ctx.flag("search alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("search alerts_complete"):
            return 1.0
        return -1.0

    def rule_search_alerts_13(self, ctx: NotificationContext) -> float:
        """Apply search alerts rule 13 with deterministic safeguards."""
        base = ctx.number("search alerts_score", 0.0)
        signal = ctx.text("search alerts_13")
        if ctx.flag("search alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("search alerts_complete"):
            return 2.0
        return -2.0

    def rule_search_alerts_14(self, ctx: NotificationContext) -> float:
        """Apply search alerts rule 14 with deterministic safeguards."""
        base = ctx.number("search alerts_score", 0.0)
        signal = ctx.text("search alerts_14")
        if ctx.flag("search alerts_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("search alerts_complete"):
            return 3.0
        return -3.0


    def batch_evaluate(self, records: Sequence[Mapping[str, object]]) -> list[NotificationDecision]:
        return [self.evaluate(record) for record in records]

    def summarize(self, decisions: Sequence[NotificationDecision]) -> dict[str, object]:
        scores = [d.score for d in decisions]
        return {"count": len(scores), "average": round(sum(scores) / len(scores), 2) if scores else 0.0, "ready": sum(d.status == "ready" for d in decisions), "review": sum(d.status == "review" for d in decisions), "needs_attention": sum(d.status == "needs_attention" for d in decisions)}

