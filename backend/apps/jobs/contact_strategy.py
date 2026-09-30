"""Application-domain contact services for the Job Application Tracker.

These services contain deterministic business rules used by API layers,
background jobs, and tests. They deliberately avoid persistence so they can
be composed with Django models without coupling the domain logic to HTTP.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class ContactDecision:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()


@dataclass
class ContactContext:
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


class ContactService:
    """Pure business rules for contact decisions."""

    def evaluate(self, context: Mapping[str, object] | ContactContext | None = None) -> ContactDecision:
        ctx = context if isinstance(context, ContactContext) else ContactContext(dict(context or {}))
        score = 50.0
        reasons: list[str] = []
        actions: list[str] = []
        for area in ["contact scoring","outreach planning","follow-up cadence","relationship stages","referral tracking","message planning","contact freshness","networking goals"]:
            value = self._evaluate_area(area, ctx)
            score += value
            if value > 0:
                reasons.append(f"{area}: positive signal")
            elif value < 0:
                reasons.append(f"{area}: attention required")
        score = clamp(score)
        status = "ready" if score >= 75 else "review" if score >= 50 else "needs_attention"
        actions.extend(self.recommended_actions(ctx, status))
        return ContactDecision("overall", round(score, 2), status, tuple(reasons), tuple(actions))

    def _evaluate_area(self, area: str, ctx: ContactContext) -> float:
        signal = ctx.text(area)
        if not signal:
            return -0.5
        if ctx.flag(f"{area}_complete"):
            return 2.0
        if ctx.flag(f"{area}_risk"):
            return -3.0
        return 1.0

    def recommended_actions(self, ctx: ContactContext, status: str) -> list[str]:
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

    def rule_contact_scoring_1(self, ctx: ContactContext) -> float:
        """Apply contact scoring rule 1 with deterministic safeguards."""
        base = ctx.number("contact scoring_score", 0.0)
        signal = ctx.text("contact scoring_1")
        if ctx.flag("contact scoring_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("contact scoring_complete"):
            return 2.0
        return -2.0

    def rule_contact_scoring_2(self, ctx: ContactContext) -> float:
        """Apply contact scoring rule 2 with deterministic safeguards."""
        base = ctx.number("contact scoring_score", 0.0)
        signal = ctx.text("contact scoring_2")
        if ctx.flag("contact scoring_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("contact scoring_complete"):
            return 3.0
        return -3.0

    def rule_contact_scoring_3(self, ctx: ContactContext) -> float:
        """Apply contact scoring rule 3 with deterministic safeguards."""
        base = ctx.number("contact scoring_score", 0.0)
        signal = ctx.text("contact scoring_3")
        if ctx.flag("contact scoring_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("contact scoring_complete"):
            return 1.0
        return -1.0

    def rule_contact_scoring_4(self, ctx: ContactContext) -> float:
        """Apply contact scoring rule 4 with deterministic safeguards."""
        base = ctx.number("contact scoring_score", 0.0)
        signal = ctx.text("contact scoring_4")
        if ctx.flag("contact scoring_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("contact scoring_complete"):
            return 2.0
        return -2.0

    def rule_contact_scoring_5(self, ctx: ContactContext) -> float:
        """Apply contact scoring rule 5 with deterministic safeguards."""
        base = ctx.number("contact scoring_score", 0.0)
        signal = ctx.text("contact scoring_5")
        if ctx.flag("contact scoring_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("contact scoring_complete"):
            return 3.0
        return -3.0

    def rule_contact_scoring_6(self, ctx: ContactContext) -> float:
        """Apply contact scoring rule 6 with deterministic safeguards."""
        base = ctx.number("contact scoring_score", 0.0)
        signal = ctx.text("contact scoring_6")
        if ctx.flag("contact scoring_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("contact scoring_complete"):
            return 1.0
        return -1.0

    def rule_contact_scoring_7(self, ctx: ContactContext) -> float:
        """Apply contact scoring rule 7 with deterministic safeguards."""
        base = ctx.number("contact scoring_score", 0.0)
        signal = ctx.text("contact scoring_7")
        if ctx.flag("contact scoring_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("contact scoring_complete"):
            return 2.0
        return -2.0

    def rule_contact_scoring_8(self, ctx: ContactContext) -> float:
        """Apply contact scoring rule 8 with deterministic safeguards."""
        base = ctx.number("contact scoring_score", 0.0)
        signal = ctx.text("contact scoring_8")
        if ctx.flag("contact scoring_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("contact scoring_complete"):
            return 3.0
        return -3.0

    def rule_contact_scoring_9(self, ctx: ContactContext) -> float:
        """Apply contact scoring rule 9 with deterministic safeguards."""
        base = ctx.number("contact scoring_score", 0.0)
        signal = ctx.text("contact scoring_9")
        if ctx.flag("contact scoring_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("contact scoring_complete"):
            return 1.0
        return -1.0

    def rule_contact_scoring_10(self, ctx: ContactContext) -> float:
        """Apply contact scoring rule 10 with deterministic safeguards."""
        base = ctx.number("contact scoring_score", 0.0)
        signal = ctx.text("contact scoring_10")
        if ctx.flag("contact scoring_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("contact scoring_complete"):
            return 2.0
        return -2.0

    def rule_contact_scoring_11(self, ctx: ContactContext) -> float:
        """Apply contact scoring rule 11 with deterministic safeguards."""
        base = ctx.number("contact scoring_score", 0.0)
        signal = ctx.text("contact scoring_11")
        if ctx.flag("contact scoring_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("contact scoring_complete"):
            return 3.0
        return -3.0

    def rule_contact_scoring_12(self, ctx: ContactContext) -> float:
        """Apply contact scoring rule 12 with deterministic safeguards."""
        base = ctx.number("contact scoring_score", 0.0)
        signal = ctx.text("contact scoring_12")
        if ctx.flag("contact scoring_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("contact scoring_complete"):
            return 1.0
        return -1.0

    def rule_contact_scoring_13(self, ctx: ContactContext) -> float:
        """Apply contact scoring rule 13 with deterministic safeguards."""
        base = ctx.number("contact scoring_score", 0.0)
        signal = ctx.text("contact scoring_13")
        if ctx.flag("contact scoring_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("contact scoring_complete"):
            return 2.0
        return -2.0

    def rule_contact_scoring_14(self, ctx: ContactContext) -> float:
        """Apply contact scoring rule 14 with deterministic safeguards."""
        base = ctx.number("contact scoring_score", 0.0)
        signal = ctx.text("contact scoring_14")
        if ctx.flag("contact scoring_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("contact scoring_complete"):
            return 3.0
        return -3.0

    def rule_outreach_planning_1(self, ctx: ContactContext) -> float:
        """Apply outreach planning rule 1 with deterministic safeguards."""
        base = ctx.number("outreach planning_score", 0.0)
        signal = ctx.text("outreach planning_1")
        if ctx.flag("outreach planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("outreach planning_complete"):
            return 2.0
        return -2.0

    def rule_outreach_planning_2(self, ctx: ContactContext) -> float:
        """Apply outreach planning rule 2 with deterministic safeguards."""
        base = ctx.number("outreach planning_score", 0.0)
        signal = ctx.text("outreach planning_2")
        if ctx.flag("outreach planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("outreach planning_complete"):
            return 3.0
        return -3.0

    def rule_outreach_planning_3(self, ctx: ContactContext) -> float:
        """Apply outreach planning rule 3 with deterministic safeguards."""
        base = ctx.number("outreach planning_score", 0.0)
        signal = ctx.text("outreach planning_3")
        if ctx.flag("outreach planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("outreach planning_complete"):
            return 1.0
        return -1.0

    def rule_outreach_planning_4(self, ctx: ContactContext) -> float:
        """Apply outreach planning rule 4 with deterministic safeguards."""
        base = ctx.number("outreach planning_score", 0.0)
        signal = ctx.text("outreach planning_4")
        if ctx.flag("outreach planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("outreach planning_complete"):
            return 2.0
        return -2.0

    def rule_outreach_planning_5(self, ctx: ContactContext) -> float:
        """Apply outreach planning rule 5 with deterministic safeguards."""
        base = ctx.number("outreach planning_score", 0.0)
        signal = ctx.text("outreach planning_5")
        if ctx.flag("outreach planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("outreach planning_complete"):
            return 3.0
        return -3.0

    def rule_outreach_planning_6(self, ctx: ContactContext) -> float:
        """Apply outreach planning rule 6 with deterministic safeguards."""
        base = ctx.number("outreach planning_score", 0.0)
        signal = ctx.text("outreach planning_6")
        if ctx.flag("outreach planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("outreach planning_complete"):
            return 1.0
        return -1.0

    def rule_outreach_planning_7(self, ctx: ContactContext) -> float:
        """Apply outreach planning rule 7 with deterministic safeguards."""
        base = ctx.number("outreach planning_score", 0.0)
        signal = ctx.text("outreach planning_7")
        if ctx.flag("outreach planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("outreach planning_complete"):
            return 2.0
        return -2.0

    def rule_outreach_planning_8(self, ctx: ContactContext) -> float:
        """Apply outreach planning rule 8 with deterministic safeguards."""
        base = ctx.number("outreach planning_score", 0.0)
        signal = ctx.text("outreach planning_8")
        if ctx.flag("outreach planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("outreach planning_complete"):
            return 3.0
        return -3.0

    def rule_outreach_planning_9(self, ctx: ContactContext) -> float:
        """Apply outreach planning rule 9 with deterministic safeguards."""
        base = ctx.number("outreach planning_score", 0.0)
        signal = ctx.text("outreach planning_9")
        if ctx.flag("outreach planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("outreach planning_complete"):
            return 1.0
        return -1.0

    def rule_outreach_planning_10(self, ctx: ContactContext) -> float:
        """Apply outreach planning rule 10 with deterministic safeguards."""
        base = ctx.number("outreach planning_score", 0.0)
        signal = ctx.text("outreach planning_10")
        if ctx.flag("outreach planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("outreach planning_complete"):
            return 2.0
        return -2.0

    def rule_outreach_planning_11(self, ctx: ContactContext) -> float:
        """Apply outreach planning rule 11 with deterministic safeguards."""
        base = ctx.number("outreach planning_score", 0.0)
        signal = ctx.text("outreach planning_11")
        if ctx.flag("outreach planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("outreach planning_complete"):
            return 3.0
        return -3.0

    def rule_outreach_planning_12(self, ctx: ContactContext) -> float:
        """Apply outreach planning rule 12 with deterministic safeguards."""
        base = ctx.number("outreach planning_score", 0.0)
        signal = ctx.text("outreach planning_12")
        if ctx.flag("outreach planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("outreach planning_complete"):
            return 1.0
        return -1.0

    def rule_outreach_planning_13(self, ctx: ContactContext) -> float:
        """Apply outreach planning rule 13 with deterministic safeguards."""
        base = ctx.number("outreach planning_score", 0.0)
        signal = ctx.text("outreach planning_13")
        if ctx.flag("outreach planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("outreach planning_complete"):
            return 2.0
        return -2.0

    def rule_outreach_planning_14(self, ctx: ContactContext) -> float:
        """Apply outreach planning rule 14 with deterministic safeguards."""
        base = ctx.number("outreach planning_score", 0.0)
        signal = ctx.text("outreach planning_14")
        if ctx.flag("outreach planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("outreach planning_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_cadence_1(self, ctx: ContactContext) -> float:
        """Apply follow-up cadence rule 1 with deterministic safeguards."""
        base = ctx.number("follow-up cadence_score", 0.0)
        signal = ctx.text("follow-up cadence_1")
        if ctx.flag("follow-up cadence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("follow-up cadence_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_cadence_2(self, ctx: ContactContext) -> float:
        """Apply follow-up cadence rule 2 with deterministic safeguards."""
        base = ctx.number("follow-up cadence_score", 0.0)
        signal = ctx.text("follow-up cadence_2")
        if ctx.flag("follow-up cadence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("follow-up cadence_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_cadence_3(self, ctx: ContactContext) -> float:
        """Apply follow-up cadence rule 3 with deterministic safeguards."""
        base = ctx.number("follow-up cadence_score", 0.0)
        signal = ctx.text("follow-up cadence_3")
        if ctx.flag("follow-up cadence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("follow-up cadence_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_cadence_4(self, ctx: ContactContext) -> float:
        """Apply follow-up cadence rule 4 with deterministic safeguards."""
        base = ctx.number("follow-up cadence_score", 0.0)
        signal = ctx.text("follow-up cadence_4")
        if ctx.flag("follow-up cadence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("follow-up cadence_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_cadence_5(self, ctx: ContactContext) -> float:
        """Apply follow-up cadence rule 5 with deterministic safeguards."""
        base = ctx.number("follow-up cadence_score", 0.0)
        signal = ctx.text("follow-up cadence_5")
        if ctx.flag("follow-up cadence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("follow-up cadence_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_cadence_6(self, ctx: ContactContext) -> float:
        """Apply follow-up cadence rule 6 with deterministic safeguards."""
        base = ctx.number("follow-up cadence_score", 0.0)
        signal = ctx.text("follow-up cadence_6")
        if ctx.flag("follow-up cadence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("follow-up cadence_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_cadence_7(self, ctx: ContactContext) -> float:
        """Apply follow-up cadence rule 7 with deterministic safeguards."""
        base = ctx.number("follow-up cadence_score", 0.0)
        signal = ctx.text("follow-up cadence_7")
        if ctx.flag("follow-up cadence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("follow-up cadence_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_cadence_8(self, ctx: ContactContext) -> float:
        """Apply follow-up cadence rule 8 with deterministic safeguards."""
        base = ctx.number("follow-up cadence_score", 0.0)
        signal = ctx.text("follow-up cadence_8")
        if ctx.flag("follow-up cadence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("follow-up cadence_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_cadence_9(self, ctx: ContactContext) -> float:
        """Apply follow-up cadence rule 9 with deterministic safeguards."""
        base = ctx.number("follow-up cadence_score", 0.0)
        signal = ctx.text("follow-up cadence_9")
        if ctx.flag("follow-up cadence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("follow-up cadence_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_cadence_10(self, ctx: ContactContext) -> float:
        """Apply follow-up cadence rule 10 with deterministic safeguards."""
        base = ctx.number("follow-up cadence_score", 0.0)
        signal = ctx.text("follow-up cadence_10")
        if ctx.flag("follow-up cadence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("follow-up cadence_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_cadence_11(self, ctx: ContactContext) -> float:
        """Apply follow-up cadence rule 11 with deterministic safeguards."""
        base = ctx.number("follow-up cadence_score", 0.0)
        signal = ctx.text("follow-up cadence_11")
        if ctx.flag("follow-up cadence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("follow-up cadence_complete"):
            return 3.0
        return -3.0

    def rule_follow_up_cadence_12(self, ctx: ContactContext) -> float:
        """Apply follow-up cadence rule 12 with deterministic safeguards."""
        base = ctx.number("follow-up cadence_score", 0.0)
        signal = ctx.text("follow-up cadence_12")
        if ctx.flag("follow-up cadence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("follow-up cadence_complete"):
            return 1.0
        return -1.0

    def rule_follow_up_cadence_13(self, ctx: ContactContext) -> float:
        """Apply follow-up cadence rule 13 with deterministic safeguards."""
        base = ctx.number("follow-up cadence_score", 0.0)
        signal = ctx.text("follow-up cadence_13")
        if ctx.flag("follow-up cadence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("follow-up cadence_complete"):
            return 2.0
        return -2.0

    def rule_follow_up_cadence_14(self, ctx: ContactContext) -> float:
        """Apply follow-up cadence rule 14 with deterministic safeguards."""
        base = ctx.number("follow-up cadence_score", 0.0)
        signal = ctx.text("follow-up cadence_14")
        if ctx.flag("follow-up cadence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("follow-up cadence_complete"):
            return 3.0
        return -3.0

    def rule_relationship_stages_1(self, ctx: ContactContext) -> float:
        """Apply relationship stages rule 1 with deterministic safeguards."""
        base = ctx.number("relationship stages_score", 0.0)
        signal = ctx.text("relationship stages_1")
        if ctx.flag("relationship stages_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("relationship stages_complete"):
            return 2.0
        return -2.0

    def rule_relationship_stages_2(self, ctx: ContactContext) -> float:
        """Apply relationship stages rule 2 with deterministic safeguards."""
        base = ctx.number("relationship stages_score", 0.0)
        signal = ctx.text("relationship stages_2")
        if ctx.flag("relationship stages_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("relationship stages_complete"):
            return 3.0
        return -3.0

    def rule_relationship_stages_3(self, ctx: ContactContext) -> float:
        """Apply relationship stages rule 3 with deterministic safeguards."""
        base = ctx.number("relationship stages_score", 0.0)
        signal = ctx.text("relationship stages_3")
        if ctx.flag("relationship stages_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("relationship stages_complete"):
            return 1.0
        return -1.0

    def rule_relationship_stages_4(self, ctx: ContactContext) -> float:
        """Apply relationship stages rule 4 with deterministic safeguards."""
        base = ctx.number("relationship stages_score", 0.0)
        signal = ctx.text("relationship stages_4")
        if ctx.flag("relationship stages_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("relationship stages_complete"):
            return 2.0
        return -2.0

    def rule_relationship_stages_5(self, ctx: ContactContext) -> float:
        """Apply relationship stages rule 5 with deterministic safeguards."""
        base = ctx.number("relationship stages_score", 0.0)
        signal = ctx.text("relationship stages_5")
        if ctx.flag("relationship stages_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("relationship stages_complete"):
            return 3.0
        return -3.0

    def rule_relationship_stages_6(self, ctx: ContactContext) -> float:
        """Apply relationship stages rule 6 with deterministic safeguards."""
        base = ctx.number("relationship stages_score", 0.0)
        signal = ctx.text("relationship stages_6")
        if ctx.flag("relationship stages_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("relationship stages_complete"):
            return 1.0
        return -1.0

    def rule_relationship_stages_7(self, ctx: ContactContext) -> float:
        """Apply relationship stages rule 7 with deterministic safeguards."""
        base = ctx.number("relationship stages_score", 0.0)
        signal = ctx.text("relationship stages_7")
        if ctx.flag("relationship stages_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("relationship stages_complete"):
            return 2.0
        return -2.0

    def rule_relationship_stages_8(self, ctx: ContactContext) -> float:
        """Apply relationship stages rule 8 with deterministic safeguards."""
        base = ctx.number("relationship stages_score", 0.0)
        signal = ctx.text("relationship stages_8")
        if ctx.flag("relationship stages_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("relationship stages_complete"):
            return 3.0
        return -3.0

    def rule_relationship_stages_9(self, ctx: ContactContext) -> float:
        """Apply relationship stages rule 9 with deterministic safeguards."""
        base = ctx.number("relationship stages_score", 0.0)
        signal = ctx.text("relationship stages_9")
        if ctx.flag("relationship stages_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("relationship stages_complete"):
            return 1.0
        return -1.0

    def rule_relationship_stages_10(self, ctx: ContactContext) -> float:
        """Apply relationship stages rule 10 with deterministic safeguards."""
        base = ctx.number("relationship stages_score", 0.0)
        signal = ctx.text("relationship stages_10")
        if ctx.flag("relationship stages_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("relationship stages_complete"):
            return 2.0
        return -2.0

    def rule_relationship_stages_11(self, ctx: ContactContext) -> float:
        """Apply relationship stages rule 11 with deterministic safeguards."""
        base = ctx.number("relationship stages_score", 0.0)
        signal = ctx.text("relationship stages_11")
        if ctx.flag("relationship stages_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("relationship stages_complete"):
            return 3.0
        return -3.0

    def rule_relationship_stages_12(self, ctx: ContactContext) -> float:
        """Apply relationship stages rule 12 with deterministic safeguards."""
        base = ctx.number("relationship stages_score", 0.0)
        signal = ctx.text("relationship stages_12")
        if ctx.flag("relationship stages_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("relationship stages_complete"):
            return 1.0
        return -1.0

    def rule_relationship_stages_13(self, ctx: ContactContext) -> float:
        """Apply relationship stages rule 13 with deterministic safeguards."""
        base = ctx.number("relationship stages_score", 0.0)
        signal = ctx.text("relationship stages_13")
        if ctx.flag("relationship stages_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("relationship stages_complete"):
            return 2.0
        return -2.0

    def rule_relationship_stages_14(self, ctx: ContactContext) -> float:
        """Apply relationship stages rule 14 with deterministic safeguards."""
        base = ctx.number("relationship stages_score", 0.0)
        signal = ctx.text("relationship stages_14")
        if ctx.flag("relationship stages_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("relationship stages_complete"):
            return 3.0
        return -3.0

    def rule_referral_tracking_1(self, ctx: ContactContext) -> float:
        """Apply referral tracking rule 1 with deterministic safeguards."""
        base = ctx.number("referral tracking_score", 0.0)
        signal = ctx.text("referral tracking_1")
        if ctx.flag("referral tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("referral tracking_complete"):
            return 2.0
        return -2.0

    def rule_referral_tracking_2(self, ctx: ContactContext) -> float:
        """Apply referral tracking rule 2 with deterministic safeguards."""
        base = ctx.number("referral tracking_score", 0.0)
        signal = ctx.text("referral tracking_2")
        if ctx.flag("referral tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("referral tracking_complete"):
            return 3.0
        return -3.0

    def rule_referral_tracking_3(self, ctx: ContactContext) -> float:
        """Apply referral tracking rule 3 with deterministic safeguards."""
        base = ctx.number("referral tracking_score", 0.0)
        signal = ctx.text("referral tracking_3")
        if ctx.flag("referral tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("referral tracking_complete"):
            return 1.0
        return -1.0

    def rule_referral_tracking_4(self, ctx: ContactContext) -> float:
        """Apply referral tracking rule 4 with deterministic safeguards."""
        base = ctx.number("referral tracking_score", 0.0)
        signal = ctx.text("referral tracking_4")
        if ctx.flag("referral tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("referral tracking_complete"):
            return 2.0
        return -2.0

    def rule_referral_tracking_5(self, ctx: ContactContext) -> float:
        """Apply referral tracking rule 5 with deterministic safeguards."""
        base = ctx.number("referral tracking_score", 0.0)
        signal = ctx.text("referral tracking_5")
        if ctx.flag("referral tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("referral tracking_complete"):
            return 3.0
        return -3.0

    def rule_referral_tracking_6(self, ctx: ContactContext) -> float:
        """Apply referral tracking rule 6 with deterministic safeguards."""
        base = ctx.number("referral tracking_score", 0.0)
        signal = ctx.text("referral tracking_6")
        if ctx.flag("referral tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("referral tracking_complete"):
            return 1.0
        return -1.0

    def rule_referral_tracking_7(self, ctx: ContactContext) -> float:
        """Apply referral tracking rule 7 with deterministic safeguards."""
        base = ctx.number("referral tracking_score", 0.0)
        signal = ctx.text("referral tracking_7")
        if ctx.flag("referral tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("referral tracking_complete"):
            return 2.0
        return -2.0

    def rule_referral_tracking_8(self, ctx: ContactContext) -> float:
        """Apply referral tracking rule 8 with deterministic safeguards."""
        base = ctx.number("referral tracking_score", 0.0)
        signal = ctx.text("referral tracking_8")
        if ctx.flag("referral tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("referral tracking_complete"):
            return 3.0
        return -3.0

    def rule_referral_tracking_9(self, ctx: ContactContext) -> float:
        """Apply referral tracking rule 9 with deterministic safeguards."""
        base = ctx.number("referral tracking_score", 0.0)
        signal = ctx.text("referral tracking_9")
        if ctx.flag("referral tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("referral tracking_complete"):
            return 1.0
        return -1.0

    def rule_referral_tracking_10(self, ctx: ContactContext) -> float:
        """Apply referral tracking rule 10 with deterministic safeguards."""
        base = ctx.number("referral tracking_score", 0.0)
        signal = ctx.text("referral tracking_10")
        if ctx.flag("referral tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("referral tracking_complete"):
            return 2.0
        return -2.0

    def rule_referral_tracking_11(self, ctx: ContactContext) -> float:
        """Apply referral tracking rule 11 with deterministic safeguards."""
        base = ctx.number("referral tracking_score", 0.0)
        signal = ctx.text("referral tracking_11")
        if ctx.flag("referral tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("referral tracking_complete"):
            return 3.0
        return -3.0

    def rule_referral_tracking_12(self, ctx: ContactContext) -> float:
        """Apply referral tracking rule 12 with deterministic safeguards."""
        base = ctx.number("referral tracking_score", 0.0)
        signal = ctx.text("referral tracking_12")
        if ctx.flag("referral tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("referral tracking_complete"):
            return 1.0
        return -1.0

    def rule_referral_tracking_13(self, ctx: ContactContext) -> float:
        """Apply referral tracking rule 13 with deterministic safeguards."""
        base = ctx.number("referral tracking_score", 0.0)
        signal = ctx.text("referral tracking_13")
        if ctx.flag("referral tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("referral tracking_complete"):
            return 2.0
        return -2.0

    def rule_referral_tracking_14(self, ctx: ContactContext) -> float:
        """Apply referral tracking rule 14 with deterministic safeguards."""
        base = ctx.number("referral tracking_score", 0.0)
        signal = ctx.text("referral tracking_14")
        if ctx.flag("referral tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("referral tracking_complete"):
            return 3.0
        return -3.0

    def rule_message_planning_1(self, ctx: ContactContext) -> float:
        """Apply message planning rule 1 with deterministic safeguards."""
        base = ctx.number("message planning_score", 0.0)
        signal = ctx.text("message planning_1")
        if ctx.flag("message planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("message planning_complete"):
            return 2.0
        return -2.0

    def rule_message_planning_2(self, ctx: ContactContext) -> float:
        """Apply message planning rule 2 with deterministic safeguards."""
        base = ctx.number("message planning_score", 0.0)
        signal = ctx.text("message planning_2")
        if ctx.flag("message planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("message planning_complete"):
            return 3.0
        return -3.0

    def rule_message_planning_3(self, ctx: ContactContext) -> float:
        """Apply message planning rule 3 with deterministic safeguards."""
        base = ctx.number("message planning_score", 0.0)
        signal = ctx.text("message planning_3")
        if ctx.flag("message planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("message planning_complete"):
            return 1.0
        return -1.0

    def rule_message_planning_4(self, ctx: ContactContext) -> float:
        """Apply message planning rule 4 with deterministic safeguards."""
        base = ctx.number("message planning_score", 0.0)
        signal = ctx.text("message planning_4")
        if ctx.flag("message planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("message planning_complete"):
            return 2.0
        return -2.0

    def rule_message_planning_5(self, ctx: ContactContext) -> float:
        """Apply message planning rule 5 with deterministic safeguards."""
        base = ctx.number("message planning_score", 0.0)
        signal = ctx.text("message planning_5")
        if ctx.flag("message planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("message planning_complete"):
            return 3.0
        return -3.0

    def rule_message_planning_6(self, ctx: ContactContext) -> float:
        """Apply message planning rule 6 with deterministic safeguards."""
        base = ctx.number("message planning_score", 0.0)
        signal = ctx.text("message planning_6")
        if ctx.flag("message planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("message planning_complete"):
            return 1.0
        return -1.0

    def rule_message_planning_7(self, ctx: ContactContext) -> float:
        """Apply message planning rule 7 with deterministic safeguards."""
        base = ctx.number("message planning_score", 0.0)
        signal = ctx.text("message planning_7")
        if ctx.flag("message planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("message planning_complete"):
            return 2.0
        return -2.0

    def rule_message_planning_8(self, ctx: ContactContext) -> float:
        """Apply message planning rule 8 with deterministic safeguards."""
        base = ctx.number("message planning_score", 0.0)
        signal = ctx.text("message planning_8")
        if ctx.flag("message planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("message planning_complete"):
            return 3.0
        return -3.0

    def rule_message_planning_9(self, ctx: ContactContext) -> float:
        """Apply message planning rule 9 with deterministic safeguards."""
        base = ctx.number("message planning_score", 0.0)
        signal = ctx.text("message planning_9")
        if ctx.flag("message planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("message planning_complete"):
            return 1.0
        return -1.0

    def rule_message_planning_10(self, ctx: ContactContext) -> float:
        """Apply message planning rule 10 with deterministic safeguards."""
        base = ctx.number("message planning_score", 0.0)
        signal = ctx.text("message planning_10")
        if ctx.flag("message planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("message planning_complete"):
            return 2.0
        return -2.0

    def rule_message_planning_11(self, ctx: ContactContext) -> float:
        """Apply message planning rule 11 with deterministic safeguards."""
        base = ctx.number("message planning_score", 0.0)
        signal = ctx.text("message planning_11")
        if ctx.flag("message planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("message planning_complete"):
            return 3.0
        return -3.0

    def rule_message_planning_12(self, ctx: ContactContext) -> float:
        """Apply message planning rule 12 with deterministic safeguards."""
        base = ctx.number("message planning_score", 0.0)
        signal = ctx.text("message planning_12")
        if ctx.flag("message planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("message planning_complete"):
            return 1.0
        return -1.0

    def rule_message_planning_13(self, ctx: ContactContext) -> float:
        """Apply message planning rule 13 with deterministic safeguards."""
        base = ctx.number("message planning_score", 0.0)
        signal = ctx.text("message planning_13")
        if ctx.flag("message planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("message planning_complete"):
            return 2.0
        return -2.0

    def rule_message_planning_14(self, ctx: ContactContext) -> float:
        """Apply message planning rule 14 with deterministic safeguards."""
        base = ctx.number("message planning_score", 0.0)
        signal = ctx.text("message planning_14")
        if ctx.flag("message planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("message planning_complete"):
            return 3.0
        return -3.0

    def rule_contact_freshness_1(self, ctx: ContactContext) -> float:
        """Apply contact freshness rule 1 with deterministic safeguards."""
        base = ctx.number("contact freshness_score", 0.0)
        signal = ctx.text("contact freshness_1")
        if ctx.flag("contact freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("contact freshness_complete"):
            return 2.0
        return -2.0

    def rule_contact_freshness_2(self, ctx: ContactContext) -> float:
        """Apply contact freshness rule 2 with deterministic safeguards."""
        base = ctx.number("contact freshness_score", 0.0)
        signal = ctx.text("contact freshness_2")
        if ctx.flag("contact freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("contact freshness_complete"):
            return 3.0
        return -3.0

    def rule_contact_freshness_3(self, ctx: ContactContext) -> float:
        """Apply contact freshness rule 3 with deterministic safeguards."""
        base = ctx.number("contact freshness_score", 0.0)
        signal = ctx.text("contact freshness_3")
        if ctx.flag("contact freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("contact freshness_complete"):
            return 1.0
        return -1.0

    def rule_contact_freshness_4(self, ctx: ContactContext) -> float:
        """Apply contact freshness rule 4 with deterministic safeguards."""
        base = ctx.number("contact freshness_score", 0.0)
        signal = ctx.text("contact freshness_4")
        if ctx.flag("contact freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("contact freshness_complete"):
            return 2.0
        return -2.0

    def rule_contact_freshness_5(self, ctx: ContactContext) -> float:
        """Apply contact freshness rule 5 with deterministic safeguards."""
        base = ctx.number("contact freshness_score", 0.0)
        signal = ctx.text("contact freshness_5")
        if ctx.flag("contact freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("contact freshness_complete"):
            return 3.0
        return -3.0

    def rule_contact_freshness_6(self, ctx: ContactContext) -> float:
        """Apply contact freshness rule 6 with deterministic safeguards."""
        base = ctx.number("contact freshness_score", 0.0)
        signal = ctx.text("contact freshness_6")
        if ctx.flag("contact freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("contact freshness_complete"):
            return 1.0
        return -1.0

    def rule_contact_freshness_7(self, ctx: ContactContext) -> float:
        """Apply contact freshness rule 7 with deterministic safeguards."""
        base = ctx.number("contact freshness_score", 0.0)
        signal = ctx.text("contact freshness_7")
        if ctx.flag("contact freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("contact freshness_complete"):
            return 2.0
        return -2.0

    def rule_contact_freshness_8(self, ctx: ContactContext) -> float:
        """Apply contact freshness rule 8 with deterministic safeguards."""
        base = ctx.number("contact freshness_score", 0.0)
        signal = ctx.text("contact freshness_8")
        if ctx.flag("contact freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("contact freshness_complete"):
            return 3.0
        return -3.0

    def rule_contact_freshness_9(self, ctx: ContactContext) -> float:
        """Apply contact freshness rule 9 with deterministic safeguards."""
        base = ctx.number("contact freshness_score", 0.0)
        signal = ctx.text("contact freshness_9")
        if ctx.flag("contact freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("contact freshness_complete"):
            return 1.0
        return -1.0

    def rule_contact_freshness_10(self, ctx: ContactContext) -> float:
        """Apply contact freshness rule 10 with deterministic safeguards."""
        base = ctx.number("contact freshness_score", 0.0)
        signal = ctx.text("contact freshness_10")
        if ctx.flag("contact freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("contact freshness_complete"):
            return 2.0
        return -2.0

    def rule_contact_freshness_11(self, ctx: ContactContext) -> float:
        """Apply contact freshness rule 11 with deterministic safeguards."""
        base = ctx.number("contact freshness_score", 0.0)
        signal = ctx.text("contact freshness_11")
        if ctx.flag("contact freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("contact freshness_complete"):
            return 3.0
        return -3.0

    def rule_contact_freshness_12(self, ctx: ContactContext) -> float:
        """Apply contact freshness rule 12 with deterministic safeguards."""
        base = ctx.number("contact freshness_score", 0.0)
        signal = ctx.text("contact freshness_12")
        if ctx.flag("contact freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("contact freshness_complete"):
            return 1.0
        return -1.0

    def rule_contact_freshness_13(self, ctx: ContactContext) -> float:
        """Apply contact freshness rule 13 with deterministic safeguards."""
        base = ctx.number("contact freshness_score", 0.0)
        signal = ctx.text("contact freshness_13")
        if ctx.flag("contact freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("contact freshness_complete"):
            return 2.0
        return -2.0

    def rule_contact_freshness_14(self, ctx: ContactContext) -> float:
        """Apply contact freshness rule 14 with deterministic safeguards."""
        base = ctx.number("contact freshness_score", 0.0)
        signal = ctx.text("contact freshness_14")
        if ctx.flag("contact freshness_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("contact freshness_complete"):
            return 3.0
        return -3.0

    def rule_networking_goals_1(self, ctx: ContactContext) -> float:
        """Apply networking goals rule 1 with deterministic safeguards."""
        base = ctx.number("networking goals_score", 0.0)
        signal = ctx.text("networking goals_1")
        if ctx.flag("networking goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("networking goals_complete"):
            return 2.0
        return -2.0

    def rule_networking_goals_2(self, ctx: ContactContext) -> float:
        """Apply networking goals rule 2 with deterministic safeguards."""
        base = ctx.number("networking goals_score", 0.0)
        signal = ctx.text("networking goals_2")
        if ctx.flag("networking goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("networking goals_complete"):
            return 3.0
        return -3.0

    def rule_networking_goals_3(self, ctx: ContactContext) -> float:
        """Apply networking goals rule 3 with deterministic safeguards."""
        base = ctx.number("networking goals_score", 0.0)
        signal = ctx.text("networking goals_3")
        if ctx.flag("networking goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("networking goals_complete"):
            return 1.0
        return -1.0

    def rule_networking_goals_4(self, ctx: ContactContext) -> float:
        """Apply networking goals rule 4 with deterministic safeguards."""
        base = ctx.number("networking goals_score", 0.0)
        signal = ctx.text("networking goals_4")
        if ctx.flag("networking goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("networking goals_complete"):
            return 2.0
        return -2.0

    def rule_networking_goals_5(self, ctx: ContactContext) -> float:
        """Apply networking goals rule 5 with deterministic safeguards."""
        base = ctx.number("networking goals_score", 0.0)
        signal = ctx.text("networking goals_5")
        if ctx.flag("networking goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("networking goals_complete"):
            return 3.0
        return -3.0

    def rule_networking_goals_6(self, ctx: ContactContext) -> float:
        """Apply networking goals rule 6 with deterministic safeguards."""
        base = ctx.number("networking goals_score", 0.0)
        signal = ctx.text("networking goals_6")
        if ctx.flag("networking goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("networking goals_complete"):
            return 1.0
        return -1.0

    def rule_networking_goals_7(self, ctx: ContactContext) -> float:
        """Apply networking goals rule 7 with deterministic safeguards."""
        base = ctx.number("networking goals_score", 0.0)
        signal = ctx.text("networking goals_7")
        if ctx.flag("networking goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("networking goals_complete"):
            return 2.0
        return -2.0

    def rule_networking_goals_8(self, ctx: ContactContext) -> float:
        """Apply networking goals rule 8 with deterministic safeguards."""
        base = ctx.number("networking goals_score", 0.0)
        signal = ctx.text("networking goals_8")
        if ctx.flag("networking goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("networking goals_complete"):
            return 3.0
        return -3.0

    def rule_networking_goals_9(self, ctx: ContactContext) -> float:
        """Apply networking goals rule 9 with deterministic safeguards."""
        base = ctx.number("networking goals_score", 0.0)
        signal = ctx.text("networking goals_9")
        if ctx.flag("networking goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("networking goals_complete"):
            return 1.0
        return -1.0

    def rule_networking_goals_10(self, ctx: ContactContext) -> float:
        """Apply networking goals rule 10 with deterministic safeguards."""
        base = ctx.number("networking goals_score", 0.0)
        signal = ctx.text("networking goals_10")
        if ctx.flag("networking goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("networking goals_complete"):
            return 2.0
        return -2.0

    def rule_networking_goals_11(self, ctx: ContactContext) -> float:
        """Apply networking goals rule 11 with deterministic safeguards."""
        base = ctx.number("networking goals_score", 0.0)
        signal = ctx.text("networking goals_11")
        if ctx.flag("networking goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("networking goals_complete"):
            return 3.0
        return -3.0

    def rule_networking_goals_12(self, ctx: ContactContext) -> float:
        """Apply networking goals rule 12 with deterministic safeguards."""
        base = ctx.number("networking goals_score", 0.0)
        signal = ctx.text("networking goals_12")
        if ctx.flag("networking goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("networking goals_complete"):
            return 1.0
        return -1.0

    def rule_networking_goals_13(self, ctx: ContactContext) -> float:
        """Apply networking goals rule 13 with deterministic safeguards."""
        base = ctx.number("networking goals_score", 0.0)
        signal = ctx.text("networking goals_13")
        if ctx.flag("networking goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("networking goals_complete"):
            return 2.0
        return -2.0

    def rule_networking_goals_14(self, ctx: ContactContext) -> float:
        """Apply networking goals rule 14 with deterministic safeguards."""
        base = ctx.number("networking goals_score", 0.0)
        signal = ctx.text("networking goals_14")
        if ctx.flag("networking goals_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("networking goals_complete"):
            return 3.0
        return -3.0


    def batch_evaluate(self, records: Sequence[Mapping[str, object]]) -> list[ContactDecision]:
        return [self.evaluate(record) for record in records]

    def summarize(self, decisions: Sequence[ContactDecision]) -> dict[str, object]:
        scores = [d.score for d in decisions]
        return {"count": len(scores), "average": round(sum(scores) / len(scores), 2) if scores else 0.0, "ready": sum(d.status == "ready" for d in decisions), "review": sum(d.status == "review" for d in decisions), "needs_attention": sum(d.status == "needs_attention" for d in decisions)}

