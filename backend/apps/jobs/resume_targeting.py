"""Explainable, dependency-free resume and job-description comparison utilities."""
import re
from collections import Counter
from typing import Iterable, Mapping

TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,40}")
STOP_WORDS = frozenset("""a an and are as at be by for from has have in into is it its of on or our that the their this to with you your we will can using use used""".split())
SKILL_ALIASES = {
    "js": "javascript", "ts": "typescript", "py": "python", "postgres": "postgresql",
    "postgres sql": "postgresql", "amazon web services": "aws", "google cloud platform": "gcp",
    "microsoft azure": "azure", "ci/cd": "continuous integration", "ml": "machine learning",
    "ai": "artificial intelligence", "nlp": "natural language processing",
    "k8s": "kubernetes", "restful api": "rest api", "rest apis": "rest api",
    "powerbi": "power bi", "ms excel": "excel", "scikit-learn": "scikit learn",
}
SKILL_CATALOG = frozenset("""
python javascript typescript java c c++ c# go rust ruby php sql postgresql mysql sqlite mongodb redis
django flask fastapi react vue angular next.js html css sass tailwind bootstrap node.js express
rest api graphql grpc openapi oauth jwt docker kubernetes terraform ansible linux bash powershell
git github gitlab github actions jenkins continuous integration continuous deployment pytest unittest
jest playwright selenium pandas numpy scipy scikit learn pytorch tensorflow keras machine learning
deep learning artificial intelligence natural language processing computer vision llm prompt engineering
data analysis data visualization tableau power bi excel statistics probability sql server spark kafka
airflow dbt snowflake bigquery redshift aws azure gcp cloud security penetration testing threat modeling
owasp oauth2 oidc iam incident response risk assessment compliance gdpr privacy encryption monitoring
prometheus grafana elasticsearch jira agile scrum kanban product management stakeholder management
communication writing editing research customer support sales negotiation project management leadership
budgeting forecasting accounting bookkeeping payroll crm erp sap salesforce marketing seo analytics
figma ux design ui design accessibility responsive design testing debugging code review architecture
microservices event driven systems message queues rabbitmq celery redis cache performance optimization
api design data modeling database design migrations transactions indexing query optimization
""".split())

def normalize_text(value) -> str:
    text = str(value or "").lower().replace("&", " and ")
    for alias, canonical in sorted(SKILL_ALIASES.items(), key=lambda pair: len(pair[0]), reverse=True):
        text = re.sub(r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])", canonical, text)
    return re.sub(r"\s+", " ", text).strip()

def tokenize(value) -> list[str]:
    return [token.lower().strip(".-+#") for token in TOKEN_RE.findall(normalize_text(value))
            if len(token.strip(".-+#")) > 1 and token.lower() not in STOP_WORDS]

def extract_skills(value, catalog: Iterable[str] = SKILL_CATALOG) -> list[str]:
    text = " " + normalize_text(value) + " "
    found = set()
    for skill in catalog:
        normalized = normalize_text(skill)
        if not normalized:
            continue
        pattern = r"(?<![a-z0-9])" + re.escape(normalized) + r"(?![a-z0-9])"
        if re.search(pattern, text):
            found.add(normalized)
    return sorted(found)

def keyword_frequency(value, limit: int = 30) -> list[dict]:
    if not 1 <= limit <= 200:
        raise ValueError("limit must be between 1 and 200")
    tokens = tokenize(value)
    counts = Counter(tokens)
    return [{"keyword": word, "count": count} for word, count in
            sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:limit]]

def compare_resume_to_job(resume_text: str, job_description: str, extra_skills: Iterable[str] = ()) -> dict:
    if not str(resume_text or "").strip():
        raise ValueError("Resume text is required")
    if not str(job_description or "").strip():
        raise ValueError("Job description is required")
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))
    job_skills.update(normalize_text(skill) for skill in extra_skills if normalize_text(skill))
    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    resume_tokens, job_tokens = set(tokenize(resume_text)), set(tokenize(job_description))
    keyword_overlap = sorted(resume_tokens & job_tokens)
    union = resume_tokens | job_tokens
    lexical_score = round(100 * len(keyword_overlap) / len(union), 2) if union else 0.0
    skill_score = round(100 * len(matched) / len(job_skills), 2) if job_skills else 0.0
    recommendations = []
    if missing:
        recommendations.append({"priority": "high", "action": "Review skill gaps",
                                 "detail": "Consider adding truthful evidence for: " + ", ".join(missing[:12])})
    if not resume_skills:
        recommendations.append({"priority": "medium", "action": "Add concrete technical or professional skills",
                                 "detail": "The resume text did not contain recognized catalog skills."})
    if len(resume_tokens) < 80:
        recommendations.append({"priority": "medium", "action": "Add specific evidence",
                                 "detail": "Include projects, responsibilities, outcomes, and relevant tools where accurate."})
    if not recommendations:
        recommendations.append({"priority": "info", "action": "Tailor evidence",
                                 "detail": "Prioritize the most relevant achievements and preserve factual accuracy."})
    return {"skill_match_percent": skill_score, "lexical_overlap_percent": lexical_score,
            "matched_skills": matched, "missing_job_skills": missing,
            "resume_skill_count": len(resume_skills), "job_skill_count": len(job_skills),
            "shared_keywords": keyword_overlap[:50], "recommendations": recommendations,
            "limitations": ["Keyword matching cannot judge depth of experience or candidate suitability.",
                            "A missing keyword does not prove a missing skill.",
                            "Do not add skills or qualifications you do not have."]}

def rank_resume_variants(variants: Iterable[Mapping], job_description: str) -> list[dict]:
    results = []
    for variant in variants:
        identifier = variant.get("id")
        try:
            comparison = compare_resume_to_job(variant.get("text", ""), job_description)
        except ValueError as exc:
            results.append({"id": identifier, "valid": False, "error": str(exc), "score": 0.0})
            continue
        results.append({"id": identifier, "valid": True, "score": comparison["skill_match_percent"],
                        "matched_skills": comparison["matched_skills"],
                        "missing_skills": comparison["missing_job_skills"],
                        "recommendations": comparison["recommendations"]})
    results.sort(key=lambda item: (-item["score"], str(item["id"] or "")))
    for rank, item in enumerate(results, 1):
        item["rank"] = rank
    return results

def evidence_inventory(resume_text: str, job_description: str) -> dict:
    resume = normalize_text(resume_text)
    description = normalize_text(job_description)
    required = extract_skills(description)
    inventory = []
    for skill in required:
        positions = [match.start() for match in re.finditer(r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])", resume)]
        inventory.append({"skill": skill, "mentioned": bool(positions), "mention_count": len(positions),
                          "evidence_status": "mentioned_not_verified" if positions else "not_found"})
    return {"required_skill_count": len(required), "mentioned_count": sum(item["mentioned"] for item in inventory),
            "skills": inventory,
            "note": "Mentions are not evidence of proficiency; verify each skill against real work or study."}

def tailor_summary_guidance(resume_text: str, job_description: str, max_suggestions: int = 8) -> list[dict]:
    if not 1 <= max_suggestions <= 20:
        raise ValueError("max_suggestions must be between 1 and 20")
    comparison = compare_resume_to_job(resume_text, job_description)
    suggestions = []
    for skill in comparison["matched_skills"][:max_suggestions]:
        suggestions.append({"kind": "emphasize_existing_evidence", "skill": skill,
                            "guidance": f"Bring your real example of {skill} closer to the top if it is relevant."})
    for skill in comparison["missing_job_skills"][:max(0, max_suggestions - len(suggestions))]:
        suggestions.append({"kind": "verify_before_adding", "skill": skill,
                            "guidance": f"Only include {skill} if you can support it with actual experience or study."})
    return suggestions[:max_suggestions]

def parse_required_and_preferred(description: str) -> dict:
    lines = [line.strip(" -*\t") for line in str(description or "").splitlines() if line.strip()]
    required, preferred, neutral = [], [], []
    mode = "neutral"
    for line in lines:
        lower = line.lower().rstrip(":")
        if any(word in lower for word in ("required qualifications", "must have", "requirements", "essential skills")):
            mode = "required"
            continue
        if any(word in lower for word in ("preferred qualifications", "nice to have", "bonus skills", "desirable")):
            mode = "preferred"
            continue
        if line.endswith(":") and len(line) < 80:
            mode = "neutral"
        target = required if mode == "required" else preferred if mode == "preferred" else neutral
        target.append(line[:500])
    return {"required": required, "preferred": preferred, "other": neutral,
            "warning": "Section headings are heuristic; review the original job posting."}

def resume_completeness_report(resume: Mapping) -> dict:
    fields = {
        "contact": any(str(resume.get(key) or "").strip() for key in ("email", "phone", "linkedin")),
        "summary": bool(str(resume.get("summary") or "").strip()),
        "experience": bool(resume.get("experience")),
        "education": bool(resume.get("education")),
        "skills": bool(resume.get("skills")),
        "projects": bool(resume.get("projects")),
        "achievements": bool(resume.get("achievements")),
    }
    present = sum(fields.values())
    return {"fields": fields, "present_sections": present, "section_count": len(fields),
            "completeness_percent": round(100 * present / len(fields), 1),
            "missing_sections": [key for key, value in fields.items() if not value],
            "note": "A section checklist is not a quality score; include only relevant and truthful information."}

def sanitize_job_description(description: str, max_length: int = 30000) -> str:
    text = str(description or "").replace("\x00", "")
    if max_length < 1:
        raise ValueError("max_length must be positive")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text[:max_length].strip()
