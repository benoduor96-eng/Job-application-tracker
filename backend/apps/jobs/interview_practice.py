"""Structured interview practice tools; feedback is rubric-based, not predictive."""
import re
from collections import Counter
from typing import Iterable, Mapping

QUESTION_BANK = {
    "behavioral": [
        {"id": "b01", "question": "Tell me about a time you solved a difficult problem.", "competencies": ["problem_solving", "communication"]},
        {"id": "b02", "question": "Describe a disagreement and how you handled it.", "competencies": ["collaboration", "conflict_resolution"]},
        {"id": "b03", "question": "Tell me about a mistake and what you learned.", "competencies": ["accountability", "learning"]},
        {"id": "b04", "question": "Describe a time you had competing priorities.", "competencies": ["prioritization", "execution"]},
        {"id": "b05", "question": "Give an example of receiving difficult feedback.", "competencies": ["growth", "communication"]},
        {"id": "b06", "question": "Describe a project where you influenced others.", "competencies": ["leadership", "influence"]},
    ],
    "technical": [
        {"id": "t01", "question": "Explain a technical decision and its trade-offs.", "competencies": ["architecture", "reasoning"]},
        {"id": "t02", "question": "How would you investigate a production defect?", "competencies": ["debugging", "reliability"]},
        {"id": "t03", "question": "How do you test a change that touches multiple layers?", "competencies": ["testing", "design"]},
        {"id": "t04", "question": "How would you improve a slow database query?", "competencies": ["databases", "performance"]},
        {"id": "t05", "question": "Describe how you would secure an API endpoint.", "competencies": ["security", "api_design"]},
        {"id": "t06", "question": "How do you make a system observable?", "competencies": ["monitoring", "reliability"]},
    ],
    "role_fit": [
        {"id": "r01", "question": "Which part of this role best matches your experience?", "competencies": ["role_alignment"]},
        {"id": "r02", "question": "What would you aim to learn in your first 90 days?", "competencies": ["learning", "planning"]},
        {"id": "r03", "question": "Which achievement best demonstrates your impact?", "competencies": ["impact", "evidence"]},
        {"id": "r04", "question": "What questions would help you evaluate this team?", "competencies": ["judgment", "communication"]},
    ],
    "situational": [
        {"id": "s01", "question": "A deadline is at risk. How do you respond?", "competencies": ["prioritization", "communication"]},
        {"id": "s02", "question": "A requirement is ambiguous. What do you do first?", "competencies": ["clarification", "risk_management"]},
        {"id": "s03", "question": "A stakeholder asks for an unsafe shortcut. How do you respond?", "competencies": ["ethics", "security"]},
        {"id": "s04", "question": "A teammate is blocked and the deadline is near. What do you do?", "competencies": ["collaboration", "execution"]},
    ],
}
STAR_SECTIONS = ("situation", "task", "action", "result")
ANSWER_RUBRIC = {
    "specificity": "Does the answer describe a concrete situation rather than general claims?",
    "ownership": "Does it clarify the candidate's own role and decisions?",
    "action": "Are actions specific, understandable, and relevant?",
    "outcome": "Does it explain results, learning, or measurable impact?",
    "relevance": "Does the example connect to the question and role?",
}

def normalize_category(value):
    category = str(value or "behavioral").strip().lower()
    if category not in QUESTION_BANK:
        raise ValueError("Category must be behavioral, technical, role_fit, or situational")
    return category

def question_bank(category=None) -> list[dict]:
    categories = [normalize_category(category)] if category else list(QUESTION_BANK)
    return [{"category": name, **question, "rubric": list(ANSWER_RUBRIC)} for name in categories
            for question in QUESTION_BANK[name]]

def generate_practice_set(categories: Iterable[str] | None = None, count: int = 8,
                          seed: int | None = None) -> dict:
    import random
    if not 1 <= count <= 40:
        raise ValueError("count must be between 1 and 40")
    names = list(dict.fromkeys(normalize_category(name) for name in (categories or QUESTION_BANK)))
    if not names:
        raise ValueError("At least one category is required")
    pool = [dict(category=name, **item) for name in names for item in QUESTION_BANK[name]]
    generator = random.Random(seed)
    generator.shuffle(pool)
    selected = pool[:min(count, len(pool))]
    return {"questions": selected, "requested_count": count, "returned_count": len(selected),
            "categories": names, "seed": seed,
            "note": "Questions are practice prompts and do not predict what an employer will ask."}

def parse_star_answer(answer: str) -> dict:
    text = str(answer or "").strip()
    if not text:
        return {"sections": {key: "" for key in STAR_SECTIONS}, "missing_sections": list(STAR_SECTIONS),
                "complete": False, "character_count": 0}
    sections = {key: "" for key in STAR_SECTIONS}
    patterns = {
        "situation": r"(?:^|\n)\s*(?:situation|context)\s*:\s*",
        "task": r"(?:^|\n)\s*(?:task|goal)\s*:\s*",
        "action": r"(?:^|\n)\s*(?:action|actions)\s*:\s*",
        "result": r"(?:^|\n)\s*(?:result|outcome|impact)\s*:\s*",
    }
    matches = []
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.I)
        if match:
            matches.append((match.start(), match.end(), key))
    matches.sort()
    for index, (_, start, key) in enumerate(matches):
        end = matches[index + 1][0] if index + 1 < len(matches) else len(text)
        sections[key] = text[start:end].strip()
    missing = [key for key, value in sections.items() if not value]
    return {"sections": sections, "missing_sections": missing, "complete": not missing,
            "character_count": len(text), "word_count": len(text.split())}

def star_prompt_template() -> dict:
    return {"sections": [
        {"name": "Situation", "prompt": "What was happening? Include only context needed to understand the example."},
        {"name": "Task", "prompt": "What responsibility, goal, or constraint was yours?"},
        {"name": "Action", "prompt": "What did you personally do, and why did you choose those steps?"},
        {"name": "Result", "prompt": "What changed? Include a measurable outcome or honest learning where possible."},
    ], "reminder": "Use a real example. Do not invent metrics, responsibilities, or outcomes."}

def answer_review(answer: str, question: str = "", target_words: int = 180) -> dict:
    text = str(answer or "").strip()
    words = re.findall(r"\b[\w'-]+\b", text)
    lower = text.lower()
    star = parse_star_answer(text)
    first_person = len(re.findall(r"\b(i|my|me|we|our)\b", lower))
    vague = sum(lower.count(phrase) for phrase in (
        "hard worker", "team player", "many things", "various tasks", "very good", "a lot"))
    evidence = sum(1 for token in ("%", "$", "users", "customers", "hours", "days", "reduced",
                                    "increased", "improved", "delivered", "completed") if token in lower)
    checks = {
        "has_concrete_example": len(words) >= 35,
        "shows_ownership": first_person > 0,
        "mentions_actions": any(word in lower for word in ("built", "created", "tested", "organized", "analysed", "analyzed", "led", "changed", "resolved", "designed")),
        "mentions_outcome": any(word in lower for word in ("result", "outcome", "learned", "improved", "reduced", "increased", "delivered", "because")),
        "avoids_excessive_vagueness": vague < 3,
        "reasonable_length": 50 <= len(words) <= max(80, target_words * 2),
    }
    score = round(100 * sum(checks.values()) / len(checks))
    suggestions = []
    if not checks["has_concrete_example"]:
        suggestions.append("Add a real example with enough context to understand the challenge.")
    if not checks["shows_ownership"]:
        suggestions.append("Clarify your own contribution instead of describing only what the team did.")
    if not checks["mentions_actions"]:
        suggestions.append("Describe the specific steps you took and why.")
    if not checks["mentions_outcome"]:
        suggestions.append("Explain the result, learning, or trade-off, without inventing metrics.")
    if not checks["reasonable_length"]:
        suggestions.append("Aim for a concise answer with context, action, and outcome.")
    if not checks["avoids_excessive_vagueness"]:
        suggestions.append("Replace vague claims with a specific example.")
    return {"word_count": len(words), "character_count": len(text), "checks": checks,
            "rubric_score": score, "evidence_marker_count": evidence,
            "star_sections": star["missing_sections"], "suggestions": suggestions,
            "question": str(question or "")[:500],
            "limitations": ["Automated checks assess structure, not truth or interview performance.",
                            "A high score is not a guarantee of hiring success."]}

def build_interview_agenda(duration_minutes: int = 45, interview_type: str = "mixed") -> dict:
    if not 15 <= duration_minutes <= 240:
        raise ValueError("duration_minutes must be between 15 and 240")
    if interview_type not in {"behavioral", "technical", "mixed", "screening"}:
        raise ValueError("Unsupported interview type")
    proportions = {
        "behavioral": [("Opening", .10), ("Behavioral examples", .55), ("Candidate questions", .20), ("Closing", .15)],
        "technical": [("Opening", .10), ("Technical reasoning", .55), ("Testing and trade-offs", .20), ("Candidate questions", .15)],
        "mixed": [("Opening", .10), ("Experience examples", .30), ("Technical or role discussion", .35), ("Candidate questions", .15), ("Closing", .10)],
        "screening": [("Opening", .10), ("Motivation and experience", .45), ("Role logistics", .20), ("Candidate questions", .15), ("Closing", .10)],
    }
    agenda, remaining = [], duration_minutes
    parts = proportions[interview_type]
    for index, (name, share) in enumerate(parts):
        minutes = remaining if index == len(parts) - 1 else max(1, round(duration_minutes * share))
        minutes = min(minutes, remaining)
        agenda.append({"segment": name, "minutes": minutes})
        remaining -= minutes
    if remaining:
        agenda[-1]["minutes"] += remaining
    return {"duration_minutes": duration_minutes, "interview_type": interview_type, "agenda": agenda,
            "note": "Use this as a flexible rehearsal plan, not a prediction of the actual interview."}

def question_coverage(answers: Iterable[Mapping]) -> dict:
    counts = Counter()
    for answer in answers:
        for competency in answer.get("competencies", []) or []:
            counts[str(competency)] += 1
    return {"competency_counts": dict(sorted(counts.items())),
            "uncovered_competencies": [name for name in ("communication", "problem_solving", "ownership",
                "collaboration", "learning", "impact", "prioritization", "technical_reasoning")
                if counts[name] == 0],
            "note": "Coverage indicates practice breadth only; it does not grade capability."}

def follow_up_questions(role: str, company: str, interview_type: str = "mixed") -> list[dict]:
    role, company = str(role or "this role").strip(), str(company or "the organization").strip()
    if interview_type not in {"behavioral", "technical", "mixed", "screening"}:
        raise ValueError("Unsupported interview type")
    questions = [
        ("success", f"What would strong performance in {role} look like after 90 days?"),
        ("team", "How does the team share feedback and review work?"),
        ("challenges", "What are the most important problems this person would help solve?"),
        ("process", f"What are the next steps in the {company} interview process?"),
    ]
    if interview_type in {"technical", "mixed"}:
        questions.insert(2, ("engineering", "How are technical trade-offs and reliability concerns evaluated?"))
    return [{"topic": topic, "question": question} for topic, question in questions]

def preparation_checklist() -> list[dict]:
    return [
        {"id": "role", "label": "Review the role requirements", "category": "research"},
        {"id": "company", "label": "Review public information about the employer", "category": "research"},
        {"id": "examples", "label": "Prepare three truthful examples of impact", "category": "evidence"},
        {"id": "questions", "label": "Prepare two or three questions for the interviewer", "category": "questions"},
        {"id": "logistics", "label": "Confirm time zone, format, location or meeting link", "category": "logistics"},
        {"id": "technology", "label": "Test audio, camera, connection and required software", "category": "logistics"},
        {"id": "documents", "label": "Keep the resume and role description available", "category": "materials"},
        {"id": "rest", "label": "Leave time to rest and arrive prepared", "category": "wellbeing"},
    ]
