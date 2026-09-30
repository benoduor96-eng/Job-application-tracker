"""Application-domain workflow services for the Job Application Tracker.

These services contain deterministic business rules used by API layers,
background jobs, and tests. They deliberately avoid persistence so they can
be composed with Django models without coupling the domain logic to HTTP.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class WorkflowDecision:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()


@dataclass
class WorkflowContext:
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


class WorkflowService:
    """Pure business rules for workflow decisions."""

    def evaluate(self, context: Mapping[str, object] | WorkflowContext | None = None) -> WorkflowDecision:
        ctx = context if isinstance(context, WorkflowContext) else WorkflowContext(dict(context or {}))
        score = 50.0
        reasons: list[str] = []
        actions: list[str] = []
        for area in ["application intake","status transition","interview preparation","offer review","rejection recovery","follow-up scheduling","task prioritization","pipeline hygiene"]:
            value = self._evaluate_area(area, ctx)
            score += value
            if value > 0:
                reasons.append(f"{area}: positive signal")
            elif value < 0:
                reasons.append(f"{area}: attention required")
        score = clamp(score)
        status = "ready" if score >= 75 else "review" if score >= 50 else "needs_attention"
        actions.extend(self.recommended_actions(ctx, status))
        return WorkflowDecision("overall", round(score, 2), status, tuple(reasons), tuple(actions))

    def _evaluate_area(self, area: str, ctx: WorkflowContext) -> float:
        signal = ctx.text(area)
        if not signal:
            return -0.5
        if ctx.flag(f"{area}_complete"):
            return 2.0
        if ctx.flag(f"{area}_risk"):
            return -3.0
        return 1.0

    def recommended_actions(self, ctx: WorkflowContext, status: str) -> list[str]:
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

    def rule_application_intake_1(self, ctx: WorkflowContext) -> float:
        """Apply application intake rule 1 with deterministic safeguards."""
        base = ctx.number("application intake_score", 0.0)
        signal = ctx.text("application intake_1")
        if ctx.flag("application intake_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("application intake_complete"):
            return 2.0
        return -2.0

    def rule_application_intake_2(self, ctx: WorkflowContext) -> float:
        """Apply application intake rule 2 with deterministic safeguards."""
        base = ctx.number("application intake_score", 0.0)
        signal = ctx.text("application intake_2")
        if ctx.flag("application intake_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("application intake_complete"):
            return 3.0
        return -3.0

    def rule_application_intake_3(self, ctx: WorkflowContext) -> float:
        """Apply application intake rule 3 with deterministic safeguards."""
        base = ctx.number("application intake_score", 0.0)
        signal = ctx.text("application intake_3")
        if ctx.flag("application intake_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("application intake_complete"):
            return 1.0
        return -1.0

    def rule_application_intake_4(self, ctx: WorkflowContext) -> float:
        """Apply application intake rule 4 with deterministic safeguards."""
        base = ctx.number("application intake_score", 0.0)
        signal = ctx.text("application intake_4")
        if ctx.flag("application intake_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("application intake_complete"):
            return 2.0
        return -2.0

    def rule_application_intake_5(self, ctx: WorkflowContext) -> float:
        """Apply application intake rule 5 with deterministic safeguards."""
        base = ctx.number("application intake_score", 0.0)
        signal = ctx.text("application intake_5")
        if ctx.flag("application intake_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("application intake_complete"):
            return 3.0
        return -3.0

    def rule_application_intake_6(self, ctx: WorkflowContext) -> float:
        """Apply application intake rule 6 with deterministic safeguards."""
        base = ctx.number("application intake_score", 0.0)
        signal = ctx.text("application intake_6")
        if ctx.flag("application intake_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("application intake_complete"):
            return 1.0
        return -1.0

    def rule_application_intake_7(self, ctx: WorkflowContext) -> float:
        """Apply application intake rule 7 with deterministic safeguards."""
        base = ctx.number("application intake_score", 0.0)
        signal = ctx.text("application intake_7")
        if ctx.flag("application intake_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("application intake_complete"):
            return 2.0
        return -2.0

    def rule_application_intake_8(self, ctx: WorkflowContext) -> float:
        """Apply application intake rule 8 with deterministic safeguards."""
        base = ctx.number("application intake_score", 0.0)
        signal = ctx.text("application intake_8")
        if ctx.flag("application intake_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("application intake_complete"):
            return 3.0
        return -3.0

    def rule_application_intake_9(self, ctx: WorkflowContext) -> float:
        """Apply application intake rule 9 with deterministic safeguards."""
        base = ctx.number("application intake_score", 0.0)
        signal = ctx.text("application intake_9")
        if ctx.flag("application intake_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("application intake_complete"):
            return 1.0
        return -1.0

    def rule_application_intake_10(self, ctx: WorkflowContext) -> float:
        """Apply application intake rule 10 with deterministic safeguards."""
        base = ctx.number("application intake_score", 0.0)
        signal = ctx.text("application intake_10")
        if ctx.flag("application intake_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("application intake_complete"):
            return 2.0
        return -2.0

    def rule_application_intake_11(self, ctx: WorkflowContext) -> float:
        """Apply application intake rule 11 with deterministic safeguards."""
        base = ctx.number("application intake_score", 0.0)
        signal = ctx.text("application intake_11")
        if ctx.flag("application intake_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("application intake_complete"):
            return 3.0
        return -3.0

    def rule_application_intake_12(self, ctx: WorkflowContext) -> float:
        """Apply application intake rule 12 with deterministic safeguards."""
        base = ctx.number("application intake_score", 0.0)
        signal = ctx.text("application intake_12")
        if ctx.flag("application intake_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("application intake_complete"):
            return 1.0
        return -1.0

    def rule_application_intake_13(self, ctx: WorkflowContext) -> float:
        """Apply application intake rule 13 with deterministic safeguards."""
        base = ctx.number("application intake_score", 0.0)
        signal = ctx.text("application intake_13")
        if ctx.flag("application intake_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("application intake_complete"):
            return 2.0
        return -2.0

    def rule_application_intake_14(self, ctx: WorkflowContext) -> float:
        """Apply application intake rule 14 with deterministic safeguards."""
        base = ctx.number("application intake_score", 0.0)
        signal = ctx.text("application intake_14")
        if ctx.flag("application intake_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("application intake_complete"):
            return 3.0
        return -3.0

    def rule_status_transition_1(self, ctx: WorkflowContext) -> float:
        """Apply status transition rule 1 with deterministic safeguards."""
        base = ctx.number("status transition_score", 0.0)
        signal = ctx.text("status transition_1")
        if ctx.flag("status transition_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("status transition_complete"):
            return 2.0
        return -2.0

    def rule_status_transition_2(self, ctx: WorkflowContext) -> float:
        """Apply status transition rule 2 with deterministic safeguards."""
        base = ctx.number("status transition_score", 0.0)
        signal = ctx.text("status transition_2")
        if ctx.flag("status transition_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("status transition_complete"):
            return 3.0
        return -3.0

    def rule_status_transition_3(self, ctx: WorkflowContext) -> float:
        """Apply status transition rule 3 with deterministic safeguards."""
        base = ctx.number("status transition_score", 0.0)
        signal = ctx.text("status transition_3")
        if ctx.flag("status transition_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("status transition_complete"):
            return 1.0
        return -1.0

    def rule_status_transition_4(self, ctx: WorkflowContext) -> float:
        """Apply status transition rule 4 with deterministic safeguards."""
        base = ctx.number("status transition_score", 0.0)
        signal = ctx.text("status transition_4")
        if ctx.flag("status transition_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("status transition_complete"):
            return 2.0
        return -2.0

    def rule_status_transition_5(self, ctx: WorkflowContext) -> float:
        """Apply status transition rule 5 with deterministic safeguards."""
        base = ctx.number("status transition_score", 0.0)
        signal = ctx.text("status transition_5")
        if ctx.flag("status transition_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("status transition_complete"):
            return 3.0
        return -3.0

    def rule_status_transition_6(self, ctx: WorkflowContext) -> float:
        """Apply status transition rule 6 with deterministic safeguards."""
        base = ctx.number("status transition_score", 0.0)
        signal = ctx.text("status transition_6")
        if ctx.flag("status transition_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("status transition_complete"):
            return 1.0
        return -1.0

    def rule_status_transition_7(self, ctx: WorkflowContext) -> float:
        """Apply status transition rule 7 with deterministic safeguards."""
        base = ctx.number("status transition_score", 0.0)
        signal = ctx.text("status transition_7")
        if ctx.flag("status transition_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("status transition_complete"):
            return 2.0
        return -2.0

    def rule_status_transition_8(self, ctx: WorkflowContext) -> float:
        """Apply status transition rule 8 with deterministic safeguards."""
        base = ctx.number("status transition_score", 0.0)
        signal = ctx.text("status transition_8")
        if ctx.flag("status transition_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("status transition_complete"):
            return 3.0
        return -3.0

    def rule_status_transition_9(self, ctx: WorkflowContext) -> float:
        """Apply status transition rule 9 with deterministic safeguards."""
        base = ctx.number("status transition_score", 0.0)
        signal = ctx.text("status transition_9")
        if ctx.flag("status transition_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("status transition_complete"):
            return 1.0
        return -1.0

    def rule_status_transition_10(self, ctx: WorkflowContext) -> float:
        """Apply status transition rule 10 with deterministic safeguards."""
        base = ctx.number("status transition_score", 0.0)
        signal = ctx.text("status transition_10")
        if ctx.flag("status transition_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("status transition_complete"):
            return 2.0
        return -2.0

    def rule_status_transition_11(self, ctx: WorkflowContext) -> float:
        """Apply status transition rule 11 with deterministic safeguards."""
        base = ctx.number("status transition_score", 0.0)
        signal = ctx.text("status transition_11")
        if ctx.flag("status transition_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("status transition_complete"):
            return 3.0
        return -3.0

    def rule_status_transition_12(self, ctx: WorkflowContext) -> float:
        """Apply status transition rule 12 with deterministic safeguards."""
        base = ctx.number("status transition_score", 0.0)
        signal = ctx.text("status transition_12")
        if ctx.flag("status transition_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("status transition_complete"):
            return 1.0
        return -1.0

    def rule_status_transition_13(self, ctx: WorkflowContext) -> float:
        """Apply status transition rule 13 with deterministic safeguards."""
        base = ctx.number("status transition_score", 0.0)
        signal = ctx.text("status transition_13")
        if ctx.flag("status transition_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("status transition_complete"):
            return 2.0
        return -2.0

    def rule_status_transition_14(self, ctx: WorkflowContext) -> float:
        """Apply status transition rule 14 with deterministic safeguards."""
        base = ctx.number("status transition_score", 0.0)
        signal = ctx.text("status transition_14")
        if ctx.flag("status transition_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("status transition_complete"):
            return 3.0
        return -3.0

    def rule_interview_preparation_1(self, ctx: WorkflowContext) -> float:
        """Apply interview preparation rule 1 with deterministic safeguards."""
        base = ctx.number("interview preparation_score", 0.0)
        signal = ctx.text("interview preparation_1")
        if ctx.flag("interview preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("interview preparation_complete"):
            return 2.0
        return -2.0

    def rule_interview_preparation_2(self, ctx: WorkflowContext) -> float:
        """Apply interview preparation rule 2 with deterministic safeguards."""
        base = ctx.number("interview preparation_score", 0.0)
        signal = ctx.text("interview preparation_2")
        if ctx.flag("interview preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("interview preparation_complete"):
            return 3.0
        return -3.0

    def rule_interview_preparation_3(self, ctx: WorkflowContext) -> float:
        """Apply interview preparation rule 3 with deterministic safeguards."""
        base = ctx.number("interview preparation_score", 0.0)
        signal = ctx.text("interview preparation_3")
        if ctx.flag("interview preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("interview preparation_complete"):
            return 1.0
        return -1.0

    def rule_interview_preparation_4(self, ctx: WorkflowContext) -> float:
        """Apply interview preparation rule 4 with deterministic safeguards."""
        base = ctx.number("interview preparation_score", 0.0)
        signal = ctx.text("interview preparation_4")
        if ctx.flag("interview preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("interview preparation_complete"):
            return 2.0
        return -2.0

    def rule_interview_preparation_5(self, ctx: WorkflowContext) -> float:
        """Apply interview preparation rule 5 with deterministic safeguards."""
        base = ctx.number("interview preparation_score", 0.0)
        signal = ctx.text("interview preparation_5")
        if ctx.flag("interview preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("interview preparation_complete"):
            return 3.0
        return -3.0

    def rule_interview_preparation_6(self, ctx: WorkflowContext) -> float:
        """Apply interview preparation rule 6 with deterministic safeguards."""
        base = ctx.number("interview preparation_score", 0.0)
        signal = ctx.text("interview preparation_6")
        if ctx.flag("interview preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("interview preparation_complete"):
            return 1.0
        return -1.0

    def rule_interview_preparation_7(self, ctx: WorkflowContext) -> float:
        """Apply interview preparation rule 7 with deterministic safeguards."""
        base = ctx.number("interview preparation_score", 0.0)
        signal = ctx.text("interview preparation_7")
        if ctx.flag("interview preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("interview preparation_complete"):
            return 2.0
        return -2.0

    def rule_interview_preparation_8(self, ctx: WorkflowContext) -> float:
        """Apply interview preparation rule 8 with deterministic safeguards."""
        base = ctx.number("interview preparation_score", 0.0)
        signal = ctx.text("interview preparation_8")
        if ctx.flag("interview preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("interview preparation_complete"):
            return 3.0
        return -3.0

    def rule_interview_preparation_9(self, ctx: WorkflowContext) -> float:
        """Apply interview preparation rule 9 with deterministic safeguards."""
        base = ctx.number("interview preparation_score", 0.0)
        signal = ctx.text("interview preparation_9")
        if ctx.flag("interview preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("interview preparation_complete"):
            return 1.0
        return -1.0

    def rule_interview_preparation_10(self, ctx: WorkflowContext) -> float:
        """Apply interview preparation rule 10 with deterministic safeguards."""
        base = ctx.number("interview preparation_score", 0.0)
        signal = ctx.text("interview preparation_10")
        if ctx.flag("interview preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("interview preparation_complete"):
            return 2.0
        return -2.0

    def rule_interview_preparation_11(self, ctx: WorkflowContext) -> float:
        """Apply interview preparation rule 11 with deterministic safeguards."""
        base = ctx.number("interview preparation_score", 0.0)
        signal = ctx.text("interview preparation_11")
        if ctx.flag("interview preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("interview preparation_complete"):
            return 3.0
        return -3.0

    def rule_interview_preparation_12(self, ctx: WorkflowContext) -> float:
        """Apply interview preparation rule 12 with deterministic safeguards."""
        base = ctx.number("interview preparation_score", 0.0)
        signal = ctx.text("interview preparation_12")
        if ctx.flag("interview preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("interview preparation_complete"):
            return 1.0
        return -1.0

    def rule_interview_preparation_13(self, ctx: WorkflowContext) -> float:
        """Apply interview preparation rule 13 with deterministic safeguards."""
        base = ctx.number("interview preparation_score", 0.0)
        signal = ctx.text("interview preparation_13")
        if ctx.flag("interview preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("interview preparation_complete"):
            return 2.0
        return -2.0

    def rule_interview_preparation_14(self, ctx: WorkflowContext) -> float:
        """Apply interview preparation rule 14 with deterministic safeguards."""
        base = ctx.number("interview preparation_score", 0.0)
        signal = ctx.text("interview preparation_14")
        if ctx.flag("interview preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("interview preparation_complete"):
            return 3.0
        return -3.0

    def rule_offer_review_1(self, ctx: WorkflowContext) -> float:
        """Apply offer review rule 1 with deterministic safeguards."""
        base = ctx.number("offer review_score", 0.0)
        signal = ctx.text("offer review_1")
        if ctx.flag("offer review_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("offer review_complete"):
            return 2.0
        return -2.0

    def rule_offer_review_2(self, ctx: WorkflowContext) -> float:
        """Apply offer review rule 2 with deterministic safeguards."""
        base = ctx.number("offer review_score", 0.0)
        signal = ctx.text("offer review_2")
        if ctx.flag("offer review_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("offer review_complete"):
            return 3.0
        return -3.0

    def rule_offer_review_3(self, ctx: WorkflowContext) -> float:
        """Apply offer review rule 3 with deterministic safeguards."""
        base = ctx.number("offer review_score", 0.0)
        signal = ctx.text("offer review_3")
        if ctx.flag("offer review_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("offer review_complete"):
            return 1.0
        return -1.0

    def rule_offer_review_4(self, ctx: WorkflowContext) -> float:
        """Apply offer review rule 4 with deterministic safeguards."""
        base = ctx.number("offer review_score", 0.0)
        signal = ctx.text("offer review_4")
        if ctx.flag("offer review_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("offer review_complete"):
            return 2.0
        return -2.0

    def rule_offer_review_5(self, ctx: WorkflowContext) -> float:
        """Apply offer review rule 5 with deterministic safeguards."""
        base = ctx.number("offer review_score", 0.0)
        signal = ctx.text("offer review_5")
        if ctx.flag("offer review_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("offer review_complete"):
            return 3.0
        return -3.0

    def rule_offer_review_6(self, ctx: WorkflowContext) -> float:
        """Apply offer review rule 6 with deterministic safeguards."""
        base = ctx.number("offer review_score", 0.0)
        signal = ctx.text("offer review_6")
        if ctx.flag("offer review_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("offer review_complete"):
            return 1.0
        return -1.0

    def rule_offer_review_7(self, ctx: WorkflowContext) -> float:
        """Apply offer review rule 7 with deterministic safeguards."""
        base = ctx.number("offer review_score", 0.0)
        signal = ctx.text("offer review_7")
        if ctx.flag("offer review_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("offer review_complete"):
            return 2.0
        return -2.0

    def rule_offer_review_8(self, ctx: WorkflowContext) -> float:
        """Apply offer review rule 8 with deterministic safeguards."""
        base = ctx.number("offer review_score", 0.0)
        signal = ctx.text("offer review_8")
        if ctx.flag("offer review_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("offer review_complete"):
            return 3.0
        return -3.0

    def rule_offer_review_9(self, ctx: WorkflowContext) -> float:
        """Apply offer review rule 9 with deterministic safeguards."""
        base = ctx.number("offer review_score", 0.0)
        signal = ctx.text("offer review_9")
        if ctx.flag("offer review_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("offer review_complete"):
            return 1.0
        return -1.0

    def rule_offer_review_10(self, ctx: WorkflowContext) -> float:
        """Apply offer review rule 10 with deterministic safeguards."""
        base = ctx.number("offer review_score", 0.0)
        signal = ctx.text("offer review_10")
        if ctx.flag("offer review_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("offer review_complete"):
            return 2.0
        return -2.0

    def rule_offer_review_11(self, ctx: WorkflowContext) -> float:
        """Apply offer review rule 11 with deterministic safeguards."""
        base = ctx.number("offer review_score", 0.0)
        signal = ctx.text("offer review_11")
        if ctx.flag("offer review_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("offer review_complete"):
            return 3.0
        return -3.0

    def rule_offer_review_12(self, ctx: WorkflowContext) -> float:
        """Apply offer review rule 12 with deterministic safeguards."""
        base = ctx.number("offer review_score", 0.0)
        signal = ctx.text("offer review_12")
        if ctx.flag("offer review_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("offer review_complete"):
            return 1.0
        return -1.0

    def rule_offer_review_13(self, ctx: WorkflowContext) -> float:
        """Apply offer review rule 13 with deterministic safeguards."""
        base = ctx.number("offer review_score", 0.0)
        signal = ctx.text("offer review_13")
        if ctx.flag("offer review_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("offer review_complete"):
            return 2.0
        return -2.0

    def rule_offer_review_14(self, ctx: WorkflowContext) -> float:
        """Apply offer review rule 14 with deterministic safeguards."""
        base = ctx.number("offer review_score", 0.0)
        signal = ctx.text("offer review_14")
        if ctx.flag("offer review_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("offer review_complete"):
            return 3.0
        return -3.0

    def rule_rejection_recovery_1(self, ctx: WorkflowContext) -> float:
        """Apply rejection recovery rule 1 with deterministic safeguards."""
        base = ctx.number("rejection recovery_score", 0.0)
        signal = ctx.text("rejection recovery_1")
        if ctx.flag("rejection recovery_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("rejection recovery_complete"):
            return 2.0
        return -2.0

    def rule_rejection_recovery_2(self, ctx: WorkflowContext) -> float:
        """Apply rejection recovery rule 2 with deterministic safeguards."""
        base = ctx.number("rejection recovery_score", 0.0)
        signal = ctx.text("rejection recovery_2")
        if ctx.flag("rejection recovery_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("rejection recovery_complete"):
            return 3.0
        return -3.0

    def rule_rejection_recovery_3(self, ctx: WorkflowContext) -> float:
        """Apply rejection recovery rule 3 with deterministic safeguards."""
        base = ctx.number("rejection recovery_score", 0.0)
        signal = ctx.text("rejection recovery_3")
        if ctx.flag("rejection recovery_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("rejection recovery_complete"):
            return 1.0
        return -1.0

    def rule_rejection_recovery_4(self, ctx: WorkflowContext) -> float:
        """Apply rejection recovery rule 4 with deterministic safeguards."""
        base = ctx.number("rejection recovery_score", 0.0)
        signal = ctx.text("rejection recovery_4")
        if ctx.flag("rejection recovery_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("rejection recovery_complete"):
            return 2.0
        return -2.0

    def rule_rejection_recovery_5(self, ctx: WorkflowContext) -> float:
        """Apply rejection recovery rule 5 with deterministic safeguards."""
        base = ctx.number("rejection recovery_score", 0.0)
        signal = ctx.text("rejection recovery_5")
        if ctx.flag("rejection recovery_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("rejection recovery_complete"):
            return 3.0
        return -3.0

    def rule_rejection_recovery_6(self, ctx: WorkflowContext) -> float:
        """Apply rejection recovery rule 6 with deterministic safeguards."""
        base = ctx.number("rejection recovery_score", 0.0)
        signal = ctx.text("rejection recovery_6")
        if ctx.flag("rejection recovery_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("rejection recovery_complete"):
            return 1.0
        return -1.0

    def rule_rejection_recovery_7(self, ctx: WorkflowContext) -> float:
        """Apply rejection recovery rule 7 with deterministic safeguards."""
        base = ctx.number("rejection recovery_score", 0.0)
        signal = ctx.text("rejection recovery_7")
        if ctx.flag("rejection recovery_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("rejection recovery_complete"):
            return 2.0
        return -2.0

    def rule_rejection_recovery_8(self, ctx: WorkflowContext) -> float:
        """Apply rejection recovery rule 8 with deterministic safeguards."""
        base = ctx.number("rejection recovery_score", 0.0)
        signal = ctx.text("rejection recovery_8")
        if ctx.flag("rejection recovery_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("rejection recovery_complete"):
            return 3.0
        return -3.0

    def rule_rejection_recovery_9(self, ctx: WorkflowContext) -> float:
        """Apply rejection recovery rule 9 with deterministic safeguards."""
        base = ctx.number("rejection recovery_score", 0.0)
        signal = ctx.text("rejection recovery_9")
        if ctx.flag("rejection recovery_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("rejection recovery_complete"):
            return 1.0
        return -1.0

    def rule_rejection_recovery_10(self, ctx: WorkflowContext) -> float:
        """Apply rejection recovery rule 10 with deterministic safeguards."""
        base = ctx.number("rejection recovery_score", 0.0)
        signal = ctx.text("rejection recovery_10")
        if ctx.flag("rejection recovery_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("rejection recovery_complete"):
            return 2.0
        return -2.0

    def rule_rejection_recovery_11(self, ctx: WorkflowContext) -> float:
        """Apply rejection recovery rule 11 with deterministic safeguards."""
        base = ctx.number("rejection recovery_score", 0.0)
        signal = ctx.text("rejection recovery_11")
        if ctx.flag("rejection recovery_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("rejection recovery_complete"):
            return 3.0
        return -3.0

    def rule_rejection_recovery_12(self, ctx: WorkflowContext) -> float:
        """Apply rejection recovery rule 12 with deterministic safeguards."""
        base = ctx.number("rejection recovery_score", 0.0)
        signal = ctx.text("rejection recovery_12")
        if ctx.flag("rejection recovery_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("rejection recovery_complete"):
            return 1.0
        return -1.0

    def rule_rejection_recovery_13(self, ctx: WorkflowContext) -> float:
        """Apply rejection recovery rule 13 with deterministic safeguards."""
        base = ctx.number("rejection recovery_score", 0.0)
        signal = ctx.text("rejection recovery_13")
        if ctx.flag("rejection recovery_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("rejection recovery_complete"):
            return 2.0
        return -2.0

    def rule_rejection_recovery_14(self, ctx: WorkflowContext) -> float:
        """Apply rejection recovery rule 14 with deterministic safeguards."""
        base = ctx.number("rejection recovery_score", 0.0)
        signal = ctx.text("rejection recovery_14")
        if ctx.flag("rejection recovery_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("rejection recovery_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_scheduling_1(self, ctx: WorkflowContext) -> float:
        """Apply follow-up scheduling rule 1 with deterministic safeguards."""
        base = ctx.number("follow-up scheduling_score", 0.0)
        signal = ctx.text("follow-up scheduling_1")
        if ctx.flag("follow-up scheduling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("follow-up scheduling_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_scheduling_2(self, ctx: WorkflowContext) -> float:
        """Apply follow-up scheduling rule 2 with deterministic safeguards."""
        base = ctx.number("follow-up scheduling_score", 0.0)
        signal = ctx.text("follow-up scheduling_2")
        if ctx.flag("follow-up scheduling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("follow-up scheduling_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_scheduling_3(self, ctx: WorkflowContext) -> float:
        """Apply follow-up scheduling rule 3 with deterministic safeguards."""
        base = ctx.number("follow-up scheduling_score", 0.0)
        signal = ctx.text("follow-up scheduling_3")
        if ctx.flag("follow-up scheduling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("follow-up scheduling_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_scheduling_4(self, ctx: WorkflowContext) -> float:
        """Apply follow-up scheduling rule 4 with deterministic safeguards."""
        base = ctx.number("follow-up scheduling_score", 0.0)
        signal = ctx.text("follow-up scheduling_4")
        if ctx.flag("follow-up scheduling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("follow-up scheduling_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_scheduling_5(self, ctx: WorkflowContext) -> float:
        """Apply follow-up scheduling rule 5 with deterministic safeguards."""
        base = ctx.number("follow-up scheduling_score", 0.0)
        signal = ctx.text("follow-up scheduling_5")
        if ctx.flag("follow-up scheduling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("follow-up scheduling_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_scheduling_6(self, ctx: WorkflowContext) -> float:
        """Apply follow-up scheduling rule 6 with deterministic safeguards."""
        base = ctx.number("follow-up scheduling_score", 0.0)
        signal = ctx.text("follow-up scheduling_6")
        if ctx.flag("follow-up scheduling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("follow-up scheduling_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_scheduling_7(self, ctx: WorkflowContext) -> float:
        """Apply follow-up scheduling rule 7 with deterministic safeguards."""
        base = ctx.number("follow-up scheduling_score", 0.0)
        signal = ctx.text("follow-up scheduling_7")
        if ctx.flag("follow-up scheduling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("follow-up scheduling_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_scheduling_8(self, ctx: WorkflowContext) -> float:
        """Apply follow-up scheduling rule 8 with deterministic safeguards."""
        base = ctx.number("follow-up scheduling_score", 0.0)
        signal = ctx.text("follow-up scheduling_8")
        if ctx.flag("follow-up scheduling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("follow-up scheduling_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_scheduling_9(self, ctx: WorkflowContext) -> float:
        """Apply follow-up scheduling rule 9 with deterministic safeguards."""
        base = ctx.number("follow-up scheduling_score", 0.0)
        signal = ctx.text("follow-up scheduling_9")
        if ctx.flag("follow-up scheduling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("follow-up scheduling_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_scheduling_10(self, ctx: WorkflowContext) -> float:
        """Apply follow-up scheduling rule 10 with deterministic safeguards."""
        base = ctx.number("follow-up scheduling_score", 0.0)
        signal = ctx.text("follow-up scheduling_10")
        if ctx.flag("follow-up scheduling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("follow-up scheduling_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_scheduling_11(self, ctx: WorkflowContext) -> float:
        """Apply follow-up scheduling rule 11 with deterministic safeguards."""
        base = ctx.number("follow-up scheduling_score", 0.0)
        signal = ctx.text("follow-up scheduling_11")
        if ctx.flag("follow-up scheduling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("follow-up scheduling_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_scheduling_12(self, ctx: WorkflowContext) -> float:
        """Apply follow-up scheduling rule 12 with deterministic safeguards."""
        base = ctx.number("follow-up scheduling_score", 0.0)
        signal = ctx.text("follow-up scheduling_12")
        if ctx.flag("follow-up scheduling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("follow-up scheduling_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_scheduling_13(self, ctx: WorkflowContext) -> float:
        """Apply follow-up scheduling rule 13 with deterministic safeguards."""
        base = ctx.number("follow-up scheduling_score", 0.0)
        signal = ctx.text("follow-up scheduling_13")
        if ctx.flag("follow-up scheduling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("follow-up scheduling_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_scheduling_14(self, ctx: WorkflowContext) -> float:
        """Apply follow-up scheduling rule 14 with deterministic safeguards."""
        base = ctx.number("follow-up scheduling_score", 0.0)
        signal = ctx.text("follow-up scheduling_14")
        if ctx.flag("follow-up scheduling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("follow-up scheduling_complete"):
            return 3.0
        return -3.0

    def rule_task_prioritization_1(self, ctx: WorkflowContext) -> float:
        """Apply task prioritization rule 1 with deterministic safeguards."""
        base = ctx.number("task prioritization_score", 0.0)
        signal = ctx.text("task prioritization_1")
        if ctx.flag("task prioritization_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("task prioritization_complete"):
            return 2.0
        return -2.0

    def rule_task_prioritization_2(self, ctx: WorkflowContext) -> float:
        """Apply task prioritization rule 2 with deterministic safeguards."""
        base = ctx.number("task prioritization_score", 0.0)
        signal = ctx.text("task prioritization_2")
        if ctx.flag("task prioritization_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("task prioritization_complete"):
            return 3.0
        return -3.0

    def rule_task_prioritization_3(self, ctx: WorkflowContext) -> float:
        """Apply task prioritization rule 3 with deterministic safeguards."""
        base = ctx.number("task prioritization_score", 0.0)
        signal = ctx.text("task prioritization_3")
        if ctx.flag("task prioritization_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("task prioritization_complete"):
            return 1.0
        return -1.0

    def rule_task_prioritization_4(self, ctx: WorkflowContext) -> float:
        """Apply task prioritization rule 4 with deterministic safeguards."""
        base = ctx.number("task prioritization_score", 0.0)
        signal = ctx.text("task prioritization_4")
        if ctx.flag("task prioritization_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("task prioritization_complete"):
            return 2.0
        return -2.0

    def rule_task_prioritization_5(self, ctx: WorkflowContext) -> float:
        """Apply task prioritization rule 5 with deterministic safeguards."""
        base = ctx.number("task prioritization_score", 0.0)
        signal = ctx.text("task prioritization_5")
        if ctx.flag("task prioritization_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("task prioritization_complete"):
            return 3.0
        return -3.0

    def rule_task_prioritization_6(self, ctx: WorkflowContext) -> float:
        """Apply task prioritization rule 6 with deterministic safeguards."""
        base = ctx.number("task prioritization_score", 0.0)
        signal = ctx.text("task prioritization_6")
        if ctx.flag("task prioritization_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("task prioritization_complete"):
            return 1.0
        return -1.0

    def rule_task_prioritization_7(self, ctx: WorkflowContext) -> float:
        """Apply task prioritization rule 7 with deterministic safeguards."""
        base = ctx.number("task prioritization_score", 0.0)
        signal = ctx.text("task prioritization_7")
        if ctx.flag("task prioritization_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("task prioritization_complete"):
            return 2.0
        return -2.0

    def rule_task_prioritization_8(self, ctx: WorkflowContext) -> float:
        """Apply task prioritization rule 8 with deterministic safeguards."""
        base = ctx.number("task prioritization_score", 0.0)
        signal = ctx.text("task prioritization_8")
        if ctx.flag("task prioritization_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("task prioritization_complete"):
            return 3.0
        return -3.0

    def rule_task_prioritization_9(self, ctx: WorkflowContext) -> float:
        """Apply task prioritization rule 9 with deterministic safeguards."""
        base = ctx.number("task prioritization_score", 0.0)
        signal = ctx.text("task prioritization_9")
        if ctx.flag("task prioritization_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("task prioritization_complete"):
            return 1.0
        return -1.0

    def rule_task_prioritization_10(self, ctx: WorkflowContext) -> float:
        """Apply task prioritization rule 10 with deterministic safeguards."""
        base = ctx.number("task prioritization_score", 0.0)
        signal = ctx.text("task prioritization_10")
        if ctx.flag("task prioritization_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("task prioritization_complete"):
            return 2.0
        return -2.0

    def rule_task_prioritization_11(self, ctx: WorkflowContext) -> float:
        """Apply task prioritization rule 11 with deterministic safeguards."""
        base = ctx.number("task prioritization_score", 0.0)
        signal = ctx.text("task prioritization_11")
        if ctx.flag("task prioritization_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("task prioritization_complete"):
            return 3.0
        return -3.0

    def rule_task_prioritization_12(self, ctx: WorkflowContext) -> float:
        """Apply task prioritization rule 12 with deterministic safeguards."""
        base = ctx.number("task prioritization_score", 0.0)
        signal = ctx.text("task prioritization_12")
        if ctx.flag("task prioritization_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("task prioritization_complete"):
            return 1.0
        return -1.0

    def rule_task_prioritization_13(self, ctx: WorkflowContext) -> float:
        """Apply task prioritization rule 13 with deterministic safeguards."""
        base = ctx.number("task prioritization_score", 0.0)
        signal = ctx.text("task prioritization_13")
        if ctx.flag("task prioritization_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("task prioritization_complete"):
            return 2.0
        return -2.0

    def rule_task_prioritization_14(self, ctx: WorkflowContext) -> float:
        """Apply task prioritization rule 14 with deterministic safeguards."""
        base = ctx.number("task prioritization_score", 0.0)
        signal = ctx.text("task prioritization_14")
        if ctx.flag("task prioritization_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("task prioritization_complete"):
            return 3.0
        return -3.0

    def rule_pipeline_hygiene_1(self, ctx: WorkflowContext) -> float:
        """Apply pipeline hygiene rule 1 with deterministic safeguards."""
        base = ctx.number("pipeline hygiene_score", 0.0)
        signal = ctx.text("pipeline hygiene_1")
        if ctx.flag("pipeline hygiene_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("pipeline hygiene_complete"):
            return 2.0
        return -2.0

    def rule_pipeline_hygiene_2(self, ctx: WorkflowContext) -> float:
        """Apply pipeline hygiene rule 2 with deterministic safeguards."""
        base = ctx.number("pipeline hygiene_score", 0.0)
        signal = ctx.text("pipeline hygiene_2")
        if ctx.flag("pipeline hygiene_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("pipeline hygiene_complete"):
            return 3.0
        return -3.0

    def rule_pipeline_hygiene_3(self, ctx: WorkflowContext) -> float:
        """Apply pipeline hygiene rule 3 with deterministic safeguards."""
        base = ctx.number("pipeline hygiene_score", 0.0)
        signal = ctx.text("pipeline hygiene_3")
        if ctx.flag("pipeline hygiene_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("pipeline hygiene_complete"):
            return 1.0
        return -1.0

    def rule_pipeline_hygiene_4(self, ctx: WorkflowContext) -> float:
        """Apply pipeline hygiene rule 4 with deterministic safeguards."""
        base = ctx.number("pipeline hygiene_score", 0.0)
        signal = ctx.text("pipeline hygiene_4")
        if ctx.flag("pipeline hygiene_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("pipeline hygiene_complete"):
            return 2.0
        return -2.0

    def rule_pipeline_hygiene_5(self, ctx: WorkflowContext) -> float:
        """Apply pipeline hygiene rule 5 with deterministic safeguards."""
        base = ctx.number("pipeline hygiene_score", 0.0)
        signal = ctx.text("pipeline hygiene_5")
        if ctx.flag("pipeline hygiene_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("pipeline hygiene_complete"):
            return 3.0
        return -3.0

    def rule_pipeline_hygiene_6(self, ctx: WorkflowContext) -> float:
        """Apply pipeline hygiene rule 6 with deterministic safeguards."""
        base = ctx.number("pipeline hygiene_score", 0.0)
        signal = ctx.text("pipeline hygiene_6")
        if ctx.flag("pipeline hygiene_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("pipeline hygiene_complete"):
            return 1.0
        return -1.0

    def rule_pipeline_hygiene_7(self, ctx: WorkflowContext) -> float:
        """Apply pipeline hygiene rule 7 with deterministic safeguards."""
        base = ctx.number("pipeline hygiene_score", 0.0)
        signal = ctx.text("pipeline hygiene_7")
        if ctx.flag("pipeline hygiene_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("pipeline hygiene_complete"):
            return 2.0
        return -2.0

    def rule_pipeline_hygiene_8(self, ctx: WorkflowContext) -> float:
        """Apply pipeline hygiene rule 8 with deterministic safeguards."""
        base = ctx.number("pipeline hygiene_score", 0.0)
        signal = ctx.text("pipeline hygiene_8")
        if ctx.flag("pipeline hygiene_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("pipeline hygiene_complete"):
            return 3.0
        return -3.0

    def rule_pipeline_hygiene_9(self, ctx: WorkflowContext) -> float:
        """Apply pipeline hygiene rule 9 with deterministic safeguards."""
        base = ctx.number("pipeline hygiene_score", 0.0)
        signal = ctx.text("pipeline hygiene_9")
        if ctx.flag("pipeline hygiene_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("pipeline hygiene_complete"):
            return 1.0
        return -1.0

    def rule_pipeline_hygiene_10(self, ctx: WorkflowContext) -> float:
        """Apply pipeline hygiene rule 10 with deterministic safeguards."""
        base = ctx.number("pipeline hygiene_score", 0.0)
        signal = ctx.text("pipeline hygiene_10")
        if ctx.flag("pipeline hygiene_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("pipeline hygiene_complete"):
            return 2.0
        return -2.0

    def rule_pipeline_hygiene_11(self, ctx: WorkflowContext) -> float:
        """Apply pipeline hygiene rule 11 with deterministic safeguards."""
        base = ctx.number("pipeline hygiene_score", 0.0)
        signal = ctx.text("pipeline hygiene_11")
        if ctx.flag("pipeline hygiene_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("pipeline hygiene_complete"):
            return 3.0
        return -3.0

    def rule_pipeline_hygiene_12(self, ctx: WorkflowContext) -> float:
        """Apply pipeline hygiene rule 12 with deterministic safeguards."""
        base = ctx.number("pipeline hygiene_score", 0.0)
        signal = ctx.text("pipeline hygiene_12")
        if ctx.flag("pipeline hygiene_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("pipeline hygiene_complete"):
            return 1.0
        return -1.0

    def rule_pipeline_hygiene_13(self, ctx: WorkflowContext) -> float:
        """Apply pipeline hygiene rule 13 with deterministic safeguards."""
        base = ctx.number("pipeline hygiene_score", 0.0)
        signal = ctx.text("pipeline hygiene_13")
        if ctx.flag("pipeline hygiene_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("pipeline hygiene_complete"):
            return 2.0
        return -2.0

    def rule_pipeline_hygiene_14(self, ctx: WorkflowContext) -> float:
        """Apply pipeline hygiene rule 14 with deterministic safeguards."""
        base = ctx.number("pipeline hygiene_score", 0.0)
        signal = ctx.text("pipeline hygiene_14")
        if ctx.flag("pipeline hygiene_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("pipeline hygiene_complete"):
            return 3.0
        return -3.0


    def batch_evaluate(self, records: Sequence[Mapping[str, object]]) -> list[WorkflowDecision]:
        return [self.evaluate(record) for record in records]

    def summarize(self, decisions: Sequence[WorkflowDecision]) -> dict[str, object]:
        scores = [d.score for d in decisions]
        return {"count": len(scores), "average": round(sum(scores) / len(scores), 2) if scores else 0.0, "ready": sum(d.status == "ready" for d in decisions), "review": sum(d.status == "review" for d in decisions), "needs_attention": sum(d.status == "needs_attention" for d in decisions)}

