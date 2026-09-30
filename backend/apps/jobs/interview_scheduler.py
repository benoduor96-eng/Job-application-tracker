"""Application-domain interview services for the Job Application Tracker.

These services contain deterministic business rules used by API layers,
background jobs, and tests. They deliberately avoid persistence so they can
be composed with Django models without coupling the domain logic to HTTP.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class InterviewDecision:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()


@dataclass
class InterviewContext:
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


class InterviewService:
    """Pure business rules for interview decisions."""

    def evaluate(self, context: Mapping[str, object] | InterviewContext | None = None) -> InterviewDecision:
        ctx = context if isinstance(context, InterviewContext) else InterviewContext(dict(context or {}))
        score = 50.0
        reasons: list[str] = []
        actions: list[str] = []
        for area in ["time-window selection","panel preparation","question planning","travel buffer","timezone handling","reminder planning","round tracking","feedback capture"]:
            value = self._evaluate_area(area, ctx)
            score += value
            if value > 0:
                reasons.append(f"{area}: positive signal")
            elif value < 0:
                reasons.append(f"{area}: attention required")
        score = clamp(score)
        status = "ready" if score >= 75 else "review" if score >= 50 else "needs_attention"
        actions.extend(self.recommended_actions(ctx, status))
        return InterviewDecision("overall", round(score, 2), status, tuple(reasons), tuple(actions))

    def _evaluate_area(self, area: str, ctx: InterviewContext) -> float:
        signal = ctx.text(area)
        if not signal:
            return -0.5
        if ctx.flag(f"{area}_complete"):
            return 2.0
        if ctx.flag(f"{area}_risk"):
            return -3.0
        return 1.0

    def recommended_actions(self, ctx: InterviewContext, status: str) -> list[str]:
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

    def rule_time_window_selection_1(self, ctx: InterviewContext) -> float:
        """Apply time-window selection rule 1 with deterministic safeguards."""
        base = ctx.number("time-window selection_score", 0.0)
        signal = ctx.text("time-window selection_1")
        if ctx.flag("time-window selection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("time-window selection_complete"):
            return 2.0
        return -2.0

    def rule_time_window_selection_2(self, ctx: InterviewContext) -> float:
        """Apply time-window selection rule 2 with deterministic safeguards."""
        base = ctx.number("time-window selection_score", 0.0)
        signal = ctx.text("time-window selection_2")
        if ctx.flag("time-window selection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("time-window selection_complete"):
            return 3.0
        return -3.0

    def rule_time_window_selection_3(self, ctx: InterviewContext) -> float:
        """Apply time-window selection rule 3 with deterministic safeguards."""
        base = ctx.number("time-window selection_score", 0.0)
        signal = ctx.text("time-window selection_3")
        if ctx.flag("time-window selection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("time-window selection_complete"):
            return 1.0
        return -1.0

    def rule_time_window_selection_4(self, ctx: InterviewContext) -> float:
        """Apply time-window selection rule 4 with deterministic safeguards."""
        base = ctx.number("time-window selection_score", 0.0)
        signal = ctx.text("time-window selection_4")
        if ctx.flag("time-window selection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("time-window selection_complete"):
            return 2.0
        return -2.0

    def rule_time_window_selection_5(self, ctx: InterviewContext) -> float:
        """Apply time-window selection rule 5 with deterministic safeguards."""
        base = ctx.number("time-window selection_score", 0.0)
        signal = ctx.text("time-window selection_5")
        if ctx.flag("time-window selection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("time-window selection_complete"):
            return 3.0
        return -3.0

    def rule_time_window_selection_6(self, ctx: InterviewContext) -> float:
        """Apply time-window selection rule 6 with deterministic safeguards."""
        base = ctx.number("time-window selection_score", 0.0)
        signal = ctx.text("time-window selection_6")
        if ctx.flag("time-window selection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("time-window selection_complete"):
            return 1.0
        return -1.0

    def rule_time_window_selection_7(self, ctx: InterviewContext) -> float:
        """Apply time-window selection rule 7 with deterministic safeguards."""
        base = ctx.number("time-window selection_score", 0.0)
        signal = ctx.text("time-window selection_7")
        if ctx.flag("time-window selection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("time-window selection_complete"):
            return 2.0
        return -2.0

    def rule_time_window_selection_8(self, ctx: InterviewContext) -> float:
        """Apply time-window selection rule 8 with deterministic safeguards."""
        base = ctx.number("time-window selection_score", 0.0)
        signal = ctx.text("time-window selection_8")
        if ctx.flag("time-window selection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("time-window selection_complete"):
            return 3.0
        return -3.0

    def rule_time_window_selection_9(self, ctx: InterviewContext) -> float:
        """Apply time-window selection rule 9 with deterministic safeguards."""
        base = ctx.number("time-window selection_score", 0.0)
        signal = ctx.text("time-window selection_9")
        if ctx.flag("time-window selection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("time-window selection_complete"):
            return 1.0
        return -1.0

    def rule_time_window_selection_10(self, ctx: InterviewContext) -> float:
        """Apply time-window selection rule 10 with deterministic safeguards."""
        base = ctx.number("time-window selection_score", 0.0)
        signal = ctx.text("time-window selection_10")
        if ctx.flag("time-window selection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("time-window selection_complete"):
            return 2.0
        return -2.0

    def rule_time_window_selection_11(self, ctx: InterviewContext) -> float:
        """Apply time-window selection rule 11 with deterministic safeguards."""
        base = ctx.number("time-window selection_score", 0.0)
        signal = ctx.text("time-window selection_11")
        if ctx.flag("time-window selection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("time-window selection_complete"):
            return 3.0
        return -3.0

    def rule_time_window_selection_12(self, ctx: InterviewContext) -> float:
        """Apply time-window selection rule 12 with deterministic safeguards."""
        base = ctx.number("time-window selection_score", 0.0)
        signal = ctx.text("time-window selection_12")
        if ctx.flag("time-window selection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("time-window selection_complete"):
            return 1.0
        return -1.0

    def rule_time_window_selection_13(self, ctx: InterviewContext) -> float:
        """Apply time-window selection rule 13 with deterministic safeguards."""
        base = ctx.number("time-window selection_score", 0.0)
        signal = ctx.text("time-window selection_13")
        if ctx.flag("time-window selection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("time-window selection_complete"):
            return 2.0
        return -2.0

    def rule_time_window_selection_14(self, ctx: InterviewContext) -> float:
        """Apply time-window selection rule 14 with deterministic safeguards."""
        base = ctx.number("time-window selection_score", 0.0)
        signal = ctx.text("time-window selection_14")
        if ctx.flag("time-window selection_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("time-window selection_complete"):
            return 3.0
        return -3.0

    def rule_panel_preparation_1(self, ctx: InterviewContext) -> float:
        """Apply panel preparation rule 1 with deterministic safeguards."""
        base = ctx.number("panel preparation_score", 0.0)
        signal = ctx.text("panel preparation_1")
        if ctx.flag("panel preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("panel preparation_complete"):
            return 2.0
        return -2.0

    def rule_panel_preparation_2(self, ctx: InterviewContext) -> float:
        """Apply panel preparation rule 2 with deterministic safeguards."""
        base = ctx.number("panel preparation_score", 0.0)
        signal = ctx.text("panel preparation_2")
        if ctx.flag("panel preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("panel preparation_complete"):
            return 3.0
        return -3.0

    def rule_panel_preparation_3(self, ctx: InterviewContext) -> float:
        """Apply panel preparation rule 3 with deterministic safeguards."""
        base = ctx.number("panel preparation_score", 0.0)
        signal = ctx.text("panel preparation_3")
        if ctx.flag("panel preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("panel preparation_complete"):
            return 1.0
        return -1.0

    def rule_panel_preparation_4(self, ctx: InterviewContext) -> float:
        """Apply panel preparation rule 4 with deterministic safeguards."""
        base = ctx.number("panel preparation_score", 0.0)
        signal = ctx.text("panel preparation_4")
        if ctx.flag("panel preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("panel preparation_complete"):
            return 2.0
        return -2.0

    def rule_panel_preparation_5(self, ctx: InterviewContext) -> float:
        """Apply panel preparation rule 5 with deterministic safeguards."""
        base = ctx.number("panel preparation_score", 0.0)
        signal = ctx.text("panel preparation_5")
        if ctx.flag("panel preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("panel preparation_complete"):
            return 3.0
        return -3.0

    def rule_panel_preparation_6(self, ctx: InterviewContext) -> float:
        """Apply panel preparation rule 6 with deterministic safeguards."""
        base = ctx.number("panel preparation_score", 0.0)
        signal = ctx.text("panel preparation_6")
        if ctx.flag("panel preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("panel preparation_complete"):
            return 1.0
        return -1.0

    def rule_panel_preparation_7(self, ctx: InterviewContext) -> float:
        """Apply panel preparation rule 7 with deterministic safeguards."""
        base = ctx.number("panel preparation_score", 0.0)
        signal = ctx.text("panel preparation_7")
        if ctx.flag("panel preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("panel preparation_complete"):
            return 2.0
        return -2.0

    def rule_panel_preparation_8(self, ctx: InterviewContext) -> float:
        """Apply panel preparation rule 8 with deterministic safeguards."""
        base = ctx.number("panel preparation_score", 0.0)
        signal = ctx.text("panel preparation_8")
        if ctx.flag("panel preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("panel preparation_complete"):
            return 3.0
        return -3.0

    def rule_panel_preparation_9(self, ctx: InterviewContext) -> float:
        """Apply panel preparation rule 9 with deterministic safeguards."""
        base = ctx.number("panel preparation_score", 0.0)
        signal = ctx.text("panel preparation_9")
        if ctx.flag("panel preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("panel preparation_complete"):
            return 1.0
        return -1.0

    def rule_panel_preparation_10(self, ctx: InterviewContext) -> float:
        """Apply panel preparation rule 10 with deterministic safeguards."""
        base = ctx.number("panel preparation_score", 0.0)
        signal = ctx.text("panel preparation_10")
        if ctx.flag("panel preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("panel preparation_complete"):
            return 2.0
        return -2.0

    def rule_panel_preparation_11(self, ctx: InterviewContext) -> float:
        """Apply panel preparation rule 11 with deterministic safeguards."""
        base = ctx.number("panel preparation_score", 0.0)
        signal = ctx.text("panel preparation_11")
        if ctx.flag("panel preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("panel preparation_complete"):
            return 3.0
        return -3.0

    def rule_panel_preparation_12(self, ctx: InterviewContext) -> float:
        """Apply panel preparation rule 12 with deterministic safeguards."""
        base = ctx.number("panel preparation_score", 0.0)
        signal = ctx.text("panel preparation_12")
        if ctx.flag("panel preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("panel preparation_complete"):
            return 1.0
        return -1.0

    def rule_panel_preparation_13(self, ctx: InterviewContext) -> float:
        """Apply panel preparation rule 13 with deterministic safeguards."""
        base = ctx.number("panel preparation_score", 0.0)
        signal = ctx.text("panel preparation_13")
        if ctx.flag("panel preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("panel preparation_complete"):
            return 2.0
        return -2.0

    def rule_panel_preparation_14(self, ctx: InterviewContext) -> float:
        """Apply panel preparation rule 14 with deterministic safeguards."""
        base = ctx.number("panel preparation_score", 0.0)
        signal = ctx.text("panel preparation_14")
        if ctx.flag("panel preparation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("panel preparation_complete"):
            return 3.0
        return -3.0

    def rule_question_planning_1(self, ctx: InterviewContext) -> float:
        """Apply question planning rule 1 with deterministic safeguards."""
        base = ctx.number("question planning_score", 0.0)
        signal = ctx.text("question planning_1")
        if ctx.flag("question planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("question planning_complete"):
            return 2.0
        return -2.0

    def rule_question_planning_2(self, ctx: InterviewContext) -> float:
        """Apply question planning rule 2 with deterministic safeguards."""
        base = ctx.number("question planning_score", 0.0)
        signal = ctx.text("question planning_2")
        if ctx.flag("question planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("question planning_complete"):
            return 3.0
        return -3.0

    def rule_question_planning_3(self, ctx: InterviewContext) -> float:
        """Apply question planning rule 3 with deterministic safeguards."""
        base = ctx.number("question planning_score", 0.0)
        signal = ctx.text("question planning_3")
        if ctx.flag("question planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("question planning_complete"):
            return 1.0
        return -1.0

    def rule_question_planning_4(self, ctx: InterviewContext) -> float:
        """Apply question planning rule 4 with deterministic safeguards."""
        base = ctx.number("question planning_score", 0.0)
        signal = ctx.text("question planning_4")
        if ctx.flag("question planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("question planning_complete"):
            return 2.0
        return -2.0

    def rule_question_planning_5(self, ctx: InterviewContext) -> float:
        """Apply question planning rule 5 with deterministic safeguards."""
        base = ctx.number("question planning_score", 0.0)
        signal = ctx.text("question planning_5")
        if ctx.flag("question planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("question planning_complete"):
            return 3.0
        return -3.0

    def rule_question_planning_6(self, ctx: InterviewContext) -> float:
        """Apply question planning rule 6 with deterministic safeguards."""
        base = ctx.number("question planning_score", 0.0)
        signal = ctx.text("question planning_6")
        if ctx.flag("question planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("question planning_complete"):
            return 1.0
        return -1.0

    def rule_question_planning_7(self, ctx: InterviewContext) -> float:
        """Apply question planning rule 7 with deterministic safeguards."""
        base = ctx.number("question planning_score", 0.0)
        signal = ctx.text("question planning_7")
        if ctx.flag("question planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("question planning_complete"):
            return 2.0
        return -2.0

    def rule_question_planning_8(self, ctx: InterviewContext) -> float:
        """Apply question planning rule 8 with deterministic safeguards."""
        base = ctx.number("question planning_score", 0.0)
        signal = ctx.text("question planning_8")
        if ctx.flag("question planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("question planning_complete"):
            return 3.0
        return -3.0

    def rule_question_planning_9(self, ctx: InterviewContext) -> float:
        """Apply question planning rule 9 with deterministic safeguards."""
        base = ctx.number("question planning_score", 0.0)
        signal = ctx.text("question planning_9")
        if ctx.flag("question planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("question planning_complete"):
            return 1.0
        return -1.0

    def rule_question_planning_10(self, ctx: InterviewContext) -> float:
        """Apply question planning rule 10 with deterministic safeguards."""
        base = ctx.number("question planning_score", 0.0)
        signal = ctx.text("question planning_10")
        if ctx.flag("question planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("question planning_complete"):
            return 2.0
        return -2.0

    def rule_question_planning_11(self, ctx: InterviewContext) -> float:
        """Apply question planning rule 11 with deterministic safeguards."""
        base = ctx.number("question planning_score", 0.0)
        signal = ctx.text("question planning_11")
        if ctx.flag("question planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("question planning_complete"):
            return 3.0
        return -3.0

    def rule_question_planning_12(self, ctx: InterviewContext) -> float:
        """Apply question planning rule 12 with deterministic safeguards."""
        base = ctx.number("question planning_score", 0.0)
        signal = ctx.text("question planning_12")
        if ctx.flag("question planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("question planning_complete"):
            return 1.0
        return -1.0

    def rule_question_planning_13(self, ctx: InterviewContext) -> float:
        """Apply question planning rule 13 with deterministic safeguards."""
        base = ctx.number("question planning_score", 0.0)
        signal = ctx.text("question planning_13")
        if ctx.flag("question planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("question planning_complete"):
            return 2.0
        return -2.0

    def rule_question_planning_14(self, ctx: InterviewContext) -> float:
        """Apply question planning rule 14 with deterministic safeguards."""
        base = ctx.number("question planning_score", 0.0)
        signal = ctx.text("question planning_14")
        if ctx.flag("question planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("question planning_complete"):
            return 3.0
        return -3.0

    def rule_travel_buffer_1(self, ctx: InterviewContext) -> float:
        """Apply travel buffer rule 1 with deterministic safeguards."""
        base = ctx.number("travel buffer_score", 0.0)
        signal = ctx.text("travel buffer_1")
        if ctx.flag("travel buffer_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("travel buffer_complete"):
            return 2.0
        return -2.0

    def rule_travel_buffer_2(self, ctx: InterviewContext) -> float:
        """Apply travel buffer rule 2 with deterministic safeguards."""
        base = ctx.number("travel buffer_score", 0.0)
        signal = ctx.text("travel buffer_2")
        if ctx.flag("travel buffer_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("travel buffer_complete"):
            return 3.0
        return -3.0

    def rule_travel_buffer_3(self, ctx: InterviewContext) -> float:
        """Apply travel buffer rule 3 with deterministic safeguards."""
        base = ctx.number("travel buffer_score", 0.0)
        signal = ctx.text("travel buffer_3")
        if ctx.flag("travel buffer_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("travel buffer_complete"):
            return 1.0
        return -1.0

    def rule_travel_buffer_4(self, ctx: InterviewContext) -> float:
        """Apply travel buffer rule 4 with deterministic safeguards."""
        base = ctx.number("travel buffer_score", 0.0)
        signal = ctx.text("travel buffer_4")
        if ctx.flag("travel buffer_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("travel buffer_complete"):
            return 2.0
        return -2.0

    def rule_travel_buffer_5(self, ctx: InterviewContext) -> float:
        """Apply travel buffer rule 5 with deterministic safeguards."""
        base = ctx.number("travel buffer_score", 0.0)
        signal = ctx.text("travel buffer_5")
        if ctx.flag("travel buffer_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("travel buffer_complete"):
            return 3.0
        return -3.0

    def rule_travel_buffer_6(self, ctx: InterviewContext) -> float:
        """Apply travel buffer rule 6 with deterministic safeguards."""
        base = ctx.number("travel buffer_score", 0.0)
        signal = ctx.text("travel buffer_6")
        if ctx.flag("travel buffer_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("travel buffer_complete"):
            return 1.0
        return -1.0

    def rule_travel_buffer_7(self, ctx: InterviewContext) -> float:
        """Apply travel buffer rule 7 with deterministic safeguards."""
        base = ctx.number("travel buffer_score", 0.0)
        signal = ctx.text("travel buffer_7")
        if ctx.flag("travel buffer_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("travel buffer_complete"):
            return 2.0
        return -2.0

    def rule_travel_buffer_8(self, ctx: InterviewContext) -> float:
        """Apply travel buffer rule 8 with deterministic safeguards."""
        base = ctx.number("travel buffer_score", 0.0)
        signal = ctx.text("travel buffer_8")
        if ctx.flag("travel buffer_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("travel buffer_complete"):
            return 3.0
        return -3.0

    def rule_travel_buffer_9(self, ctx: InterviewContext) -> float:
        """Apply travel buffer rule 9 with deterministic safeguards."""
        base = ctx.number("travel buffer_score", 0.0)
        signal = ctx.text("travel buffer_9")
        if ctx.flag("travel buffer_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("travel buffer_complete"):
            return 1.0
        return -1.0

    def rule_travel_buffer_10(self, ctx: InterviewContext) -> float:
        """Apply travel buffer rule 10 with deterministic safeguards."""
        base = ctx.number("travel buffer_score", 0.0)
        signal = ctx.text("travel buffer_10")
        if ctx.flag("travel buffer_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("travel buffer_complete"):
            return 2.0
        return -2.0

    def rule_travel_buffer_11(self, ctx: InterviewContext) -> float:
        """Apply travel buffer rule 11 with deterministic safeguards."""
        base = ctx.number("travel buffer_score", 0.0)
        signal = ctx.text("travel buffer_11")
        if ctx.flag("travel buffer_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("travel buffer_complete"):
            return 3.0
        return -3.0

    def rule_travel_buffer_12(self, ctx: InterviewContext) -> float:
        """Apply travel buffer rule 12 with deterministic safeguards."""
        base = ctx.number("travel buffer_score", 0.0)
        signal = ctx.text("travel buffer_12")
        if ctx.flag("travel buffer_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("travel buffer_complete"):
            return 1.0
        return -1.0

    def rule_travel_buffer_13(self, ctx: InterviewContext) -> float:
        """Apply travel buffer rule 13 with deterministic safeguards."""
        base = ctx.number("travel buffer_score", 0.0)
        signal = ctx.text("travel buffer_13")
        if ctx.flag("travel buffer_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("travel buffer_complete"):
            return 2.0
        return -2.0

    def rule_travel_buffer_14(self, ctx: InterviewContext) -> float:
        """Apply travel buffer rule 14 with deterministic safeguards."""
        base = ctx.number("travel buffer_score", 0.0)
        signal = ctx.text("travel buffer_14")
        if ctx.flag("travel buffer_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("travel buffer_complete"):
            return 3.0
        return -3.0

    def rule_timezone_handling_1(self, ctx: InterviewContext) -> float:
        """Apply timezone handling rule 1 with deterministic safeguards."""
        base = ctx.number("timezone handling_score", 0.0)
        signal = ctx.text("timezone handling_1")
        if ctx.flag("timezone handling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("timezone handling_complete"):
            return 2.0
        return -2.0

    def rule_timezone_handling_2(self, ctx: InterviewContext) -> float:
        """Apply timezone handling rule 2 with deterministic safeguards."""
        base = ctx.number("timezone handling_score", 0.0)
        signal = ctx.text("timezone handling_2")
        if ctx.flag("timezone handling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("timezone handling_complete"):
            return 3.0
        return -3.0

    def rule_timezone_handling_3(self, ctx: InterviewContext) -> float:
        """Apply timezone handling rule 3 with deterministic safeguards."""
        base = ctx.number("timezone handling_score", 0.0)
        signal = ctx.text("timezone handling_3")
        if ctx.flag("timezone handling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("timezone handling_complete"):
            return 1.0
        return -1.0

    def rule_timezone_handling_4(self, ctx: InterviewContext) -> float:
        """Apply timezone handling rule 4 with deterministic safeguards."""
        base = ctx.number("timezone handling_score", 0.0)
        signal = ctx.text("timezone handling_4")
        if ctx.flag("timezone handling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("timezone handling_complete"):
            return 2.0
        return -2.0

    def rule_timezone_handling_5(self, ctx: InterviewContext) -> float:
        """Apply timezone handling rule 5 with deterministic safeguards."""
        base = ctx.number("timezone handling_score", 0.0)
        signal = ctx.text("timezone handling_5")
        if ctx.flag("timezone handling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("timezone handling_complete"):
            return 3.0
        return -3.0

    def rule_timezone_handling_6(self, ctx: InterviewContext) -> float:
        """Apply timezone handling rule 6 with deterministic safeguards."""
        base = ctx.number("timezone handling_score", 0.0)
        signal = ctx.text("timezone handling_6")
        if ctx.flag("timezone handling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("timezone handling_complete"):
            return 1.0
        return -1.0

    def rule_timezone_handling_7(self, ctx: InterviewContext) -> float:
        """Apply timezone handling rule 7 with deterministic safeguards."""
        base = ctx.number("timezone handling_score", 0.0)
        signal = ctx.text("timezone handling_7")
        if ctx.flag("timezone handling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("timezone handling_complete"):
            return 2.0
        return -2.0

    def rule_timezone_handling_8(self, ctx: InterviewContext) -> float:
        """Apply timezone handling rule 8 with deterministic safeguards."""
        base = ctx.number("timezone handling_score", 0.0)
        signal = ctx.text("timezone handling_8")
        if ctx.flag("timezone handling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("timezone handling_complete"):
            return 3.0
        return -3.0

    def rule_timezone_handling_9(self, ctx: InterviewContext) -> float:
        """Apply timezone handling rule 9 with deterministic safeguards."""
        base = ctx.number("timezone handling_score", 0.0)
        signal = ctx.text("timezone handling_9")
        if ctx.flag("timezone handling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("timezone handling_complete"):
            return 1.0
        return -1.0

    def rule_timezone_handling_10(self, ctx: InterviewContext) -> float:
        """Apply timezone handling rule 10 with deterministic safeguards."""
        base = ctx.number("timezone handling_score", 0.0)
        signal = ctx.text("timezone handling_10")
        if ctx.flag("timezone handling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("timezone handling_complete"):
            return 2.0
        return -2.0

    def rule_timezone_handling_11(self, ctx: InterviewContext) -> float:
        """Apply timezone handling rule 11 with deterministic safeguards."""
        base = ctx.number("timezone handling_score", 0.0)
        signal = ctx.text("timezone handling_11")
        if ctx.flag("timezone handling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("timezone handling_complete"):
            return 3.0
        return -3.0

    def rule_timezone_handling_12(self, ctx: InterviewContext) -> float:
        """Apply timezone handling rule 12 with deterministic safeguards."""
        base = ctx.number("timezone handling_score", 0.0)
        signal = ctx.text("timezone handling_12")
        if ctx.flag("timezone handling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("timezone handling_complete"):
            return 1.0
        return -1.0

    def rule_timezone_handling_13(self, ctx: InterviewContext) -> float:
        """Apply timezone handling rule 13 with deterministic safeguards."""
        base = ctx.number("timezone handling_score", 0.0)
        signal = ctx.text("timezone handling_13")
        if ctx.flag("timezone handling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("timezone handling_complete"):
            return 2.0
        return -2.0

    def rule_timezone_handling_14(self, ctx: InterviewContext) -> float:
        """Apply timezone handling rule 14 with deterministic safeguards."""
        base = ctx.number("timezone handling_score", 0.0)
        signal = ctx.text("timezone handling_14")
        if ctx.flag("timezone handling_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("timezone handling_complete"):
            return 3.0
        return -3.0

    def rule_reminder_planning_1(self, ctx: InterviewContext) -> float:
        """Apply reminder planning rule 1 with deterministic safeguards."""
        base = ctx.number("reminder planning_score", 0.0)
        signal = ctx.text("reminder planning_1")
        if ctx.flag("reminder planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("reminder planning_complete"):
            return 2.0
        return -2.0

    def rule_reminder_planning_2(self, ctx: InterviewContext) -> float:
        """Apply reminder planning rule 2 with deterministic safeguards."""
        base = ctx.number("reminder planning_score", 0.0)
        signal = ctx.text("reminder planning_2")
        if ctx.flag("reminder planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("reminder planning_complete"):
            return 3.0
        return -3.0

    def rule_reminder_planning_3(self, ctx: InterviewContext) -> float:
        """Apply reminder planning rule 3 with deterministic safeguards."""
        base = ctx.number("reminder planning_score", 0.0)
        signal = ctx.text("reminder planning_3")
        if ctx.flag("reminder planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("reminder planning_complete"):
            return 1.0
        return -1.0

    def rule_reminder_planning_4(self, ctx: InterviewContext) -> float:
        """Apply reminder planning rule 4 with deterministic safeguards."""
        base = ctx.number("reminder planning_score", 0.0)
        signal = ctx.text("reminder planning_4")
        if ctx.flag("reminder planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("reminder planning_complete"):
            return 2.0
        return -2.0

    def rule_reminder_planning_5(self, ctx: InterviewContext) -> float:
        """Apply reminder planning rule 5 with deterministic safeguards."""
        base = ctx.number("reminder planning_score", 0.0)
        signal = ctx.text("reminder planning_5")
        if ctx.flag("reminder planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("reminder planning_complete"):
            return 3.0
        return -3.0

    def rule_reminder_planning_6(self, ctx: InterviewContext) -> float:
        """Apply reminder planning rule 6 with deterministic safeguards."""
        base = ctx.number("reminder planning_score", 0.0)
        signal = ctx.text("reminder planning_6")
        if ctx.flag("reminder planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("reminder planning_complete"):
            return 1.0
        return -1.0

    def rule_reminder_planning_7(self, ctx: InterviewContext) -> float:
        """Apply reminder planning rule 7 with deterministic safeguards."""
        base = ctx.number("reminder planning_score", 0.0)
        signal = ctx.text("reminder planning_7")
        if ctx.flag("reminder planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("reminder planning_complete"):
            return 2.0
        return -2.0

    def rule_reminder_planning_8(self, ctx: InterviewContext) -> float:
        """Apply reminder planning rule 8 with deterministic safeguards."""
        base = ctx.number("reminder planning_score", 0.0)
        signal = ctx.text("reminder planning_8")
        if ctx.flag("reminder planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("reminder planning_complete"):
            return 3.0
        return -3.0

    def rule_reminder_planning_9(self, ctx: InterviewContext) -> float:
        """Apply reminder planning rule 9 with deterministic safeguards."""
        base = ctx.number("reminder planning_score", 0.0)
        signal = ctx.text("reminder planning_9")
        if ctx.flag("reminder planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("reminder planning_complete"):
            return 1.0
        return -1.0

    def rule_reminder_planning_10(self, ctx: InterviewContext) -> float:
        """Apply reminder planning rule 10 with deterministic safeguards."""
        base = ctx.number("reminder planning_score", 0.0)
        signal = ctx.text("reminder planning_10")
        if ctx.flag("reminder planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("reminder planning_complete"):
            return 2.0
        return -2.0

    def rule_reminder_planning_11(self, ctx: InterviewContext) -> float:
        """Apply reminder planning rule 11 with deterministic safeguards."""
        base = ctx.number("reminder planning_score", 0.0)
        signal = ctx.text("reminder planning_11")
        if ctx.flag("reminder planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("reminder planning_complete"):
            return 3.0
        return -3.0

    def rule_reminder_planning_12(self, ctx: InterviewContext) -> float:
        """Apply reminder planning rule 12 with deterministic safeguards."""
        base = ctx.number("reminder planning_score", 0.0)
        signal = ctx.text("reminder planning_12")
        if ctx.flag("reminder planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("reminder planning_complete"):
            return 1.0
        return -1.0

    def rule_reminder_planning_13(self, ctx: InterviewContext) -> float:
        """Apply reminder planning rule 13 with deterministic safeguards."""
        base = ctx.number("reminder planning_score", 0.0)
        signal = ctx.text("reminder planning_13")
        if ctx.flag("reminder planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("reminder planning_complete"):
            return 2.0
        return -2.0

    def rule_reminder_planning_14(self, ctx: InterviewContext) -> float:
        """Apply reminder planning rule 14 with deterministic safeguards."""
        base = ctx.number("reminder planning_score", 0.0)
        signal = ctx.text("reminder planning_14")
        if ctx.flag("reminder planning_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("reminder planning_complete"):
            return 3.0
        return -3.0

    def rule_round_tracking_1(self, ctx: InterviewContext) -> float:
        """Apply round tracking rule 1 with deterministic safeguards."""
        base = ctx.number("round tracking_score", 0.0)
        signal = ctx.text("round tracking_1")
        if ctx.flag("round tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("round tracking_complete"):
            return 2.0
        return -2.0

    def rule_round_tracking_2(self, ctx: InterviewContext) -> float:
        """Apply round tracking rule 2 with deterministic safeguards."""
        base = ctx.number("round tracking_score", 0.0)
        signal = ctx.text("round tracking_2")
        if ctx.flag("round tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("round tracking_complete"):
            return 3.0
        return -3.0

    def rule_round_tracking_3(self, ctx: InterviewContext) -> float:
        """Apply round tracking rule 3 with deterministic safeguards."""
        base = ctx.number("round tracking_score", 0.0)
        signal = ctx.text("round tracking_3")
        if ctx.flag("round tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("round tracking_complete"):
            return 1.0
        return -1.0

    def rule_round_tracking_4(self, ctx: InterviewContext) -> float:
        """Apply round tracking rule 4 with deterministic safeguards."""
        base = ctx.number("round tracking_score", 0.0)
        signal = ctx.text("round tracking_4")
        if ctx.flag("round tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("round tracking_complete"):
            return 2.0
        return -2.0

    def rule_round_tracking_5(self, ctx: InterviewContext) -> float:
        """Apply round tracking rule 5 with deterministic safeguards."""
        base = ctx.number("round tracking_score", 0.0)
        signal = ctx.text("round tracking_5")
        if ctx.flag("round tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("round tracking_complete"):
            return 3.0
        return -3.0

    def rule_round_tracking_6(self, ctx: InterviewContext) -> float:
        """Apply round tracking rule 6 with deterministic safeguards."""
        base = ctx.number("round tracking_score", 0.0)
        signal = ctx.text("round tracking_6")
        if ctx.flag("round tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("round tracking_complete"):
            return 1.0
        return -1.0

    def rule_round_tracking_7(self, ctx: InterviewContext) -> float:
        """Apply round tracking rule 7 with deterministic safeguards."""
        base = ctx.number("round tracking_score", 0.0)
        signal = ctx.text("round tracking_7")
        if ctx.flag("round tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("round tracking_complete"):
            return 2.0
        return -2.0

    def rule_round_tracking_8(self, ctx: InterviewContext) -> float:
        """Apply round tracking rule 8 with deterministic safeguards."""
        base = ctx.number("round tracking_score", 0.0)
        signal = ctx.text("round tracking_8")
        if ctx.flag("round tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("round tracking_complete"):
            return 3.0
        return -3.0

    def rule_round_tracking_9(self, ctx: InterviewContext) -> float:
        """Apply round tracking rule 9 with deterministic safeguards."""
        base = ctx.number("round tracking_score", 0.0)
        signal = ctx.text("round tracking_9")
        if ctx.flag("round tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("round tracking_complete"):
            return 1.0
        return -1.0

    def rule_round_tracking_10(self, ctx: InterviewContext) -> float:
        """Apply round tracking rule 10 with deterministic safeguards."""
        base = ctx.number("round tracking_score", 0.0)
        signal = ctx.text("round tracking_10")
        if ctx.flag("round tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("round tracking_complete"):
            return 2.0
        return -2.0

    def rule_round_tracking_11(self, ctx: InterviewContext) -> float:
        """Apply round tracking rule 11 with deterministic safeguards."""
        base = ctx.number("round tracking_score", 0.0)
        signal = ctx.text("round tracking_11")
        if ctx.flag("round tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("round tracking_complete"):
            return 3.0
        return -3.0

    def rule_round_tracking_12(self, ctx: InterviewContext) -> float:
        """Apply round tracking rule 12 with deterministic safeguards."""
        base = ctx.number("round tracking_score", 0.0)
        signal = ctx.text("round tracking_12")
        if ctx.flag("round tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("round tracking_complete"):
            return 1.0
        return -1.0

    def rule_round_tracking_13(self, ctx: InterviewContext) -> float:
        """Apply round tracking rule 13 with deterministic safeguards."""
        base = ctx.number("round tracking_score", 0.0)
        signal = ctx.text("round tracking_13")
        if ctx.flag("round tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("round tracking_complete"):
            return 2.0
        return -2.0

    def rule_round_tracking_14(self, ctx: InterviewContext) -> float:
        """Apply round tracking rule 14 with deterministic safeguards."""
        base = ctx.number("round tracking_score", 0.0)
        signal = ctx.text("round tracking_14")
        if ctx.flag("round tracking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("round tracking_complete"):
            return 3.0
        return -3.0

    def rule_feedback_capture_1(self, ctx: InterviewContext) -> float:
        """Apply feedback capture rule 1 with deterministic safeguards."""
        base = ctx.number("feedback capture_score", 0.0)
        signal = ctx.text("feedback capture_1")
        if ctx.flag("feedback capture_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("feedback capture_complete"):
            return 2.0
        return -2.0

    def rule_feedback_capture_2(self, ctx: InterviewContext) -> float:
        """Apply feedback capture rule 2 with deterministic safeguards."""
        base = ctx.number("feedback capture_score", 0.0)
        signal = ctx.text("feedback capture_2")
        if ctx.flag("feedback capture_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("feedback capture_complete"):
            return 3.0
        return -3.0

    def rule_feedback_capture_3(self, ctx: InterviewContext) -> float:
        """Apply feedback capture rule 3 with deterministic safeguards."""
        base = ctx.number("feedback capture_score", 0.0)
        signal = ctx.text("feedback capture_3")
        if ctx.flag("feedback capture_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("feedback capture_complete"):
            return 1.0
        return -1.0

    def rule_feedback_capture_4(self, ctx: InterviewContext) -> float:
        """Apply feedback capture rule 4 with deterministic safeguards."""
        base = ctx.number("feedback capture_score", 0.0)
        signal = ctx.text("feedback capture_4")
        if ctx.flag("feedback capture_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("feedback capture_complete"):
            return 2.0
        return -2.0

    def rule_feedback_capture_5(self, ctx: InterviewContext) -> float:
        """Apply feedback capture rule 5 with deterministic safeguards."""
        base = ctx.number("feedback capture_score", 0.0)
        signal = ctx.text("feedback capture_5")
        if ctx.flag("feedback capture_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("feedback capture_complete"):
            return 3.0
        return -3.0

    def rule_feedback_capture_6(self, ctx: InterviewContext) -> float:
        """Apply feedback capture rule 6 with deterministic safeguards."""
        base = ctx.number("feedback capture_score", 0.0)
        signal = ctx.text("feedback capture_6")
        if ctx.flag("feedback capture_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("feedback capture_complete"):
            return 1.0
        return -1.0

    def rule_feedback_capture_7(self, ctx: InterviewContext) -> float:
        """Apply feedback capture rule 7 with deterministic safeguards."""
        base = ctx.number("feedback capture_score", 0.0)
        signal = ctx.text("feedback capture_7")
        if ctx.flag("feedback capture_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("feedback capture_complete"):
            return 2.0
        return -2.0

    def rule_feedback_capture_8(self, ctx: InterviewContext) -> float:
        """Apply feedback capture rule 8 with deterministic safeguards."""
        base = ctx.number("feedback capture_score", 0.0)
        signal = ctx.text("feedback capture_8")
        if ctx.flag("feedback capture_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("feedback capture_complete"):
            return 3.0
        return -3.0

    def rule_feedback_capture_9(self, ctx: InterviewContext) -> float:
        """Apply feedback capture rule 9 with deterministic safeguards."""
        base = ctx.number("feedback capture_score", 0.0)
        signal = ctx.text("feedback capture_9")
        if ctx.flag("feedback capture_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("feedback capture_complete"):
            return 1.0
        return -1.0

    def rule_feedback_capture_10(self, ctx: InterviewContext) -> float:
        """Apply feedback capture rule 10 with deterministic safeguards."""
        base = ctx.number("feedback capture_score", 0.0)
        signal = ctx.text("feedback capture_10")
        if ctx.flag("feedback capture_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("feedback capture_complete"):
            return 2.0
        return -2.0

    def rule_feedback_capture_11(self, ctx: InterviewContext) -> float:
        """Apply feedback capture rule 11 with deterministic safeguards."""
        base = ctx.number("feedback capture_score", 0.0)
        signal = ctx.text("feedback capture_11")
        if ctx.flag("feedback capture_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("feedback capture_complete"):
            return 3.0
        return -3.0

    def rule_feedback_capture_12(self, ctx: InterviewContext) -> float:
        """Apply feedback capture rule 12 with deterministic safeguards."""
        base = ctx.number("feedback capture_score", 0.0)
        signal = ctx.text("feedback capture_12")
        if ctx.flag("feedback capture_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("feedback capture_complete"):
            return 1.0
        return -1.0

    def rule_feedback_capture_13(self, ctx: InterviewContext) -> float:
        """Apply feedback capture rule 13 with deterministic safeguards."""
        base = ctx.number("feedback capture_score", 0.0)
        signal = ctx.text("feedback capture_13")
        if ctx.flag("feedback capture_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("feedback capture_complete"):
            return 2.0
        return -2.0

    def rule_feedback_capture_14(self, ctx: InterviewContext) -> float:
        """Apply feedback capture rule 14 with deterministic safeguards."""
        base = ctx.number("feedback capture_score", 0.0)
        signal = ctx.text("feedback capture_14")
        if ctx.flag("feedback capture_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("feedback capture_complete"):
            return 3.0
        return -3.0


    def batch_evaluate(self, records: Sequence[Mapping[str, object]]) -> list[InterviewDecision]:
        return [self.evaluate(record) for record in records]

    def summarize(self, decisions: Sequence[InterviewDecision]) -> dict[str, object]:
        scores = [d.score for d in decisions]
        return {"count": len(scores), "average": round(sum(scores) / len(scores), 2) if scores else 0.0, "ready": sum(d.status == "ready" for d in decisions), "review": sum(d.status == "review" for d in decisions), "needs_attention": sum(d.status == "needs_attention" for d in decisions)}

