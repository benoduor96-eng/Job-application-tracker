"""Deterministic rule evaluation for user-configured application workflows.

Rules are data, not executable Python. The evaluator deliberately supports a small
allow-list of operators so client input can never become a dynamic expression.
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Iterable, Mapping
import re

SUPPORTED_EVENTS = {
    "application.created", "application.status_changed", "application.follow_up_due",
    "interview.scheduled", "interview.completed", "resume.updated", "task.overdue",
}
SUPPORTED_FIELDS = {
    "status", "company", "role", "location", "next_action", "days_since_created",
    "days_until_follow_up", "salary_min", "salary_max", "interview_type", "outcome",
}
SUPPORTED_OPERATORS = {"equals", "not_equals", "contains", "not_contains", "in",
                       "not_in", "exists", "gt", "gte", "lt", "lte", "matches"}
SUPPORTED_ACTIONS = {"create_task", "suggest_follow_up", "add_note", "notify_in_app"}
MAX_RULES_PER_EVALUATION = 100
MAX_CONDITIONS_PER_RULE = 20
MAX_ACTIONS_PER_RULE = 10
MAX_TEXT_LENGTH = 500
MAX_REGEX_LENGTH = 120
_SAFE_REGEX = re.compile(r"^[\w\s.,@+()\-\[\]{}|^$*?]+$")


class RuleValidationError(ValueError):
    """Raised when a workflow rule violates the public rule schema."""


@dataclass(frozen=True)
class Condition:
    field: str
    operator: str
    value: Any = None

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "Condition":
        if not isinstance(payload, Mapping):
            raise RuleValidationError("Each condition must be an object.")
        field_name = payload.get("field")
        operator = payload.get("operator")
        if field_name not in SUPPORTED_FIELDS:
            raise RuleValidationError(f"Unsupported condition field: {field_name!r}.")
        if operator not in SUPPORTED_OPERATORS:
            raise RuleValidationError(f"Unsupported condition operator: {operator!r}.")
        value = payload.get("value")
        if isinstance(value, str) and len(value) > MAX_TEXT_LENGTH:
            raise RuleValidationError("Condition text is too long.")
        if operator in {"in", "not_in"} and (
            not isinstance(value, (list, tuple)) or len(value) > 100
        ):
            raise RuleValidationError("The in operator requires a list of at most 100 values.")
        if operator == "matches":
            if not isinstance(value, str) or len(value) > MAX_REGEX_LENGTH:
                raise RuleValidationError("Regex patterns must be short strings.")
            if not _SAFE_REGEX.fullmatch(value):
                raise RuleValidationError("Regex pattern contains unsupported characters.")
        return cls(field=field_name, operator=operator, value=value)


@dataclass(frozen=True)
class Action:
    kind: str
    parameters: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "Action":
        if not isinstance(payload, Mapping):
            raise RuleValidationError("Each action must be an object.")
        kind = payload.get("kind")
        if kind not in SUPPORTED_ACTIONS:
            raise RuleValidationError(f"Unsupported action kind: {kind!r}.")
        parameters = payload.get("parameters", {})
        if not isinstance(parameters, Mapping):
            raise RuleValidationError("Action parameters must be an object.")
        clean = {}
        for key, value in parameters.items():
            if not isinstance(key, str) or len(key) > 80:
                raise RuleValidationError("Action parameter names must be short strings.")
            if isinstance(value, str) and len(value) > MAX_TEXT_LENGTH:
                raise RuleValidationError("Action parameter text is too long.")
            if isinstance(value, (dict, list)) and len(value) > 100:
                raise RuleValidationError("Action parameter collections are too large.")
            clean[key] = value
        return cls(kind=kind, parameters=clean)


@dataclass(frozen=True)
class WorkflowRule:
    id: str
    name: str
    event: str
    conditions: tuple[Condition, ...]
    actions: tuple[Action, ...]
    enabled: bool = True
    match_all: bool = True
    priority: int = 100

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "WorkflowRule":
        if not isinstance(payload, Mapping):
            raise RuleValidationError("A rule must be an object.")
        rule_id = str(payload.get("id", "")).strip()
        name = str(payload.get("name", "")).strip()
        event = payload.get("event")
        if not rule_id or len(rule_id) > 80:
            raise RuleValidationError("Rule id is required and must be at most 80 characters.")
        if not name or len(name) > 160:
            raise RuleValidationError("Rule name is required and must be at most 160 characters.")
        if event not in SUPPORTED_EVENTS:
            raise RuleValidationError(f"Unsupported workflow event: {event!r}.")
        raw_conditions = payload.get("conditions", [])
        raw_actions = payload.get("actions", [])
        if not isinstance(raw_conditions, list) or len(raw_conditions) > MAX_CONDITIONS_PER_RULE:
            raise RuleValidationError("A rule must have at most 20 conditions.")
        if not isinstance(raw_actions, list) or not 1 <= len(raw_actions) <= MAX_ACTIONS_PER_RULE:
            raise RuleValidationError("A rule must have between 1 and 10 actions.")
        priority = payload.get("priority", 100)
        if isinstance(priority, bool) or not isinstance(priority, int) or not 0 <= priority <= 1000:
            raise RuleValidationError("Priority must be an integer from 0 through 1000.")
        return cls(
            id=rule_id, name=name, event=event,
            conditions=tuple(Condition.from_mapping(item) for item in raw_conditions),
            actions=tuple(Action.from_mapping(item) for item in raw_actions),
            enabled=payload.get("enabled", True) is True,
            match_all=payload.get("match_all", True) is not False,
            priority=priority,
        )


def _normal(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip().casefold()
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def _compare(actual: Any, condition: Condition) -> bool:
    expected = condition.value
    operator = condition.operator
    left, right = _normal(actual), _normal(expected)
    if operator == "exists":
        return (actual is not None and actual != "") is bool(expected if expected is not None else True)
    if operator == "equals":
        return left == right
    if operator == "not_equals":
        return left != right
    if operator == "contains":
        return right in left if isinstance(left, str) and isinstance(right, str) else (
            expected in actual if isinstance(actual, (list, tuple, set)) else False)
    if operator == "not_contains":
        return not _compare(actual, Condition(condition.field, "contains", expected))
    if operator == "in":
        return left in [_normal(item) for item in expected]
    if operator == "not_in":
        return left not in [_normal(item) for item in expected]
    if operator in {"gt", "gte", "lt", "lte"}:
        try:
            a, b = float(actual), float(expected)
        except (TypeError, ValueError):
            return False
        return {"gt": a > b, "gte": a >= b, "lt": a < b, "lte": a <= b}[operator]
    if operator == "matches":
        if not isinstance(actual, str) or not isinstance(expected, str):
            return False
        try:
            return re.search(expected, actual, flags=re.IGNORECASE) is not None
        except re.error:
            return False
    return False


def condition_matches(condition: Condition, context: Mapping[str, Any]) -> bool:
    """Evaluate one condition without evaluating expressions or accessing attributes."""
    return _compare(context.get(condition.field), condition)


def rule_matches(rule: WorkflowRule, event: str, context: Mapping[str, Any]) -> bool:
    if not rule.enabled or rule.event != event:
        return False
    if not rule.conditions:
        return True
    outcomes = [condition_matches(condition, context) for condition in rule.conditions]
    return all(outcomes) if rule.match_all else any(outcomes)


def evaluate_rules(
    rules: Iterable[Mapping[str, Any] | WorkflowRule],
    event: str,
    context: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Return ordered action plans; this function does not perform side effects."""
    if event not in SUPPORTED_EVENTS:
        raise RuleValidationError(f"Unsupported workflow event: {event!r}.")
    candidates = list(rules)
    if len(candidates) > MAX_RULES_PER_EVALUATION:
        raise RuleValidationError("At most 100 rules may be evaluated at once.")
    parsed = [item if isinstance(item, WorkflowRule) else WorkflowRule.from_mapping(item)
              for item in candidates]
    parsed.sort(key=lambda rule: (rule.priority, rule.id))
    plans = []
    for rule in parsed:
        if rule_matches(rule, event, context):
            plans.append({
                "rule_id": rule.id,
                "rule_name": rule.name,
                "event": event,
                "actions": [{"kind": action.kind, "parameters": dict(action.parameters)}
                            for action in rule.actions],
            })
    return plans


def summarize_rule_set(rules: Iterable[Mapping[str, Any] | WorkflowRule]) -> dict[str, Any]:
    """Produce a safe overview for a settings page without returning action payloads."""
    parsed = [item if isinstance(item, WorkflowRule) else WorkflowRule.from_mapping(item)
              for item in rules]
    events: dict[str, int] = {}
    actions: dict[str, int] = {}
    for rule in parsed:
        events[rule.event] = events.get(rule.event, 0) + 1
        for action in rule.actions:
            actions[action.kind] = actions.get(action.kind, 0) + 1
    return {
        "total": len(parsed),
        "enabled": sum(1 for rule in parsed if rule.enabled),
        "disabled": sum(1 for rule in parsed if not rule.enabled),
        "events": dict(sorted(events.items())),
        "actions": dict(sorted(actions.items())),
    }
