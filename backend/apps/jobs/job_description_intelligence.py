"""Heuristic job-description parsing with explicit uncertainty and review cues."""
import re
from collections import Counter
from typing import Iterable

SECTION_ALIASES = {
    "responsibilities": ("responsibilities", "what you will do", "your role", "the role"),
    "requirements": ("requirements", "required qualifications", "what you bring", "must have", "essential"),
    "preferred": ("preferred qualifications", "nice to have", "bonus points", "desirable"),
    "benefits": ("benefits", "what we offer", "perks", "compensation and benefits"),
    "company": ("about us", "about the company", "who we are"),
}
POTENTIAL_RED_FLAGS = [
    ("upfront_payment", r"\b(pay|send|transfer)\b.{0,30}\b(fee|deposit|training cost|equipment cost)\b",
     "Requests for upfront payment deserve independent verification."),
    ("guaranteed_income", r"\bguaranteed\b.{0,25}\b(income|earnings|salary)\b",
     "Verify compensation claims against a written contract."),
    ("unpaid_trial", r"\b(unpaid|free)\b.{0,30}\b(trial|work assignment|project)\b",
     "Clarify whether any assessment is paid and how much work it requires."),
    ("vague_employer", r"\bconfidential employer\b|\bno company name\b",
     "Ask for verifiable employer identity before sharing sensitive information."),
    ("personal_financial_data", r"\b(bank password|card pin|crypto wallet seed|private key)\b",
     "Do not share passwords, PINs, or wallet recovery phrases during recruitment."),
]
def clean_description(text: str, maximum: int = 50000) -> str:
    if maximum < 1 or maximum > 200000:
        raise ValueError("maximum must be between 1 and 200000")
    value = str(text or "").replace("\x00", "").replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"[ \t]+\n", "\n", value)
    value = re.sub(r"\n{4,}", "\n\n\n", value)
    return value[:maximum].strip()

def split_sections(description: str) -> dict:
    text = clean_description(description)
    lines = text.splitlines()
    sections, current, body = {}, "overview", []
    aliases = {alias: section for section, values in SECTION_ALIASES.items() for alias in values}
    def flush():
        if body:
            sections.setdefault(current, []).extend(body[:])
            body.clear()
    for line in lines:
        candidate = re.sub(r"^[#*\-\s]+|[:*_\s]+$", "", line.lower()).strip()
        if candidate in aliases and len(candidate) < 100:
            flush()
            current = aliases[candidate]
        else:
            body.append(line.strip())
    flush()
    return {key: "\n".join(value).strip() for key, value in sections.items()}

def extract_requirement_bullets(description: str) -> dict:
    sections = split_sections(description)
    result = {}
    for key in ("responsibilities", "requirements", "preferred", "benefits"):
        text = sections.get(key, "")
        bullets = []
        for line in text.splitlines():
            cleaned = re.sub(r"^\s*(?:[-*•]|\d+[.)])\s*", "", line).strip()
            if cleaned and len(cleaned) <= 1000:
                bullets.append(cleaned)
        result[key] = bullets
    result["unsectioned_text"] = sections.get("overview", "")
    result["warning"] = "Section detection is heuristic; inspect the original posting before making decisions."
    return result

def detect_recruitment_red_flags(description: str) -> list[dict]:
    text = clean_description(description)
    results = []
    for code, pattern, explanation in POTENTIAL_RED_FLAGS:
        match = re.search(pattern, text, re.I | re.S)
        if match:
            snippet = re.sub(r"\s+", " ", text[max(0, match.start()-60):min(len(text), match.end()+60)])
            results.append({"code": code, "matched_text": match.group(0)[:180],
                            "context_snippet": snippet[:250], "explanation": explanation,
                            "severity": "high" if code == "personal_financial_data" else "review"})
    return results

def requirement_keyword_summary(description: str, limit: int = 30) -> list[dict]:
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    text = clean_description(description).lower()
    words = re.findall(r"\b[a-z][a-z0-9+#.-]{2,30}\b", text)
    stop = set("the and for with from that this will you your our are have has who what when where their they role team work job".split())
    counts = Counter(word for word in words if word not in stop)
    return [{"term": term, "occurrences": count} for term, count in
            sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]]

def build_application_questions(description: str) -> list[dict]:
    sections = split_sections(description)
    questions = []
    if not sections.get("requirements"):
        questions.append({"topic": "requirements", "question": "Which qualifications are essential versus preferred?"})
    if re.search(r"\bcompetitive salary\b|\bmarket rate\b|\bcompensation commensurate\b", description, re.I):
        questions.append({"topic": "compensation", "question": "What salary range, currency, and pay period apply to this role?"})
    if re.search(r"\bremote\b|\bhybrid\b|\bon[- ]site\b", description, re.I):
        questions.append({"topic": "location", "question": "What location, time-zone overlap, and attendance expectations apply?"})
    if re.search(r"\bcontract\b|\btemporary\b|\bfreelance\b", description, re.I):
        questions.append({"topic": "employment_type", "question": "What are the contract duration, payment schedule, and renewal terms?"})
    if re.search(r"\bvisa\b|\bsponsorship\b|\bwork authorization\b", description, re.I):
        questions.append({"topic": "authorization", "question": "What work authorization or sponsorship arrangements are available?"})
    questions.append({"topic": "success", "question": "What outcomes define success during the first 90 days?"})
    return questions

def posting_completeness(description: str) -> dict:
    sections = split_sections(description)
    checks = {
        "company_context": bool(sections.get("company") or sections.get("overview")),
        "responsibilities": bool(sections.get("responsibilities")),
        "requirements": bool(sections.get("requirements")),
        "benefits_or_compensation": bool(sections.get("benefits") or re.search(r"\$|salary|compensation|pay range", description, re.I)),
        "location_or_work_mode": bool(re.search(r"\b(remote|hybrid|onsite|on-site|location|based in)\b", description, re.I)),
        "application_process": bool(re.search(r"\b(apply|application|interview|submit your resume)\b", description, re.I)),
    }
    return {"checks": checks, "completeness_percent": round(100 * sum(checks.values()) / len(checks), 1),
            "missing_information": [key for key, present in checks.items() if not present],
            "note": "A complete posting can still be fraudulent; verify the employer and domain independently."}

def summarize_posting(description: str) -> dict:
    text = clean_description(description)
    sections = split_sections(text)
    return {"character_count": len(text), "word_count": len(text.split()),
            "sections_found": sorted(sections),
            "requirements": extract_requirement_bullets(text),
            "keyword_summary": requirement_keyword_summary(text, limit=20),
            "potential_red_flags": detect_recruitment_red_flags(text),
            "questions_to_ask": build_application_questions(text),
            "completeness": posting_completeness(text),
            "disclaimer": "These are heuristic review aids, not a determination that a job or employer is legitimate."}

def compare_postings(first: str, second: str) -> dict:
    left, right = set(requirement_keyword_summary(first, 100)[i]["term"] for i in range(len(requirement_keyword_summary(first, 100)))), set(
        requirement_keyword_summary(second, 100)[i]["term"] for i in range(len(requirement_keyword_summary(second, 100))))
    shared = sorted(left & right)
    return {"first_keyword_count": len(left), "second_keyword_count": len(right),
            "shared_terms": shared, "first_only_terms": sorted(left-right), "second_only_terms": sorted(right-left),
            "jaccard_percent": round(100*len(shared)/len(left|right), 2) if left|right else 0,
            "warning": "Keyword overlap is not a measure of job quality or candidate suitability."}
