"""
Cover-letter generation utilities.

This module creates structured drafts from information already stored in the
tracker. It does not call external AI services and never invents credentials,
employers, dates, or achievements.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from apps.jobs.models import CareerProfile, JobApplication, JobDescription, Resume


@dataclass(frozen=True)
class CoverLetterDraft:
    subject: str
    greeting: str
    opening: str
    evidence: tuple[str, ...]
    motivation: str
    closing: str
    full_text: str


def _clean(value: str | None, fallback: str = "") -> str:
    return re.sub(r"\s+", " ", (value or "")).strip() or fallback


def _first_name(username: str) -> str:
    token = _clean(username, "there")
    return token.split()[0].capitalize()


def _join_skills(values: Iterable[str], limit: int = 5) -> str:
    values = [str(item).strip() for item in values if str(item).strip()]
    return ", ".join(values[:limit])


class CoverLetterBuilder:
    """Build factual cover letters from user-provided application data."""

    def __init__(
        self,
        profile: CareerProfile | None = None,
        resume: Resume | None = None,
        description: JobDescription | None = None,
        application: JobApplication | None = None,
    ):
        self.profile = profile
        self.resume = resume
        self.description = description
        self.application = application

    def _company(self) -> str:
        return _clean(
            self.description.company if self.description else None,
            self.application.company if self.application else "the company",
        )

    def _role(self) -> str:
        return _clean(
            self.description.title if self.description else None,
            self.application.role if self.application else "the role",
        )

    def _skills(self) -> list[str]:
        profile = set(self.profile.skills if self.profile else [])
        required = set(self.description.required_skills if self.description else [])
        preferred = set(self.description.preferred_skills if self.description else [])
        matched = [skill for skill in sorted(required | preferred) if skill in profile]
        return matched or sorted(profile)

    def build(self, recipient: str = "Hiring Team") -> CoverLetterDraft:
        company = self._company()
        role = self._role()
        headline = _clean(
            self.profile.headline if self.profile else None,
            "software engineering professional",
        )
        summary = _clean(
            self.resume.summary if self.resume else None,
            self.profile.professional_summary if self.profile else "",
        )
        skills = _join_skills(self._skills())
        preferred = _join_skills(
            self.description.required_skills if self.description else []
        )

        subject = f"Application for {role} at {company}"
        greeting = f"Dear {_clean(recipient, 'Hiring Team')},"
        opening = (
            f"I am writing to apply for the {role} position at {company}. "
            f"My background as a {headline} aligns with the responsibilities "
            "described for this opportunity."
        )

        evidence_parts = []
        if summary:
            evidence_parts.append(summary)
        if skills:
            evidence_parts.append(
                f"My relevant skills include {skills}."
            )
        if preferred and preferred != skills:
            evidence_parts.append(
                f"The role's stated requirements include {preferred}, "
                "which I would be prepared to discuss with specific examples."
            )
        if not evidence_parts:
            evidence_parts.append(
                "I would welcome the opportunity to discuss my experience "
                "and how it relates to the position."
            )

        motivation = (
            f"I am interested in {company} because this role provides an "
            "opportunity to apply my experience to meaningful engineering work "
            "while continuing to grow professionally."
        )
        closing = (
            "Thank you for considering my application. I would welcome the "
            "opportunity to discuss the role and my relevant experience."
        )

        paragraphs = [
            subject,
            greeting,
            opening,
            *evidence_parts,
            motivation,
            closing,
            "Sincerely,",
            _first_name(
                self.profile.user.get_full_name()
                if self.profile and self.profile.user.get_full_name()
                else self.profile.user.username
                if self.profile
                else "Applicant"
            ),
        ]
        return CoverLetterDraft(
            subject=subject,
            greeting=greeting,
            opening=opening,
            evidence=tuple(evidence_parts),
            motivation=motivation,
            closing=closing,
            full_text="\n\n".join(paragraphs),
        )

    def sections(self, recipient: str = "Hiring Team") -> dict:
        draft = self.build(recipient)
        return {
            "subject": draft.subject,
            "greeting": draft.greeting,
            "opening": draft.opening,
            "evidence": list(draft.evidence),
            "motivation": draft.motivation,
            "closing": draft.closing,
            "full_text": draft.full_text,
        }


def build_application_cover_letter(
    application: JobApplication,
    profile: CareerProfile | None,
    resume: Resume | None,
    description: JobDescription | None,
) -> CoverLetterDraft:
    return CoverLetterBuilder(
        profile=profile,
        resume=resume,
        description=description,
        application=application,
    ).build()


def validate_cover_letter_source(
    application: JobApplication | None,
    profile: CareerProfile | None,
    resume: Resume | None,
    description: JobDescription | None,
) -> list[str]:
    warnings: list[str] = []
    if not application and not description:
        warnings.append("No application or job description was supplied.")
    if not profile:
        warnings.append("No career profile is available for personalization.")
    if not resume:
        warnings.append("No resume summary is available for evidence.")
    if description and not description.raw_text.strip():
        warnings.append("The job description contains no source text.")
    return warnings
