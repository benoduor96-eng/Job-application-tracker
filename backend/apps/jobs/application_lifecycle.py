"""Application lifecycle rules and transition planning.

This module keeps state-transition policy explicit and independently testable.
It deliberately separates a valid transition from a successful database write.
"""
from dataclasses import dataclass
from datetime import date
from typing import Iterable, Mapping

VALID_STATUSES = ("saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn")
TERMINAL_STATUSES = frozenset({"rejected", "withdrawn"})
ACTIVE_STATUSES = frozenset({"saved", "applied", "screening", "interview"})
ALLOWED_TRANSITIONS = {
    "saved": frozenset({"applied", "withdrawn"}),
    "applied": frozenset({"screening", "interview", "offer", "rejected", "withdrawn"}),
    "screening": frozenset({"interview", "offer", "rejected", "withdrawn"}),
    "interview": frozenset({"screening", "offer", "rejected", "withdrawn"}),
    "offer": frozenset({"interview", "withdrawn"}),
    "rejected": frozenset(),
    "withdrawn": frozenset(),
}


class LifecycleError(ValueError):
    """Raised for a lifecycle request that cannot be applied safely."""


@dataclass(frozen=True)
class TransitionDecision:
    allowed: bool
    current_status: str
    requested_status: str
    reason: str
    requires_confirmation: bool = False


def validate_status(status: str) -> str:
    if status not in VALID_STATUSES:
        raise LifecycleError(f"Unknown application status: {status!r}.")
    return status


def can_transition(current: str, target: str, *, reopen: bool = False) -> TransitionDecision:
    validate_status(current)
    validate_status(target)
    if current == target:
        return TransitionDecision(True, current, target, "No status change is needed.")
    if target in ALLOWED_TRANSITIONS[current]:
        confirmation = target in {"rejected", "withdrawn"}
        return TransitionDecision(True, current, target, "Transition is permitted.", confirmation)
    if reopen and current in TERMINAL_STATUSES and target in {"applied", "screening"}:
        return TransitionDecision(True, current, target, "Explicit reopen requested.", True)
    return TransitionDecision(False, current, target,
                              f"Transition from {current!r} to {target!r} is not allowed.")


def transition_payload(current: str, target: str, *, actor_id=None, note="", at=None,
                       reopen=False) -> dict:
    decision = can_transition(current, target, reopen=reopen)
    if not decision.allowed:
        raise LifecycleError(decision.reason)
    return {
        "from_status": current,
        "to_status": target,
        "changed": current != target,
        "requires_confirmation": decision.requires_confirmation,
        "actor_id": actor_id,
        "note": str(note).strip()[:1000],
        "occurred_at": at.isoformat() if hasattr(at, "isoformat") else at,
        "event_type": "application.status_changed" if current != target else "application.status_unchanged",
    }


def plan_bulk_transition(
    records: Iterable[Mapping],
    target: str,
    *,
    reopen_ids: Iterable[int] = (),
) -> dict:
    """Validate a mixed batch before any caller writes rows to the database."""
    validate_status(target)
    reopen_ids = set(reopen_ids)
    accepted, rejected = [], []
    seen = set()
    for record in records:
        record_id = record.get("id")
        if record_id in seen:
            rejected.append({"id": record_id, "reason": "Duplicate id in request."})
            continue
        seen.add(record_id)
        current = record.get("status")
        try:
            decision = can_transition(current, target, reopen=record_id in reopen_ids)
        except LifecycleError as exc:
            rejected.append({"id": record_id, "reason": str(exc)})
            continue
        if not decision.allowed:
            rejected.append({"id": record_id, "reason": decision.reason})
            continue
        accepted.append({
            "id": record_id, "from_status": current, "to_status": target,
            "changed": current != target,
            "requires_confirmation": decision.requires_confirmation,
        })
    return {
        "requested": len(seen),
        "accepted": accepted,
        "rejected": rejected,
        "ready_to_commit": not rejected,
        "change_count": sum(1 for item in accepted if item["changed"]),
    }


def follow_up_state(due_date: date | None, today: date | None = None) -> str:
    """Classify a follow-up date in a way suitable for dashboards and reminders."""
    if due_date is None:
        return "unscheduled"
    today = today or date.today()
    if due_date < today:
        return "overdue"
    if due_date == today:
        return "due_today"
    if (due_date - today).days <= 7:
        return "due_soon"
    return "scheduled"


def transition_matrix() -> dict[str, list[str]]:
    return {status: sorted(ALLOWED_TRANSITIONS[status]) for status in VALID_STATUSES}


def validate_transition_history(events: Iterable[Mapping]) -> list[dict]:
    """Check a supplied history for broken links without modifying or trusting it."""
    issues = []
    previous = None
    for index, event in enumerate(events):
        source, target = event.get("from_status"), event.get("to_status")
        if source not in VALID_STATUSES or target not in VALID_STATUSES:
            issues.append({"index": index, "issue": "unknown_status"})
            previous = target
            continue
        if previous is not None and source != previous:
            issues.append({"index": index, "issue": "disconnected_history",
                           "expected_from": previous, "actual_from": source})
        decision = can_transition(source, target, reopen=bool(event.get("reopened")))
        if not decision.allowed:
            issues.append({"index": index, "issue": "invalid_transition",
                           "from_status": source, "to_status": target})
        previous = target
    return issues
