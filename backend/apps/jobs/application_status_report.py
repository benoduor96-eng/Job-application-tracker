"""Application status reporting with explicit denominator and unknown-state handling."""
from collections import Counter, defaultdict
from typing import Iterable, Mapping

STATUSES = ("saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn")
TERMINAL = {"offer", "rejected", "withdrawn"}
def summarize_statuses(records: Iterable[Mapping]) -> dict:
    rows = list(records)
    counts = Counter(str(row.get("status") or "unknown").lower() for row in rows)
    known = sum(counts[status] for status in STATUSES)
    return {"total_records": len(rows), "known_status_records": known,
            "unknown_status_records": len(rows)-known,
            "counts": {status: counts[status] for status in STATUSES},
            "unknown_values": dict(sorted((key, value) for key, value in counts.items() if key not in STATUSES)),
            "active_records": sum(counts[status] for status in STATUSES if status not in TERMINAL),
            "terminal_records": sum(counts[status] for status in TERMINAL)}

def status_by_company(records: Iterable[Mapping], limit: int = 50) -> list[dict]:
    if not 1 <= limit <= 500:
        raise ValueError("limit must be between 1 and 500")
    groups = defaultdict(Counter)
    for row in records:
        company = str(row.get("company") or "Unknown company").strip() or "Unknown company"
        groups[company][str(row.get("status") or "unknown").lower()] += 1
    result = []
    for company, counts in groups.items():
        result.append({"company": company, "total": sum(counts.values()),
                       "offers": counts["offer"], "interviews": counts["interview"],
                       "rejections": counts["rejected"], "unknown": counts["unknown"],
                       "statuses": {status: counts[status] for status in STATUSES}})
    return sorted(result, key=lambda row: (-row["offers"], -row["interviews"], -row["total"],
                                           row["company"].casefold()))[:limit]

def transition_counts(events: Iterable[Mapping]) -> dict:
    counts = Counter()
    invalid = 0
    for event in events:
        source = str(event.get("from_status") or "").lower()
        target = str(event.get("to_status") or "").lower()
        if source not in STATUSES or target not in STATUSES:
            invalid += 1
            continue
        counts[(source, target)] += 1
    return {"transition_count": sum(counts.values()), "invalid_transition_events": invalid,
            "transitions": [{"from": source, "to": target, "count": count}
                            for (source, target), count in sorted(counts.items())]}

def outcome_audit(records: Iterable[Mapping]) -> dict:
    rows = list(records)
    resolved = [row for row in rows if str(row.get("status") or "").lower() in TERMINAL]
    offers = sum(str(row.get("status") or "").lower() == "offer" for row in resolved)
    return {"total": len(rows), "resolved": len(resolved), "offers": offers,
            "offer_percent_all": round(100*offers/len(rows), 2) if rows else 0,
            "offer_percent_resolved": round(100*offers/len(resolved), 2) if resolved else None,
            "unresolved": len(rows)-len(resolved),
            "warning": "Descriptive statistics only; do not interpret as causal or predictive."}
