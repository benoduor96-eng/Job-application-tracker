"""Explicit lifecycle rules for job applications; this module does not mutate models."""
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Sequence
from .models import JobApplication

class InvalidTransition(ValueError):
    """Raised when a requested lifecycle transition is not allowed."""

class TransitionReasonRequired(InvalidTransition):
    """Raised when a transition needs an explanation."""

@dataclass(frozen=True)
class TransitionRule:
    source: str
    target: str
    requires_reason: bool = False
    terminal: bool = False
    guidance: str = ""

@dataclass(frozen=True)
class TransitionDecision:
    allowed: bool
    source: str
    target: str
    requires_reason: bool
    guidance: str
    blockers: tuple[str, ...] = ()
    def as_dict(self):
        return {"allowed": self.allowed, "source": self.source, "target": self.target,
                "requires_reason": self.requires_reason, "guidance": self.guidance,
                "blockers": list(self.blockers)}

ACTIVE_STATUSES = frozenset({"saved", "applied", "screening", "interview", "offer"})
TERMINAL_STATUSES = frozenset({"rejected", "withdrawn"})
ALL_STATUSES = frozenset(choice[0] for choice in JobApplication.STATUS_CHOICES)
_RULE_ROWS = (
    ("saved", "applied", False, False, "Record the submission date and source."),
    ("saved", "withdrawn", True, True, "Add a reason so the record remains useful."),
    ("applied", "screening", False, False, "Prepare for the recruiter screen."),
    ("applied", "interview", False, False, "Add an interview event and preparation notes."),
    ("applied", "rejected", False, True, "Capture feedback if supplied."),
    ("applied", "withdrawn", True, True, "Record why you chose to withdraw."),
    ("screening", "interview", False, False, "Confirm interview format and date."),
    ("screening", "rejected", False, True, "Save any recruiter feedback."),
    ("screening", "withdrawn", True, True, "Record the withdrawal reason."),
    ("interview", "offer", False, False, "Review compensation, scope, and deadlines."),
    ("interview", "rejected", False, True, "Record feedback while it is fresh."),
    ("interview", "withdrawn", True, True, "Record the withdrawal reason."),
    ("offer", "withdrawn", True, True, "Record why the offer was declined."),
    ("offer", "rejected", True, True, "Explain if the offer was rescinded or entered in error."),
    ("rejected", "applied", True, False, "Reopen only for a genuine new application."),
    ("withdrawn", "applied", True, False, "Reopen only when the process has resumed."),
)
TRANSITION_RULES = {(s, t): TransitionRule(s, t, r, terminal, guidance)
                    for s, t, r, terminal, guidance in _RULE_ROWS}

def valid_status(value: str) -> bool:
    return value in ALL_STATUSES

def status_label(value: str) -> str:
    labels = dict(JobApplication.STATUS_CHOICES)
    if value not in labels:
        raise ValueError(f"Unknown application status: {value!r}")
    return labels[value]

def transition_decision(source: str, target: str, reason: str = "") -> TransitionDecision:
    if source not in ALL_STATUSES:
        return TransitionDecision(False, source, target, False, "", ("Unknown source status.",))
    if target not in ALL_STATUSES:
        return TransitionDecision(False, source, target, False, "", ("Unknown target status.",))
    if source == target:
        return TransitionDecision(True, source, target, False, "No status change is needed.")
    rule = TRANSITION_RULES.get((source, target))
    if rule is None:
        return TransitionDecision(False, source, target, False, "",
            (f"Transition from {status_label(source)} to {status_label(target)} is not supported.",))
    blockers = ("Provide a reason for this transition.",) if rule.requires_reason and not reason.strip() else ()
    return TransitionDecision(not blockers, source, target, rule.requires_reason, rule.guidance, blockers)

def validate_transition(source: str, target: str, reason: str = "") -> TransitionRule | None:
    decision = transition_decision(source, target, reason)
    if not decision.allowed:
        if any("reason" in item.lower() for item in decision.blockers):
            raise TransitionReasonRequired("; ".join(decision.blockers))
        raise InvalidTransition("; ".join(decision.blockers))
    return TRANSITION_RULES.get((source, target))

def transition_matrix() -> list[dict]:
    return [{"source": source, "target": target, "allowed": (source, target) in TRANSITION_RULES,
             "requires_reason": TRANSITION_RULES.get((source, target), TransitionRule(source, target)).requires_reason,
             "guidance": TRANSITION_RULES.get((source, target), TransitionRule(source, target)).guidance}
            for source in sorted(ALL_STATUSES) for target in sorted(ALL_STATUSES) if source != target]

def plan_bulk_transition(applications: Iterable[Mapping], target: str,
                         reasons: Mapping[int, str] | None = None) -> dict:
    reasons = reasons or {}
    accepted, rejected = [], []
    for row in applications:
        try:
            identifier, source = int(row["id"]), str(row["status"])
        except (KeyError, TypeError, ValueError):
            rejected.append({"id": row.get("id"), "error": "Each row needs a numeric id and status."})
            continue
        decision = transition_decision(source, target, str(reasons.get(identifier, "")))
        if decision.allowed:
            accepted.append({"id": identifier, "source": source, "target": target})
        else:
            rejected.append({"id": identifier, "source": source, "target": target,
                             "blockers": list(decision.blockers)})
    return {"accepted": accepted, "rejected": rejected, "ready": bool(accepted) and not rejected}

def follow_up_sla(status: str, applied_on: date | None, today: date | None = None,
                  overrides: Mapping[str, int] | None = None) -> dict:
    today = today or date.today()
    days_by_status = {"saved": 0, "applied": 7, "screening": 3, "interview": 2,
                      "offer": 1, "rejected": 0, "withdrawn": 0}
    days_by_status.update(overrides or {})
    if status not in ALL_STATUSES:
        raise ValueError(f"Unknown application status: {status!r}")
    days = max(0, int(days_by_status[status]))
    if status in TERMINAL_STATUSES or not days:
        return {"status": status, "due_date": None, "days": 0, "reason": "no_follow_up"}
    due = (applied_on or today) + timedelta(days=days)
    return {"status": status, "due_date": due.isoformat(), "days": days,
            "overdue": due < today, "reason": "status_sla"}

def next_actions_for_status(status: str) -> list[str]:
    actions = {
        "saved": ["Review the job description", "Check role requirements", "Tailor your resume"],
        "applied": ["Save the confirmation", "Schedule a follow-up", "Prepare an introduction"],
        "screening": ["Review the company", "Prepare availability", "Practice career examples"],
        "interview": ["Confirm time and format", "Prepare examples", "Write questions"],
        "offer": ["Read the offer", "Compare benefits", "Clarify the response deadline"],
        "rejected": ["Capture feedback", "Review improvements", "Continue active opportunities"],
        "withdrawn": ["Record the reason", "Close pending reminders", "Keep useful notes"],
    }
    if status not in actions:
        raise ValueError(f"Unknown application status: {status!r}")
    return list(actions[status])

def overdue_days(due_date: date | datetime | None, today: date | None = None) -> int:
    if due_date is None:
        return 0
    if isinstance(due_date, datetime):
        due_date = due_date.date()
    return max(0, ((today or date.today()) - due_date).days)

def prioritize_follow_ups(rows: Sequence[Mapping], today: date | None = None) -> list[dict]:
    today = today or date.today()
    result = []
    for row in rows:
        due = row.get("due_date")
        if isinstance(due, str):
            try:
                due = date.fromisoformat(due)
            except ValueError:
                due = None
        late = overdue_days(due, today)
        priority = str(row.get("priority", "medium")).lower()
        weight = {"urgent": 4, "high": 3, "medium": 2, "low": 1}.get(priority, 2)
        result.append({**dict(row), "overdue_days": late, "priority_weight": weight})
    result.sort(key=lambda row: (-row["overdue_days"], -row["priority_weight"],
                                 str(row.get("due_date") or "9999-12-31")))
    return result

def status_summary(rows: Iterable[Mapping]) -> dict:
    counts = {status: 0 for status in sorted(ALL_STATUSES)}
    invalid = 0
    for row in rows:
        status = row.get("status")
        if status in counts:
            counts[status] += 1
        else:
            invalid += 1
    return {"total": sum(counts.values()), "counts": counts, "invalid_rows": invalid,
            "active": sum(counts[s] for s in ACTIVE_STATUSES),
            "terminal": sum(counts[s] for s in TERMINAL_STATUSES)}

def transition_history_is_consistent(events: Sequence[Mapping],
                                     initial_status: str | None = None) -> dict:
    current, errors = initial_status, []
    for index, event in enumerate(events):
        source, target = event.get("source"), event.get("target")
        if source not in ALL_STATUSES or target not in ALL_STATUSES:
            errors.append({"index": index, "error": "unknown_status"})
            continue
        if current is not None and source != current:
            errors.append({"index": index, "error": "source_does_not_match_previous_target",
                           "expected": current, "actual": source})
        decision = transition_decision(source, target, str(event.get("reason", "")))
        if not decision.allowed:
            errors.append({"index": index, "error": "invalid_transition",
                           "blockers": list(decision.blockers)})
        current = target
    return {"consistent": not errors, "final_status": current, "errors": errors}

def transition_timestamp_policy(timestamp: datetime, now: datetime | None = None,
                               max_future_minutes: int = 5) -> dict:
    now = now or datetime.now(timestamp.tzinfo)
    if timestamp.tzinfo != now.tzinfo:
        return {"valid": False, "reason": "timezone_mismatch"}
    if timestamp > now + timedelta(minutes=max_future_minutes):
        return {"valid": False, "reason": "future_timestamp"}
    return {"valid": True, "reason": "accepted"}
