"""Safe search syntax for career records; queries are parsed, never evaluated."""
from dataclasses import dataclass, field
from datetime import date
import re
import shlex
from typing import Iterable

ALLOWED_FIELDS = frozenset({"company", "role", "status", "location", "notes", "source"})
DATE_FIELDS = frozenset({"after", "before"})
SALARY_PATTERN = re.compile(r"^salary(>=|<=|>|<|=)(\\d+(?:\\.\\d{1,2})?)$", re.I)
FIELD_PATTERN = re.compile(r"^([a-z_]+):(.*)$", re.I)

class SearchSyntaxError(ValueError):
    """Malformed or unsupported search query."""

@dataclass(frozen=True)
class SearchTerm:
    kind: str
    value: str
    operator: str = ""
    negated: bool = False
    def as_dict(self):
        return {"kind": self.kind, "value": self.value, "operator": self.operator,
                "negated": self.negated}

@dataclass
class SearchQuery:
    raw: str
    terms: list[SearchTerm] = field(default_factory=list)
    def as_dict(self):
        return {"raw": self.raw, "terms": [term.as_dict() for term in self.terms]}

def parse_search_query(query: str, max_length: int = 500, max_terms: int = 30) -> SearchQuery:
    if not isinstance(query, str):
        raise SearchSyntaxError("Query must be text.")
    if len(query) > max_length:
        raise SearchSyntaxError(f"Query is limited to {max_length} characters.")
    try:
        tokens = shlex.split(query)
    except ValueError as exc:
        raise SearchSyntaxError("Quoted phrase is not closed.") from exc
    if len(tokens) > max_terms:
        raise SearchSyntaxError(f"Query may contain at most {max_terms} terms.")
    terms = []
    for raw in tokens:
        negated = raw.startswith("-") and len(raw) > 1
        token = raw[1:] if negated else raw
        salary = SALARY_PATTERN.match(token)
        if salary:
            terms.append(SearchTerm("salary", salary.group(2), salary.group(1), negated))
            continue
        match = FIELD_PATTERN.match(token)
        if match:
            name, value = match.group(1).lower(), match.group(2).strip()
            if name in DATE_FIELDS:
                try:
                    date.fromisoformat(value)
                except ValueError as exc:
                    raise SearchSyntaxError(f"{name}: must use YYYY-MM-DD.") from exc
                terms.append(SearchTerm(name, value, "", negated))
            elif name in ALLOWED_FIELDS:
                if not value:
                    raise SearchSyntaxError(f"{name}: needs a value.")
                terms.append(SearchTerm(name, value, "contains", negated))
            else:
                raise SearchSyntaxError(f"Unsupported search field: {name}")
            continue
        if token.startswith("salary"):
            raise SearchSyntaxError("Salary filters look like salary>=70000.")
        terms.append(SearchTerm("text", token, "contains", negated))
    return SearchQuery(query, terms)

def _value(row: dict, name: str) -> str:
    value = row.get(name)
    return "" if value is None else str(value).casefold()

def _matches_term(row: dict, term: SearchTerm) -> bool:
    if term.kind == "text":
        haystack = " ".join(_value(row, name) for name in ("company", "role", "location", "notes"))
        matched = term.value.casefold() in haystack
    elif term.kind in ALLOWED_FIELDS:
        matched = term.value.casefold() in _value(row, term.kind)
    elif term.kind in DATE_FIELDS:
        try:
            actual = date.fromisoformat(str(row.get("applied_date", ""))[:10])
            target = date.fromisoformat(term.value)
            matched = actual >= target if term.kind == "after" else actual <= target
        except ValueError:
            matched = False
    elif term.kind == "salary":
        value = row.get("salary_min")
        if value is None:
            value = row.get("salary_max")
        try:
            amount, target = float(value), float(term.value)
        except (TypeError, ValueError):
            matched = False
        else:
            matched = {">=": amount >= target, "<=": amount <= target, ">": amount > target,
                       "<": amount < target, "=": amount == target}[term.operator]
    else:
        matched = False
    return not matched if term.negated else matched

def matches_search(row: dict, query: SearchQuery | str) -> bool:
    parsed = parse_search_query(query) if isinstance(query, str) else query
    return all(_matches_term(row, term) for term in parsed.terms)

def filter_records(rows: Iterable[dict], query: SearchQuery | str) -> list[dict]:
    parsed = parse_search_query(query) if isinstance(query, str) else query
    return [row for row in rows if matches_search(row, parsed)]

def rank_records(rows: Iterable[dict], query: SearchQuery | str) -> list[dict]:
    parsed = parse_search_query(query) if isinstance(query, str) else query
    positives = [term for term in parsed.terms if not term.negated]
    ranked = []
    for row in rows:
        if not matches_search(row, parsed):
            continue
        haystack = " ".join(_value(row, name) for name in ("company", "role", "location", "notes"))
        score = 0
        for term in positives:
            needle = term.value.casefold()
            if term.kind == "text":
                score += 5 if needle == haystack else 3 if needle in haystack else 0
            elif term.kind in {"company", "role", "location"}:
                value = _value(row, term.kind)
                score += 6 if value == needle else 4 if needle in value else 0
            else:
                score += 1
        score += 2 if row.get("status") == "interview" else 0
        ranked.append({**row, "_search_score": score})
    ranked.sort(key=lambda row: (-row["_search_score"], str(row.get("updated_at", "")),
                                 str(row.get("id", ""))))
    return ranked

def explain_query(query: str) -> dict:
    parsed = parse_search_query(query)
    explanations = []
    for term in parsed.terms:
        if term.kind == "text":
            message = f"Search company, role, location, and notes for {term.value!r}."
        elif term.kind in DATE_FIELDS:
            phrase = "on or after" if term.kind == "after" else "on or before"
            message = f"Restrict application date to {phrase} {term.value}."
        elif term.kind == "salary":
            message = f"Compare salary value {term.operator} {term.value}."
        else:
            message = f"Match {term.kind} containing {term.value!r}."
        if term.negated:
            message = "Exclude records matching: " + message
        explanations.append({"term": term.as_dict(), "explanation": message})
    return {"query": query, "term_count": len(parsed.terms), "explanations": explanations}

def autocomplete_suggestions(prefix: str, values: Iterable[str], limit: int = 8) -> list[str]:
    if limit < 1:
        return []
    needle = prefix.strip().casefold()
    unique = {str(value).strip() for value in values if str(value).strip()}
    matches = [value for value in unique if value.casefold().startswith(needle)]
    return sorted(matches, key=lambda value: (value.casefold(), value))[:min(limit, 50)]
