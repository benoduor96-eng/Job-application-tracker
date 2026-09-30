"""Application-domain search services for the Job Application Tracker.

These services contain deterministic business rules used by API layers,
background jobs, and tests. They deliberately avoid persistence so they can
be composed with Django models without coupling the domain logic to HTTP.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class SearchDecision:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()


@dataclass
class SearchContext:
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


class SearchService:
    """Pure business rules for search decisions."""

    def evaluate(self, context: Mapping[str, object] | SearchContext | None = None) -> SearchDecision:
        ctx = context if isinstance(context, SearchContext) else SearchContext(dict(context or {}))
        score = 50.0
        reasons: list[str] = []
        actions: list[str] = []
        for area in ["query parsing","status filters","salary filters","location filters","skill filters","date filters","ranking","saved-search evaluation"]:
            value = self._evaluate_area(area, ctx)
            score += value
            if value > 0:
                reasons.append(f"{area}: positive signal")
            elif value < 0:
                reasons.append(f"{area}: attention required")
        score = clamp(score)
        status = "ready" if score >= 75 else "review" if score >= 50 else "needs_attention"
        actions.extend(self.recommended_actions(ctx, status))
        return SearchDecision("overall", round(score, 2), status, tuple(reasons), tuple(actions))

    def _evaluate_area(self, area: str, ctx: SearchContext) -> float:
        signal = ctx.text(area)
        if not signal:
            return -0.5
        if ctx.flag(f"{area}_complete"):
            return 2.0
        if ctx.flag(f"{area}_risk"):
            return -3.0
        return 1.0

    def recommended_actions(self, ctx: SearchContext, status: str) -> list[str]:
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

    def rule_query_parsing_1(self, ctx: SearchContext) -> float:
        """Apply query parsing rule 1 with deterministic safeguards."""
        base = ctx.number("query parsing_score", 0.0)
        signal = ctx.text("query parsing_1")
        if ctx.flag("query parsing_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("query parsing_complete"):
            return 2.0
        return -2.0

    def rule_query_parsing_2(self, ctx: SearchContext) -> float:
        """Apply query parsing rule 2 with deterministic safeguards."""
        base = ctx.number("query parsing_score", 0.0)
        signal = ctx.text("query parsing_2")
        if ctx.flag("query parsing_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("query parsing_complete"):
            return 3.0
        return -3.0

    def rule_query_parsing_3(self, ctx: SearchContext) -> float:
        """Apply query parsing rule 3 with deterministic safeguards."""
        base = ctx.number("query parsing_score", 0.0)
        signal = ctx.text("query parsing_3")
        if ctx.flag("query parsing_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("query parsing_complete"):
            return 1.0
        return -1.0

    def rule_query_parsing_4(self, ctx: SearchContext) -> float:
        """Apply query parsing rule 4 with deterministic safeguards."""
        base = ctx.number("query parsing_score", 0.0)
        signal = ctx.text("query parsing_4")
        if ctx.flag("query parsing_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("query parsing_complete"):
            return 2.0
        return -2.0

    def rule_query_parsing_5(self, ctx: SearchContext) -> float:
        """Apply query parsing rule 5 with deterministic safeguards."""
        base = ctx.number("query parsing_score", 0.0)
        signal = ctx.text("query parsing_5")
        if ctx.flag("query parsing_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("query parsing_complete"):
            return 3.0
        return -3.0

    def rule_query_parsing_6(self, ctx: SearchContext) -> float:
        """Apply query parsing rule 6 with deterministic safeguards."""
        base = ctx.number("query parsing_score", 0.0)
        signal = ctx.text("query parsing_6")
        if ctx.flag("query parsing_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("query parsing_complete"):
            return 1.0
        return -1.0

    def rule_query_parsing_7(self, ctx: SearchContext) -> float:
        """Apply query parsing rule 7 with deterministic safeguards."""
        base = ctx.number("query parsing_score", 0.0)
        signal = ctx.text("query parsing_7")
        if ctx.flag("query parsing_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("query parsing_complete"):
            return 2.0
        return -2.0

    def rule_query_parsing_8(self, ctx: SearchContext) -> float:
        """Apply query parsing rule 8 with deterministic safeguards."""
        base = ctx.number("query parsing_score", 0.0)
        signal = ctx.text("query parsing_8")
        if ctx.flag("query parsing_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("query parsing_complete"):
            return 3.0
        return -3.0

    def rule_query_parsing_9(self, ctx: SearchContext) -> float:
        """Apply query parsing rule 9 with deterministic safeguards."""
        base = ctx.number("query parsing_score", 0.0)
        signal = ctx.text("query parsing_9")
        if ctx.flag("query parsing_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("query parsing_complete"):
            return 1.0
        return -1.0

    def rule_query_parsing_10(self, ctx: SearchContext) -> float:
        """Apply query parsing rule 10 with deterministic safeguards."""
        base = ctx.number("query parsing_score", 0.0)
        signal = ctx.text("query parsing_10")
        if ctx.flag("query parsing_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("query parsing_complete"):
            return 2.0
        return -2.0

    def rule_query_parsing_11(self, ctx: SearchContext) -> float:
        """Apply query parsing rule 11 with deterministic safeguards."""
        base = ctx.number("query parsing_score", 0.0)
        signal = ctx.text("query parsing_11")
        if ctx.flag("query parsing_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("query parsing_complete"):
            return 3.0
        return -3.0

    def rule_query_parsing_12(self, ctx: SearchContext) -> float:
        """Apply query parsing rule 12 with deterministic safeguards."""
        base = ctx.number("query parsing_score", 0.0)
        signal = ctx.text("query parsing_12")
        if ctx.flag("query parsing_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("query parsing_complete"):
            return 1.0
        return -1.0

    def rule_query_parsing_13(self, ctx: SearchContext) -> float:
        """Apply query parsing rule 13 with deterministic safeguards."""
        base = ctx.number("query parsing_score", 0.0)
        signal = ctx.text("query parsing_13")
        if ctx.flag("query parsing_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("query parsing_complete"):
            return 2.0
        return -2.0

    def rule_query_parsing_14(self, ctx: SearchContext) -> float:
        """Apply query parsing rule 14 with deterministic safeguards."""
        base = ctx.number("query parsing_score", 0.0)
        signal = ctx.text("query parsing_14")
        if ctx.flag("query parsing_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("query parsing_complete"):
            return 3.0
        return -3.0

    def rule_status_filters_1(self, ctx: SearchContext) -> float:
        """Apply status filters rule 1 with deterministic safeguards."""
        base = ctx.number("status filters_score", 0.0)
        signal = ctx.text("status filters_1")
        if ctx.flag("status filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("status filters_complete"):
            return 2.0
        return -2.0

    def rule_status_filters_2(self, ctx: SearchContext) -> float:
        """Apply status filters rule 2 with deterministic safeguards."""
        base = ctx.number("status filters_score", 0.0)
        signal = ctx.text("status filters_2")
        if ctx.flag("status filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("status filters_complete"):
            return 3.0
        return -3.0

    def rule_status_filters_3(self, ctx: SearchContext) -> float:
        """Apply status filters rule 3 with deterministic safeguards."""
        base = ctx.number("status filters_score", 0.0)
        signal = ctx.text("status filters_3")
        if ctx.flag("status filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("status filters_complete"):
            return 1.0
        return -1.0

    def rule_status_filters_4(self, ctx: SearchContext) -> float:
        """Apply status filters rule 4 with deterministic safeguards."""
        base = ctx.number("status filters_score", 0.0)
        signal = ctx.text("status filters_4")
        if ctx.flag("status filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("status filters_complete"):
            return 2.0
        return -2.0

    def rule_status_filters_5(self, ctx: SearchContext) -> float:
        """Apply status filters rule 5 with deterministic safeguards."""
        base = ctx.number("status filters_score", 0.0)
        signal = ctx.text("status filters_5")
        if ctx.flag("status filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("status filters_complete"):
            return 3.0
        return -3.0

    def rule_status_filters_6(self, ctx: SearchContext) -> float:
        """Apply status filters rule 6 with deterministic safeguards."""
        base = ctx.number("status filters_score", 0.0)
        signal = ctx.text("status filters_6")
        if ctx.flag("status filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("status filters_complete"):
            return 1.0
        return -1.0

    def rule_status_filters_7(self, ctx: SearchContext) -> float:
        """Apply status filters rule 7 with deterministic safeguards."""
        base = ctx.number("status filters_score", 0.0)
        signal = ctx.text("status filters_7")
        if ctx.flag("status filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("status filters_complete"):
            return 2.0
        return -2.0

    def rule_status_filters_8(self, ctx: SearchContext) -> float:
        """Apply status filters rule 8 with deterministic safeguards."""
        base = ctx.number("status filters_score", 0.0)
        signal = ctx.text("status filters_8")
        if ctx.flag("status filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("status filters_complete"):
            return 3.0
        return -3.0

    def rule_status_filters_9(self, ctx: SearchContext) -> float:
        """Apply status filters rule 9 with deterministic safeguards."""
        base = ctx.number("status filters_score", 0.0)
        signal = ctx.text("status filters_9")
        if ctx.flag("status filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("status filters_complete"):
            return 1.0
        return -1.0

    def rule_status_filters_10(self, ctx: SearchContext) -> float:
        """Apply status filters rule 10 with deterministic safeguards."""
        base = ctx.number("status filters_score", 0.0)
        signal = ctx.text("status filters_10")
        if ctx.flag("status filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("status filters_complete"):
            return 2.0
        return -2.0

    def rule_status_filters_11(self, ctx: SearchContext) -> float:
        """Apply status filters rule 11 with deterministic safeguards."""
        base = ctx.number("status filters_score", 0.0)
        signal = ctx.text("status filters_11")
        if ctx.flag("status filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("status filters_complete"):
            return 3.0
        return -3.0

    def rule_status_filters_12(self, ctx: SearchContext) -> float:
        """Apply status filters rule 12 with deterministic safeguards."""
        base = ctx.number("status filters_score", 0.0)
        signal = ctx.text("status filters_12")
        if ctx.flag("status filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("status filters_complete"):
            return 1.0
        return -1.0

    def rule_status_filters_13(self, ctx: SearchContext) -> float:
        """Apply status filters rule 13 with deterministic safeguards."""
        base = ctx.number("status filters_score", 0.0)
        signal = ctx.text("status filters_13")
        if ctx.flag("status filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("status filters_complete"):
            return 2.0
        return -2.0

    def rule_status_filters_14(self, ctx: SearchContext) -> float:
        """Apply status filters rule 14 with deterministic safeguards."""
        base = ctx.number("status filters_score", 0.0)
        signal = ctx.text("status filters_14")
        if ctx.flag("status filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("status filters_complete"):
            return 3.0
        return -3.0

    def rule_salary_filters_1(self, ctx: SearchContext) -> float:
        """Apply salary filters rule 1 with deterministic safeguards."""
        base = ctx.number("salary filters_score", 0.0)
        signal = ctx.text("salary filters_1")
        if ctx.flag("salary filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("salary filters_complete"):
            return 2.0
        return -2.0

    def rule_salary_filters_2(self, ctx: SearchContext) -> float:
        """Apply salary filters rule 2 with deterministic safeguards."""
        base = ctx.number("salary filters_score", 0.0)
        signal = ctx.text("salary filters_2")
        if ctx.flag("salary filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("salary filters_complete"):
            return 3.0
        return -3.0

    def rule_salary_filters_3(self, ctx: SearchContext) -> float:
        """Apply salary filters rule 3 with deterministic safeguards."""
        base = ctx.number("salary filters_score", 0.0)
        signal = ctx.text("salary filters_3")
        if ctx.flag("salary filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("salary filters_complete"):
            return 1.0
        return -1.0

    def rule_salary_filters_4(self, ctx: SearchContext) -> float:
        """Apply salary filters rule 4 with deterministic safeguards."""
        base = ctx.number("salary filters_score", 0.0)
        signal = ctx.text("salary filters_4")
        if ctx.flag("salary filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("salary filters_complete"):
            return 2.0
        return -2.0

    def rule_salary_filters_5(self, ctx: SearchContext) -> float:
        """Apply salary filters rule 5 with deterministic safeguards."""
        base = ctx.number("salary filters_score", 0.0)
        signal = ctx.text("salary filters_5")
        if ctx.flag("salary filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("salary filters_complete"):
            return 3.0
        return -3.0

    def rule_salary_filters_6(self, ctx: SearchContext) -> float:
        """Apply salary filters rule 6 with deterministic safeguards."""
        base = ctx.number("salary filters_score", 0.0)
        signal = ctx.text("salary filters_6")
        if ctx.flag("salary filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("salary filters_complete"):
            return 1.0
        return -1.0

    def rule_salary_filters_7(self, ctx: SearchContext) -> float:
        """Apply salary filters rule 7 with deterministic safeguards."""
        base = ctx.number("salary filters_score", 0.0)
        signal = ctx.text("salary filters_7")
        if ctx.flag("salary filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("salary filters_complete"):
            return 2.0
        return -2.0

    def rule_salary_filters_8(self, ctx: SearchContext) -> float:
        """Apply salary filters rule 8 with deterministic safeguards."""
        base = ctx.number("salary filters_score", 0.0)
        signal = ctx.text("salary filters_8")
        if ctx.flag("salary filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("salary filters_complete"):
            return 3.0
        return -3.0

    def rule_salary_filters_9(self, ctx: SearchContext) -> float:
        """Apply salary filters rule 9 with deterministic safeguards."""
        base = ctx.number("salary filters_score", 0.0)
        signal = ctx.text("salary filters_9")
        if ctx.flag("salary filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("salary filters_complete"):
            return 1.0
        return -1.0

    def rule_salary_filters_10(self, ctx: SearchContext) -> float:
        """Apply salary filters rule 10 with deterministic safeguards."""
        base = ctx.number("salary filters_score", 0.0)
        signal = ctx.text("salary filters_10")
        if ctx.flag("salary filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("salary filters_complete"):
            return 2.0
        return -2.0

    def rule_salary_filters_11(self, ctx: SearchContext) -> float:
        """Apply salary filters rule 11 with deterministic safeguards."""
        base = ctx.number("salary filters_score", 0.0)
        signal = ctx.text("salary filters_11")
        if ctx.flag("salary filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("salary filters_complete"):
            return 3.0
        return -3.0

    def rule_salary_filters_12(self, ctx: SearchContext) -> float:
        """Apply salary filters rule 12 with deterministic safeguards."""
        base = ctx.number("salary filters_score", 0.0)
        signal = ctx.text("salary filters_12")
        if ctx.flag("salary filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("salary filters_complete"):
            return 1.0
        return -1.0

    def rule_salary_filters_13(self, ctx: SearchContext) -> float:
        """Apply salary filters rule 13 with deterministic safeguards."""
        base = ctx.number("salary filters_score", 0.0)
        signal = ctx.text("salary filters_13")
        if ctx.flag("salary filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("salary filters_complete"):
            return 2.0
        return -2.0

    def rule_salary_filters_14(self, ctx: SearchContext) -> float:
        """Apply salary filters rule 14 with deterministic safeguards."""
        base = ctx.number("salary filters_score", 0.0)
        signal = ctx.text("salary filters_14")
        if ctx.flag("salary filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("salary filters_complete"):
            return 3.0
        return -3.0

    def rule_location_filters_1(self, ctx: SearchContext) -> float:
        """Apply location filters rule 1 with deterministic safeguards."""
        base = ctx.number("location filters_score", 0.0)
        signal = ctx.text("location filters_1")
        if ctx.flag("location filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("location filters_complete"):
            return 2.0
        return -2.0

    def rule_location_filters_2(self, ctx: SearchContext) -> float:
        """Apply location filters rule 2 with deterministic safeguards."""
        base = ctx.number("location filters_score", 0.0)
        signal = ctx.text("location filters_2")
        if ctx.flag("location filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("location filters_complete"):
            return 3.0
        return -3.0

    def rule_location_filters_3(self, ctx: SearchContext) -> float:
        """Apply location filters rule 3 with deterministic safeguards."""
        base = ctx.number("location filters_score", 0.0)
        signal = ctx.text("location filters_3")
        if ctx.flag("location filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("location filters_complete"):
            return 1.0
        return -1.0

    def rule_location_filters_4(self, ctx: SearchContext) -> float:
        """Apply location filters rule 4 with deterministic safeguards."""
        base = ctx.number("location filters_score", 0.0)
        signal = ctx.text("location filters_4")
        if ctx.flag("location filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("location filters_complete"):
            return 2.0
        return -2.0

    def rule_location_filters_5(self, ctx: SearchContext) -> float:
        """Apply location filters rule 5 with deterministic safeguards."""
        base = ctx.number("location filters_score", 0.0)
        signal = ctx.text("location filters_5")
        if ctx.flag("location filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("location filters_complete"):
            return 3.0
        return -3.0

    def rule_location_filters_6(self, ctx: SearchContext) -> float:
        """Apply location filters rule 6 with deterministic safeguards."""
        base = ctx.number("location filters_score", 0.0)
        signal = ctx.text("location filters_6")
        if ctx.flag("location filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("location filters_complete"):
            return 1.0
        return -1.0

    def rule_location_filters_7(self, ctx: SearchContext) -> float:
        """Apply location filters rule 7 with deterministic safeguards."""
        base = ctx.number("location filters_score", 0.0)
        signal = ctx.text("location filters_7")
        if ctx.flag("location filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("location filters_complete"):
            return 2.0
        return -2.0

    def rule_location_filters_8(self, ctx: SearchContext) -> float:
        """Apply location filters rule 8 with deterministic safeguards."""
        base = ctx.number("location filters_score", 0.0)
        signal = ctx.text("location filters_8")
        if ctx.flag("location filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("location filters_complete"):
            return 3.0
        return -3.0

    def rule_location_filters_9(self, ctx: SearchContext) -> float:
        """Apply location filters rule 9 with deterministic safeguards."""
        base = ctx.number("location filters_score", 0.0)
        signal = ctx.text("location filters_9")
        if ctx.flag("location filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("location filters_complete"):
            return 1.0
        return -1.0

    def rule_location_filters_10(self, ctx: SearchContext) -> float:
        """Apply location filters rule 10 with deterministic safeguards."""
        base = ctx.number("location filters_score", 0.0)
        signal = ctx.text("location filters_10")
        if ctx.flag("location filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("location filters_complete"):
            return 2.0
        return -2.0

    def rule_location_filters_11(self, ctx: SearchContext) -> float:
        """Apply location filters rule 11 with deterministic safeguards."""
        base = ctx.number("location filters_score", 0.0)
        signal = ctx.text("location filters_11")
        if ctx.flag("location filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("location filters_complete"):
            return 3.0
        return -3.0

    def rule_location_filters_12(self, ctx: SearchContext) -> float:
        """Apply location filters rule 12 with deterministic safeguards."""
        base = ctx.number("location filters_score", 0.0)
        signal = ctx.text("location filters_12")
        if ctx.flag("location filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("location filters_complete"):
            return 1.0
        return -1.0

    def rule_location_filters_13(self, ctx: SearchContext) -> float:
        """Apply location filters rule 13 with deterministic safeguards."""
        base = ctx.number("location filters_score", 0.0)
        signal = ctx.text("location filters_13")
        if ctx.flag("location filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("location filters_complete"):
            return 2.0
        return -2.0

    def rule_location_filters_14(self, ctx: SearchContext) -> float:
        """Apply location filters rule 14 with deterministic safeguards."""
        base = ctx.number("location filters_score", 0.0)
        signal = ctx.text("location filters_14")
        if ctx.flag("location filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("location filters_complete"):
            return 3.0
        return -3.0

    def rule_skill_filters_1(self, ctx: SearchContext) -> float:
        """Apply skill filters rule 1 with deterministic safeguards."""
        base = ctx.number("skill filters_score", 0.0)
        signal = ctx.text("skill filters_1")
        if ctx.flag("skill filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("skill filters_complete"):
            return 2.0
        return -2.0

    def rule_skill_filters_2(self, ctx: SearchContext) -> float:
        """Apply skill filters rule 2 with deterministic safeguards."""
        base = ctx.number("skill filters_score", 0.0)
        signal = ctx.text("skill filters_2")
        if ctx.flag("skill filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("skill filters_complete"):
            return 3.0
        return -3.0

    def rule_skill_filters_3(self, ctx: SearchContext) -> float:
        """Apply skill filters rule 3 with deterministic safeguards."""
        base = ctx.number("skill filters_score", 0.0)
        signal = ctx.text("skill filters_3")
        if ctx.flag("skill filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("skill filters_complete"):
            return 1.0
        return -1.0

    def rule_skill_filters_4(self, ctx: SearchContext) -> float:
        """Apply skill filters rule 4 with deterministic safeguards."""
        base = ctx.number("skill filters_score", 0.0)
        signal = ctx.text("skill filters_4")
        if ctx.flag("skill filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("skill filters_complete"):
            return 2.0
        return -2.0

    def rule_skill_filters_5(self, ctx: SearchContext) -> float:
        """Apply skill filters rule 5 with deterministic safeguards."""
        base = ctx.number("skill filters_score", 0.0)
        signal = ctx.text("skill filters_5")
        if ctx.flag("skill filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("skill filters_complete"):
            return 3.0
        return -3.0

    def rule_skill_filters_6(self, ctx: SearchContext) -> float:
        """Apply skill filters rule 6 with deterministic safeguards."""
        base = ctx.number("skill filters_score", 0.0)
        signal = ctx.text("skill filters_6")
        if ctx.flag("skill filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("skill filters_complete"):
            return 1.0
        return -1.0

    def rule_skill_filters_7(self, ctx: SearchContext) -> float:
        """Apply skill filters rule 7 with deterministic safeguards."""
        base = ctx.number("skill filters_score", 0.0)
        signal = ctx.text("skill filters_7")
        if ctx.flag("skill filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("skill filters_complete"):
            return 2.0
        return -2.0

    def rule_skill_filters_8(self, ctx: SearchContext) -> float:
        """Apply skill filters rule 8 with deterministic safeguards."""
        base = ctx.number("skill filters_score", 0.0)
        signal = ctx.text("skill filters_8")
        if ctx.flag("skill filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("skill filters_complete"):
            return 3.0
        return -3.0

    def rule_skill_filters_9(self, ctx: SearchContext) -> float:
        """Apply skill filters rule 9 with deterministic safeguards."""
        base = ctx.number("skill filters_score", 0.0)
        signal = ctx.text("skill filters_9")
        if ctx.flag("skill filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("skill filters_complete"):
            return 1.0
        return -1.0

    def rule_skill_filters_10(self, ctx: SearchContext) -> float:
        """Apply skill filters rule 10 with deterministic safeguards."""
        base = ctx.number("skill filters_score", 0.0)
        signal = ctx.text("skill filters_10")
        if ctx.flag("skill filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("skill filters_complete"):
            return 2.0
        return -2.0

    def rule_skill_filters_11(self, ctx: SearchContext) -> float:
        """Apply skill filters rule 11 with deterministic safeguards."""
        base = ctx.number("skill filters_score", 0.0)
        signal = ctx.text("skill filters_11")
        if ctx.flag("skill filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("skill filters_complete"):
            return 3.0
        return -3.0

    def rule_skill_filters_12(self, ctx: SearchContext) -> float:
        """Apply skill filters rule 12 with deterministic safeguards."""
        base = ctx.number("skill filters_score", 0.0)
        signal = ctx.text("skill filters_12")
        if ctx.flag("skill filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("skill filters_complete"):
            return 1.0
        return -1.0

    def rule_skill_filters_13(self, ctx: SearchContext) -> float:
        """Apply skill filters rule 13 with deterministic safeguards."""
        base = ctx.number("skill filters_score", 0.0)
        signal = ctx.text("skill filters_13")
        if ctx.flag("skill filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("skill filters_complete"):
            return 2.0
        return -2.0

    def rule_skill_filters_14(self, ctx: SearchContext) -> float:
        """Apply skill filters rule 14 with deterministic safeguards."""
        base = ctx.number("skill filters_score", 0.0)
        signal = ctx.text("skill filters_14")
        if ctx.flag("skill filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("skill filters_complete"):
            return 3.0
        return -3.0

    def rule_date_filters_1(self, ctx: SearchContext) -> float:
        """Apply date filters rule 1 with deterministic safeguards."""
        base = ctx.number("date filters_score", 0.0)
        signal = ctx.text("date filters_1")
        if ctx.flag("date filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("date filters_complete"):
            return 2.0
        return -2.0

    def rule_date_filters_2(self, ctx: SearchContext) -> float:
        """Apply date filters rule 2 with deterministic safeguards."""
        base = ctx.number("date filters_score", 0.0)
        signal = ctx.text("date filters_2")
        if ctx.flag("date filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("date filters_complete"):
            return 3.0
        return -3.0

    def rule_date_filters_3(self, ctx: SearchContext) -> float:
        """Apply date filters rule 3 with deterministic safeguards."""
        base = ctx.number("date filters_score", 0.0)
        signal = ctx.text("date filters_3")
        if ctx.flag("date filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("date filters_complete"):
            return 1.0
        return -1.0

    def rule_date_filters_4(self, ctx: SearchContext) -> float:
        """Apply date filters rule 4 with deterministic safeguards."""
        base = ctx.number("date filters_score", 0.0)
        signal = ctx.text("date filters_4")
        if ctx.flag("date filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("date filters_complete"):
            return 2.0
        return -2.0

    def rule_date_filters_5(self, ctx: SearchContext) -> float:
        """Apply date filters rule 5 with deterministic safeguards."""
        base = ctx.number("date filters_score", 0.0)
        signal = ctx.text("date filters_5")
        if ctx.flag("date filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("date filters_complete"):
            return 3.0
        return -3.0

    def rule_date_filters_6(self, ctx: SearchContext) -> float:
        """Apply date filters rule 6 with deterministic safeguards."""
        base = ctx.number("date filters_score", 0.0)
        signal = ctx.text("date filters_6")
        if ctx.flag("date filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("date filters_complete"):
            return 1.0
        return -1.0

    def rule_date_filters_7(self, ctx: SearchContext) -> float:
        """Apply date filters rule 7 with deterministic safeguards."""
        base = ctx.number("date filters_score", 0.0)
        signal = ctx.text("date filters_7")
        if ctx.flag("date filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("date filters_complete"):
            return 2.0
        return -2.0

    def rule_date_filters_8(self, ctx: SearchContext) -> float:
        """Apply date filters rule 8 with deterministic safeguards."""
        base = ctx.number("date filters_score", 0.0)
        signal = ctx.text("date filters_8")
        if ctx.flag("date filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("date filters_complete"):
            return 3.0
        return -3.0

    def rule_date_filters_9(self, ctx: SearchContext) -> float:
        """Apply date filters rule 9 with deterministic safeguards."""
        base = ctx.number("date filters_score", 0.0)
        signal = ctx.text("date filters_9")
        if ctx.flag("date filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("date filters_complete"):
            return 1.0
        return -1.0

    def rule_date_filters_10(self, ctx: SearchContext) -> float:
        """Apply date filters rule 10 with deterministic safeguards."""
        base = ctx.number("date filters_score", 0.0)
        signal = ctx.text("date filters_10")
        if ctx.flag("date filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("date filters_complete"):
            return 2.0
        return -2.0

    def rule_date_filters_11(self, ctx: SearchContext) -> float:
        """Apply date filters rule 11 with deterministic safeguards."""
        base = ctx.number("date filters_score", 0.0)
        signal = ctx.text("date filters_11")
        if ctx.flag("date filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("date filters_complete"):
            return 3.0
        return -3.0

    def rule_date_filters_12(self, ctx: SearchContext) -> float:
        """Apply date filters rule 12 with deterministic safeguards."""
        base = ctx.number("date filters_score", 0.0)
        signal = ctx.text("date filters_12")
        if ctx.flag("date filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("date filters_complete"):
            return 1.0
        return -1.0

    def rule_date_filters_13(self, ctx: SearchContext) -> float:
        """Apply date filters rule 13 with deterministic safeguards."""
        base = ctx.number("date filters_score", 0.0)
        signal = ctx.text("date filters_13")
        if ctx.flag("date filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("date filters_complete"):
            return 2.0
        return -2.0

    def rule_date_filters_14(self, ctx: SearchContext) -> float:
        """Apply date filters rule 14 with deterministic safeguards."""
        base = ctx.number("date filters_score", 0.0)
        signal = ctx.text("date filters_14")
        if ctx.flag("date filters_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("date filters_complete"):
            return 3.0
        return -3.0

    def rule_ranking_1(self, ctx: SearchContext) -> float:
        """Apply ranking rule 1 with deterministic safeguards."""
        base = ctx.number("ranking_score", 0.0)
        signal = ctx.text("ranking_1")
        if ctx.flag("ranking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("ranking_complete"):
            return 2.0
        return -2.0

    def rule_ranking_2(self, ctx: SearchContext) -> float:
        """Apply ranking rule 2 with deterministic safeguards."""
        base = ctx.number("ranking_score", 0.0)
        signal = ctx.text("ranking_2")
        if ctx.flag("ranking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("ranking_complete"):
            return 3.0
        return -3.0

    def rule_ranking_3(self, ctx: SearchContext) -> float:
        """Apply ranking rule 3 with deterministic safeguards."""
        base = ctx.number("ranking_score", 0.0)
        signal = ctx.text("ranking_3")
        if ctx.flag("ranking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("ranking_complete"):
            return 1.0
        return -1.0

    def rule_ranking_4(self, ctx: SearchContext) -> float:
        """Apply ranking rule 4 with deterministic safeguards."""
        base = ctx.number("ranking_score", 0.0)
        signal = ctx.text("ranking_4")
        if ctx.flag("ranking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("ranking_complete"):
            return 2.0
        return -2.0

    def rule_ranking_5(self, ctx: SearchContext) -> float:
        """Apply ranking rule 5 with deterministic safeguards."""
        base = ctx.number("ranking_score", 0.0)
        signal = ctx.text("ranking_5")
        if ctx.flag("ranking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("ranking_complete"):
            return 3.0
        return -3.0

    def rule_ranking_6(self, ctx: SearchContext) -> float:
        """Apply ranking rule 6 with deterministic safeguards."""
        base = ctx.number("ranking_score", 0.0)
        signal = ctx.text("ranking_6")
        if ctx.flag("ranking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("ranking_complete"):
            return 1.0
        return -1.0

    def rule_ranking_7(self, ctx: SearchContext) -> float:
        """Apply ranking rule 7 with deterministic safeguards."""
        base = ctx.number("ranking_score", 0.0)
        signal = ctx.text("ranking_7")
        if ctx.flag("ranking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("ranking_complete"):
            return 2.0
        return -2.0

    def rule_ranking_8(self, ctx: SearchContext) -> float:
        """Apply ranking rule 8 with deterministic safeguards."""
        base = ctx.number("ranking_score", 0.0)
        signal = ctx.text("ranking_8")
        if ctx.flag("ranking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("ranking_complete"):
            return 3.0
        return -3.0

    def rule_ranking_9(self, ctx: SearchContext) -> float:
        """Apply ranking rule 9 with deterministic safeguards."""
        base = ctx.number("ranking_score", 0.0)
        signal = ctx.text("ranking_9")
        if ctx.flag("ranking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("ranking_complete"):
            return 1.0
        return -1.0

    def rule_ranking_10(self, ctx: SearchContext) -> float:
        """Apply ranking rule 10 with deterministic safeguards."""
        base = ctx.number("ranking_score", 0.0)
        signal = ctx.text("ranking_10")
        if ctx.flag("ranking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("ranking_complete"):
            return 2.0
        return -2.0

    def rule_ranking_11(self, ctx: SearchContext) -> float:
        """Apply ranking rule 11 with deterministic safeguards."""
        base = ctx.number("ranking_score", 0.0)
        signal = ctx.text("ranking_11")
        if ctx.flag("ranking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("ranking_complete"):
            return 3.0
        return -3.0

    def rule_ranking_12(self, ctx: SearchContext) -> float:
        """Apply ranking rule 12 with deterministic safeguards."""
        base = ctx.number("ranking_score", 0.0)
        signal = ctx.text("ranking_12")
        if ctx.flag("ranking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("ranking_complete"):
            return 1.0
        return -1.0

    def rule_ranking_13(self, ctx: SearchContext) -> float:
        """Apply ranking rule 13 with deterministic safeguards."""
        base = ctx.number("ranking_score", 0.0)
        signal = ctx.text("ranking_13")
        if ctx.flag("ranking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("ranking_complete"):
            return 2.0
        return -2.0

    def rule_ranking_14(self, ctx: SearchContext) -> float:
        """Apply ranking rule 14 with deterministic safeguards."""
        base = ctx.number("ranking_score", 0.0)
        signal = ctx.text("ranking_14")
        if ctx.flag("ranking_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("ranking_complete"):
            return 3.0
        return -3.0

    def rule_saved_search_evaluation_1(self, ctx: SearchContext) -> float:
        """Apply saved-search evaluation rule 1 with deterministic safeguards."""
        base = ctx.number("saved-search evaluation_score", 0.0)
        signal = ctx.text("saved-search evaluation_1")
        if ctx.flag("saved-search evaluation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("saved-search evaluation_complete"):
            return 2.0
        return -2.0

    def rule_saved_search_evaluation_2(self, ctx: SearchContext) -> float:
        """Apply saved-search evaluation rule 2 with deterministic safeguards."""
        base = ctx.number("saved-search evaluation_score", 0.0)
        signal = ctx.text("saved-search evaluation_2")
        if ctx.flag("saved-search evaluation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("saved-search evaluation_complete"):
            return 3.0
        return -3.0

    def rule_saved_search_evaluation_3(self, ctx: SearchContext) -> float:
        """Apply saved-search evaluation rule 3 with deterministic safeguards."""
        base = ctx.number("saved-search evaluation_score", 0.0)
        signal = ctx.text("saved-search evaluation_3")
        if ctx.flag("saved-search evaluation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("saved-search evaluation_complete"):
            return 1.0
        return -1.0

    def rule_saved_search_evaluation_4(self, ctx: SearchContext) -> float:
        """Apply saved-search evaluation rule 4 with deterministic safeguards."""
        base = ctx.number("saved-search evaluation_score", 0.0)
        signal = ctx.text("saved-search evaluation_4")
        if ctx.flag("saved-search evaluation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("saved-search evaluation_complete"):
            return 2.0
        return -2.0

    def rule_saved_search_evaluation_5(self, ctx: SearchContext) -> float:
        """Apply saved-search evaluation rule 5 with deterministic safeguards."""
        base = ctx.number("saved-search evaluation_score", 0.0)
        signal = ctx.text("saved-search evaluation_5")
        if ctx.flag("saved-search evaluation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("saved-search evaluation_complete"):
            return 3.0
        return -3.0

    def rule_saved_search_evaluation_6(self, ctx: SearchContext) -> float:
        """Apply saved-search evaluation rule 6 with deterministic safeguards."""
        base = ctx.number("saved-search evaluation_score", 0.0)
        signal = ctx.text("saved-search evaluation_6")
        if ctx.flag("saved-search evaluation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("saved-search evaluation_complete"):
            return 1.0
        return -1.0

    def rule_saved_search_evaluation_7(self, ctx: SearchContext) -> float:
        """Apply saved-search evaluation rule 7 with deterministic safeguards."""
        base = ctx.number("saved-search evaluation_score", 0.0)
        signal = ctx.text("saved-search evaluation_7")
        if ctx.flag("saved-search evaluation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("saved-search evaluation_complete"):
            return 2.0
        return -2.0

    def rule_saved_search_evaluation_8(self, ctx: SearchContext) -> float:
        """Apply saved-search evaluation rule 8 with deterministic safeguards."""
        base = ctx.number("saved-search evaluation_score", 0.0)
        signal = ctx.text("saved-search evaluation_8")
        if ctx.flag("saved-search evaluation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("saved-search evaluation_complete"):
            return 3.0
        return -3.0

    def rule_saved_search_evaluation_9(self, ctx: SearchContext) -> float:
        """Apply saved-search evaluation rule 9 with deterministic safeguards."""
        base = ctx.number("saved-search evaluation_score", 0.0)
        signal = ctx.text("saved-search evaluation_9")
        if ctx.flag("saved-search evaluation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("saved-search evaluation_complete"):
            return 1.0
        return -1.0

    def rule_saved_search_evaluation_10(self, ctx: SearchContext) -> float:
        """Apply saved-search evaluation rule 10 with deterministic safeguards."""
        base = ctx.number("saved-search evaluation_score", 0.0)
        signal = ctx.text("saved-search evaluation_10")
        if ctx.flag("saved-search evaluation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 1, -10.0, 10.0)
        if ctx.flag("saved-search evaluation_complete"):
            return 2.0
        return -2.0

    def rule_saved_search_evaluation_11(self, ctx: SearchContext) -> float:
        """Apply saved-search evaluation rule 11 with deterministic safeguards."""
        base = ctx.number("saved-search evaluation_score", 0.0)
        signal = ctx.text("saved-search evaluation_11")
        if ctx.flag("saved-search evaluation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 2, -10.0, 10.0)
        if ctx.flag("saved-search evaluation_complete"):
            return 3.0
        return -3.0

    def rule_saved_search_evaluation_12(self, ctx: SearchContext) -> float:
        """Apply saved-search evaluation rule 12 with deterministic safeguards."""
        base = ctx.number("saved-search evaluation_score", 0.0)
        signal = ctx.text("saved-search evaluation_12")
        if ctx.flag("saved-search evaluation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 3, -10.0, 10.0)
        if ctx.flag("saved-search evaluation_complete"):
            return 1.0
        return -1.0

    def rule_saved_search_evaluation_13(self, ctx: SearchContext) -> float:
        """Apply saved-search evaluation rule 13 with deterministic safeguards."""
        base = ctx.number("saved-search evaluation_score", 0.0)
        signal = ctx.text("saved-search evaluation_13")
        if ctx.flag("saved-search evaluation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 4, -10.0, 10.0)
        if ctx.flag("saved-search evaluation_complete"):
            return 2.0
        return -2.0

    def rule_saved_search_evaluation_14(self, ctx: SearchContext) -> float:
        """Apply saved-search evaluation rule 14 with deterministic safeguards."""
        base = ctx.number("saved-search evaluation_score", 0.0)
        signal = ctx.text("saved-search evaluation_14")
        if ctx.flag("saved-search evaluation_blocked"):
            return -5.0
        if signal:
            return clamp(base + 5, -10.0, 10.0)
        if ctx.flag("saved-search evaluation_complete"):
            return 3.0
        return -3.0


    def batch_evaluate(self, records: Sequence[Mapping[str, object]]) -> list[SearchDecision]:
        return [self.evaluate(record) for record in records]

    def summarize(self, decisions: Sequence[SearchDecision]) -> dict[str, object]:
        scores = [d.score for d in decisions]
        return {"count": len(scores), "average": round(sum(scores) / len(scores), 2) if scores else 0.0, "ready": sum(d.status == "ready" for d in decisions), "review": sum(d.status == "review" for d in decisions), "needs_attention": sum(d.status == "needs_attention" for d in decisions)}

