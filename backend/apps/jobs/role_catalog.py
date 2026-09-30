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


# Additional distinct role profiles for broader career search coverage.
ROLES.append(RoleProfile(
    title="Cloud Security Engineering",
    domain="Security Engineering",
    seniority="specialist",
    skills=("cloud-security", "iam", "siem", "aws", "azure"),
    keywords=("cloud security", "iam", "security", "aws", "azure"),
    responsibilities=(
        "Define delivery outcomes for cloud security engineering.",
        "Translate requirements into measurable security engineering outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in cloud security engineering",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Machine Learning Operations",
    domain="ML Engineering",
    seniority="specialist",
    skills=("python", "mlops", "model-serving", "docker", "kubernetes"),
    keywords=("mlops", "machine learning", "model serving", "python", "kubernetes"),
    responsibilities=(
        "Define delivery outcomes for machine learning operations.",
        "Translate requirements into measurable ml engineering outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in machine learning operations",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Data Governance",
    domain="Data Management",
    seniority="specialist",
    skills=("data-governance", "privacy", "compliance", "sql", "catalog"),
    keywords=("data governance", "privacy", "compliance", "sql", "data catalog"),
    responsibilities=(
        "Define delivery outcomes for data governance.",
        "Translate requirements into measurable data management outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in data governance",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Privacy Engineering",
    domain="Security Engineering",
    seniority="specialist",
    skills=("privacy", "python", "security", "compliance", "data-protection"),
    keywords=("privacy engineering", "privacy", "security", "compliance"),
    responsibilities=(
        "Define delivery outcomes for privacy engineering.",
        "Translate requirements into measurable security engineering outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in privacy engineering",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Platform Engineering",
    domain="Infrastructure",
    seniority="specialist",
    skills=("linux", "kubernetes", "terraform", "python", "platform"),
    keywords=("platform engineering", "kubernetes", "terraform", "linux"),
    responsibilities=(
        "Define delivery outcomes for platform engineering.",
        "Translate requirements into measurable infrastructure outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in platform engineering",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Site Reliability Engineering",
    domain="Infrastructure",
    seniority="specialist",
    skills=("linux", "kubernetes", "observability", "terraform", "incident-response"),
    keywords=("site reliability", "sre", "kubernetes", "observability"),
    responsibilities=(
        "Define delivery outcomes for site reliability engineering.",
        "Translate requirements into measurable infrastructure outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in site reliability engineering",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="DevSecOps Engineering",
    domain="Security Engineering",
    seniority="specialist",
    skills=("ci-cd", "security", "docker", "kubernetes", "terraform"),
    keywords=("devsecops", "security", "ci-cd", "docker", "terraform"),
    responsibilities=(
        "Define delivery outcomes for devsecops engineering.",
        "Translate requirements into measurable security engineering outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in devsecops engineering",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Cloud Architecture",
    domain="Cloud Engineering",
    seniority="specialist",
    skills=("aws", "azure", "gcp", "networking", "architecture"),
    keywords=("cloud architecture", "aws", "azure", "gcp"),
    responsibilities=(
        "Define delivery outcomes for cloud architecture.",
        "Translate requirements into measurable cloud engineering outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in cloud architecture",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Data Platform Engineering",
    domain="Data Engineering",
    seniority="specialist",
    skills=("python", "sql", "spark", "airflow", "kafka"),
    keywords=("data platform", "python", "sql", "spark", "airflow"),
    responsibilities=(
        "Define delivery outcomes for data platform engineering.",
        "Translate requirements into measurable data engineering outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in data platform engineering",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Analytics Engineering",
    domain="Data Analytics",
    seniority="specialist",
    skills=("sql", "dbt", "python", "warehouse", "analytics"),
    keywords=("analytics engineering", "sql", "dbt", "data warehouse"),
    responsibilities=(
        "Define delivery outcomes for analytics engineering.",
        "Translate requirements into measurable data analytics outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in analytics engineering",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Business Intelligence",
    domain="Data Analytics",
    seniority="specialist",
    skills=("sql", "tableau", "power-bi", "dashboards", "analytics"),
    keywords=("business intelligence", "sql", "tableau", "power bi"),
    responsibilities=(
        "Define delivery outcomes for business intelligence.",
        "Translate requirements into measurable data analytics outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in business intelligence",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Technical Product Management",
    domain="Product Management",
    seniority="specialist",
    skills=("roadmaps", "api", "analytics", "stakeholders", "agile"),
    keywords=("technical product", "product management", "roadmap", "api"),
    responsibilities=(
        "Define delivery outcomes for technical product management.",
        "Translate requirements into measurable product management outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in technical product management",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Product Operations",
    domain="Product Management",
    seniority="specialist",
    skills=("analytics", "process", "operations", "stakeholders", "product"),
    keywords=("product operations", "analytics", "product", "operations"),
    responsibilities=(
        "Define delivery outcomes for product operations.",
        "Translate requirements into measurable product management outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in product operations",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Technical Program Management",
    domain="Program Management",
    seniority="specialist",
    skills=("program-management", "delivery", "risk", "stakeholders", "agile"),
    keywords=("technical program", "program management", "delivery", "risk"),
    responsibilities=(
        "Define delivery outcomes for technical program management.",
        "Translate requirements into measurable program management outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in technical program management",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Release Engineering",
    domain="Developer Experience",
    seniority="specialist",
    skills=("ci-cd", "release", "automation", "git", "linux"),
    keywords=("release engineering", "ci-cd", "automation", "git"),
    responsibilities=(
        "Define delivery outcomes for release engineering.",
        "Translate requirements into measurable developer experience outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in release engineering",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Developer Experience Engineering",
    domain="Developer Experience",
    seniority="specialist",
    skills=("tooling", "automation", "git", "python", "documentation"),
    keywords=("developer experience", "developer tooling", "automation"),
    responsibilities=(
        "Define delivery outcomes for developer experience engineering.",
        "Translate requirements into measurable developer experience outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in developer experience engineering",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Solutions Architecture",
    domain="Solutions Engineering",
    seniority="specialist",
    skills=("architecture", "apis", "cloud", "integration", "stakeholders"),
    keywords=("solutions architecture", "architecture", "apis", "cloud"),
    responsibilities=(
        "Define delivery outcomes for solutions architecture.",
        "Translate requirements into measurable solutions engineering outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in solutions architecture",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Sales Engineering",
    domain="Solutions Engineering",
    seniority="specialist",
    skills=("technical-sales", "demos", "apis", "cloud", "discovery"),
    keywords=("sales engineering", "technical sales", "demos", "apis"),
    responsibilities=(
        "Define delivery outcomes for sales engineering.",
        "Translate requirements into measurable solutions engineering outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in sales engineering",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Customer Success Engineering",
    domain="Customer Success",
    seniority="specialist",
    skills=("api", "troubleshooting", "automation", "python", "customer-success"),
    keywords=("customer success engineering", "api", "troubleshooting"),
    responsibilities=(
        "Define delivery outcomes for customer success engineering.",
        "Translate requirements into measurable customer success outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in customer success engineering",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Technical Support Engineering",
    domain="Support Engineering",
    seniority="specialist",
    skills=("linux", "networking", "sql", "troubleshooting", "python"),
    keywords=("technical support", "linux", "networking", "troubleshooting"),
    responsibilities=(
        "Define delivery outcomes for technical support engineering.",
        "Translate requirements into measurable support engineering outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in technical support engineering",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Security Operations",
    domain="Cybersecurity",
    seniority="specialist",
    skills=("siem", "incident-response", "linux", "networking", "threat-detection"),
    keywords=("security operations", "siem", "incident response"),
    responsibilities=(
        "Define delivery outcomes for security operations.",
        "Translate requirements into measurable cybersecurity outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in security operations",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Threat Intelligence",
    domain="Cybersecurity",
    seniority="specialist",
    skills=("threat-intelligence", "osint", "python", "security", "analysis"),
    keywords=("threat intelligence", "osint", "security", "analysis"),
    responsibilities=(
        "Define delivery outcomes for threat intelligence.",
        "Translate requirements into measurable cybersecurity outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in threat intelligence",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Application Security",
    domain="Cybersecurity",
    seniority="specialist",
    skills=("security", "python", "owasp", "code-review", "threat-modeling"),
    keywords=("application security", "owasp", "code review", "threat modeling"),
    responsibilities=(
        "Define delivery outcomes for application security.",
        "Translate requirements into measurable cybersecurity outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in application security",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Quality Engineering",
    domain="Quality Assurance",
    seniority="specialist",
    skills=("python", "testing", "automation", "api", "ci-cd"),
    keywords=("quality engineering", "test automation", "python", "api"),
    responsibilities=(
        "Define delivery outcomes for quality engineering.",
        "Translate requirements into measurable quality assurance outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in quality engineering",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
))
ROLES.append(RoleProfile(
    title="Performance Engineering",
    domain="Software Engineering",
    seniority="specialist",
    skills=("profiling", "python", "linux", "databases", "benchmarking"),
    keywords=("performance engineering", "profiling", "benchmarking", "linux"),
    responsibilities=(
        "Define delivery outcomes for performance engineering.",
        "Translate requirements into measurable software engineering outcomes.",
        "Review implementation quality, delivery risk, and operational impact.",
        "Document decisions, assumptions, dependencies, and follow-up work."
    ),
    interview_focus=(
        "core practices in performance engineering",
        "trade-offs and decision making",
        "debugging and incident response",
        "communication and delivery planning"
    ),
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
