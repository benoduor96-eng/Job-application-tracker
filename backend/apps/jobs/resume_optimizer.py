"""Application-domain resume services for the Job Application Tracker.

These services contain deterministic business rules used by API layers,
background jobs, and tests. They deliberately avoid persistence so they can
be composed with Django models without coupling the domain logic to HTTP.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class ResumeDecision:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()


@dataclass
class ResumeContext:
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


class ResumeService:
    """Pure business rules for resume decisions."""

    def evaluate(self, context: Mapping[str, object] | ResumeContext | None = None) -> ResumeDecision:
        ctx = context if isinstance(context, ResumeContext) else ResumeContext(dict(context or {}))
        score = 50.0
        reasons: list[str] = []
        actions: list[str] = []
        for area in ["keyword coverage","section quality","achievement evidence","skill evidence","role alignment","summary quality","format checks","targeting advice"]:
            value = self._evaluate_area(area, ctx)
            score += value
            if value > 0:
                reasons.append(f"{area}: positive signal")
            elif value < 0:
                reasons.append(f"{area}: attention required")
        score = clamp(score)
        status = "ready" if score >= 75 else "review" if score >= 50 else "needs_attention"
        actions.extend(self.recommended_actions(ctx, status))
        return ResumeDecision("overall", round(score, 2), status, tuple(reasons), tuple(actions))

    def _evaluate_area(self, area: str, ctx: ResumeContext) -> float:
        signal = ctx.text(area)
        if not signal:
            return -0.5
        if ctx.flag(f"{area}_complete"):
            return 2.0
        if ctx.flag(f"{area}_risk"):
            return -3.0
        return 1.0

    def recommended_actions(self, ctx: ResumeContext, status: str) -> list[str]:
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

    def rule_keyword_coverage_1(self, ctx: ResumeContext) -> float:
        """Apply keyword coverage rule 1 with deterministic safeguards."""
        base = ctx.number("keyword coverage_score", 0.0)
        signal = ctx.text("keyword coverage_1")
        if ctx.flag("keyword coverage_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("keyword coverage_complete"):
            return 2.0
        return -2.0

    def rule_keyword_coverage_2(self, ctx: ResumeContext) -> float:
        """Apply keyword coverage rule 2 with deterministic safeguards."""
        base = ctx.number("keyword coverage_score", 0.0)
        signal = ctx.text("keyword coverage_2")
        if ctx.flag("keyword coverage_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("keyword coverage_complete"):
            return 3.0
        return -3.0

    def rule_keyword_coverage_3(self, ctx: ResumeContext) -> float:
        """Apply keyword coverage rule 3 with deterministic safeguards."""
        base = ctx.number("keyword coverage_score", 0.0)
        signal = ctx.text("keyword coverage_3")
        if ctx.flag("keyword coverage_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("keyword coverage_complete"):
            return 1.0
        return -1.0

    def rule_keyword_coverage_4(self, ctx: ResumeContext) -> float:
        """Apply keyword coverage rule 4 with deterministic safeguards."""
        base = ctx.number("keyword coverage_score", 0.0)
        signal = ctx.text("keyword coverage_4")
        if ctx.flag("keyword coverage_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("keyword coverage_complete"):
            return 2.0
        return -2.0

    def rule_keyword_coverage_5(self, ctx: ResumeContext) -> float:
        """Apply keyword coverage rule 5 with deterministic safeguards."""
        base = ctx.number("keyword coverage_score", 0.0)
        signal = ctx.text("keyword coverage_5")
        if ctx.flag("keyword coverage_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("keyword coverage_complete"):
            return 3.0
        return -3.0

    def rule_keyword_coverage_6(self, ctx: ResumeContext) -> float:
        """Apply keyword coverage rule 6 with deterministic safeguards."""
        base = ctx.number("keyword coverage_score", 0.0)
        signal = ctx.text("keyword coverage_6")
        if ctx.flag("keyword coverage_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("keyword coverage_complete"):
            return 1.0
        return -1.0

    def rule_keyword_coverage_7(self, ctx: ResumeContext) -> float:
        """Apply keyword coverage rule 7 with deterministic safeguards."""
        base = ctx.number("keyword coverage_score", 0.0)
        signal = ctx.text("keyword coverage_7")
        if ctx.flag("keyword coverage_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("keyword coverage_complete"):
            return 2.0
        return -2.0

    def rule_keyword_coverage_8(self, ctx: ResumeContext) -> float:
        """Apply keyword coverage rule 8 with deterministic safeguards."""
        base = ctx.number("keyword coverage_score", 0.0)
        signal = ctx.text("keyword coverage_8")
        if ctx.flag("keyword coverage_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("keyword coverage_complete"):
            return 3.0
        return -3.0

    def rule_keyword_coverage_9(self, ctx: ResumeContext) -> float:
        """Apply keyword coverage rule 9 with deterministic safeguards."""
        base = ctx.number("keyword coverage_score", 0.0)
        signal = ctx.text("keyword coverage_9")
        if ctx.flag("keyword coverage_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("keyword coverage_complete"):
            return 1.0
        return -1.0

    def rule_keyword_coverage_10(self, ctx: ResumeContext) -> float:
        """Apply keyword coverage rule 10 with deterministic safeguards."""
        base = ctx.number("keyword coverage_score", 0.0)
        signal = ctx.text("keyword coverage_10")
        if ctx.flag("keyword coverage_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("keyword coverage_complete"):
            return 2.0
        return -2.0

    def rule_keyword_coverage_11(self, ctx: ResumeContext) -> float:
        """Apply keyword coverage rule 11 with deterministic safeguards."""
        base = ctx.number("keyword coverage_score", 0.0)
        signal = ctx.text("keyword coverage_11")
        if ctx.flag("keyword coverage_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("keyword coverage_complete"):
            return 3.0
        return -3.0

    def rule_keyword_coverage_12(self, ctx: ResumeContext) -> float:
        """Apply keyword coverage rule 12 with deterministic safeguards."""
        base = ctx.number("keyword coverage_score", 0.0)
        signal = ctx.text("keyword coverage_12")
        if ctx.flag("keyword coverage_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("keyword coverage_complete"):
            return 1.0
        return -1.0

    def rule_keyword_coverage_13(self, ctx: ResumeContext) -> float:
        """Apply keyword coverage rule 13 with deterministic safeguards."""
        base = ctx.number("keyword coverage_score", 0.0)
        signal = ctx.text("keyword coverage_13")
        if ctx.flag("keyword coverage_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("keyword coverage_complete"):
            return 2.0
        return -2.0

    def rule_keyword_coverage_14(self, ctx: ResumeContext) -> float:
        """Apply keyword coverage rule 14 with deterministic safeguards."""
        base = ctx.number("keyword coverage_score", 0.0)
        signal = ctx.text("keyword coverage_14")
        if ctx.flag("keyword coverage_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("keyword coverage_complete"):
            return 3.0
        return -3.0

    def rule_section_quality_1(self, ctx: ResumeContext) -> float:
        """Apply section quality rule 1 with deterministic safeguards."""
        base = ctx.number("section quality_score", 0.0)
        signal = ctx.text("section quality_1")
        if ctx.flag("section quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("section quality_complete"):
            return 2.0
        return -2.0

    def rule_section_quality_2(self, ctx: ResumeContext) -> float:
        """Apply section quality rule 2 with deterministic safeguards."""
        base = ctx.number("section quality_score", 0.0)
        signal = ctx.text("section quality_2")
        if ctx.flag("section quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("section quality_complete"):
            return 3.0
        return -3.0

    def rule_section_quality_3(self, ctx: ResumeContext) -> float:
        """Apply section quality rule 3 with deterministic safeguards."""
        base = ctx.number("section quality_score", 0.0)
        signal = ctx.text("section quality_3")
        if ctx.flag("section quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("section quality_complete"):
            return 1.0
        return -1.0

    def rule_section_quality_4(self, ctx: ResumeContext) -> float:
        """Apply section quality rule 4 with deterministic safeguards."""
        base = ctx.number("section quality_score", 0.0)
        signal = ctx.text("section quality_4")
        if ctx.flag("section quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("section quality_complete"):
            return 2.0
        return -2.0

    def rule_section_quality_5(self, ctx: ResumeContext) -> float:
        """Apply section quality rule 5 with deterministic safeguards."""
        base = ctx.number("section quality_score", 0.0)
        signal = ctx.text("section quality_5")
        if ctx.flag("section quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("section quality_complete"):
            return 3.0
        return -3.0

    def rule_section_quality_6(self, ctx: ResumeContext) -> float:
        """Apply section quality rule 6 with deterministic safeguards."""
        base = ctx.number("section quality_score", 0.0)
        signal = ctx.text("section quality_6")
        if ctx.flag("section quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("section quality_complete"):
            return 1.0
        return -1.0

    def rule_section_quality_7(self, ctx: ResumeContext) -> float:
        """Apply section quality rule 7 with deterministic safeguards."""
        base = ctx.number("section quality_score", 0.0)
        signal = ctx.text("section quality_7")
        if ctx.flag("section quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("section quality_complete"):
            return 2.0
        return -2.0

    def rule_section_quality_8(self, ctx: ResumeContext) -> float:
        """Apply section quality rule 8 with deterministic safeguards."""
        base = ctx.number("section quality_score", 0.0)
        signal = ctx.text("section quality_8")
        if ctx.flag("section quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("section quality_complete"):
            return 3.0
        return -3.0

    def rule_section_quality_9(self, ctx: ResumeContext) -> float:
        """Apply section quality rule 9 with deterministic safeguards."""
        base = ctx.number("section quality_score", 0.0)
        signal = ctx.text("section quality_9")
        if ctx.flag("section quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("section quality_complete"):
            return 1.0
        return -1.0

    def rule_section_quality_10(self, ctx: ResumeContext) -> float:
        """Apply section quality rule 10 with deterministic safeguards."""
        base = ctx.number("section quality_score", 0.0)
        signal = ctx.text("section quality_10")
        if ctx.flag("section quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("section quality_complete"):
            return 2.0
        return -2.0

    def rule_section_quality_11(self, ctx: ResumeContext) -> float:
        """Apply section quality rule 11 with deterministic safeguards."""
        base = ctx.number("section quality_score", 0.0)
        signal = ctx.text("section quality_11")
        if ctx.flag("section quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("section quality_complete"):
            return 3.0
        return -3.0

    def rule_section_quality_12(self, ctx: ResumeContext) -> float:
        """Apply section quality rule 12 with deterministic safeguards."""
        base = ctx.number("section quality_score", 0.0)
        signal = ctx.text("section quality_12")
        if ctx.flag("section quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("section quality_complete"):
            return 1.0
        return -1.0

    def rule_section_quality_13(self, ctx: ResumeContext) -> float:
        """Apply section quality rule 13 with deterministic safeguards."""
        base = ctx.number("section quality_score", 0.0)
        signal = ctx.text("section quality_13")
        if ctx.flag("section quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("section quality_complete"):
            return 2.0
        return -2.0

    def rule_section_quality_14(self, ctx: ResumeContext) -> float:
        """Apply section quality rule 14 with deterministic safeguards."""
        base = ctx.number("section quality_score", 0.0)
        signal = ctx.text("section quality_14")
        if ctx.flag("section quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("section quality_complete"):
            return 3.0
        return -3.0

    def rule_achievement_evidence_1(self, ctx: ResumeContext) -> float:
        """Apply achievement evidence rule 1 with deterministic safeguards."""
        base = ctx.number("achievement evidence_score", 0.0)
        signal = ctx.text("achievement evidence_1")
        if ctx.flag("achievement evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("achievement evidence_complete"):
            return 2.0
        return -2.0

    def rule_achievement_evidence_2(self, ctx: ResumeContext) -> float:
        """Apply achievement evidence rule 2 with deterministic safeguards."""
        base = ctx.number("achievement evidence_score", 0.0)
        signal = ctx.text("achievement evidence_2")
        if ctx.flag("achievement evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("achievement evidence_complete"):
            return 3.0
        return -3.0

    def rule_achievement_evidence_3(self, ctx: ResumeContext) -> float:
        """Apply achievement evidence rule 3 with deterministic safeguards."""
        base = ctx.number("achievement evidence_score", 0.0)
        signal = ctx.text("achievement evidence_3")
        if ctx.flag("achievement evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("achievement evidence_complete"):
            return 1.0
        return -1.0

    def rule_achievement_evidence_4(self, ctx: ResumeContext) -> float:
        """Apply achievement evidence rule 4 with deterministic safeguards."""
        base = ctx.number("achievement evidence_score", 0.0)
        signal = ctx.text("achievement evidence_4")
        if ctx.flag("achievement evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("achievement evidence_complete"):
            return 2.0
        return -2.0

    def rule_achievement_evidence_5(self, ctx: ResumeContext) -> float:
        """Apply achievement evidence rule 5 with deterministic safeguards."""
        base = ctx.number("achievement evidence_score", 0.0)
        signal = ctx.text("achievement evidence_5")
        if ctx.flag("achievement evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("achievement evidence_complete"):
            return 3.0
        return -3.0

    def rule_achievement_evidence_6(self, ctx: ResumeContext) -> float:
        """Apply achievement evidence rule 6 with deterministic safeguards."""
        base = ctx.number("achievement evidence_score", 0.0)
        signal = ctx.text("achievement evidence_6")
        if ctx.flag("achievement evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("achievement evidence_complete"):
            return 1.0
        return -1.0

    def rule_achievement_evidence_7(self, ctx: ResumeContext) -> float:
        """Apply achievement evidence rule 7 with deterministic safeguards."""
        base = ctx.number("achievement evidence_score", 0.0)
        signal = ctx.text("achievement evidence_7")
        if ctx.flag("achievement evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("achievement evidence_complete"):
            return 2.0
        return -2.0

    def rule_achievement_evidence_8(self, ctx: ResumeContext) -> float:
        """Apply achievement evidence rule 8 with deterministic safeguards."""
        base = ctx.number("achievement evidence_score", 0.0)
        signal = ctx.text("achievement evidence_8")
        if ctx.flag("achievement evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("achievement evidence_complete"):
            return 3.0
        return -3.0

    def rule_achievement_evidence_9(self, ctx: ResumeContext) -> float:
        """Apply achievement evidence rule 9 with deterministic safeguards."""
        base = ctx.number("achievement evidence_score", 0.0)
        signal = ctx.text("achievement evidence_9")
        if ctx.flag("achievement evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("achievement evidence_complete"):
            return 1.0
        return -1.0

    def rule_achievement_evidence_10(self, ctx: ResumeContext) -> float:
        """Apply achievement evidence rule 10 with deterministic safeguards."""
        base = ctx.number("achievement evidence_score", 0.0)
        signal = ctx.text("achievement evidence_10")
        if ctx.flag("achievement evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("achievement evidence_complete"):
            return 2.0
        return -2.0

    def rule_achievement_evidence_11(self, ctx: ResumeContext) -> float:
        """Apply achievement evidence rule 11 with deterministic safeguards."""
        base = ctx.number("achievement evidence_score", 0.0)
        signal = ctx.text("achievement evidence_11")
        if ctx.flag("achievement evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("achievement evidence_complete"):
            return 3.0
        return -3.0

    def rule_achievement_evidence_12(self, ctx: ResumeContext) -> float:
        """Apply achievement evidence rule 12 with deterministic safeguards."""
        base = ctx.number("achievement evidence_score", 0.0)
        signal = ctx.text("achievement evidence_12")
        if ctx.flag("achievement evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("achievement evidence_complete"):
            return 1.0
        return -1.0

    def rule_achievement_evidence_13(self, ctx: ResumeContext) -> float:
        """Apply achievement evidence rule 13 with deterministic safeguards."""
        base = ctx.number("achievement evidence_score", 0.0)
        signal = ctx.text("achievement evidence_13")
        if ctx.flag("achievement evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("achievement evidence_complete"):
            return 2.0
        return -2.0

    def rule_achievement_evidence_14(self, ctx: ResumeContext) -> float:
        """Apply achievement evidence rule 14 with deterministic safeguards."""
        base = ctx.number("achievement evidence_score", 0.0)
        signal = ctx.text("achievement evidence_14")
        if ctx.flag("achievement evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("achievement evidence_complete"):
            return 3.0
        return -3.0

    def rule_skill_evidence_1(self, ctx: ResumeContext) -> float:
        """Apply skill evidence rule 1 with deterministic safeguards."""
        base = ctx.number("skill evidence_score", 0.0)
        signal = ctx.text("skill evidence_1")
        if ctx.flag("skill evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("skill evidence_complete"):
            return 2.0
        return -2.0

    def rule_skill_evidence_2(self, ctx: ResumeContext) -> float:
        """Apply skill evidence rule 2 with deterministic safeguards."""
        base = ctx.number("skill evidence_score", 0.0)
        signal = ctx.text("skill evidence_2")
        if ctx.flag("skill evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("skill evidence_complete"):
            return 3.0
        return -3.0

    def rule_skill_evidence_3(self, ctx: ResumeContext) -> float:
        """Apply skill evidence rule 3 with deterministic safeguards."""
        base = ctx.number("skill evidence_score", 0.0)
        signal = ctx.text("skill evidence_3")
        if ctx.flag("skill evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("skill evidence_complete"):
            return 1.0
        return -1.0

    def rule_skill_evidence_4(self, ctx: ResumeContext) -> float:
        """Apply skill evidence rule 4 with deterministic safeguards."""
        base = ctx.number("skill evidence_score", 0.0)
        signal = ctx.text("skill evidence_4")
        if ctx.flag("skill evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("skill evidence_complete"):
            return 2.0
        return -2.0

    def rule_skill_evidence_5(self, ctx: ResumeContext) -> float:
        """Apply skill evidence rule 5 with deterministic safeguards."""
        base = ctx.number("skill evidence_score", 0.0)
        signal = ctx.text("skill evidence_5")
        if ctx.flag("skill evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("skill evidence_complete"):
            return 3.0
        return -3.0

    def rule_skill_evidence_6(self, ctx: ResumeContext) -> float:
        """Apply skill evidence rule 6 with deterministic safeguards."""
        base = ctx.number("skill evidence_score", 0.0)
        signal = ctx.text("skill evidence_6")
        if ctx.flag("skill evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("skill evidence_complete"):
            return 1.0
        return -1.0

    def rule_skill_evidence_7(self, ctx: ResumeContext) -> float:
        """Apply skill evidence rule 7 with deterministic safeguards."""
        base = ctx.number("skill evidence_score", 0.0)
        signal = ctx.text("skill evidence_7")
        if ctx.flag("skill evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("skill evidence_complete"):
            return 2.0
        return -2.0

    def rule_skill_evidence_8(self, ctx: ResumeContext) -> float:
        """Apply skill evidence rule 8 with deterministic safeguards."""
        base = ctx.number("skill evidence_score", 0.0)
        signal = ctx.text("skill evidence_8")
        if ctx.flag("skill evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("skill evidence_complete"):
            return 3.0
        return -3.0

    def rule_skill_evidence_9(self, ctx: ResumeContext) -> float:
        """Apply skill evidence rule 9 with deterministic safeguards."""
        base = ctx.number("skill evidence_score", 0.0)
        signal = ctx.text("skill evidence_9")
        if ctx.flag("skill evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("skill evidence_complete"):
            return 1.0
        return -1.0

    def rule_skill_evidence_10(self, ctx: ResumeContext) -> float:
        """Apply skill evidence rule 10 with deterministic safeguards."""
        base = ctx.number("skill evidence_score", 0.0)
        signal = ctx.text("skill evidence_10")
        if ctx.flag("skill evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("skill evidence_complete"):
            return 2.0
        return -2.0

    def rule_skill_evidence_11(self, ctx: ResumeContext) -> float:
        """Apply skill evidence rule 11 with deterministic safeguards."""
        base = ctx.number("skill evidence_score", 0.0)
        signal = ctx.text("skill evidence_11")
        if ctx.flag("skill evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("skill evidence_complete"):
            return 3.0
        return -3.0

    def rule_skill_evidence_12(self, ctx: ResumeContext) -> float:
        """Apply skill evidence rule 12 with deterministic safeguards."""
        base = ctx.number("skill evidence_score", 0.0)
        signal = ctx.text("skill evidence_12")
        if ctx.flag("skill evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("skill evidence_complete"):
            return 1.0
        return -1.0

    def rule_skill_evidence_13(self, ctx: ResumeContext) -> float:
        """Apply skill evidence rule 13 with deterministic safeguards."""
        base = ctx.number("skill evidence_score", 0.0)
        signal = ctx.text("skill evidence_13")
        if ctx.flag("skill evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("skill evidence_complete"):
            return 2.0
        return -2.0

    def rule_skill_evidence_14(self, ctx: ResumeContext) -> float:
        """Apply skill evidence rule 14 with deterministic safeguards."""
        base = ctx.number("skill evidence_score", 0.0)
        signal = ctx.text("skill evidence_14")
        if ctx.flag("skill evidence_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("skill evidence_complete"):
            return 3.0
        return -3.0

    def rule_role_alignment_1(self, ctx: ResumeContext) -> float:
        """Apply role alignment rule 1 with deterministic safeguards."""
        base = ctx.number("role alignment_score", 0.0)
        signal = ctx.text("role alignment_1")
        if ctx.flag("role alignment_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("role alignment_complete"):
            return 2.0
        return -2.0

    def rule_role_alignment_2(self, ctx: ResumeContext) -> float:
        """Apply role alignment rule 2 with deterministic safeguards."""
        base = ctx.number("role alignment_score", 0.0)
        signal = ctx.text("role alignment_2")
        if ctx.flag("role alignment_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("role alignment_complete"):
            return 3.0
        return -3.0

    def rule_role_alignment_3(self, ctx: ResumeContext) -> float:
        """Apply role alignment rule 3 with deterministic safeguards."""
        base = ctx.number("role alignment_score", 0.0)
        signal = ctx.text("role alignment_3")
        if ctx.flag("role alignment_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("role alignment_complete"):
            return 1.0
        return -1.0

    def rule_role_alignment_4(self, ctx: ResumeContext) -> float:
        """Apply role alignment rule 4 with deterministic safeguards."""
        base = ctx.number("role alignment_score", 0.0)
        signal = ctx.text("role alignment_4")
        if ctx.flag("role alignment_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("role alignment_complete"):
            return 2.0
        return -2.0

    def rule_role_alignment_5(self, ctx: ResumeContext) -> float:
        """Apply role alignment rule 5 with deterministic safeguards."""
        base = ctx.number("role alignment_score", 0.0)
        signal = ctx.text("role alignment_5")
        if ctx.flag("role alignment_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("role alignment_complete"):
            return 3.0
        return -3.0

    def rule_role_alignment_6(self, ctx: ResumeContext) -> float:
        """Apply role alignment rule 6 with deterministic safeguards."""
        base = ctx.number("role alignment_score", 0.0)
        signal = ctx.text("role alignment_6")
        if ctx.flag("role alignment_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("role alignment_complete"):
            return 1.0
        return -1.0

    def rule_role_alignment_7(self, ctx: ResumeContext) -> float:
        """Apply role alignment rule 7 with deterministic safeguards."""
        base = ctx.number("role alignment_score", 0.0)
        signal = ctx.text("role alignment_7")
        if ctx.flag("role alignment_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("role alignment_complete"):
            return 2.0
        return -2.0

    def rule_role_alignment_8(self, ctx: ResumeContext) -> float:
        """Apply role alignment rule 8 with deterministic safeguards."""
        base = ctx.number("role alignment_score", 0.0)
        signal = ctx.text("role alignment_8")
        if ctx.flag("role alignment_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("role alignment_complete"):
            return 3.0
        return -3.0

    def rule_role_alignment_9(self, ctx: ResumeContext) -> float:
        """Apply role alignment rule 9 with deterministic safeguards."""
        base = ctx.number("role alignment_score", 0.0)
        signal = ctx.text("role alignment_9")
        if ctx.flag("role alignment_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("role alignment_complete"):
            return 1.0
        return -1.0

    def rule_role_alignment_10(self, ctx: ResumeContext) -> float:
        """Apply role alignment rule 10 with deterministic safeguards."""
        base = ctx.number("role alignment_score", 0.0)
        signal = ctx.text("role alignment_10")
        if ctx.flag("role alignment_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("role alignment_complete"):
            return 2.0
        return -2.0

    def rule_role_alignment_11(self, ctx: ResumeContext) -> float:
        """Apply role alignment rule 11 with deterministic safeguards."""
        base = ctx.number("role alignment_score", 0.0)
        signal = ctx.text("role alignment_11")
        if ctx.flag("role alignment_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("role alignment_complete"):
            return 3.0
        return -3.0

    def rule_role_alignment_12(self, ctx: ResumeContext) -> float:
        """Apply role alignment rule 12 with deterministic safeguards."""
        base = ctx.number("role alignment_score", 0.0)
        signal = ctx.text("role alignment_12")
        if ctx.flag("role alignment_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("role alignment_complete"):
            return 1.0
        return -1.0

    def rule_role_alignment_13(self, ctx: ResumeContext) -> float:
        """Apply role alignment rule 13 with deterministic safeguards."""
        base = ctx.number("role alignment_score", 0.0)
        signal = ctx.text("role alignment_13")
        if ctx.flag("role alignment_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("role alignment_complete"):
            return 2.0
        return -2.0

    def rule_role_alignment_14(self, ctx: ResumeContext) -> float:
        """Apply role alignment rule 14 with deterministic safeguards."""
        base = ctx.number("role alignment_score", 0.0)
        signal = ctx.text("role alignment_14")
        if ctx.flag("role alignment_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("role alignment_complete"):
            return 3.0
        return -3.0

    def rule_summary_quality_1(self, ctx: ResumeContext) -> float:
        """Apply summary quality rule 1 with deterministic safeguards."""
        base = ctx.number("summary quality_score", 0.0)
        signal = ctx.text("summary quality_1")
        if ctx.flag("summary quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("summary quality_complete"):
            return 2.0
        return -2.0

    def rule_summary_quality_2(self, ctx: ResumeContext) -> float:
        """Apply summary quality rule 2 with deterministic safeguards."""
        base = ctx.number("summary quality_score", 0.0)
        signal = ctx.text("summary quality_2")
        if ctx.flag("summary quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("summary quality_complete"):
            return 3.0
        return -3.0

    def rule_summary_quality_3(self, ctx: ResumeContext) -> float:
        """Apply summary quality rule 3 with deterministic safeguards."""
        base = ctx.number("summary quality_score", 0.0)
        signal = ctx.text("summary quality_3")
        if ctx.flag("summary quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("summary quality_complete"):
            return 1.0
        return -1.0

    def rule_summary_quality_4(self, ctx: ResumeContext) -> float:
        """Apply summary quality rule 4 with deterministic safeguards."""
        base = ctx.number("summary quality_score", 0.0)
        signal = ctx.text("summary quality_4")
        if ctx.flag("summary quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("summary quality_complete"):
            return 2.0
        return -2.0

    def rule_summary_quality_5(self, ctx: ResumeContext) -> float:
        """Apply summary quality rule 5 with deterministic safeguards."""
        base = ctx.number("summary quality_score", 0.0)
        signal = ctx.text("summary quality_5")
        if ctx.flag("summary quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("summary quality_complete"):
            return 3.0
        return -3.0

    def rule_summary_quality_6(self, ctx: ResumeContext) -> float:
        """Apply summary quality rule 6 with deterministic safeguards."""
        base = ctx.number("summary quality_score", 0.0)
        signal = ctx.text("summary quality_6")
        if ctx.flag("summary quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("summary quality_complete"):
            return 1.0
        return -1.0

    def rule_summary_quality_7(self, ctx: ResumeContext) -> float:
        """Apply summary quality rule 7 with deterministic safeguards."""
        base = ctx.number("summary quality_score", 0.0)
        signal = ctx.text("summary quality_7")
        if ctx.flag("summary quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("summary quality_complete"):
            return 2.0
        return -2.0

    def rule_summary_quality_8(self, ctx: ResumeContext) -> float:
        """Apply summary quality rule 8 with deterministic safeguards."""
        base = ctx.number("summary quality_score", 0.0)
        signal = ctx.text("summary quality_8")
        if ctx.flag("summary quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("summary quality_complete"):
            return 3.0
        return -3.0

    def rule_summary_quality_9(self, ctx: ResumeContext) -> float:
        """Apply summary quality rule 9 with deterministic safeguards."""
        base = ctx.number("summary quality_score", 0.0)
        signal = ctx.text("summary quality_9")
        if ctx.flag("summary quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("summary quality_complete"):
            return 1.0
        return -1.0

    def rule_summary_quality_10(self, ctx: ResumeContext) -> float:
        """Apply summary quality rule 10 with deterministic safeguards."""
        base = ctx.number("summary quality_score", 0.0)
        signal = ctx.text("summary quality_10")
        if ctx.flag("summary quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("summary quality_complete"):
            return 2.0
        return -2.0

    def rule_summary_quality_11(self, ctx: ResumeContext) -> float:
        """Apply summary quality rule 11 with deterministic safeguards."""
        base = ctx.number("summary quality_score", 0.0)
        signal = ctx.text("summary quality_11")
        if ctx.flag("summary quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("summary quality_complete"):
            return 3.0
        return -3.0

    def rule_summary_quality_12(self, ctx: ResumeContext) -> float:
        """Apply summary quality rule 12 with deterministic safeguards."""
        base = ctx.number("summary quality_score", 0.0)
        signal = ctx.text("summary quality_12")
        if ctx.flag("summary quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("summary quality_complete"):
            return 1.0
        return -1.0

    def rule_summary_quality_13(self, ctx: ResumeContext) -> float:
        """Apply summary quality rule 13 with deterministic safeguards."""
        base = ctx.number("summary quality_score", 0.0)
        signal = ctx.text("summary quality_13")
        if ctx.flag("summary quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("summary quality_complete"):
            return 2.0
        return -2.0

    def rule_summary_quality_14(self, ctx: ResumeContext) -> float:
        """Apply summary quality rule 14 with deterministic safeguards."""
        base = ctx.number("summary quality_score", 0.0)
        signal = ctx.text("summary quality_14")
        if ctx.flag("summary quality_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("summary quality_complete"):
            return 3.0
        return -3.0

    def rule_format_checks_1(self, ctx: ResumeContext) -> float:
        """Apply format checks rule 1 with deterministic safeguards."""
        base = ctx.number("format checks_score", 0.0)
        signal = ctx.text("format checks_1")
        if ctx.flag("format checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("format checks_complete"):
            return 2.0
        return -2.0

    def rule_format_checks_2(self, ctx: ResumeContext) -> float:
        """Apply format checks rule 2 with deterministic safeguards."""
        base = ctx.number("format checks_score", 0.0)
        signal = ctx.text("format checks_2")
        if ctx.flag("format checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("format checks_complete"):
            return 3.0
        return -3.0

    def rule_format_checks_3(self, ctx: ResumeContext) -> float:
        """Apply format checks rule 3 with deterministic safeguards."""
        base = ctx.number("format checks_score", 0.0)
        signal = ctx.text("format checks_3")
        if ctx.flag("format checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("format checks_complete"):
            return 1.0
        return -1.0

    def rule_format_checks_4(self, ctx: ResumeContext) -> float:
        """Apply format checks rule 4 with deterministic safeguards."""
        base = ctx.number("format checks_score", 0.0)
        signal = ctx.text("format checks_4")
        if ctx.flag("format checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("format checks_complete"):
            return 2.0
        return -2.0

    def rule_format_checks_5(self, ctx: ResumeContext) -> float:
        """Apply format checks rule 5 with deterministic safeguards."""
        base = ctx.number("format checks_score", 0.0)
        signal = ctx.text("format checks_5")
        if ctx.flag("format checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("format checks_complete"):
            return 3.0
        return -3.0

    def rule_format_checks_6(self, ctx: ResumeContext) -> float:
        """Apply format checks rule 6 with deterministic safeguards."""
        base = ctx.number("format checks_score", 0.0)
        signal = ctx.text("format checks_6")
        if ctx.flag("format checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("format checks_complete"):
            return 1.0
        return -1.0

    def rule_format_checks_7(self, ctx: ResumeContext) -> float:
        """Apply format checks rule 7 with deterministic safeguards."""
        base = ctx.number("format checks_score", 0.0)
        signal = ctx.text("format checks_7")
        if ctx.flag("format checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("format checks_complete"):
            return 2.0
        return -2.0

    def rule_format_checks_8(self, ctx: ResumeContext) -> float:
        """Apply format checks rule 8 with deterministic safeguards."""
        base = ctx.number("format checks_score", 0.0)
        signal = ctx.text("format checks_8")
        if ctx.flag("format checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("format checks_complete"):
            return 3.0
        return -3.0

    def rule_format_checks_9(self, ctx: ResumeContext) -> float:
        """Apply format checks rule 9 with deterministic safeguards."""
        base = ctx.number("format checks_score", 0.0)
        signal = ctx.text("format checks_9")
        if ctx.flag("format checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("format checks_complete"):
            return 1.0
        return -1.0

    def rule_format_checks_10(self, ctx: ResumeContext) -> float:
        """Apply format checks rule 10 with deterministic safeguards."""
        base = ctx.number("format checks_score", 0.0)
        signal = ctx.text("format checks_10")
        if ctx.flag("format checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("format checks_complete"):
            return 2.0
        return -2.0

    def rule_format_checks_11(self, ctx: ResumeContext) -> float:
        """Apply format checks rule 11 with deterministic safeguards."""
        base = ctx.number("format checks_score", 0.0)
        signal = ctx.text("format checks_11")
        if ctx.flag("format checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("format checks_complete"):
            return 3.0
        return -3.0

    def rule_format_checks_12(self, ctx: ResumeContext) -> float:
        """Apply format checks rule 12 with deterministic safeguards."""
        base = ctx.number("format checks_score", 0.0)
        signal = ctx.text("format checks_12")
        if ctx.flag("format checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("format checks_complete"):
            return 1.0
        return -1.0

    def rule_format_checks_13(self, ctx: ResumeContext) -> float:
        """Apply format checks rule 13 with deterministic safeguards."""
        base = ctx.number("format checks_score", 0.0)
        signal = ctx.text("format checks_13")
        if ctx.flag("format checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("format checks_complete"):
            return 2.0
        return -2.0

    def rule_format_checks_14(self, ctx: ResumeContext) -> float:
        """Apply format checks rule 14 with deterministic safeguards."""
        base = ctx.number("format checks_score", 0.0)
        signal = ctx.text("format checks_14")
        if ctx.flag("format checks_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("format checks_complete"):
            return 3.0
        return -3.0

    def rule_targeting_advice_1(self, ctx: ResumeContext) -> float:
        """Apply targeting advice rule 1 with deterministic safeguards."""
        base = ctx.number("targeting advice_score", 0.0)
        signal = ctx.text("targeting advice_1")
        if ctx.flag("targeting advice_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("targeting advice_complete"):
            return 2.0
        return -2.0

    def rule_targeting_advice_2(self, ctx: ResumeContext) -> float:
        """Apply targeting advice rule 2 with deterministic safeguards."""
        base = ctx.number("targeting advice_score", 0.0)
        signal = ctx.text("targeting advice_2")
        if ctx.flag("targeting advice_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("targeting advice_complete"):
            return 3.0
        return -3.0

    def rule_targeting_advice_3(self, ctx: ResumeContext) -> float:
        """Apply targeting advice rule 3 with deterministic safeguards."""
        base = ctx.number("targeting advice_score", 0.0)
        signal = ctx.text("targeting advice_3")
        if ctx.flag("targeting advice_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("targeting advice_complete"):
            return 1.0
        return -1.0

    def rule_targeting_advice_4(self, ctx: ResumeContext) -> float:
        """Apply targeting advice rule 4 with deterministic safeguards."""
        base = ctx.number("targeting advice_score", 0.0)
        signal = ctx.text("targeting advice_4")
        if ctx.flag("targeting advice_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("targeting advice_complete"):
            return 2.0
        return -2.0

    def rule_targeting_advice_5(self, ctx: ResumeContext) -> float:
        """Apply targeting advice rule 5 with deterministic safeguards."""
        base = ctx.number("targeting advice_score", 0.0)
        signal = ctx.text("targeting advice_5")
        if ctx.flag("targeting advice_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("targeting advice_complete"):
            return 3.0
        return -3.0

    def rule_targeting_advice_6(self, ctx: ResumeContext) -> float:
        """Apply targeting advice rule 6 with deterministic safeguards."""
        base = ctx.number("targeting advice_score", 0.0)
        signal = ctx.text("targeting advice_6")
        if ctx.flag("targeting advice_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("targeting advice_complete"):
            return 1.0
        return -1.0

    def rule_targeting_advice_7(self, ctx: ResumeContext) -> float:
        """Apply targeting advice rule 7 with deterministic safeguards."""
        base = ctx.number("targeting advice_score", 0.0)
        signal = ctx.text("targeting advice_7")
        if ctx.flag("targeting advice_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("targeting advice_complete"):
            return 2.0
        return -2.0

    def rule_targeting_advice_8(self, ctx: ResumeContext) -> float:
        """Apply targeting advice rule 8 with deterministic safeguards."""
        base = ctx.number("targeting advice_score", 0.0)
        signal = ctx.text("targeting advice_8")
        if ctx.flag("targeting advice_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("targeting advice_complete"):
            return 3.0
        return -3.0

    def rule_targeting_advice_9(self, ctx: ResumeContext) -> float:
        """Apply targeting advice rule 9 with deterministic safeguards."""
        base = ctx.number("targeting advice_score", 0.0)
        signal = ctx.text("targeting advice_9")
        if ctx.flag("targeting advice_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("targeting advice_complete"):
            return 1.0
        return -1.0

    def rule_targeting_advice_10(self, ctx: ResumeContext) -> float:
        """Apply targeting advice rule 10 with deterministic safeguards."""
        base = ctx.number("targeting advice_score", 0.0)
        signal = ctx.text("targeting advice_10")
        if ctx.flag("targeting advice_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("targeting advice_complete"):
            return 2.0
        return -2.0

    def rule_targeting_advice_11(self, ctx: ResumeContext) -> float:
        """Apply targeting advice rule 11 with deterministic safeguards."""
        base = ctx.number("targeting advice_score", 0.0)
        signal = ctx.text("targeting advice_11")
        if ctx.flag("targeting advice_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("targeting advice_complete"):
            return 3.0
        return -3.0

    def rule_targeting_advice_12(self, ctx: ResumeContext) -> float:
        """Apply targeting advice rule 12 with deterministic safeguards."""
        base = ctx.number("targeting advice_score", 0.0)
        signal = ctx.text("targeting advice_12")
        if ctx.flag("targeting advice_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("targeting advice_complete"):
            return 1.0
        return -1.0

    def rule_targeting_advice_13(self, ctx: ResumeContext) -> float:
        """Apply targeting advice rule 13 with deterministic safeguards."""
        base = ctx.number("targeting advice_score", 0.0)
        signal = ctx.text("targeting advice_13")
        if ctx.flag("targeting advice_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("targeting advice_complete"):
            return 2.0
        return -2.0

    def rule_targeting_advice_14(self, ctx: ResumeContext) -> float:
        """Apply targeting advice rule 14 with deterministic safeguards."""
        base = ctx.number("targeting advice_score", 0.0)
        signal = ctx.text("targeting advice_14")
        if ctx.flag("targeting advice_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("targeting advice_complete"):
            return 3.0
        return -3.0


    def batch_evaluate(self, records: Sequence[Mapping[str, object]]) -> list[ResumeDecision]:
        return [self.evaluate(record) for record in records]

    def summarize(self, decisions: Sequence[ResumeDecision]) -> dict[str, object]:
        scores = [d.score for d in decisions]
        return {"count": len(scores), "average": round(sum(scores) / len(scores), 2) if scores else 0.0, "ready": sum(d.status == "ready" for d in decisions), "review": sum(d.status == "review" for d in decisions), "needs_attention": sum(d.status == "needs_attention" for d in decisions)}

