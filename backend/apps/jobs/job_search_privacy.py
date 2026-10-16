"""Privacy minimization checks for user-controlled job-search exports and sharing."""
from typing import Iterable, Mapping

SENSITIVE_FIELDS = {"password", "password_hash", "access_token", "refresh_token", "api_key", "secret",
                    "bank_account", "bank_password", "national_id", "passport_number", "date_of_birth"}
PERSONAL_FIELDS = {"email", "phone", "address", "linkedin", "personal_website", "full_name"}
def classify_field(name: str) -> str:
    normalized = str(name or "").strip().lower().replace("-", "_").replace(" ", "_")
    if normalized in SENSITIVE_FIELDS or any(part in normalized for part in ("password", "token", "secret", "api_key")):
        return "sensitive"
    if normalized in PERSONAL_FIELDS or any(part in normalized for part in ("email", "phone", "address")):
        return "personal"
    return "ordinary"

def privacy_review(payload: Mapping, include_personal: bool = False) -> dict:
    fields = []
    for key, value in payload.items():
        classification = classify_field(key)
        fields.append({"field": str(key), "classification": classification,
                       "included": classification == "ordinary" or (classification == "personal" and include_personal),
                       "redacted": classification == "sensitive" or (classification == "personal" and not include_personal),
                       "value_type": type(value).__name__})
    return {"field_count": len(fields), "sensitive_count": sum(row["classification"] == "sensitive" for row in fields),
            "personal_count": sum(row["classification"] == "personal" for row in fields),
            "include_personal": bool(include_personal), "fields": fields,
            "warning": "Never export passwords, access tokens, API keys, or secrets."}

def sanitize_share_payload(payload: Mapping, include_personal: bool = False) -> dict:
    output = {}
    for key, value in payload.items():
        kind = classify_field(key)
        if kind == "sensitive" or (kind == "personal" and not include_personal):
            output[key] = "[REDACTED]"
        elif isinstance(value, Mapping):
            output[key] = sanitize_share_payload(value, include_personal)
        elif isinstance(value, list):
            output[key] = [sanitize_share_payload(item, include_personal) if isinstance(item, Mapping)
                           else "[REDACTED]" if kind == "sensitive" else item for item in value]
        else:
            output[key] = value
    return output

def validate_share_options(options: Mapping) -> dict:
    allowed = {"include_applications", "include_notes", "include_personal", "include_activity"}
    unknown = set(options) - allowed
    if unknown:
        raise ValueError("Unknown share options: " + ", ".join(sorted(unknown)))
    if not any(bool(options.get(key)) for key in ("include_applications", "include_notes", "include_activity")):
        raise ValueError("Choose at least one data category to share")
    return {"include_applications": bool(options.get("include_applications")),
            "include_notes": bool(options.get("include_notes")),
            "include_personal": bool(options.get("include_personal")),
            "include_activity": bool(options.get("include_activity")),
            "include_credentials": False,
            "note": "Review the recipient, purpose, and data minimization before sharing."}

def sharing_risk_report(payload: Mapping) -> dict:
    review = privacy_review(payload, include_personal=True)
    sensitive = [row["field"] for row in review["fields"] if row["classification"] == "sensitive"]
    personal = [row["field"] for row in review["fields"] if row["classification"] == "personal"]
    return {"sensitive_fields": sensitive, "personal_fields": personal,
            "risk_level": "high" if sensitive else "review" if personal else "lower",
            "recommended_action": "Remove sensitive fields" if sensitive else
                "Confirm recipient and purpose for personal fields" if personal else "Review context and recipient",
            "automatic_sharing_performed": False}

def allowed_share_fields(fields: Iterable[str], include_personal: bool = False) -> dict:
    included, excluded = [], []
    for field in fields:
        kind = classify_field(field)
        if kind == "ordinary" or (kind == "personal" and include_personal):
            included.append(str(field))
        else:
            excluded.append({"field": str(field), "reason": "sensitive" if kind == "sensitive" else "personal_data_not_requested"})
    return {"included": sorted(included), "excluded": excluded, "credentials_allowed": False}
