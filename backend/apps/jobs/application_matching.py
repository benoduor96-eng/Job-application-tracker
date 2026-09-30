from dataclasses import dataclass
from typing import Iterable

from .models import JobApplication


@dataclass(frozen=True)
class ApplicationMatch:
    application_id: int
    company: str
    role: str
    score: float
    reasons: tuple[str, ...]


def _normalize(value: str) -> str:
    return " ".join((value or "").lower().split())


def _token_set(value: str) -> set[str]:
    return {token for token in _normalize(value).replace("/", " ").split() if len(token) > 2}


def similarity(left: str, right: str) -> float:
    a, b = _token_set(left), _token_set(right)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def find_possible_duplicates(
    application: JobApplication,
    candidates: Iterable[JobApplication],
    threshold: float = 0.45,
) -> list[ApplicationMatch]:
    target_company = _normalize(application.company)
    target_role = _normalize(application.role)
    results: list[ApplicationMatch] = []

    for candidate in candidates:
        if candidate.pk == application.pk:
            continue

        company_score = similarity(target_company, candidate.company)
        role_score = similarity(target_role, candidate.role)
        url_score = 1.0 if application.job_url and application.job_url == candidate.job_url else 0.0
        score = round((company_score * 0.45) + (role_score * 0.45) + (url_score * 0.10), 3)

        reasons = []
        if company_score >= threshold:
            reasons.append("similar company")
        if role_score >= threshold:
            reasons.append("similar role")
        if url_score:
            reasons.append("same job URL")

        if score >= threshold or url_score:
            results.append(
                ApplicationMatch(
                    application_id=candidate.id,
                    company=candidate.company,
                    role=candidate.role,
                    score=score,
                    reasons=tuple(reasons),
                )
            )

    return sorted(results, key=lambda item: (-item.score, item.company.lower(), item.role.lower()))
