"""Safe import validation primitives; callers remain responsible for persistence and ownership."""
import csv
import io
import json
import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Iterable, Mapping

MAX_ROWS = 5000
MAX_TEXT = 20000
ALLOWED_STATUSES = {"saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn"}
FIELD_ALIASES = {
    "company": ("company", "employer", "organization", "organisation", "company_name"),
    "role": ("role", "title", "job_title", "position", "job_role"),
    "location": ("location", "city", "work_location", "job_location"),
    "job_url": ("job_url", "url", "link", "posting_url", "job_link"),
    "status": ("status", "application_status", "stage"),
    "applied_date": ("applied_date", "date_applied", "application_date", "applied_at"),
    "salary_min": ("salary_min", "minimum_salary", "min_salary", "salary_from"),
    "salary_max": ("salary_max", "maximum_salary", "max_salary", "salary_to"),
    "notes": ("notes", "description", "comments", "details"),
    "next_action": ("next_action", "follow_up", "reminder"),
    "next_action_date": ("next_action_date", "follow_up_date", "reminder_date"),
}

def _header(value):
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().lower()).strip("_")

def _text(value, limit=MAX_TEXT):
    if value is None:
        return ""
    return str(value).replace("\x00", "").strip()[:limit]

def _date(value):
    text = _text(value, 80)
    if not text:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except ValueError:
        raise ValueError("Use a recognizable date such as YYYY-MM-DD")

def _money(value):
    text = _text(value, 100).replace(",", "").replace("$", "").replace("£", "").replace("€", "")
    if not text:
        return None
    try:
        amount = Decimal(text)
    except InvalidOperation:
        raise ValueError("Salary must be numeric")
    if not amount.is_finite() or amount < 0 or amount > Decimal("9999999999.99"):
        raise ValueError("Salary must be a non-negative finite amount within supported limits")
    return str(amount.quantize(Decimal("0.01")))

def map_headers(headers: Iterable[str]) -> dict:
    normalized = [_header(header) for header in headers]
    mapping, used = {}, set()
    for field, aliases in FIELD_ALIASES.items():
        matches = [index for index, name in enumerate(normalized) if name in aliases]
        if matches:
            mapping[field] = matches[0]
            used.add(matches[0])
    return {"mapping": mapping, "unmapped_headers": [headers[index] for index in range(len(headers)) if index not in used],
            "missing_required": [field for field in ("company", "role") if field not in mapping],
            "duplicate_normalized_headers": sorted({name for name in normalized if normalized.count(name) > 1 and name})}

def validate_row(raw: Mapping, row_number: int = 1) -> dict:
    row = {_header(key): value for key, value in raw.items()}
    result, errors, warnings = {}, [], []
    for field, aliases in FIELD_ALIASES.items():
        value = next((row[alias] for alias in aliases if alias in row and row[alias] not in (None, "")), None)
        if field in ("company", "role"):
            text = _text(value, 200)
            if not text:
                errors.append({"field": field, "code": "required", "message": f"{field} is required"})
            result[field] = text
        elif field in ("location", "job_url", "status", "notes", "next_action"):
            result[field] = _text(value, 2000 if field == "notes" else 500)
        elif field in ("applied_date", "next_action_date"):
            try:
                result[field] = _date(value).isoformat() if value not in (None, "") else None
            except ValueError as exc:
                errors.append({"field": field, "code": "invalid_date", "message": str(exc)})
                result[field] = None
        elif field in ("salary_min", "salary_max"):
            try:
                result[field] = _money(value)
            except ValueError as exc:
                errors.append({"field": field, "code": "invalid_salary", "message": str(exc)})
                result[field] = None
    status = (result.get("status") or "saved").lower()
    if status not in ALLOWED_STATUSES:
        errors.append({"field": "status", "code": "invalid_choice", "message": "Unsupported application status"})
    result["status"] = status
    low, high = result.get("salary_min"), result.get("salary_max")
    if low is not None and high is not None and Decimal(low) > Decimal(high):
        errors.append({"field": "salary_max", "code": "inverted_range", "message": "Maximum salary is below minimum salary"})
    url = result.get("job_url") or ""
    if url and not re.match(r"^https?://", url, re.I):
        warnings.append({"field": "job_url", "code": "unusual_scheme", "message": "Only HTTP(S) job links are recommended"})
    result["row_number"] = row_number
    result["errors"] = errors
    result["warnings"] = warnings
    result["valid"] = not errors
    return result

def validate_rows(rows: Iterable[Mapping], maximum: int = MAX_ROWS) -> dict:
    if not 1 <= maximum <= MAX_ROWS:
        raise ValueError(f"maximum must be between 1 and {MAX_ROWS}")
    output, duplicates, seen = [], [], {}
    truncated = False
    for index, row in enumerate(rows, 1):
        if index > maximum:
            truncated = True
            break
        item = validate_row(row, index)
        key = (item.get("company", "").casefold(), item.get("role", "").casefold(),
               item.get("applied_date") or "")
        if item["valid"] and key in seen:
            item["warnings"].append({"field": "row", "code": "possible_duplicate",
                                     "message": f"Similar to row {seen[key]}; review before importing"})
            duplicates.append({"row_number": index, "similar_row": seen[key]})
        elif item["valid"]:
            seen[key] = index
        output.append(item)
    valid_count = sum(item["valid"] for item in output)
    return {"rows": output, "row_count": len(output), "valid_count": valid_count,
            "invalid_count": len(output) - valid_count, "duplicate_warnings": duplicates,
            "truncated": truncated, "can_import": valid_count > 0,
            "warning": "Validation does not save records. Review duplicates and confirm before persistence."}

def parse_csv(content: str, maximum: int = MAX_ROWS) -> dict:
    text = _text(content, 10_000_000)
    if not text:
        raise ValueError("CSV content is empty")
    try:
        reader = csv.DictReader(io.StringIO(text, newline=""))
        if not reader.fieldnames:
            raise ValueError("CSV header row is required")
        headers = reader.fieldnames
        rows = list(reader)
    except csv.Error as exc:
        raise ValueError(f"Invalid CSV: {exc}")
    mapping = map_headers(headers)
    report = validate_rows(rows, maximum=maximum)
    report["header_mapping"] = mapping
    report["format"] = "csv"
    if mapping["missing_required"]:
        report["can_import"] = False
        report["header_errors"] = [{"field": field, "message": "Required column was not recognized"}
                                   for field in mapping["missing_required"]]
    return report

def parse_json_records(content: str, maximum: int = MAX_ROWS) -> dict:
    text = _text(content, 10_000_000)
    if not text:
        raise ValueError("JSON content is empty")
    try:
        decoded = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON at line {exc.lineno}, column {exc.colno}")
    if isinstance(decoded, dict):
        decoded = decoded.get("applications", decoded.get("results", [decoded]))
    if not isinstance(decoded, list) or any(not isinstance(row, dict) for row in decoded):
        raise ValueError("JSON must be an object or a list of application objects")
    report = validate_rows(decoded, maximum=maximum)
    report["format"] = "json"
    return report

def preview_import(rows: Iterable[Mapping], mode: str = "create_only", maximum: int = MAX_ROWS) -> dict:
    if mode not in {"create_only", "skip_duplicates", "manual_review"}:
        raise ValueError("Unsupported import mode")
    report = validate_rows(rows, maximum)
    accepted, skipped = [], []
    for row in report["rows"]:
        if not row["valid"]:
            skipped.append({"row_number": row["row_number"], "reason": "validation_error"})
            continue
        if any(warning["code"] == "possible_duplicate" for warning in row["warnings"]) and mode == "skip_duplicates":
            skipped.append({"row_number": row["row_number"], "reason": "possible_duplicate"})
            continue
        accepted.append(row)
    return {"mode": mode, "accepted": accepted, "skipped": skipped,
            "accepted_count": len(accepted), "skipped_count": len(skipped),
            "requires_confirmation": bool(accepted),
            "persistence_performed": False,
            "notice": "Preview only. A separate authorized action must persist records."}

def export_rows(rows: Iterable[Mapping], fields: Iterable[str] | None = None) -> dict:
    fields = list(fields or FIELD_ALIASES.keys())
    unknown = set(fields) - set(FIELD_ALIASES)
    if unknown:
        raise ValueError("Unsupported export fields: " + ", ".join(sorted(unknown)))
    output = []
    for raw in rows:
        item = validate_row(raw)
        output.append({field: item.get(field) for field in fields})
    return {"fields": fields, "rows": output, "count": len(output),
            "note": "The caller must enforce ownership and choose a secure download response."}

def csv_export(rows: Iterable[Mapping], fields: Iterable[str] | None = None) -> str:
    export = export_rows(rows, fields)
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=export["fields"], extrasaction="ignore")
    writer.writeheader()
    for row in export["rows"]:
        writer.writerow({key: _spreadsheet_safe(value) for key, value in row.items()})
    return buffer.getvalue()

def _spreadsheet_safe(value):
    if value is None:
        return ""
    text = str(value)
    if text.startswith(("=", "+", "-", "@", "\t", "\r")):
        return "'" + text
    return text

def import_statistics(report: Mapping) -> dict:
    rows = report.get("rows") or []
    errors, warnings = {}, {}
    for row in rows:
        for error in row.get("errors", []):
            errors[error.get("code", "unknown")] = errors.get(error.get("code", "unknown"), 0) + 1
        for warning in row.get("warnings", []):
            warnings[warning.get("code", "unknown")] = warnings.get(warning.get("code", "unknown"), 0) + 1
    return {"row_count": len(rows), "valid": sum(bool(row.get("valid")) for row in rows),
            "invalid": sum(not bool(row.get("valid")) for row in rows),
            "errors_by_code": dict(sorted(errors.items())), "warnings_by_code": dict(sorted(warnings.items())),
            "top_error": max(errors, key=errors.get) if errors else None}
