"""Safe preflight validation and deduplication for imported job listings."""
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any, Iterable, Mapping
from urllib.parse import urlparse
import re

REQUIRED_FIELDS = ("company", "role")
ALLOWED_FIELDS = {
    "company", "role", "location", "job_url", "status", "salary_min",
    "salary_max", "applied_date", "next_action", "next_action_date", "notes",
    "source", "external_id", "description",
}
MAX_ROWS = 5000
MAX_FIELD_LENGTH = 50000
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


@dataclass
class ImportIssue:
    row: int
    field: str
    code: str
    message: str
    severity: str = "error"

    def as_dict(self):
        return {"row": self.row, "field": self.field, "code": self.code,
                "message": self.message, "severity": self.severity}


@dataclass
class ImportPreview:
    accepted: list[dict] = field(default_factory=list)
    issues: list[ImportIssue] = field(default_factory=list)
    duplicates: list[dict] = field(default_factory=list)
    total_rows: int = 0

    def as_dict(self):
        errors = sum(1 for issue in self.issues if issue.severity == "error")
        warnings = sum(1 for issue in self.issues if issue.severity == "warning")
        return {
            "total_rows": self.total_rows,
            "accepted_count": len(self.accepted),
            "duplicate_count": len(self.duplicates),
            "error_count": errors,
            "warning_count": warnings,
            "can_import": errors == 0 and bool(self.accepted),
            "accepted": self.accepted,
            "duplicates": self.duplicates,
            "issues": [issue.as_dict() for issue in self.issues],
        }


def canonical_text(value: Any) -> str:
    return " ".join(str(value or "").casefold().split())


def listing_fingerprint(record: Mapping[str, Any]) -> str:
    """Fingerprint company, role, and URL; avoid including personal notes."""
    company = canonical_text(record.get("company"))
    role = canonical_text(record.get("role"))
    parsed = urlparse(str(record.get("job_url") or "").strip())
    url = (parsed.netloc.casefold() + parsed.path.rstrip("/").casefold()) if parsed.scheme in {"http", "https"} else ""
    basis = "|".join((company, role, url))
    return sha256(basis.encode("utf-8")).hexdigest()


def _validate_url(value: Any) -> bool:
    if value in (None, ""):
        return True
    if not isinstance(value, str) or len(value) > 2048:
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc) and not parsed.username and not parsed.password


def _validate_salary(value: Any) -> bool:
    if value in (None, ""):
        return True
    if isinstance(value, bool):
        return False
    try:
        amount = float(value)
        return amount >= 0 and amount < 10**12
    except (TypeError, ValueError):
        return False


def normalize_import_record(record: Mapping[str, Any], row_number: int) -> tuple[dict, list[ImportIssue]]:
    issues = []
    if not isinstance(record, Mapping):
        return {}, [ImportIssue(row_number, "", "invalid_record", "Each row must be an object.")]
    unknown = set(record) - ALLOWED_FIELDS
    for field_name in sorted(unknown):
        issues.append(ImportIssue(row_number, field_name, "unknown_field",
                                  "This field will be ignored.", "warning"))
    normalized = {}
    for field_name in ALLOWED_FIELDS & set(record):
        value = record[field_name]
        if isinstance(value, str):
            value = value.strip()
            if len(value) > MAX_FIELD_LENGTH:
                issues.append(ImportIssue(row_number, field_name, "field_too_long",
                                          f"Field exceeds {MAX_FIELD_LENGTH} characters."))
                continue
        normalized[field_name] = value
    for required in REQUIRED_FIELDS:
        if not str(normalized.get(required) or "").strip():
            issues.append(ImportIssue(row_number, required, "required",
                                      f"{required} is required."))
    for text_field in ("company", "role", "location", "next_action", "source"):
        value = normalized.get(text_field)
        if value is not None and not isinstance(value, str):
            issues.append(ImportIssue(row_number, text_field, "invalid_type",
                                      "This field must be text."))
    if not _validate_url(normalized.get("job_url")):
        issues.append(ImportIssue(row_number, "job_url", "invalid_url",
                                  "Use a valid HTTP or HTTPS URL without embedded credentials."))
    for salary_field in ("salary_min", "salary_max"):
        if not _validate_salary(normalized.get(salary_field)):
            issues.append(ImportIssue(row_number, salary_field, "invalid_salary",
                                      "Salary must be a non-negative number."))
    low, high = normalized.get("salary_min"), normalized.get("salary_max")
    if _validate_salary(low) and _validate_salary(high) and low not in (None, "") and high not in (None, ""):
        if float(low) > float(high):
            issues.append(ImportIssue(row_number, "salary_max", "salary_range",
                                      "salary_max must be greater than or equal to salary_min."))
    status = normalized.get("status")
    valid_statuses = {"saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn"}
    if status not in (None, "") and status not in valid_statuses:
        issues.append(ImportIssue(row_number, "status", "invalid_status",
                                  "Status must be a supported application status."))
    for date_field in ("applied_date", "next_action_date"):
        value = normalized.get(date_field)
        if value in (None, ""):
            continue
        try:
            from datetime import date
            date.fromisoformat(str(value)[:10])
        except ValueError:
            issues.append(ImportIssue(row_number, date_field, "invalid_date",
                                      "Date must use ISO format YYYY-MM-DD."))
    return normalized, issues


def preview_import(
    rows: Iterable[Mapping[str, Any]],
    *,
    existing_fingerprints: Iterable[str] = (),
    max_rows: int = MAX_ROWS,
) -> ImportPreview:
    if isinstance(max_rows, bool) or not isinstance(max_rows, int) or not 1 <= max_rows <= MAX_ROWS:
        raise ValueError(f"max_rows must be between 1 and {MAX_ROWS}.")
    preview = ImportPreview()
    known = set(existing_fingerprints)
    seen = set(known)
    for row_number, row in enumerate(rows, start=1):
        preview.total_rows += 1
        if preview.total_rows > max_rows:
            preview.issues.append(ImportIssue(row_number, "", "row_limit",
                f"Import is limited to {max_rows} rows."))
            break
        normalized, issues = normalize_import_record(row, row_number)
        preview.issues.extend(issues)
        has_errors = any(issue.severity == "error" for issue in issues)
        if has_errors:
            continue
        fingerprint = listing_fingerprint(normalized)
        if fingerprint in seen:
            preview.duplicates.append({
                "row": row_number,
                "fingerprint": fingerprint,
                "company": normalized.get("company", ""),
                "role": normalized.get("role", ""),
                "reason": "Matches an existing or earlier imported listing.",
            })
            continue
        seen.add(fingerprint)
        normalized["_import_row"] = row_number
        normalized["_fingerprint"] = fingerprint
        preview.accepted.append(normalized)
    return preview
