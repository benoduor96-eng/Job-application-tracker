from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class RoleProfile:
    title: str
    domain: str
    seniority: str
    skills: tuple[str, ...]
    keywords: tuple[str, ...]
    responsibilities: tuple[str, ...]
    interview_focus: tuple[str, ...]

    def matches(self, text: str) -> bool:
        haystack = text.lower()
        return self.title.lower() in haystack or any(k.lower() in haystack for k in self.keywords)

    def skill_overlap(self, skills: Iterable[str]) -> float:
        requested = {s.strip().lower() for s in skills if s.strip()}
        required = {s.lower() for s in self.skills}
        return len(requested & required) / len(required) if required else 0.0

ROLES: list[RoleProfile] = []

ROLES.append(RoleProfile(
    title="Junior Backend Engineering",
    domain="Backend Engineering",
    seniority="junior",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "junior"),
    responsibilities=("Own backend engineering delivery for junior scope 1.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Backend Engineering",
    domain="Backend Engineering",
    seniority="junior",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "junior"),
    responsibilities=("Own backend engineering delivery for junior scope 2.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Backend Engineering",
    domain="Backend Engineering",
    seniority="junior",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "junior"),
    responsibilities=("Own backend engineering delivery for junior scope 3.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Backend Engineering",
    domain="Backend Engineering",
    seniority="junior",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "junior"),
    responsibilities=("Own backend engineering delivery for junior scope 4.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Backend Engineering",
    domain="Backend Engineering",
    seniority="junior",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "junior"),
    responsibilities=("Own backend engineering delivery for junior scope 5.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Backend Engineering",
    domain="Backend Engineering",
    seniority="junior",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "junior"),
    responsibilities=("Own backend engineering delivery for junior scope 6.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Backend Engineering",
    domain="Backend Engineering",
    seniority="mid",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "mid"),
    responsibilities=("Own backend engineering delivery for mid scope 1.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Backend Engineering",
    domain="Backend Engineering",
    seniority="mid",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "mid"),
    responsibilities=("Own backend engineering delivery for mid scope 2.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Backend Engineering",
    domain="Backend Engineering",
    seniority="mid",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "mid"),
    responsibilities=("Own backend engineering delivery for mid scope 3.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Backend Engineering",
    domain="Backend Engineering",
    seniority="mid",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "mid"),
    responsibilities=("Own backend engineering delivery for mid scope 4.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Backend Engineering",
    domain="Backend Engineering",
    seniority="mid",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "mid"),
    responsibilities=("Own backend engineering delivery for mid scope 5.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Backend Engineering",
    domain="Backend Engineering",
    seniority="mid",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "mid"),
    responsibilities=("Own backend engineering delivery for mid scope 6.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Backend Engineering",
    domain="Backend Engineering",
    seniority="senior",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "senior"),
    responsibilities=("Own backend engineering delivery for senior scope 1.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Backend Engineering",
    domain="Backend Engineering",
    seniority="senior",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "senior"),
    responsibilities=("Own backend engineering delivery for senior scope 2.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Backend Engineering",
    domain="Backend Engineering",
    seniority="senior",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "senior"),
    responsibilities=("Own backend engineering delivery for senior scope 3.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Backend Engineering",
    domain="Backend Engineering",
    seniority="senior",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "senior"),
    responsibilities=("Own backend engineering delivery for senior scope 4.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Backend Engineering",
    domain="Backend Engineering",
    seniority="senior",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "senior"),
    responsibilities=("Own backend engineering delivery for senior scope 5.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Backend Engineering",
    domain="Backend Engineering",
    seniority="senior",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "senior"),
    responsibilities=("Own backend engineering delivery for senior scope 6.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Backend Engineering",
    domain="Backend Engineering",
    seniority="lead",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "lead"),
    responsibilities=("Own backend engineering delivery for lead scope 1.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Backend Engineering",
    domain="Backend Engineering",
    seniority="lead",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "lead"),
    responsibilities=("Own backend engineering delivery for lead scope 2.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Backend Engineering",
    domain="Backend Engineering",
    seniority="lead",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "lead"),
    responsibilities=("Own backend engineering delivery for lead scope 3.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Backend Engineering",
    domain="Backend Engineering",
    seniority="lead",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "lead"),
    responsibilities=("Own backend engineering delivery for lead scope 4.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Backend Engineering",
    domain="Backend Engineering",
    seniority="lead",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "lead"),
    responsibilities=("Own backend engineering delivery for lead scope 5.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Backend Engineering",
    domain="Backend Engineering",
    seniority="lead",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "lead"),
    responsibilities=("Own backend engineering delivery for lead scope 6.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Backend Engineering",
    domain="Backend Engineering",
    seniority="staff",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "staff"),
    responsibilities=("Own backend engineering delivery for staff scope 1.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Backend Engineering",
    domain="Backend Engineering",
    seniority="staff",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "staff"),
    responsibilities=("Own backend engineering delivery for staff scope 2.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Backend Engineering",
    domain="Backend Engineering",
    seniority="staff",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "staff"),
    responsibilities=("Own backend engineering delivery for staff scope 3.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Backend Engineering",
    domain="Backend Engineering",
    seniority="staff",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "staff"),
    responsibilities=("Own backend engineering delivery for staff scope 4.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Backend Engineering",
    domain="Backend Engineering",
    seniority="staff",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "staff"),
    responsibilities=("Own backend engineering delivery for staff scope 5.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Backend Engineering",
    domain="Backend Engineering",
    seniority="staff",
    skills=("python", "django", "fastapi", "flask", "postgresql", "redis", "docker", "kubernetes"),
    keywords=("python", "django", "fastapi", "flask", "postgresql", "backend", "staff"),
    responsibilities=("Own backend engineering delivery for staff scope 6.", "Translate requirements into measurable backend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for backend engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Frontend Engineering",
    domain="Frontend Engineering",
    seniority="junior",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "junior"),
    responsibilities=("Own frontend engineering delivery for junior scope 1.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Frontend Engineering",
    domain="Frontend Engineering",
    seniority="junior",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "junior"),
    responsibilities=("Own frontend engineering delivery for junior scope 2.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Frontend Engineering",
    domain="Frontend Engineering",
    seniority="junior",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "junior"),
    responsibilities=("Own frontend engineering delivery for junior scope 3.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Frontend Engineering",
    domain="Frontend Engineering",
    seniority="junior",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "junior"),
    responsibilities=("Own frontend engineering delivery for junior scope 4.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Frontend Engineering",
    domain="Frontend Engineering",
    seniority="junior",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "junior"),
    responsibilities=("Own frontend engineering delivery for junior scope 5.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Frontend Engineering",
    domain="Frontend Engineering",
    seniority="junior",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "junior"),
    responsibilities=("Own frontend engineering delivery for junior scope 6.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Frontend Engineering",
    domain="Frontend Engineering",
    seniority="mid",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "mid"),
    responsibilities=("Own frontend engineering delivery for mid scope 1.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Frontend Engineering",
    domain="Frontend Engineering",
    seniority="mid",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "mid"),
    responsibilities=("Own frontend engineering delivery for mid scope 2.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Frontend Engineering",
    domain="Frontend Engineering",
    seniority="mid",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "mid"),
    responsibilities=("Own frontend engineering delivery for mid scope 3.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Frontend Engineering",
    domain="Frontend Engineering",
    seniority="mid",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "mid"),
    responsibilities=("Own frontend engineering delivery for mid scope 4.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Frontend Engineering",
    domain="Frontend Engineering",
    seniority="mid",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "mid"),
    responsibilities=("Own frontend engineering delivery for mid scope 5.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Frontend Engineering",
    domain="Frontend Engineering",
    seniority="mid",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "mid"),
    responsibilities=("Own frontend engineering delivery for mid scope 6.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Frontend Engineering",
    domain="Frontend Engineering",
    seniority="senior",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "senior"),
    responsibilities=("Own frontend engineering delivery for senior scope 1.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Frontend Engineering",
    domain="Frontend Engineering",
    seniority="senior",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "senior"),
    responsibilities=("Own frontend engineering delivery for senior scope 2.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Frontend Engineering",
    domain="Frontend Engineering",
    seniority="senior",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "senior"),
    responsibilities=("Own frontend engineering delivery for senior scope 3.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Frontend Engineering",
    domain="Frontend Engineering",
    seniority="senior",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "senior"),
    responsibilities=("Own frontend engineering delivery for senior scope 4.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Frontend Engineering",
    domain="Frontend Engineering",
    seniority="senior",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "senior"),
    responsibilities=("Own frontend engineering delivery for senior scope 5.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Frontend Engineering",
    domain="Frontend Engineering",
    seniority="senior",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "senior"),
    responsibilities=("Own frontend engineering delivery for senior scope 6.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Frontend Engineering",
    domain="Frontend Engineering",
    seniority="lead",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "lead"),
    responsibilities=("Own frontend engineering delivery for lead scope 1.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Frontend Engineering",
    domain="Frontend Engineering",
    seniority="lead",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "lead"),
    responsibilities=("Own frontend engineering delivery for lead scope 2.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Frontend Engineering",
    domain="Frontend Engineering",
    seniority="lead",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "lead"),
    responsibilities=("Own frontend engineering delivery for lead scope 3.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Frontend Engineering",
    domain="Frontend Engineering",
    seniority="lead",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "lead"),
    responsibilities=("Own frontend engineering delivery for lead scope 4.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Frontend Engineering",
    domain="Frontend Engineering",
    seniority="lead",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "lead"),
    responsibilities=("Own frontend engineering delivery for lead scope 5.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Frontend Engineering",
    domain="Frontend Engineering",
    seniority="lead",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "lead"),
    responsibilities=("Own frontend engineering delivery for lead scope 6.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Frontend Engineering",
    domain="Frontend Engineering",
    seniority="staff",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "staff"),
    responsibilities=("Own frontend engineering delivery for staff scope 1.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Frontend Engineering",
    domain="Frontend Engineering",
    seniority="staff",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "staff"),
    responsibilities=("Own frontend engineering delivery for staff scope 2.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Frontend Engineering",
    domain="Frontend Engineering",
    seniority="staff",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "staff"),
    responsibilities=("Own frontend engineering delivery for staff scope 3.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Frontend Engineering",
    domain="Frontend Engineering",
    seniority="staff",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "staff"),
    responsibilities=("Own frontend engineering delivery for staff scope 4.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Frontend Engineering",
    domain="Frontend Engineering",
    seniority="staff",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "staff"),
    responsibilities=("Own frontend engineering delivery for staff scope 5.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Frontend Engineering",
    domain="Frontend Engineering",
    seniority="staff",
    skills=("react", "javascript", "typescript", "vite", "css", "html", "accessibility"),
    keywords=("react", "javascript", "typescript", "vite", "css", "frontend", "staff"),
    responsibilities=("Own frontend engineering delivery for staff scope 6.", "Translate requirements into measurable frontend engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for frontend engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="junior",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "junior"),
    responsibilities=("Own full stack engineering delivery for junior scope 1.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="junior",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "junior"),
    responsibilities=("Own full stack engineering delivery for junior scope 2.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="junior",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "junior"),
    responsibilities=("Own full stack engineering delivery for junior scope 3.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="junior",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "junior"),
    responsibilities=("Own full stack engineering delivery for junior scope 4.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="junior",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "junior"),
    responsibilities=("Own full stack engineering delivery for junior scope 5.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="junior",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "junior"),
    responsibilities=("Own full stack engineering delivery for junior scope 6.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="mid",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "mid"),
    responsibilities=("Own full stack engineering delivery for mid scope 1.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="mid",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "mid"),
    responsibilities=("Own full stack engineering delivery for mid scope 2.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="mid",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "mid"),
    responsibilities=("Own full stack engineering delivery for mid scope 3.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="mid",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "mid"),
    responsibilities=("Own full stack engineering delivery for mid scope 4.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="mid",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "mid"),
    responsibilities=("Own full stack engineering delivery for mid scope 5.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="mid",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "mid"),
    responsibilities=("Own full stack engineering delivery for mid scope 6.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="senior",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "senior"),
    responsibilities=("Own full stack engineering delivery for senior scope 1.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="senior",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "senior"),
    responsibilities=("Own full stack engineering delivery for senior scope 2.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="senior",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "senior"),
    responsibilities=("Own full stack engineering delivery for senior scope 3.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="senior",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "senior"),
    responsibilities=("Own full stack engineering delivery for senior scope 4.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="senior",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "senior"),
    responsibilities=("Own full stack engineering delivery for senior scope 5.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="senior",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "senior"),
    responsibilities=("Own full stack engineering delivery for senior scope 6.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="lead",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "lead"),
    responsibilities=("Own full stack engineering delivery for lead scope 1.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="lead",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "lead"),
    responsibilities=("Own full stack engineering delivery for lead scope 2.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="lead",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "lead"),
    responsibilities=("Own full stack engineering delivery for lead scope 3.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="lead",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "lead"),
    responsibilities=("Own full stack engineering delivery for lead scope 4.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="lead",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "lead"),
    responsibilities=("Own full stack engineering delivery for lead scope 5.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="lead",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "lead"),
    responsibilities=("Own full stack engineering delivery for lead scope 6.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="staff",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "staff"),
    responsibilities=("Own full stack engineering delivery for staff scope 1.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="staff",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "staff"),
    responsibilities=("Own full stack engineering delivery for staff scope 2.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="staff",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "staff"),
    responsibilities=("Own full stack engineering delivery for staff scope 3.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="staff",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "staff"),
    responsibilities=("Own full stack engineering delivery for staff scope 4.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="staff",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "staff"),
    responsibilities=("Own full stack engineering delivery for staff scope 5.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Full Stack Engineering",
    domain="Full Stack Engineering",
    seniority="staff",
    skills=("python", "django", "react", "javascript", "postgresql", "docker"),
    keywords=("python", "django", "react", "javascript", "postgresql", "full", "staff"),
    responsibilities=("Own full stack engineering delivery for staff scope 6.", "Translate requirements into measurable full stack engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for full stack engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Data Engineering",
    domain="Data Engineering",
    seniority="junior",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "junior"),
    responsibilities=("Own data engineering delivery for junior scope 1.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Data Engineering",
    domain="Data Engineering",
    seniority="junior",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "junior"),
    responsibilities=("Own data engineering delivery for junior scope 2.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Data Engineering",
    domain="Data Engineering",
    seniority="junior",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "junior"),
    responsibilities=("Own data engineering delivery for junior scope 3.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Data Engineering",
    domain="Data Engineering",
    seniority="junior",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "junior"),
    responsibilities=("Own data engineering delivery for junior scope 4.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Data Engineering",
    domain="Data Engineering",
    seniority="junior",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "junior"),
    responsibilities=("Own data engineering delivery for junior scope 5.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Data Engineering",
    domain="Data Engineering",
    seniority="junior",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "junior"),
    responsibilities=("Own data engineering delivery for junior scope 6.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Data Engineering",
    domain="Data Engineering",
    seniority="mid",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "mid"),
    responsibilities=("Own data engineering delivery for mid scope 1.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Data Engineering",
    domain="Data Engineering",
    seniority="mid",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "mid"),
    responsibilities=("Own data engineering delivery for mid scope 2.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Data Engineering",
    domain="Data Engineering",
    seniority="mid",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "mid"),
    responsibilities=("Own data engineering delivery for mid scope 3.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Data Engineering",
    domain="Data Engineering",
    seniority="mid",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "mid"),
    responsibilities=("Own data engineering delivery for mid scope 4.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Data Engineering",
    domain="Data Engineering",
    seniority="mid",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "mid"),
    responsibilities=("Own data engineering delivery for mid scope 5.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Data Engineering",
    domain="Data Engineering",
    seniority="mid",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "mid"),
    responsibilities=("Own data engineering delivery for mid scope 6.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Data Engineering",
    domain="Data Engineering",
    seniority="senior",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "senior"),
    responsibilities=("Own data engineering delivery for senior scope 1.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Data Engineering",
    domain="Data Engineering",
    seniority="senior",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "senior"),
    responsibilities=("Own data engineering delivery for senior scope 2.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Data Engineering",
    domain="Data Engineering",
    seniority="senior",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "senior"),
    responsibilities=("Own data engineering delivery for senior scope 3.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Data Engineering",
    domain="Data Engineering",
    seniority="senior",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "senior"),
    responsibilities=("Own data engineering delivery for senior scope 4.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Data Engineering",
    domain="Data Engineering",
    seniority="senior",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "senior"),
    responsibilities=("Own data engineering delivery for senior scope 5.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Data Engineering",
    domain="Data Engineering",
    seniority="senior",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "senior"),
    responsibilities=("Own data engineering delivery for senior scope 6.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Data Engineering",
    domain="Data Engineering",
    seniority="lead",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "lead"),
    responsibilities=("Own data engineering delivery for lead scope 1.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Data Engineering",
    domain="Data Engineering",
    seniority="lead",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "lead"),
    responsibilities=("Own data engineering delivery for lead scope 2.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Data Engineering",
    domain="Data Engineering",
    seniority="lead",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "lead"),
    responsibilities=("Own data engineering delivery for lead scope 3.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Data Engineering",
    domain="Data Engineering",
    seniority="lead",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "lead"),
    responsibilities=("Own data engineering delivery for lead scope 4.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Data Engineering",
    domain="Data Engineering",
    seniority="lead",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "lead"),
    responsibilities=("Own data engineering delivery for lead scope 5.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Data Engineering",
    domain="Data Engineering",
    seniority="lead",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "lead"),
    responsibilities=("Own data engineering delivery for lead scope 6.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Data Engineering",
    domain="Data Engineering",
    seniority="staff",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "staff"),
    responsibilities=("Own data engineering delivery for staff scope 1.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Data Engineering",
    domain="Data Engineering",
    seniority="staff",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "staff"),
    responsibilities=("Own data engineering delivery for staff scope 2.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Data Engineering",
    domain="Data Engineering",
    seniority="staff",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "staff"),
    responsibilities=("Own data engineering delivery for staff scope 3.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Data Engineering",
    domain="Data Engineering",
    seniority="staff",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "staff"),
    responsibilities=("Own data engineering delivery for staff scope 4.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Data Engineering",
    domain="Data Engineering",
    seniority="staff",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "staff"),
    responsibilities=("Own data engineering delivery for staff scope 5.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Data Engineering",
    domain="Data Engineering",
    seniority="staff",
    skills=("python", "sql", "spark", "airflow", "dbt", "snowflake", "kafka"),
    keywords=("python", "sql", "spark", "airflow", "dbt", "data", "staff"),
    responsibilities=("Own data engineering delivery for staff scope 6.", "Translate requirements into measurable data engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Machine Learning",
    domain="Machine Learning",
    seniority="junior",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "junior"),
    responsibilities=("Own machine learning delivery for junior scope 1.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Machine Learning",
    domain="Machine Learning",
    seniority="junior",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "junior"),
    responsibilities=("Own machine learning delivery for junior scope 2.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Machine Learning",
    domain="Machine Learning",
    seniority="junior",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "junior"),
    responsibilities=("Own machine learning delivery for junior scope 3.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Machine Learning",
    domain="Machine Learning",
    seniority="junior",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "junior"),
    responsibilities=("Own machine learning delivery for junior scope 4.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Machine Learning",
    domain="Machine Learning",
    seniority="junior",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "junior"),
    responsibilities=("Own machine learning delivery for junior scope 5.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Machine Learning",
    domain="Machine Learning",
    seniority="junior",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "junior"),
    responsibilities=("Own machine learning delivery for junior scope 6.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Machine Learning",
    domain="Machine Learning",
    seniority="mid",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "mid"),
    responsibilities=("Own machine learning delivery for mid scope 1.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Machine Learning",
    domain="Machine Learning",
    seniority="mid",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "mid"),
    responsibilities=("Own machine learning delivery for mid scope 2.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Machine Learning",
    domain="Machine Learning",
    seniority="mid",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "mid"),
    responsibilities=("Own machine learning delivery for mid scope 3.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Machine Learning",
    domain="Machine Learning",
    seniority="mid",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "mid"),
    responsibilities=("Own machine learning delivery for mid scope 4.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Machine Learning",
    domain="Machine Learning",
    seniority="mid",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "mid"),
    responsibilities=("Own machine learning delivery for mid scope 5.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Machine Learning",
    domain="Machine Learning",
    seniority="mid",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "mid"),
    responsibilities=("Own machine learning delivery for mid scope 6.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Machine Learning",
    domain="Machine Learning",
    seniority="senior",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "senior"),
    responsibilities=("Own machine learning delivery for senior scope 1.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Machine Learning",
    domain="Machine Learning",
    seniority="senior",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "senior"),
    responsibilities=("Own machine learning delivery for senior scope 2.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Machine Learning",
    domain="Machine Learning",
    seniority="senior",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "senior"),
    responsibilities=("Own machine learning delivery for senior scope 3.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Machine Learning",
    domain="Machine Learning",
    seniority="senior",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "senior"),
    responsibilities=("Own machine learning delivery for senior scope 4.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Machine Learning",
    domain="Machine Learning",
    seniority="senior",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "senior"),
    responsibilities=("Own machine learning delivery for senior scope 5.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Machine Learning",
    domain="Machine Learning",
    seniority="senior",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "senior"),
    responsibilities=("Own machine learning delivery for senior scope 6.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Machine Learning",
    domain="Machine Learning",
    seniority="lead",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "lead"),
    responsibilities=("Own machine learning delivery for lead scope 1.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Machine Learning",
    domain="Machine Learning",
    seniority="lead",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "lead"),
    responsibilities=("Own machine learning delivery for lead scope 2.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Machine Learning",
    domain="Machine Learning",
    seniority="lead",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "lead"),
    responsibilities=("Own machine learning delivery for lead scope 3.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Machine Learning",
    domain="Machine Learning",
    seniority="lead",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "lead"),
    responsibilities=("Own machine learning delivery for lead scope 4.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Machine Learning",
    domain="Machine Learning",
    seniority="lead",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "lead"),
    responsibilities=("Own machine learning delivery for lead scope 5.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Machine Learning",
    domain="Machine Learning",
    seniority="lead",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "lead"),
    responsibilities=("Own machine learning delivery for lead scope 6.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Machine Learning",
    domain="Machine Learning",
    seniority="staff",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "staff"),
    responsibilities=("Own machine learning delivery for staff scope 1.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Machine Learning",
    domain="Machine Learning",
    seniority="staff",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "staff"),
    responsibilities=("Own machine learning delivery for staff scope 2.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Machine Learning",
    domain="Machine Learning",
    seniority="staff",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "staff"),
    responsibilities=("Own machine learning delivery for staff scope 3.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Machine Learning",
    domain="Machine Learning",
    seniority="staff",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "staff"),
    responsibilities=("Own machine learning delivery for staff scope 4.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Machine Learning",
    domain="Machine Learning",
    seniority="staff",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "staff"),
    responsibilities=("Own machine learning delivery for staff scope 5.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Machine Learning",
    domain="Machine Learning",
    seniority="staff",
    skills=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "mlflow"),
    keywords=("python", "pytorch", "tensorflow", "scikit-learn", "pandas", "machine", "staff"),
    responsibilities=("Own machine learning delivery for staff scope 6.", "Translate requirements into measurable machine learning outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for machine learning", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior DevOps",
    domain="DevOps",
    seniority="junior",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "junior"),
    responsibilities=("Own devops delivery for junior scope 1.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior DevOps",
    domain="DevOps",
    seniority="junior",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "junior"),
    responsibilities=("Own devops delivery for junior scope 2.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior DevOps",
    domain="DevOps",
    seniority="junior",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "junior"),
    responsibilities=("Own devops delivery for junior scope 3.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior DevOps",
    domain="DevOps",
    seniority="junior",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "junior"),
    responsibilities=("Own devops delivery for junior scope 4.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior DevOps",
    domain="DevOps",
    seniority="junior",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "junior"),
    responsibilities=("Own devops delivery for junior scope 5.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior DevOps",
    domain="DevOps",
    seniority="junior",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "junior"),
    responsibilities=("Own devops delivery for junior scope 6.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid DevOps",
    domain="DevOps",
    seniority="mid",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "mid"),
    responsibilities=("Own devops delivery for mid scope 1.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid DevOps",
    domain="DevOps",
    seniority="mid",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "mid"),
    responsibilities=("Own devops delivery for mid scope 2.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid DevOps",
    domain="DevOps",
    seniority="mid",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "mid"),
    responsibilities=("Own devops delivery for mid scope 3.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid DevOps",
    domain="DevOps",
    seniority="mid",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "mid"),
    responsibilities=("Own devops delivery for mid scope 4.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid DevOps",
    domain="DevOps",
    seniority="mid",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "mid"),
    responsibilities=("Own devops delivery for mid scope 5.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid DevOps",
    domain="DevOps",
    seniority="mid",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "mid"),
    responsibilities=("Own devops delivery for mid scope 6.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior DevOps",
    domain="DevOps",
    seniority="senior",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "senior"),
    responsibilities=("Own devops delivery for senior scope 1.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior DevOps",
    domain="DevOps",
    seniority="senior",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "senior"),
    responsibilities=("Own devops delivery for senior scope 2.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior DevOps",
    domain="DevOps",
    seniority="senior",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "senior"),
    responsibilities=("Own devops delivery for senior scope 3.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior DevOps",
    domain="DevOps",
    seniority="senior",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "senior"),
    responsibilities=("Own devops delivery for senior scope 4.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior DevOps",
    domain="DevOps",
    seniority="senior",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "senior"),
    responsibilities=("Own devops delivery for senior scope 5.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior DevOps",
    domain="DevOps",
    seniority="senior",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "senior"),
    responsibilities=("Own devops delivery for senior scope 6.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead DevOps",
    domain="DevOps",
    seniority="lead",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "lead"),
    responsibilities=("Own devops delivery for lead scope 1.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead DevOps",
    domain="DevOps",
    seniority="lead",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "lead"),
    responsibilities=("Own devops delivery for lead scope 2.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead DevOps",
    domain="DevOps",
    seniority="lead",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "lead"),
    responsibilities=("Own devops delivery for lead scope 3.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead DevOps",
    domain="DevOps",
    seniority="lead",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "lead"),
    responsibilities=("Own devops delivery for lead scope 4.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead DevOps",
    domain="DevOps",
    seniority="lead",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "lead"),
    responsibilities=("Own devops delivery for lead scope 5.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead DevOps",
    domain="DevOps",
    seniority="lead",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "lead"),
    responsibilities=("Own devops delivery for lead scope 6.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff DevOps",
    domain="DevOps",
    seniority="staff",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "staff"),
    responsibilities=("Own devops delivery for staff scope 1.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff DevOps",
    domain="DevOps",
    seniority="staff",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "staff"),
    responsibilities=("Own devops delivery for staff scope 2.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff DevOps",
    domain="DevOps",
    seniority="staff",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "staff"),
    responsibilities=("Own devops delivery for staff scope 3.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff DevOps",
    domain="DevOps",
    seniority="staff",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "staff"),
    responsibilities=("Own devops delivery for staff scope 4.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff DevOps",
    domain="DevOps",
    seniority="staff",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "staff"),
    responsibilities=("Own devops delivery for staff scope 5.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff DevOps",
    domain="DevOps",
    seniority="staff",
    skills=("linux", "docker", "kubernetes", "terraform", "aws", "github-actions", "observability"),
    keywords=("linux", "docker", "kubernetes", "terraform", "aws", "devops", "staff"),
    responsibilities=("Own devops delivery for staff scope 6.", "Translate requirements into measurable devops outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for devops", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior QA Engineering",
    domain="QA Engineering",
    seniority="junior",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "junior"),
    responsibilities=("Own qa engineering delivery for junior scope 1.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior QA Engineering",
    domain="QA Engineering",
    seniority="junior",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "junior"),
    responsibilities=("Own qa engineering delivery for junior scope 2.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior QA Engineering",
    domain="QA Engineering",
    seniority="junior",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "junior"),
    responsibilities=("Own qa engineering delivery for junior scope 3.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior QA Engineering",
    domain="QA Engineering",
    seniority="junior",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "junior"),
    responsibilities=("Own qa engineering delivery for junior scope 4.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior QA Engineering",
    domain="QA Engineering",
    seniority="junior",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "junior"),
    responsibilities=("Own qa engineering delivery for junior scope 5.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior QA Engineering",
    domain="QA Engineering",
    seniority="junior",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "junior"),
    responsibilities=("Own qa engineering delivery for junior scope 6.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid QA Engineering",
    domain="QA Engineering",
    seniority="mid",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "mid"),
    responsibilities=("Own qa engineering delivery for mid scope 1.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid QA Engineering",
    domain="QA Engineering",
    seniority="mid",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "mid"),
    responsibilities=("Own qa engineering delivery for mid scope 2.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid QA Engineering",
    domain="QA Engineering",
    seniority="mid",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "mid"),
    responsibilities=("Own qa engineering delivery for mid scope 3.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid QA Engineering",
    domain="QA Engineering",
    seniority="mid",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "mid"),
    responsibilities=("Own qa engineering delivery for mid scope 4.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid QA Engineering",
    domain="QA Engineering",
    seniority="mid",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "mid"),
    responsibilities=("Own qa engineering delivery for mid scope 5.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid QA Engineering",
    domain="QA Engineering",
    seniority="mid",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "mid"),
    responsibilities=("Own qa engineering delivery for mid scope 6.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior QA Engineering",
    domain="QA Engineering",
    seniority="senior",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "senior"),
    responsibilities=("Own qa engineering delivery for senior scope 1.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior QA Engineering",
    domain="QA Engineering",
    seniority="senior",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "senior"),
    responsibilities=("Own qa engineering delivery for senior scope 2.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior QA Engineering",
    domain="QA Engineering",
    seniority="senior",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "senior"),
    responsibilities=("Own qa engineering delivery for senior scope 3.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior QA Engineering",
    domain="QA Engineering",
    seniority="senior",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "senior"),
    responsibilities=("Own qa engineering delivery for senior scope 4.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior QA Engineering",
    domain="QA Engineering",
    seniority="senior",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "senior"),
    responsibilities=("Own qa engineering delivery for senior scope 5.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior QA Engineering",
    domain="QA Engineering",
    seniority="senior",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "senior"),
    responsibilities=("Own qa engineering delivery for senior scope 6.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead QA Engineering",
    domain="QA Engineering",
    seniority="lead",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "lead"),
    responsibilities=("Own qa engineering delivery for lead scope 1.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead QA Engineering",
    domain="QA Engineering",
    seniority="lead",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "lead"),
    responsibilities=("Own qa engineering delivery for lead scope 2.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead QA Engineering",
    domain="QA Engineering",
    seniority="lead",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "lead"),
    responsibilities=("Own qa engineering delivery for lead scope 3.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead QA Engineering",
    domain="QA Engineering",
    seniority="lead",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "lead"),
    responsibilities=("Own qa engineering delivery for lead scope 4.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead QA Engineering",
    domain="QA Engineering",
    seniority="lead",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "lead"),
    responsibilities=("Own qa engineering delivery for lead scope 5.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead QA Engineering",
    domain="QA Engineering",
    seniority="lead",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "lead"),
    responsibilities=("Own qa engineering delivery for lead scope 6.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff QA Engineering",
    domain="QA Engineering",
    seniority="staff",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "staff"),
    responsibilities=("Own qa engineering delivery for staff scope 1.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff QA Engineering",
    domain="QA Engineering",
    seniority="staff",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "staff"),
    responsibilities=("Own qa engineering delivery for staff scope 2.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff QA Engineering",
    domain="QA Engineering",
    seniority="staff",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "staff"),
    responsibilities=("Own qa engineering delivery for staff scope 3.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff QA Engineering",
    domain="QA Engineering",
    seniority="staff",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "staff"),
    responsibilities=("Own qa engineering delivery for staff scope 4.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff QA Engineering",
    domain="QA Engineering",
    seniority="staff",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "staff"),
    responsibilities=("Own qa engineering delivery for staff scope 5.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff QA Engineering",
    domain="QA Engineering",
    seniority="staff",
    skills=("pytest", "selenium", "playwright", "cypress", "api-testing", "test-automation"),
    keywords=("pytest", "selenium", "playwright", "cypress", "api-testing", "qa", "staff"),
    responsibilities=("Own qa engineering delivery for staff scope 6.", "Translate requirements into measurable qa engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for qa engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Security Engineering",
    domain="Security Engineering",
    seniority="junior",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "junior"),
    responsibilities=("Own security engineering delivery for junior scope 1.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Security Engineering",
    domain="Security Engineering",
    seniority="junior",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "junior"),
    responsibilities=("Own security engineering delivery for junior scope 2.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Security Engineering",
    domain="Security Engineering",
    seniority="junior",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "junior"),
    responsibilities=("Own security engineering delivery for junior scope 3.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Security Engineering",
    domain="Security Engineering",
    seniority="junior",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "junior"),
    responsibilities=("Own security engineering delivery for junior scope 4.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Security Engineering",
    domain="Security Engineering",
    seniority="junior",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "junior"),
    responsibilities=("Own security engineering delivery for junior scope 5.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Security Engineering",
    domain="Security Engineering",
    seniority="junior",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "junior"),
    responsibilities=("Own security engineering delivery for junior scope 6.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Security Engineering",
    domain="Security Engineering",
    seniority="mid",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "mid"),
    responsibilities=("Own security engineering delivery for mid scope 1.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Security Engineering",
    domain="Security Engineering",
    seniority="mid",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "mid"),
    responsibilities=("Own security engineering delivery for mid scope 2.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Security Engineering",
    domain="Security Engineering",
    seniority="mid",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "mid"),
    responsibilities=("Own security engineering delivery for mid scope 3.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Security Engineering",
    domain="Security Engineering",
    seniority="mid",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "mid"),
    responsibilities=("Own security engineering delivery for mid scope 4.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Security Engineering",
    domain="Security Engineering",
    seniority="mid",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "mid"),
    responsibilities=("Own security engineering delivery for mid scope 5.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Security Engineering",
    domain="Security Engineering",
    seniority="mid",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "mid"),
    responsibilities=("Own security engineering delivery for mid scope 6.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Security Engineering",
    domain="Security Engineering",
    seniority="senior",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "senior"),
    responsibilities=("Own security engineering delivery for senior scope 1.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Security Engineering",
    domain="Security Engineering",
    seniority="senior",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "senior"),
    responsibilities=("Own security engineering delivery for senior scope 2.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Security Engineering",
    domain="Security Engineering",
    seniority="senior",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "senior"),
    responsibilities=("Own security engineering delivery for senior scope 3.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Security Engineering",
    domain="Security Engineering",
    seniority="senior",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "senior"),
    responsibilities=("Own security engineering delivery for senior scope 4.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Security Engineering",
    domain="Security Engineering",
    seniority="senior",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "senior"),
    responsibilities=("Own security engineering delivery for senior scope 5.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Security Engineering",
    domain="Security Engineering",
    seniority="senior",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "senior"),
    responsibilities=("Own security engineering delivery for senior scope 6.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Security Engineering",
    domain="Security Engineering",
    seniority="lead",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "lead"),
    responsibilities=("Own security engineering delivery for lead scope 1.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Security Engineering",
    domain="Security Engineering",
    seniority="lead",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "lead"),
    responsibilities=("Own security engineering delivery for lead scope 2.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Security Engineering",
    domain="Security Engineering",
    seniority="lead",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "lead"),
    responsibilities=("Own security engineering delivery for lead scope 3.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Security Engineering",
    domain="Security Engineering",
    seniority="lead",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "lead"),
    responsibilities=("Own security engineering delivery for lead scope 4.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Security Engineering",
    domain="Security Engineering",
    seniority="lead",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "lead"),
    responsibilities=("Own security engineering delivery for lead scope 5.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Security Engineering",
    domain="Security Engineering",
    seniority="lead",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "lead"),
    responsibilities=("Own security engineering delivery for lead scope 6.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Security Engineering",
    domain="Security Engineering",
    seniority="staff",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "staff"),
    responsibilities=("Own security engineering delivery for staff scope 1.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Security Engineering",
    domain="Security Engineering",
    seniority="staff",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "staff"),
    responsibilities=("Own security engineering delivery for staff scope 2.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Security Engineering",
    domain="Security Engineering",
    seniority="staff",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "staff"),
    responsibilities=("Own security engineering delivery for staff scope 3.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Security Engineering",
    domain="Security Engineering",
    seniority="staff",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "staff"),
    responsibilities=("Own security engineering delivery for staff scope 4.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Security Engineering",
    domain="Security Engineering",
    seniority="staff",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "staff"),
    responsibilities=("Own security engineering delivery for staff scope 5.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Security Engineering",
    domain="Security Engineering",
    seniority="staff",
    skills=("python", "linux", "oauth", "jwt", "threat-modeling", "application-security"),
    keywords=("python", "linux", "oauth", "jwt", "threat-modeling", "security", "staff"),
    responsibilities=("Own security engineering delivery for staff scope 6.", "Translate requirements into measurable security engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for security engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Product Management",
    domain="Product Management",
    seniority="junior",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "junior"),
    responsibilities=("Own product management delivery for junior scope 1.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Product Management",
    domain="Product Management",
    seniority="junior",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "junior"),
    responsibilities=("Own product management delivery for junior scope 2.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Product Management",
    domain="Product Management",
    seniority="junior",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "junior"),
    responsibilities=("Own product management delivery for junior scope 3.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Product Management",
    domain="Product Management",
    seniority="junior",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "junior"),
    responsibilities=("Own product management delivery for junior scope 4.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Product Management",
    domain="Product Management",
    seniority="junior",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "junior"),
    responsibilities=("Own product management delivery for junior scope 5.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Product Management",
    domain="Product Management",
    seniority="junior",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "junior"),
    responsibilities=("Own product management delivery for junior scope 6.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Product Management",
    domain="Product Management",
    seniority="mid",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "mid"),
    responsibilities=("Own product management delivery for mid scope 1.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Product Management",
    domain="Product Management",
    seniority="mid",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "mid"),
    responsibilities=("Own product management delivery for mid scope 2.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Product Management",
    domain="Product Management",
    seniority="mid",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "mid"),
    responsibilities=("Own product management delivery for mid scope 3.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Product Management",
    domain="Product Management",
    seniority="mid",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "mid"),
    responsibilities=("Own product management delivery for mid scope 4.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Product Management",
    domain="Product Management",
    seniority="mid",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "mid"),
    responsibilities=("Own product management delivery for mid scope 5.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Product Management",
    domain="Product Management",
    seniority="mid",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "mid"),
    responsibilities=("Own product management delivery for mid scope 6.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Product Management",
    domain="Product Management",
    seniority="senior",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "senior"),
    responsibilities=("Own product management delivery for senior scope 1.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Product Management",
    domain="Product Management",
    seniority="senior",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "senior"),
    responsibilities=("Own product management delivery for senior scope 2.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Product Management",
    domain="Product Management",
    seniority="senior",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "senior"),
    responsibilities=("Own product management delivery for senior scope 3.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Product Management",
    domain="Product Management",
    seniority="senior",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "senior"),
    responsibilities=("Own product management delivery for senior scope 4.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Product Management",
    domain="Product Management",
    seniority="senior",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "senior"),
    responsibilities=("Own product management delivery for senior scope 5.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Product Management",
    domain="Product Management",
    seniority="senior",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "senior"),
    responsibilities=("Own product management delivery for senior scope 6.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Product Management",
    domain="Product Management",
    seniority="lead",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "lead"),
    responsibilities=("Own product management delivery for lead scope 1.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Product Management",
    domain="Product Management",
    seniority="lead",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "lead"),
    responsibilities=("Own product management delivery for lead scope 2.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Product Management",
    domain="Product Management",
    seniority="lead",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "lead"),
    responsibilities=("Own product management delivery for lead scope 3.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Product Management",
    domain="Product Management",
    seniority="lead",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "lead"),
    responsibilities=("Own product management delivery for lead scope 4.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Product Management",
    domain="Product Management",
    seniority="lead",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "lead"),
    responsibilities=("Own product management delivery for lead scope 5.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Product Management",
    domain="Product Management",
    seniority="lead",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "lead"),
    responsibilities=("Own product management delivery for lead scope 6.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Product Management",
    domain="Product Management",
    seniority="staff",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "staff"),
    responsibilities=("Own product management delivery for staff scope 1.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Product Management",
    domain="Product Management",
    seniority="staff",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "staff"),
    responsibilities=("Own product management delivery for staff scope 2.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Product Management",
    domain="Product Management",
    seniority="staff",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "staff"),
    responsibilities=("Own product management delivery for staff scope 3.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Product Management",
    domain="Product Management",
    seniority="staff",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "staff"),
    responsibilities=("Own product management delivery for staff scope 4.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Product Management",
    domain="Product Management",
    seniority="staff",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "staff"),
    responsibilities=("Own product management delivery for staff scope 5.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Product Management",
    domain="Product Management",
    seniority="staff",
    skills=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management"),
    keywords=("roadmaps", "discovery", "analytics", "prioritization", "stakeholder-management", "product", "staff"),
    responsibilities=("Own product management delivery for staff scope 6.", "Translate requirements into measurable product management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for product management", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Technical Writing",
    domain="Technical Writing",
    seniority="junior",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "junior"),
    responsibilities=("Own technical writing delivery for junior scope 1.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Technical Writing",
    domain="Technical Writing",
    seniority="junior",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "junior"),
    responsibilities=("Own technical writing delivery for junior scope 2.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Technical Writing",
    domain="Technical Writing",
    seniority="junior",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "junior"),
    responsibilities=("Own technical writing delivery for junior scope 3.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Technical Writing",
    domain="Technical Writing",
    seniority="junior",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "junior"),
    responsibilities=("Own technical writing delivery for junior scope 4.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Technical Writing",
    domain="Technical Writing",
    seniority="junior",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "junior"),
    responsibilities=("Own technical writing delivery for junior scope 5.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Technical Writing",
    domain="Technical Writing",
    seniority="junior",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "junior"),
    responsibilities=("Own technical writing delivery for junior scope 6.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Technical Writing",
    domain="Technical Writing",
    seniority="mid",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "mid"),
    responsibilities=("Own technical writing delivery for mid scope 1.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Technical Writing",
    domain="Technical Writing",
    seniority="mid",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "mid"),
    responsibilities=("Own technical writing delivery for mid scope 2.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Technical Writing",
    domain="Technical Writing",
    seniority="mid",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "mid"),
    responsibilities=("Own technical writing delivery for mid scope 3.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Technical Writing",
    domain="Technical Writing",
    seniority="mid",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "mid"),
    responsibilities=("Own technical writing delivery for mid scope 4.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Technical Writing",
    domain="Technical Writing",
    seniority="mid",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "mid"),
    responsibilities=("Own technical writing delivery for mid scope 5.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Technical Writing",
    domain="Technical Writing",
    seniority="mid",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "mid"),
    responsibilities=("Own technical writing delivery for mid scope 6.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Technical Writing",
    domain="Technical Writing",
    seniority="senior",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "senior"),
    responsibilities=("Own technical writing delivery for senior scope 1.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Technical Writing",
    domain="Technical Writing",
    seniority="senior",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "senior"),
    responsibilities=("Own technical writing delivery for senior scope 2.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Technical Writing",
    domain="Technical Writing",
    seniority="senior",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "senior"),
    responsibilities=("Own technical writing delivery for senior scope 3.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Technical Writing",
    domain="Technical Writing",
    seniority="senior",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "senior"),
    responsibilities=("Own technical writing delivery for senior scope 4.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Technical Writing",
    domain="Technical Writing",
    seniority="senior",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "senior"),
    responsibilities=("Own technical writing delivery for senior scope 5.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Technical Writing",
    domain="Technical Writing",
    seniority="senior",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "senior"),
    responsibilities=("Own technical writing delivery for senior scope 6.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Technical Writing",
    domain="Technical Writing",
    seniority="lead",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "lead"),
    responsibilities=("Own technical writing delivery for lead scope 1.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Technical Writing",
    domain="Technical Writing",
    seniority="lead",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "lead"),
    responsibilities=("Own technical writing delivery for lead scope 2.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Technical Writing",
    domain="Technical Writing",
    seniority="lead",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "lead"),
    responsibilities=("Own technical writing delivery for lead scope 3.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Technical Writing",
    domain="Technical Writing",
    seniority="lead",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "lead"),
    responsibilities=("Own technical writing delivery for lead scope 4.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Technical Writing",
    domain="Technical Writing",
    seniority="lead",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "lead"),
    responsibilities=("Own technical writing delivery for lead scope 5.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Technical Writing",
    domain="Technical Writing",
    seniority="lead",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "lead"),
    responsibilities=("Own technical writing delivery for lead scope 6.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Technical Writing",
    domain="Technical Writing",
    seniority="staff",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "staff"),
    responsibilities=("Own technical writing delivery for staff scope 1.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Technical Writing",
    domain="Technical Writing",
    seniority="staff",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "staff"),
    responsibilities=("Own technical writing delivery for staff scope 2.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Technical Writing",
    domain="Technical Writing",
    seniority="staff",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "staff"),
    responsibilities=("Own technical writing delivery for staff scope 3.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Technical Writing",
    domain="Technical Writing",
    seniority="staff",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "staff"),
    responsibilities=("Own technical writing delivery for staff scope 4.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Technical Writing",
    domain="Technical Writing",
    seniority="staff",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "staff"),
    responsibilities=("Own technical writing delivery for staff scope 5.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Technical Writing",
    domain="Technical Writing",
    seniority="staff",
    skills=("documentation", "markdown", "api-docs", "information-architecture", "editing"),
    keywords=("documentation", "markdown", "api-docs", "information-architecture", "editing", "technical", "staff"),
    responsibilities=("Own technical writing delivery for staff scope 6.", "Translate requirements into measurable technical writing outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for technical writing", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Data Analysis",
    domain="Data Analysis",
    seniority="junior",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "junior"),
    responsibilities=("Own data analysis delivery for junior scope 1.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Data Analysis",
    domain="Data Analysis",
    seniority="junior",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "junior"),
    responsibilities=("Own data analysis delivery for junior scope 2.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Data Analysis",
    domain="Data Analysis",
    seniority="junior",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "junior"),
    responsibilities=("Own data analysis delivery for junior scope 3.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Data Analysis",
    domain="Data Analysis",
    seniority="junior",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "junior"),
    responsibilities=("Own data analysis delivery for junior scope 4.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Data Analysis",
    domain="Data Analysis",
    seniority="junior",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "junior"),
    responsibilities=("Own data analysis delivery for junior scope 5.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Data Analysis",
    domain="Data Analysis",
    seniority="junior",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "junior"),
    responsibilities=("Own data analysis delivery for junior scope 6.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Data Analysis",
    domain="Data Analysis",
    seniority="mid",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "mid"),
    responsibilities=("Own data analysis delivery for mid scope 1.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Data Analysis",
    domain="Data Analysis",
    seniority="mid",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "mid"),
    responsibilities=("Own data analysis delivery for mid scope 2.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Data Analysis",
    domain="Data Analysis",
    seniority="mid",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "mid"),
    responsibilities=("Own data analysis delivery for mid scope 3.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Data Analysis",
    domain="Data Analysis",
    seniority="mid",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "mid"),
    responsibilities=("Own data analysis delivery for mid scope 4.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Data Analysis",
    domain="Data Analysis",
    seniority="mid",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "mid"),
    responsibilities=("Own data analysis delivery for mid scope 5.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Data Analysis",
    domain="Data Analysis",
    seniority="mid",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "mid"),
    responsibilities=("Own data analysis delivery for mid scope 6.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Data Analysis",
    domain="Data Analysis",
    seniority="senior",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "senior"),
    responsibilities=("Own data analysis delivery for senior scope 1.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Data Analysis",
    domain="Data Analysis",
    seniority="senior",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "senior"),
    responsibilities=("Own data analysis delivery for senior scope 2.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Data Analysis",
    domain="Data Analysis",
    seniority="senior",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "senior"),
    responsibilities=("Own data analysis delivery for senior scope 3.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Data Analysis",
    domain="Data Analysis",
    seniority="senior",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "senior"),
    responsibilities=("Own data analysis delivery for senior scope 4.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Data Analysis",
    domain="Data Analysis",
    seniority="senior",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "senior"),
    responsibilities=("Own data analysis delivery for senior scope 5.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Data Analysis",
    domain="Data Analysis",
    seniority="senior",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "senior"),
    responsibilities=("Own data analysis delivery for senior scope 6.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Data Analysis",
    domain="Data Analysis",
    seniority="lead",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "lead"),
    responsibilities=("Own data analysis delivery for lead scope 1.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Data Analysis",
    domain="Data Analysis",
    seniority="lead",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "lead"),
    responsibilities=("Own data analysis delivery for lead scope 2.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Data Analysis",
    domain="Data Analysis",
    seniority="lead",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "lead"),
    responsibilities=("Own data analysis delivery for lead scope 3.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Data Analysis",
    domain="Data Analysis",
    seniority="lead",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "lead"),
    responsibilities=("Own data analysis delivery for lead scope 4.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Data Analysis",
    domain="Data Analysis",
    seniority="lead",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "lead"),
    responsibilities=("Own data analysis delivery for lead scope 5.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Data Analysis",
    domain="Data Analysis",
    seniority="lead",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "lead"),
    responsibilities=("Own data analysis delivery for lead scope 6.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Data Analysis",
    domain="Data Analysis",
    seniority="staff",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "staff"),
    responsibilities=("Own data analysis delivery for staff scope 1.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Data Analysis",
    domain="Data Analysis",
    seniority="staff",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "staff"),
    responsibilities=("Own data analysis delivery for staff scope 2.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Data Analysis",
    domain="Data Analysis",
    seniority="staff",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "staff"),
    responsibilities=("Own data analysis delivery for staff scope 3.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Data Analysis",
    domain="Data Analysis",
    seniority="staff",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "staff"),
    responsibilities=("Own data analysis delivery for staff scope 4.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Data Analysis",
    domain="Data Analysis",
    seniority="staff",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "staff"),
    responsibilities=("Own data analysis delivery for staff scope 5.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Data Analysis",
    domain="Data Analysis",
    seniority="staff",
    skills=("python", "sql", "pandas", "tableau", "powerbi", "statistics"),
    keywords=("python", "sql", "pandas", "tableau", "powerbi", "data", "staff"),
    responsibilities=("Own data analysis delivery for staff scope 6.", "Translate requirements into measurable data analysis outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for data analysis", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior UX Research",
    domain="UX Research",
    seniority="junior",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "junior"),
    responsibilities=("Own ux research delivery for junior scope 1.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior UX Research",
    domain="UX Research",
    seniority="junior",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "junior"),
    responsibilities=("Own ux research delivery for junior scope 2.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior UX Research",
    domain="UX Research",
    seniority="junior",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "junior"),
    responsibilities=("Own ux research delivery for junior scope 3.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior UX Research",
    domain="UX Research",
    seniority="junior",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "junior"),
    responsibilities=("Own ux research delivery for junior scope 4.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior UX Research",
    domain="UX Research",
    seniority="junior",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "junior"),
    responsibilities=("Own ux research delivery for junior scope 5.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior UX Research",
    domain="UX Research",
    seniority="junior",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "junior"),
    responsibilities=("Own ux research delivery for junior scope 6.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid UX Research",
    domain="UX Research",
    seniority="mid",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "mid"),
    responsibilities=("Own ux research delivery for mid scope 1.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid UX Research",
    domain="UX Research",
    seniority="mid",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "mid"),
    responsibilities=("Own ux research delivery for mid scope 2.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid UX Research",
    domain="UX Research",
    seniority="mid",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "mid"),
    responsibilities=("Own ux research delivery for mid scope 3.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid UX Research",
    domain="UX Research",
    seniority="mid",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "mid"),
    responsibilities=("Own ux research delivery for mid scope 4.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid UX Research",
    domain="UX Research",
    seniority="mid",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "mid"),
    responsibilities=("Own ux research delivery for mid scope 5.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid UX Research",
    domain="UX Research",
    seniority="mid",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "mid"),
    responsibilities=("Own ux research delivery for mid scope 6.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior UX Research",
    domain="UX Research",
    seniority="senior",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "senior"),
    responsibilities=("Own ux research delivery for senior scope 1.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior UX Research",
    domain="UX Research",
    seniority="senior",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "senior"),
    responsibilities=("Own ux research delivery for senior scope 2.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior UX Research",
    domain="UX Research",
    seniority="senior",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "senior"),
    responsibilities=("Own ux research delivery for senior scope 3.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior UX Research",
    domain="UX Research",
    seniority="senior",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "senior"),
    responsibilities=("Own ux research delivery for senior scope 4.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior UX Research",
    domain="UX Research",
    seniority="senior",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "senior"),
    responsibilities=("Own ux research delivery for senior scope 5.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior UX Research",
    domain="UX Research",
    seniority="senior",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "senior"),
    responsibilities=("Own ux research delivery for senior scope 6.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead UX Research",
    domain="UX Research",
    seniority="lead",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "lead"),
    responsibilities=("Own ux research delivery for lead scope 1.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead UX Research",
    domain="UX Research",
    seniority="lead",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "lead"),
    responsibilities=("Own ux research delivery for lead scope 2.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead UX Research",
    domain="UX Research",
    seniority="lead",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "lead"),
    responsibilities=("Own ux research delivery for lead scope 3.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead UX Research",
    domain="UX Research",
    seniority="lead",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "lead"),
    responsibilities=("Own ux research delivery for lead scope 4.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead UX Research",
    domain="UX Research",
    seniority="lead",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "lead"),
    responsibilities=("Own ux research delivery for lead scope 5.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead UX Research",
    domain="UX Research",
    seniority="lead",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "lead"),
    responsibilities=("Own ux research delivery for lead scope 6.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff UX Research",
    domain="UX Research",
    seniority="staff",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "staff"),
    responsibilities=("Own ux research delivery for staff scope 1.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff UX Research",
    domain="UX Research",
    seniority="staff",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "staff"),
    responsibilities=("Own ux research delivery for staff scope 2.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff UX Research",
    domain="UX Research",
    seniority="staff",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "staff"),
    responsibilities=("Own ux research delivery for staff scope 3.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff UX Research",
    domain="UX Research",
    seniority="staff",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "staff"),
    responsibilities=("Own ux research delivery for staff scope 4.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff UX Research",
    domain="UX Research",
    seniority="staff",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "staff"),
    responsibilities=("Own ux research delivery for staff scope 5.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff UX Research",
    domain="UX Research",
    seniority="staff",
    skills=("research", "interviews", "usability", "testing", "synthesis", "accessibility"),
    keywords=("research", "interviews", "usability", "testing", "synthesis", "ux", "staff"),
    responsibilities=("Own ux research delivery for staff scope 6.", "Translate requirements into measurable ux research outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for ux research", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Customer Success",
    domain="Customer Success",
    seniority="junior",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "junior"),
    responsibilities=("Own customer success delivery for junior scope 1.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Customer Success",
    domain="Customer Success",
    seniority="junior",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "junior"),
    responsibilities=("Own customer success delivery for junior scope 2.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Customer Success",
    domain="Customer Success",
    seniority="junior",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "junior"),
    responsibilities=("Own customer success delivery for junior scope 3.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Customer Success",
    domain="Customer Success",
    seniority="junior",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "junior"),
    responsibilities=("Own customer success delivery for junior scope 4.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Customer Success",
    domain="Customer Success",
    seniority="junior",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "junior"),
    responsibilities=("Own customer success delivery for junior scope 5.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Customer Success",
    domain="Customer Success",
    seniority="junior",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "junior"),
    responsibilities=("Own customer success delivery for junior scope 6.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Customer Success",
    domain="Customer Success",
    seniority="mid",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "mid"),
    responsibilities=("Own customer success delivery for mid scope 1.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Customer Success",
    domain="Customer Success",
    seniority="mid",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "mid"),
    responsibilities=("Own customer success delivery for mid scope 2.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Customer Success",
    domain="Customer Success",
    seniority="mid",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "mid"),
    responsibilities=("Own customer success delivery for mid scope 3.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Customer Success",
    domain="Customer Success",
    seniority="mid",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "mid"),
    responsibilities=("Own customer success delivery for mid scope 4.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Customer Success",
    domain="Customer Success",
    seniority="mid",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "mid"),
    responsibilities=("Own customer success delivery for mid scope 5.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Customer Success",
    domain="Customer Success",
    seniority="mid",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "mid"),
    responsibilities=("Own customer success delivery for mid scope 6.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Customer Success",
    domain="Customer Success",
    seniority="senior",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "senior"),
    responsibilities=("Own customer success delivery for senior scope 1.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Customer Success",
    domain="Customer Success",
    seniority="senior",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "senior"),
    responsibilities=("Own customer success delivery for senior scope 2.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Customer Success",
    domain="Customer Success",
    seniority="senior",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "senior"),
    responsibilities=("Own customer success delivery for senior scope 3.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Customer Success",
    domain="Customer Success",
    seniority="senior",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "senior"),
    responsibilities=("Own customer success delivery for senior scope 4.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Customer Success",
    domain="Customer Success",
    seniority="senior",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "senior"),
    responsibilities=("Own customer success delivery for senior scope 5.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Customer Success",
    domain="Customer Success",
    seniority="senior",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "senior"),
    responsibilities=("Own customer success delivery for senior scope 6.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Customer Success",
    domain="Customer Success",
    seniority="lead",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "lead"),
    responsibilities=("Own customer success delivery for lead scope 1.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Customer Success",
    domain="Customer Success",
    seniority="lead",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "lead"),
    responsibilities=("Own customer success delivery for lead scope 2.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Customer Success",
    domain="Customer Success",
    seniority="lead",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "lead"),
    responsibilities=("Own customer success delivery for lead scope 3.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Customer Success",
    domain="Customer Success",
    seniority="lead",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "lead"),
    responsibilities=("Own customer success delivery for lead scope 4.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Customer Success",
    domain="Customer Success",
    seniority="lead",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "lead"),
    responsibilities=("Own customer success delivery for lead scope 5.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Customer Success",
    domain="Customer Success",
    seniority="lead",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "lead"),
    responsibilities=("Own customer success delivery for lead scope 6.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Customer Success",
    domain="Customer Success",
    seniority="staff",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "staff"),
    responsibilities=("Own customer success delivery for staff scope 1.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Customer Success",
    domain="Customer Success",
    seniority="staff",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "staff"),
    responsibilities=("Own customer success delivery for staff scope 2.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Customer Success",
    domain="Customer Success",
    seniority="staff",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "staff"),
    responsibilities=("Own customer success delivery for staff scope 3.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Customer Success",
    domain="Customer Success",
    seniority="staff",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "staff"),
    responsibilities=("Own customer success delivery for staff scope 4.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Customer Success",
    domain="Customer Success",
    seniority="staff",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "staff"),
    responsibilities=("Own customer success delivery for staff scope 5.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Customer Success",
    domain="Customer Success",
    seniority="staff",
    skills=("onboarding", "retention", "crm", "analytics", "communication"),
    keywords=("onboarding", "retention", "crm", "analytics", "communication", "customer", "staff"),
    responsibilities=("Own customer success delivery for staff scope 6.", "Translate requirements into measurable customer success outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for customer success", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Solutions Engineering",
    domain="Solutions Engineering",
    seniority="junior",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "junior"),
    responsibilities=("Own solutions engineering delivery for junior scope 1.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Solutions Engineering",
    domain="Solutions Engineering",
    seniority="junior",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "junior"),
    responsibilities=("Own solutions engineering delivery for junior scope 2.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Solutions Engineering",
    domain="Solutions Engineering",
    seniority="junior",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "junior"),
    responsibilities=("Own solutions engineering delivery for junior scope 3.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Solutions Engineering",
    domain="Solutions Engineering",
    seniority="junior",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "junior"),
    responsibilities=("Own solutions engineering delivery for junior scope 4.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Solutions Engineering",
    domain="Solutions Engineering",
    seniority="junior",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "junior"),
    responsibilities=("Own solutions engineering delivery for junior scope 5.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Solutions Engineering",
    domain="Solutions Engineering",
    seniority="junior",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "junior"),
    responsibilities=("Own solutions engineering delivery for junior scope 6.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Solutions Engineering",
    domain="Solutions Engineering",
    seniority="mid",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "mid"),
    responsibilities=("Own solutions engineering delivery for mid scope 1.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Solutions Engineering",
    domain="Solutions Engineering",
    seniority="mid",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "mid"),
    responsibilities=("Own solutions engineering delivery for mid scope 2.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Solutions Engineering",
    domain="Solutions Engineering",
    seniority="mid",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "mid"),
    responsibilities=("Own solutions engineering delivery for mid scope 3.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Solutions Engineering",
    domain="Solutions Engineering",
    seniority="mid",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "mid"),
    responsibilities=("Own solutions engineering delivery for mid scope 4.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Solutions Engineering",
    domain="Solutions Engineering",
    seniority="mid",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "mid"),
    responsibilities=("Own solutions engineering delivery for mid scope 5.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Solutions Engineering",
    domain="Solutions Engineering",
    seniority="mid",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "mid"),
    responsibilities=("Own solutions engineering delivery for mid scope 6.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Solutions Engineering",
    domain="Solutions Engineering",
    seniority="senior",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "senior"),
    responsibilities=("Own solutions engineering delivery for senior scope 1.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Solutions Engineering",
    domain="Solutions Engineering",
    seniority="senior",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "senior"),
    responsibilities=("Own solutions engineering delivery for senior scope 2.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Solutions Engineering",
    domain="Solutions Engineering",
    seniority="senior",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "senior"),
    responsibilities=("Own solutions engineering delivery for senior scope 3.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Solutions Engineering",
    domain="Solutions Engineering",
    seniority="senior",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "senior"),
    responsibilities=("Own solutions engineering delivery for senior scope 4.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Solutions Engineering",
    domain="Solutions Engineering",
    seniority="senior",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "senior"),
    responsibilities=("Own solutions engineering delivery for senior scope 5.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Solutions Engineering",
    domain="Solutions Engineering",
    seniority="senior",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "senior"),
    responsibilities=("Own solutions engineering delivery for senior scope 6.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Solutions Engineering",
    domain="Solutions Engineering",
    seniority="lead",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "lead"),
    responsibilities=("Own solutions engineering delivery for lead scope 1.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Solutions Engineering",
    domain="Solutions Engineering",
    seniority="lead",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "lead"),
    responsibilities=("Own solutions engineering delivery for lead scope 2.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Solutions Engineering",
    domain="Solutions Engineering",
    seniority="lead",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "lead"),
    responsibilities=("Own solutions engineering delivery for lead scope 3.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Solutions Engineering",
    domain="Solutions Engineering",
    seniority="lead",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "lead"),
    responsibilities=("Own solutions engineering delivery for lead scope 4.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Solutions Engineering",
    domain="Solutions Engineering",
    seniority="lead",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "lead"),
    responsibilities=("Own solutions engineering delivery for lead scope 5.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Solutions Engineering",
    domain="Solutions Engineering",
    seniority="lead",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "lead"),
    responsibilities=("Own solutions engineering delivery for lead scope 6.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Solutions Engineering",
    domain="Solutions Engineering",
    seniority="staff",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "staff"),
    responsibilities=("Own solutions engineering delivery for staff scope 1.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Solutions Engineering",
    domain="Solutions Engineering",
    seniority="staff",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "staff"),
    responsibilities=("Own solutions engineering delivery for staff scope 2.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Solutions Engineering",
    domain="Solutions Engineering",
    seniority="staff",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "staff"),
    responsibilities=("Own solutions engineering delivery for staff scope 3.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Solutions Engineering",
    domain="Solutions Engineering",
    seniority="staff",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "staff"),
    responsibilities=("Own solutions engineering delivery for staff scope 4.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Solutions Engineering",
    domain="Solutions Engineering",
    seniority="staff",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "staff"),
    responsibilities=("Own solutions engineering delivery for staff scope 5.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Solutions Engineering",
    domain="Solutions Engineering",
    seniority="staff",
    skills=("apis", "cloud", "demos", "architecture", "troubleshooting"),
    keywords=("apis", "cloud", "demos", "architecture", "troubleshooting", "solutions", "staff"),
    responsibilities=("Own solutions engineering delivery for staff scope 6.", "Translate requirements into measurable solutions engineering outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for solutions engineering", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Project Management",
    domain="Project Management",
    seniority="junior",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "junior"),
    responsibilities=("Own project management delivery for junior scope 1.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Project Management",
    domain="Project Management",
    seniority="junior",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "junior"),
    responsibilities=("Own project management delivery for junior scope 2.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Project Management",
    domain="Project Management",
    seniority="junior",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "junior"),
    responsibilities=("Own project management delivery for junior scope 3.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Project Management",
    domain="Project Management",
    seniority="junior",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "junior"),
    responsibilities=("Own project management delivery for junior scope 4.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Project Management",
    domain="Project Management",
    seniority="junior",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "junior"),
    responsibilities=("Own project management delivery for junior scope 5.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Junior Project Management",
    domain="Project Management",
    seniority="junior",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "junior"),
    responsibilities=("Own project management delivery for junior scope 6.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at junior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Project Management",
    domain="Project Management",
    seniority="mid",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "mid"),
    responsibilities=("Own project management delivery for mid scope 1.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Project Management",
    domain="Project Management",
    seniority="mid",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "mid"),
    responsibilities=("Own project management delivery for mid scope 2.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Project Management",
    domain="Project Management",
    seniority="mid",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "mid"),
    responsibilities=("Own project management delivery for mid scope 3.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Project Management",
    domain="Project Management",
    seniority="mid",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "mid"),
    responsibilities=("Own project management delivery for mid scope 4.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Project Management",
    domain="Project Management",
    seniority="mid",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "mid"),
    responsibilities=("Own project management delivery for mid scope 5.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Mid Project Management",
    domain="Project Management",
    seniority="mid",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "mid"),
    responsibilities=("Own project management delivery for mid scope 6.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at mid level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Project Management",
    domain="Project Management",
    seniority="senior",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "senior"),
    responsibilities=("Own project management delivery for senior scope 1.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Project Management",
    domain="Project Management",
    seniority="senior",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "senior"),
    responsibilities=("Own project management delivery for senior scope 2.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Project Management",
    domain="Project Management",
    seniority="senior",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "senior"),
    responsibilities=("Own project management delivery for senior scope 3.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Project Management",
    domain="Project Management",
    seniority="senior",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "senior"),
    responsibilities=("Own project management delivery for senior scope 4.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Project Management",
    domain="Project Management",
    seniority="senior",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "senior"),
    responsibilities=("Own project management delivery for senior scope 5.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Senior Project Management",
    domain="Project Management",
    seniority="senior",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "senior"),
    responsibilities=("Own project management delivery for senior scope 6.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at senior level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Project Management",
    domain="Project Management",
    seniority="lead",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "lead"),
    responsibilities=("Own project management delivery for lead scope 1.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Project Management",
    domain="Project Management",
    seniority="lead",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "lead"),
    responsibilities=("Own project management delivery for lead scope 2.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Project Management",
    domain="Project Management",
    seniority="lead",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "lead"),
    responsibilities=("Own project management delivery for lead scope 3.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Project Management",
    domain="Project Management",
    seniority="lead",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "lead"),
    responsibilities=("Own project management delivery for lead scope 4.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Project Management",
    domain="Project Management",
    seniority="lead",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "lead"),
    responsibilities=("Own project management delivery for lead scope 5.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Lead Project Management",
    domain="Project Management",
    seniority="lead",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "lead"),
    responsibilities=("Own project management delivery for lead scope 6.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at lead level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Project Management",
    domain="Project Management",
    seniority="staff",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "staff"),
    responsibilities=("Own project management delivery for staff scope 1.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Project Management",
    domain="Project Management",
    seniority="staff",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "staff"),
    responsibilities=("Own project management delivery for staff scope 2.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Project Management",
    domain="Project Management",
    seniority="staff",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "staff"),
    responsibilities=("Own project management delivery for staff scope 3.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Project Management",
    domain="Project Management",
    seniority="staff",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "staff"),
    responsibilities=("Own project management delivery for staff scope 4.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Project Management",
    domain="Project Management",
    seniority="staff",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "staff"),
    responsibilities=("Own project management delivery for staff scope 5.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))
ROLES.append(RoleProfile(
    title="Staff Project Management",
    domain="Project Management",
    seniority="staff",
    skills=("planning", "delivery", "risk-management", "agile", "stakeholder-management"),
    keywords=("planning", "delivery", "risk-management", "agile", "stakeholder-management", "project", "staff"),
    responsibilities=("Own project management delivery for staff scope 6.", "Translate requirements into measurable project management outcomes.", "Review implementation quality, delivery risk, and operational impact.", "Document decisions, assumptions, dependencies, and follow-up work."),
    interview_focus=("architecture for project management", "trade-offs at staff level", "debugging and incident response", "communication and delivery planning"),
))

def search_roles(query: str, limit: int = 20) -> list[RoleProfile]:
    tokens = {token for token in query.lower().split() if token}
    scored = []
    for role in ROLES:
        haystack = " ".join((role.title, role.domain, *role.keywords)).lower()
        score = sum(token in haystack for token in tokens)
        if score:
            scored.append((score, role))
    scored.sort(key=lambda item: (-item[0], item[1].title))
    return [role for _, role in scored[:limit]]


def roles_for_skills(skills: Iterable[str], limit: int = 20) -> list[RoleProfile]:
    scored = [(role.skill_overlap(skills), role) for role in ROLES]
    scored.sort(key=lambda item: (-item[0], item[1].title))
    return [role for score, role in scored[:limit] if score > 0]
