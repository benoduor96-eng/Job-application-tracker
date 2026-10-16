"""Deterministic career-coaching helpers with no external provider calls."""
import re
from collections import Counter

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "being", "by",
    "for", "from", "has", "have", "in", "into", "is", "it", "its", "of",
    "on", "or", "our", "that", "the", "their", "this", "to", "was", "were",
    "will", "with", "you", "your", "we", "they", "can", "may", "should",
    "must", "about", "across", "using", "use", "work", "working",
}
ACTION_VERBS = (
    "built", "created", "delivered", "designed", "developed", "improved",
    "implemented", "increased", "led", "maintained", "managed", "reduced",
    "resolved", "supported", "tested", "trained", "validated",
)


def tokenize(text):
    """Return normalized word tokens, preserving common technical symbols."""
    return re.findall(r"[a-z][a-z0-9+#.\-]{1,}", (text or "").lower())


def extract_terms(text, limit=40):
    """Rank meaningful terms by frequency, with stable alphabetical tie-breaks."""
    counts = Counter(token for token in tokenize(text) if token not in STOP_WORDS and len(token) > 2)
    return [{"term": term, "count": count} for term, count in
            sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:max(0, limit)]]


def compare_skills(candidate_skills, required_skills, preferred_skills=()):
    """Compare lists case-insensitively and report gaps without guessing."""
    candidate = {str(v).strip().casefold() for v in candidate_skills if str(v).strip()}
    required = {str(v).strip().casefold() for v in required_skills if str(v).strip()}
    preferred = {str(v).strip().casefold() for v in preferred_skills if str(v).strip()}
    return {
        "required_matches": sorted(candidate & required),
        "missing_required": sorted(required - candidate),
        "preferred_matches": sorted(candidate & preferred),
        "missing_preferred": sorted(preferred - candidate),
        "required_coverage_percent": round(100 * len(candidate & required) / len(required), 1) if required else None,
        "preferred_coverage_percent": round(100 * len(candidate & preferred) / len(preferred), 1) if preferred else None,
        "disclaimer": "Skill overlap is a review aid, not a hiring probability or guarantee.",
    }


def resume_review(text):
    """Produce transparent resume checks; do not mutate or store submitted text."""
    body = (text or "").strip()
    words = tokenize(body)
    lower = body.casefold()
    bullets = [line.strip(" •-*\t") for line in body.splitlines() if line.strip().startswith(("-", "*", "•"))]
    action_bullets = [line for line in bullets if any(re.search(r"\b" + re.escape(v) + r"\b", line.casefold()) for v in ACTION_VERBS)]
    quantified = [line for line in bullets if re.search(r"\b\d+(?:\.\d+)?\s*(?:%|percent|users|customers|hours|days|weeks|months|years|projects|records|items)?\b", line, re.I)]
    checks = [
        {"key": "contact_details", "passed": bool(re.search(r"\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b", body, re.I)), "advice": "Include a professional email address."},
        {"key": "skills_section", "passed": "skills" in lower, "advice": "Add a clearly labeled skills section when relevant."},
        {"key": "experience_section", "passed": any(t in lower for t in ("experience", "employment", "work history")), "advice": "Make work experience easy to locate."},
        {"key": "action_led_bullets", "passed": bool(action_bullets), "advice": "Start experience bullets with precise action verbs."},
        {"key": "measurable_impact", "passed": bool(quantified), "advice": "Where truthful, quantify outcomes, scope, quality, or time saved."},
        {"key": "reasonable_length", "passed": 250 <= len(words) <= 1200, "advice": "Review length; appropriate resume length varies by seniority and country."},
    ]
    return {
        "word_count": len(words), "bullet_count": len(bullets),
        "action_led_bullet_count": len(action_bullets),
        "quantified_bullet_count": len(quantified), "checks": checks,
        "suggestions": [c["advice"] for c in checks if not c["passed"]],
        "privacy_note": "This helper does not persist the submitted text.",
    }


def interview_question_set(role, skills=(), count=8):
    """Generate practical questions based on user-provided role and skills."""
    role = (role or "the role").strip()[:160] or "the role"
    skills = list(dict.fromkeys(str(s).strip() for s in skills if str(s).strip()))[:12]
    templates = [
        ("behavioral", "Tell me about a difficult problem relevant to {role}. What did you do and what changed?"),
        ("ownership", "Describe a project related to {role} that you owned from planning through delivery."),
        ("quality", "How do you validate your work and catch mistakes before delivery?"),
        ("collaboration", "Tell me about a disagreement with a teammate and how you resolved it."),
        ("prioritization", "How would you prioritize competing deadlines in {role}?"),
        ("learning", "Describe a skill you had to learn quickly and how you applied it."),
        ("impact", "Which outcome from your recent work best demonstrates your impact, and how did you measure it?"),
        ("reflection", "What would you improve about a recent project if you could do it again?"),
    ]
    questions = [{"category": c, "question": q.format(role=role)} for c, q in templates]
    questions.extend({"category": "technical", "question": f"Explain how you have used {skill} in practice. Describe a challenge, your approach, and how you verified the result."} for skill in skills)
    return questions[:max(1, min(int(count), 20))]


def build_job_fit_report(candidate_skills, description_text):
    """Summarize skill evidence; intentionally avoid an opaque hiring score."""
    terms = [item["term"] for item in extract_terms(description_text, 30)]
    return {
        **compare_skills(candidate_skills, terms),
        "description_terms": terms,
        "review_guidance": [
            "Confirm apparent matches using concrete evidence from your experience.",
            "Do not add skills to a resume unless you can support them honestly.",
            "Prioritize required skills over repeated generic terms.",
        ],
    }
