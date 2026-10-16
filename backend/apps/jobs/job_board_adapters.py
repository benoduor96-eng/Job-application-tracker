"""Normalize externally obtained job listings without making network requests."""
import csv
import io
from datetime import date, datetime
from urllib.parse import urlparse

ALLOWED_SCHEMES = {"https", "http"}
MAX_TEXT = 20_000


class JobImportError(ValueError):
    """Raised when an imported job record cannot be normalized safely."""


def _text(value, field, required=False, limit=MAX_TEXT):
    value = "" if value is None else str(value).strip()
    if required and not value:
        raise JobImportError(f"{field} is required.")
    if len(value) > limit:
        raise JobImportError(f"{field} exceeds the {limit}-character limit.")
    return value


def _url(value):
    value = _text(value, "url", limit=2048)
    if not value:
        return ""
    parsed = urlparse(value)
    if parsed.scheme not in ALLOWED_SCHEMES or not parsed.netloc:
        raise JobImportError("Job URL must be an absolute HTTP(S) URL.")
    if parsed.username or parsed.password:
        raise JobImportError("URLs containing embedded credentials are not allowed.")
    return value


def _date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value.isoformat()
    raw = str(value).strip()
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        try:
            return date.fromisoformat(raw[:10]).isoformat()
        except ValueError as exc:
            raise JobImportError("published_at must be an ISO date or datetime.") from exc


def normalize_generic(record):
    """Normalize a generic listing to the platform's canonical shape."""
    if not isinstance(record, dict):
        raise JobImportError("Each job must be an object.")
    company = _text(record.get("company") or record.get("company_name"), "company", True, 200)
    role = _text(record.get("role") or record.get("title") or record.get("position"), "role", True, 200)
    try:
        low = float(record["salary_min"]) if record.get("salary_min") not in (None, "") else None
        high = float(record["salary_max"]) if record.get("salary_max") not in (None, "") else None
    except (TypeError, ValueError) as exc:
        raise JobImportError("Salary bounds must be numeric.") from exc
    if (low is not None and low < 0) or (high is not None and high < 0):
        raise JobImportError("Salary bounds cannot be negative.")
    if low is not None and high is not None and low > high:
        raise JobImportError("salary_min cannot exceed salary_max.")
    return {
        "company": company, "role": role,
        "location": _text(record.get("location"), "location", limit=200),
        "job_url": _url(record.get("job_url") or record.get("url") or record.get("absolute_url")),
        "description": _text(record.get("description") or record.get("content") or record.get("text"), "description"),
        "employment_type": _text(record.get("employment_type") or record.get("type"), "employment_type", limit=80),
        "salary_min": low, "salary_max": high,
        "source": _text(record.get("source") or record.get("provider") or "manual", "source", limit=80),
        "source_id": _text(record.get("source_id") or record.get("id"), "source_id", limit=160),
        "published_at": _date(record.get("published_at") or record.get("created_at")),
    }


def normalize_greenhouse(record):
    """Map a Greenhouse-shaped public job payload into the canonical shape."""
    if not isinstance(record, dict):
        raise JobImportError("Greenhouse job must be an object.")
    departments = record.get("departments") or []
    location = record.get("location") or {}
    return normalize_generic({
        "company": record.get("company_name") or record.get("company") or (departments[0].get("name") if departments else ""),
        "role": record.get("title"), "location": location.get("name", "") if isinstance(location, dict) else location,
        "job_url": record.get("absolute_url"), "description": record.get("content", ""),
        "source": "greenhouse", "source_id": record.get("id"),
        "published_at": record.get("updated_at") or record.get("created_at"),
    })


def normalize_lever(record):
    """Map a Lever-shaped public posting into the canonical shape."""
    if not isinstance(record, dict):
        raise JobImportError("Lever job must be an object.")
    categories, salary = record.get("categories") or {}, record.get("salaryRange") or {}
    return normalize_generic({
        "company": record.get("company") or record.get("companyName") or categories.get("team") or "Unknown company",
        "role": record.get("text") or record.get("title"),
        "location": categories.get("location", ""),
        "job_url": record.get("hostedUrl") or record.get("applyUrl"),
        "description": record.get("descriptionPlain") or record.get("description") or "",
        "employment_type": categories.get("commitment", ""),
        "salary_min": salary.get("min"), "salary_max": salary.get("max"),
        "source": "lever", "source_id": record.get("id"),
        "published_at": record.get("createdAt"),
    })


def parse_jobs_csv(contents, limit=500):
    """Parse CSV text with strict row limits and row-level validation errors."""
    if not isinstance(contents, str):
        raise JobImportError("CSV contents must be text.")
    if len(contents) > 2_000_000:
        raise JobImportError("CSV file exceeds the 2 MB text limit.")
    reader = csv.DictReader(io.StringIO(contents))
    if not reader.fieldnames:
        raise JobImportError("CSV must include a header row.")
    rows, errors = [], []
    for line, record in enumerate(reader, start=2):
        if line > limit + 1:
            errors.append({"line": line, "error": f"Import limited to {limit} rows."})
            break
        try:
            rows.append({"line": line, "job": normalize_generic(record)})
        except JobImportError as exc:
            errors.append({"line": line, "error": str(exc)})
    return {"records": rows, "errors": errors, "accepted": len(rows), "rejected": len(errors)}
