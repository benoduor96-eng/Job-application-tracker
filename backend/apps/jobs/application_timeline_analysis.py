"""Pure timeline analytics helpers; they never modify the application's event history."""
from datetime import date, datetime
from typing import Iterable, Mapping

def _parse(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except ValueError:
        try:
            return datetime.combine(date.fromisoformat(str(value)[:10]), datetime.min.time())
        except ValueError:
            return None

def normalize_event(event: Mapping, index: int = 0) -> dict:
    occurred = _parse(event.get("occurred_at") or event.get("created_at") or event.get("date"))
    return {"id": event.get("id", index), "application_id": event.get("application_id"),
            "event_type": str(event.get("event_type") or event.get("type") or "note").strip().lower(),
            "from_status": str(event.get("from_status") or "").strip().lower(),
            "to_status": str(event.get("to_status") or "").strip().lower(),
            "occurred_at": occurred, "description": str(event.get("description") or event.get("note") or "")[:2000],
            "source": str(event.get("source") or "manual")[:80]}

def chronological_events(events: Iterable[Mapping]) -> list[dict]:
    normalized = [normalize_event(event, index) for index, event in enumerate(events)]
    normalized.sort(key=lambda item: (item["occurred_at"] is None, item["occurred_at"] or datetime.max, str(item["id"])))
    return [{**item, "occurred_at": item["occurred_at"].isoformat() if item["occurred_at"] else None}
            for item in normalized]

def timeline_integrity_report(events: Iterable[Mapping], initial_status: str | None = None) -> dict:
    normalized = [normalize_event(event, index) for index, event in enumerate(events)]
    issues, identifiers = [], set()
    known = {"saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn"}
    for event in normalized:
        if event["id"] in identifiers:
            issues.append({"event_id": event["id"], "code": "duplicate_event_id"})
        identifiers.add(event["id"])
        if event["occurred_at"] is None:
            issues.append({"event_id": event["id"], "code": "missing_or_invalid_timestamp"})
        if event["event_type"] == "status_change":
            if event["from_status"] not in known:
                issues.append({"event_id": event["id"], "code": "unknown_from_status"})
            if event["to_status"] not in known:
                issues.append({"event_id": event["id"], "code": "unknown_to_status"})
    ordered = sorted((event for event in normalized if event["occurred_at"]),
                     key=lambda item: (item["occurred_at"], str(item["id"])))
    previous = initial_status
    for event in ordered:
        if event["event_type"] != "status_change":
            continue
        if previous and event["from_status"] and previous != event["from_status"]:
            issues.append({"event_id": event["id"], "code": "status_chain_discontinuity",
                           "expected_from": previous, "actual_from": event["from_status"]})
        previous = event["to_status"] or previous
    return {"event_count": len(normalized), "chronologically_ordered": chronological_events(events),
            "issue_count": len(issues), "issues": issues, "consistent": not issues,
            "note": "Events are inspected only; this report does not rewrite or delete history."}

def timeline_summary(events: Iterable[Mapping]) -> dict:
    normalized = [normalize_event(event, index) for index, event in enumerate(events)]
    dated = sorted((event for event in normalized if event["occurred_at"]), key=lambda item: item["occurred_at"])
    changes = [event for event in dated if event["event_type"] == "status_change"]
    gaps = []
    for left, right in zip(changes, changes[1:]):
        delta = (right["occurred_at"] - left["occurred_at"]).total_seconds() / 86400
        if delta >= 0:
            gaps.append({"from_status": left["to_status"], "to_status": right["to_status"], "days": round(delta, 2)})
    return {"event_count": len(normalized), "dated_event_count": len(dated),
            "undated_event_count": len(normalized)-len(dated), "status_change_count": len(changes),
            "first_event": dated[0]["occurred_at"].isoformat() if dated else None,
            "last_event": dated[-1]["occurred_at"].isoformat() if dated else None,
            "days_between_status_changes": gaps,
            "average_gap_days": round(sum(item["days"] for item in gaps)/len(gaps), 2) if gaps else None}

def events_by_month(events: Iterable[Mapping]) -> list[dict]:
    buckets = {}
    for index, event in enumerate(events):
        row = normalize_event(event, index)
        if row["occurred_at"] is None:
            continue
        month = row["occurred_at"].strftime("%Y-%m")
        buckets.setdefault(month, {"month": month, "total": 0, "by_type": {}})
        buckets[month]["total"] += 1
        kind = row["event_type"]
        buckets[month]["by_type"][kind] = buckets[month]["by_type"].get(kind, 0)+1
    return [buckets[key] for key in sorted(buckets)]

def merge_timeline_preview(existing: Iterable[Mapping], imported: Iterable[Mapping]) -> dict:
    left = [normalize_event(event, index) for index, event in enumerate(existing)]
    right = [normalize_event(event, index+len(left)) for index, event in enumerate(imported)]
    known = {(row["event_type"], row["occurred_at"], row["description"]) for row in left}
    duplicates, additions = [], []
    for row in right:
        key = (row["event_type"], row["occurred_at"], row["description"])
        clean = {**row, "occurred_at": row["occurred_at"].isoformat() if row["occurred_at"] else None}
        if key in known:
            duplicates.append(clean)
        else:
            additions.append(clean)
            known.add(key)
    return {"existing_count": len(left), "imported_count": len(right), "proposed_additions": additions,
            "possible_duplicates": duplicates, "requires_review": bool(duplicates), "persisted": False,
            "warning": "Preview only; verify ownership, timestamps, and duplicate candidates before importing."}

def timeline_gaps(events: Iterable[Mapping], threshold_days: int = 30) -> list[dict]:
    if not 1 <= threshold_days <= 3650:
        raise ValueError("threshold_days must be between 1 and 3650")
    rows = chronological_events(events)
    gaps = []
    for left, right in zip(rows, rows[1:]):
        if not left["occurred_at"] or not right["occurred_at"]:
            continue
        delta = (_parse(right["occurred_at"]) - _parse(left["occurred_at"])).days
        if delta >= threshold_days:
            gaps.append({"from_event_id": left["id"], "to_event_id": right["id"], "days": delta,
                         "review_suggestion": "Check whether a meaningful activity was not recorded."})
    return gaps
