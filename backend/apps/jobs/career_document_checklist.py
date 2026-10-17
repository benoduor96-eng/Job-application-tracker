"""Career-document packet checks that avoid storing or generating document contents."""
from typing import Iterable, Mapping

DOCUMENT_TYPES = {"resume", "cover_letter", "portfolio", "references", "certificate", "work_sample", "other"}
def validate_document(item: Mapping) -> dict:
    title = str(item.get("title") or "").strip()
    if not title:
        raise ValueError("Document title is required")
    kind = str(item.get("document_type") or "other").lower()
    if kind not in DOCUMENT_TYPES:
        raise ValueError("Unsupported document type")
    status = str(item.get("status") or "draft").lower()
    if status not in {"draft", "reviewed", "ready", "archived"}:
        raise ValueError("Unsupported document status")
    return {"id": item.get("id"), "title": title[:180], "document_type": kind, "status": status,
            "updated_on": str(item.get("updated_on") or "")[:40],
            "target_role": str(item.get("target_role") or "")[:180],
            "confidentiality_reviewed": bool(item.get("confidentiality_reviewed", False)),
            "personal_data_reviewed": bool(item.get("personal_data_reviewed", False)),
            "notes": str(item.get("notes") or "")[:1000]}

def document_readiness(item: Mapping) -> dict:
    row = validate_document(item)
    checks = {"reviewed": row["status"] in {"reviewed", "ready"},
              "confidentiality_reviewed": row["confidentiality_reviewed"],
              "personal_data_reviewed": row["personal_data_reviewed"]}
    return {"id": row["id"], "title": row["title"], "document_type": row["document_type"],
            "checks": checks, "blockers": [key for key, passed in checks.items() if not passed],
            "ready": all(checks.values()), "automatic_changes_performed": False}

def application_packet_check(documents: Iterable[Mapping], required_types: Iterable[str]) -> dict:
    rows = [validate_document(item) for item in documents]
    required = sorted(set(required_types))
    invalid = set(required) - DOCUMENT_TYPES
    if invalid:
        raise ValueError("Unsupported required document type")
    ready_types = {row["document_type"] for row in rows if document_readiness(row)["ready"]}
    missing = [kind for kind in required if kind not in ready_types]
    return {"required_types": required, "ready_types": sorted(ready_types),
            "missing_ready_types": missing, "ready": not missing,
            "documents": [document_readiness(row) for row in rows],
            "warning": "Confirm employer instructions and never submit confidential or misleading material."}

def document_maintenance_queue(documents: Iterable[Mapping]) -> list[dict]:
    tasks = []
    for item in documents:
        row = validate_document(item)
        readiness = document_readiness(row)
        for blocker in readiness["blockers"]:
            tasks.append({"document_id": row["id"], "title": row["title"], "action": blocker,
                          "suggestion": {
                              "reviewed": "Review wording, dates, spelling, and relevance to the target role.",
                              "confidentiality_reviewed": "Remove private employer or client material unless sharing is authorized.",
                              "personal_data_reviewed": "Check for unnecessary personal information before sending.",
                          }[blocker]})
    return sorted(tasks, key=lambda task: (task["title"].casefold(), task["action"]))

def document_status_summary(documents: Iterable[Mapping]) -> dict:
    rows = [validate_document(item) for item in documents]
    counts = {status: sum(row["status"] == status for row in rows) for status in ("draft", "reviewed", "ready", "archived")}
    by_type = {kind: sum(row["document_type"] == kind for row in rows) for kind in sorted(DOCUMENT_TYPES)}
    return {"total": len(rows), "by_status": counts, "by_type": by_type,
            "ready_count": sum(document_readiness(row)["ready"] for row in rows),
            "note": "Readiness is based on checklist fields, not a professional review of document quality."}
