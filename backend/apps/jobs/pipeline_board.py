"""Pure helpers for the Kanban application pipeline board."""
from __future__ import annotations
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Iterable, Optional

STAGES = ["saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn"]
STAGE_LABELS = dict(zip(STAGES, ["Saved", "Applied", "Screening", "Interview", "Offer", "Rejected", "Withdrawn"]))
TERMINAL_STAGES = frozenset({"rejected", "withdrawn"})
WAITING_STAGES = frozenset({"applied", "screening", "interview"})
MAX_BULK_MOVE = 100

def _to_decimal(value) -> Optional[Decimal]:
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return None

def _as_date(value) -> Optional[date]:
    if value is None:
        return None
    return value.date() if isinstance(value, datetime) else value

def _average(values):
    return float(sum(values, Decimal(0)) / len(values)) if values else None

def is_stale(application, today: date, stale_days: int = 14) -> bool:
    if application.status not in WAITING_STAGES:
        return False
    touched = _as_date(getattr(application, "updated_at", None)) or _as_date(getattr(application, "applied_date", None))
    return touched is not None and (today - touched).days > stale_days

def _card(application, today, stale_days):
    low, high = _to_decimal(application.salary_min), _to_decimal(application.salary_max)
    return {
        "id": application.id, "company": application.company, "role": application.role,
        "location": application.location, "status": application.status,
        "salary_min": float(low) if low is not None else None,
        "salary_max": float(high) if high is not None else None,
        "applied_date": application.applied_date, "next_action": application.next_action,
        "next_action_date": application.next_action_date,
        "stale": is_stale(application, today, stale_days),
    }

def _card_sort_key(application):
    next_date = _as_date(application.next_action_date)
    return (next_date is None, next_date or date.max, (application.company or "").lower())

def build_board(applications: Iterable, today: Optional[date] = None, stale_days: int = 14, query: str = "") -> dict:
    today = today or date.today()
    needle = (query or "").strip().lower()
    groups = {stage: [] for stage in STAGES}
    for application in applications:
        if application.status not in groups:
            continue
        haystack = f"{application.company} {application.role} {application.location}".lower()
        if needle and needle not in haystack:
            continue
        groups[application.status].append(application)

    columns, total, active, stale = [], 0, 0, 0
    for stage in STAGES:
        items = sorted(groups[stage], key=_card_sort_key)
        cards = [_card(item, today, stale_days) for item in items]
        mins = [v for v in (_to_decimal(a.salary_min) for a in items) if v is not None]
        maxes = [v for v in (_to_decimal(a.salary_max) for a in items) if v is not None]
        stale_count = sum(1 for card in cards if card["stale"])
        columns.append({
            "status": stage, "label": STAGE_LABELS[stage], "count": len(cards),
            "avg_salary_min": _average(mins), "avg_salary_max": _average(maxes),
            "stale_count": stale_count, "cards": cards,
        })
        total += len(cards)
        if stage not in TERMINAL_STAGES:
            active += len(cards)
        stale += stale_count
    return {"columns": columns, "totals": {"applications": total, "active": active, "stale": stale}}

def parse_move_request(payload) -> tuple[list[int], str]:
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object.")
    status = payload.get("status")
    if status not in STAGES:
        raise ValueError(f"status must be one of: {', '.join(STAGES)}.")
    ids = payload.get("ids")
    if not isinstance(ids, list) or not ids:
        raise ValueError("ids must be a non-empty list of application ids.")
    if len(ids) > MAX_BULK_MOVE:
        raise ValueError(f"You can move at most {MAX_BULK_MOVE} applications at once.")
    clean = []
    for value in ids:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("ids must contain only integers.")
        clean.append(value)
    return list(dict.fromkeys(clean)), status

def plan_moves(current_status_by_id: dict[int, str], ids: list[int], target: str) -> dict:
    if target not in STAGES:
        raise ValueError(f"Unknown status: {target}")
    moved, unchanged, missing = [], [], []
    for application_id in dict.fromkeys(ids):
        if application_id not in current_status_by_id:
            missing.append(application_id)
        elif current_status_by_id[application_id] == target:
            unchanged.append(application_id)
        else:
            moved.append(application_id)
    return {"moved": moved, "unchanged": unchanged, "missing": missing}
