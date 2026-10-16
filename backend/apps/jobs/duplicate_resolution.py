"""Explainable duplicate detection. No record is changed or deleted by this module."""
from dataclasses import dataclass
from datetime import date, datetime
from difflib import SequenceMatcher
import re
import unicodedata
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TRACKING_KEYS = frozenset({"fbclid", "gclid", "ref", "source", "campaign", "utm_source",
                           "utm_medium", "utm_campaign", "utm_content", "utm_term"})
COMPANY_SUFFIXES = frozenset({"inc", "incorporated", "llc", "ltd", "limited", "corp",
                              "corporation", "company", "co", "plc", "group", "holdings"})

@dataclass(frozen=True)
class SimilarityFeature:
    name: str
    score: float
    weight: float
    explanation: str
    def as_dict(self):
        return {"name": self.name, "score": round(self.score, 4),
                "weight": self.weight, "explanation": self.explanation}

@dataclass(frozen=True)
class DuplicateCandidate:
    left_id: int | str
    right_id: int | str
    score: float
    confidence: str
    features: tuple[SimilarityFeature, ...]
    def as_dict(self):
        return {"left_id": self.left_id, "right_id": self.right_id,
                "score": round(self.score, 4), "confidence": self.confidence,
                "features": [feature.as_dict() for feature in self.features]}

def normalize_text(value: object) -> str:
    if value is None:
        return ""
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
    return " ".join(re.findall(r"[a-z0-9]+", text.casefold()))

def normalize_company(value: object) -> str:
    tokens = normalize_text(value).split()
    while tokens and tokens[-1] in COMPANY_SUFFIXES:
        tokens.pop()
    return " ".join(tokens)

def normalize_role(value: object) -> str:
    aliases = {"sr": "senior", "jr": "junior", "eng": "engineer", "dev": "developer",
               "swe": "software engineer"}
    normalized = normalize_text(value)
    for short, full in aliases.items():
        normalized = re.sub(rf"\\b{re.escape(short)}\\b", full, normalized)
    return " ".join(normalized.split())

def canonical_job_url(value: object) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    try:
        parts = urlsplit(raw)
    except ValueError:
        return ""
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        return ""
    host = parts.hostname.lower()
    if host.startswith("www."):
        host = host[4:]
    path = re.sub(r"/{2,}", "/", parts.path).rstrip("/")
    query = urlencode(sorted((key, val) for key, val in parse_qsl(parts.query, keep_blank_values=True)
                             if key.lower() not in TRACKING_KEYS))
    return urlunsplit(("https", host, path, query, ""))

def _similarity(left: str, right: str) -> float:
    if not left or not right:
        return 0.0
    if left == right:
        return 1.0
    return SequenceMatcher(None, left, right, autojunk=False).ratio()

def _parse_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None
    return None

def _date_score(left, right, window: int = 21) -> tuple[float, str]:
    a, b = _parse_date(left), _parse_date(right)
    if not a or not b:
        return 0.0, "No comparable application date was supplied."
    distance = abs((a - b).days)
    if distance == 0:
        return 1.0, "Application dates match."
    if distance <= window:
        return max(0.0, 1.0 - distance / (window + 1)), f"Dates are {distance} days apart."
    return 0.0, f"Dates are {distance} days apart, outside the review window."

def compare_records(left: dict, right: dict) -> DuplicateCandidate:
    features = []
    company = _similarity(normalize_company(left.get("company")), normalize_company(right.get("company")))
    features.append(SimilarityFeature("company", company, .30, "Normalized employer names."))
    role = _similarity(normalize_role(left.get("role") or left.get("title")),
                       normalize_role(right.get("role") or right.get("title")))
    features.append(SimilarityFeature("role", role, .28, "Normalized job titles."))
    left_url = canonical_job_url(left.get("job_url") or left.get("url"))
    right_url = canonical_job_url(right.get("job_url") or right.get("url"))
    features.append(SimilarityFeature("job_url", float(bool(left_url and left_url == right_url)),
                                      .28, "Canonical listing URL equality."))
    location = _similarity(normalize_text(left.get("location")), normalize_text(right.get("location")))
    features.append(SimilarityFeature("location", location, .08, "Normalized location similarity."))
    date_score, note = _date_score(left.get("applied_date"), right.get("applied_date"))
    features.append(SimilarityFeature("date", date_score, .06, note))
    score = sum(feature.score * feature.weight for feature in features)
    if not left_url or not right_url:
        score = min(score, .78)
    confidence = "high" if score >= .86 else "review" if score >= .62 else "low"
    return DuplicateCandidate(left.get("id", "left"), right.get("id", "right"),
                              min(1.0, score), confidence, tuple(features))

def find_duplicate_candidates(records: list[dict], threshold: float = .55,
                              max_pairs: int = 500) -> list[dict]:
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")
    if max_pairs < 1:
        raise ValueError("max_pairs must be positive")
    candidates = []
    for index, left in enumerate(records):
        for right in records[index + 1:]:
            if left.get("id") is not None and left.get("id") == right.get("id"):
                continue
            candidate = compare_records(left, right)
            if candidate.score >= threshold:
                candidates.append(candidate.as_dict())
    candidates.sort(key=lambda row: (-row["score"], str(row["left_id"]), str(row["right_id"])))
    return candidates[:max_pairs]

def build_merge_preview(primary: dict, duplicate: dict, fields: tuple[str, ...] | None = None) -> dict:
    fields = fields or ("company", "role", "location", "job_url", "status", "salary_min",
                        "salary_max", "applied_date", "notes", "next_action", "next_action_date")
    proposed, conflicts = {}, []
    for field in fields:
        first, second = primary.get(field), duplicate.get(field)
        if first not in (None, "") and second not in (None, "") and first != second:
            conflicts.append({"field": field, "primary": first, "duplicate": second})
            proposed[field] = first
        else:
            proposed[field] = first if first not in (None, "") else second
    return {"primary_id": primary.get("id"), "duplicate_id": duplicate.get("id"),
            "proposed_values": proposed, "conflicts": conflicts, "requires_review": bool(conflicts),
            "warning": "Preview only. No records were changed or deleted."}

def duplicate_report(records: list[dict]) -> dict:
    candidates = find_duplicate_candidates(records)
    return {"records_examined": len(records), "candidate_pairs": len(candidates),
            "high_confidence": sum(row["confidence"] == "high" for row in candidates),
            "needs_review": sum(row["confidence"] == "review" for row in candidates),
            "pairs": candidates}
