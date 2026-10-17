"""Privacy-first helpers for export manifests, retention planning, and redaction."""
from datetime import date, datetime, timedelta, timezone
from typing import Iterable, Mapping
import re

SENSITIVE_KEYS = frozenset({"password", "password_hash", "token", "access_token", "refresh_token",
                            "authorization", "secret", "api_key", "private_key", "sessionid"})
PERSONAL_KEYS = frozenset({"email", "phone", "address", "postal_code", "date_of_birth",
                           "linkedin_url", "github_url", "portfolio_url", "interviewer_email",
                           "contact_email"})
DEFAULT_RETENTION_DAYS = {"audit_event": 365, "notification": 180, "import_preview": 30,
                          "temporary_upload": 7, "session_record": 30, "application": None,
                          "resume": None, "contact": None}

def _parse_datetime(value):
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day, tzinfo=timezone.utc)
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    return None

def retention_decision(record: Mapping, now: datetime | None = None,
                       policy: Mapping[str, int | None] | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    retention = dict(DEFAULT_RETENTION_DAYS)
    retention.update(policy or {})
    kind, identifier = str(record.get("record_type", "unknown")), str(record.get("id", "unknown"))
    created = _parse_datetime(record.get("created_at") or record.get("occurred_at"))
    if created is None:
        return {"record_type": kind, "record_id": identifier, "action": "review", "age_days": 0,
                "retention_days": retention.get(kind), "reason": "Missing or invalid creation timestamp."}
    age, days = max(0, (now - created).days), retention.get(kind)
    if kind not in retention:
        action, reason = "review", "No retention policy exists for this record type."
    elif days is None:
        action, reason = "retain", "Record type has no automatic expiry policy."
    elif days < 0:
        raise ValueError("Retention days cannot be negative.")
    elif age > days:
        action, reason = "eligible_for_review", "Retention window elapsed; review obligations before deletion."
    else:
        action, reason = "retain", "Within retention window."
    return {"record_type": kind, "record_id": identifier, "action": action, "age_days": age,
            "retention_days": days, "reason": reason}

def build_retention_report(records: Iterable[Mapping], now: datetime | None = None,
                           policy: Mapping[str, int | None] | None = None) -> dict:
    decisions = [retention_decision(row, now=now, policy=policy) for row in records]
    return {"records_examined": len(decisions),
            "retain": sum(row["action"] == "retain" for row in decisions),
            "eligible_for_review": sum(row["action"] == "eligible_for_review" for row in decisions),
            "review": sum(row["action"] == "review" for row in decisions),
            "decisions": decisions, "automatic_deletion_performed": False}

def redact_mapping(value, include_personal: bool = False, replacement: str = "[REDACTED]"):
    """Recursively redact secret keys and optionally personal contact fields."""
    if isinstance(value, dict):
        output = {}
        for key, item in value.items():
            normalized = re.sub(r"[^a-z0-9_]", "", str(key).casefold())
            if normalized in SENSITIVE_KEYS or any(part in normalized for part in ("password", "token", "secret")):
                output[key] = replacement
            elif not include_personal and normalized in PERSONAL_KEYS:
                output[key] = replacement
            else:
                output[key] = redact_mapping(item, include_personal, replacement)
        return output
    if isinstance(value, list):
        return [redact_mapping(item, include_personal, replacement) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_mapping(item, include_personal, replacement) for item in value)
    return value

def export_manifest(data: Mapping, include_personal: bool = True) -> dict:
    collections = {}
    for name, value in data.items():
        if isinstance(value, (list, dict)):
            collections[name] = {"count": len(value), "kind": "collection" if isinstance(value, list) else "object"}
        else:
            collections[name] = {"count": int(value is not None), "kind": "scalar"}
    return {"schema_version": 1, "collection_count": len(collections),
            "record_count": sum(item["count"] for item in collections.values()),
            "contains_personal_data": bool(include_personal), "collections": collections,
            "notice": "Review the export before sharing it; it may contain private career data."}

def sanitize_export(data: Mapping, include_personal: bool = True) -> dict:
    return redact_mapping(dict(data), include_personal=include_personal)

def validate_export_request(options: Mapping) -> dict:
    allowed = {"include_applications", "include_interviews", "include_contacts", "include_resumes",
               "include_tasks", "include_activity", "include_profile", "include_personal"}
    unknown = sorted(set(options) - allowed)
    if unknown:
        raise ValueError("Unsupported export options: " + ", ".join(unknown))
    normalized = {key: bool(value) for key, value in options.items()}
    normalized.setdefault("include_personal", True)
    if not any(value for key, value in normalized.items() if key.startswith("include_") and key != "include_personal"):
        raise ValueError("Select at least one data collection to export.")
    return normalized

def expiry_timestamp(created_at, retention_days: int | None):
    created = _parse_datetime(created_at)
    if created is None or retention_days is None:
        return None
    if retention_days < 0:
        raise ValueError("Retention days cannot be negative.")
    return (created + timedelta(days=retention_days)).isoformat()

def classify_personal_data_keys(keys: Iterable[str]) -> dict:
    result = {"sensitive": [], "personal": [], "ordinary": []}
    for key in keys:
        normalized = re.sub(r"[^a-z0-9_]", "", str(key).casefold())
        if normalized in SENSITIVE_KEYS or any(part in normalized for part in ("password", "token", "secret")):
            result["sensitive"].append(str(key))
        elif normalized in PERSONAL_KEYS:
            result["personal"].append(str(key))
        else:
            result["ordinary"].append(str(key))
    return result

def retention_policy_document(policy: Mapping[str, int | None] | None = None) -> list[dict]:
    configured = dict(DEFAULT_RETENTION_DAYS)
    configured.update(policy or {})
    return [{"record_type": kind, "retention_days": days, "automatic_deletion": False,
             "description": "Review before deletion" if days is not None else "Retain until user or legal policy says otherwise"}
            for kind, days in sorted(configured.items())]
