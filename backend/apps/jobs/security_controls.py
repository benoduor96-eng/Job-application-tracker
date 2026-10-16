"""Small security helpers shared by API boundaries and import/export workflows."""
from collections.abc import Mapping, Sequence
from pathlib import PurePath
import re

MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 25
MAX_EXPORT_ROWS = 10000
SENSITIVE_KEY_PARTS = ("password", "secret", "token", "authorization", "cookie",
                       "api_key", "access_key", "refresh", "ssn", "national_id")
EMAIL_PATTERN = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE_PATTERN = re.compile(r"(?<!\w)(?:\+?\d[\d ().-]{7,}\d)(?!\w)")
BEARER_PATTERN = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]+=*")


def bounded_page_size(value, *, default=DEFAULT_PAGE_SIZE, maximum=MAX_PAGE_SIZE):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    if parsed < 1:
        return default
    return min(parsed, maximum)


def safe_filename(value, *, fallback="job-tracker-export.json", max_length=120):
    """Return a basename without control characters, traversal, or header delimiters."""
    candidate = PurePath(str(value or "")).name
    candidate = re.sub(r"[^A-Za-z0-9._-]+", "-", candidate).strip(".-_")
    candidate = candidate[:max_length]
    return candidate or fallback


def redact_mapping(value: Mapping, *, extra_keys=()):
    """Recursively redact values whose key suggests a secret or direct identifier."""
    sensitive = set(extra_keys)
    result = {}
    for key, item in value.items():
        name = str(key)
        folded = name.casefold()
        if any(part in folded for part in SENSITIVE_KEY_PARTS) or folded in sensitive:
            result[name] = "[REDACTED]"
        elif isinstance(item, Mapping):
            result[name] = redact_mapping(item, extra_keys=sensitive)
        elif isinstance(item, list):
            result[name] = [redact_mapping(child, extra_keys=sensitive)
                            if isinstance(child, Mapping) else child for child in item]
        else:
            result[name] = item
    return result


def redact_free_text(value, *, redact_emails=True, redact_phones=False):
    text = str(value or "")
    text = BEARER_PATTERN.sub("Bearer [REDACTED]", text)
    if redact_emails:
        text = EMAIL_PATTERN.sub("[EMAIL]", text)
    if redact_phones:
        text = PHONE_PATTERN.sub("[PHONE]", text)
    return text


def export_limit(requested, *, maximum=MAX_EXPORT_ROWS):
    if isinstance(requested, bool):
        raise ValueError("Export row limit must be an integer.")
    try:
        value = int(requested)
    except (TypeError, ValueError) as exc:
        raise ValueError("Export row limit must be an integer.") from exc
    if value < 1:
        raise ValueError("Export row limit must be positive.")
    return min(value, maximum)


def audit_actor(request):
    """Extract only stable, non-secret request metadata suitable for an audit record."""
    user = getattr(request, "user", None)
    authenticated = bool(getattr(user, "is_authenticated", False))
    return {
        "actor_id": getattr(user, "pk", None) if authenticated else None,
        "actor_type": "user" if authenticated else "anonymous",
        "method": str(getattr(request, "method", ""))[:12],
        "path": str(getattr(request, "path", ""))[:250],
        "request_id": str(getattr(request, "request_id", ""))[:100] or None,
    }


def safe_error_detail(error, *, maximum=300):
    """Avoid returning exception representations that can leak paths or secrets."""
    message = str(error).replace("\r", " ").replace("\n", " ").strip()
    return message[:maximum] or "The request could not be processed."


def validate_sort_field(value, allowed_fields: Sequence[str], *, default):
    if not isinstance(value, str):
        return default
    return value if value in set(allowed_fields) else default
