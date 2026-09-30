import re
from collections import Counter


STOP_WORDS = {
    "about", "after", "again", "also", "and", "are", "been", "being", "but",
    "from", "have", "into", "more", "must", "that", "their", "there", "these",
    "this", "those", "with", "your", "will", "you", "years",
}


def normalize_skills(values):
    return sorted({str(value).strip().lower() for value in values if str(value).strip()})


def extract_keywords(text, limit=25):
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{2,}", text.lower())
    counts = Counter(word for word in words if word not in STOP_WORDS)
    return [word for word, _ in counts.most_common(limit)]


def match_skills(candidate_skills, required_skills, preferred_skills=None):
    candidate = set(normalize_skills(candidate_skills))
    required = set(normalize_skills(required_skills))
    preferred = set(normalize_skills(preferred_skills or []))
    required_matches = sorted(candidate & required)
    preferred_matches = sorted(candidate & preferred)
    missing_required = sorted(required - candidate)
    denominator = len(required) + len(preferred)
    matched = len(required_matches) + len(preferred_matches)
    score = round((matched / denominator) * 100, 2) if denominator else 0
    return {
        "score": score,
        "required_matches": required_matches,
        "preferred_matches": preferred_matches,
        "missing_required": missing_required,
    }


def estimate_application_fit(application, profile):
    profile_skills = getattr(profile, "skills", []) or []
    required = []
    preferred = []
    description = getattr(application, "job_description", None)
    if description:
        required = description.required_skills
        preferred = description.preferred_skills
    return match_skills(profile_skills, required, preferred)


def salary_position(value, minimum, maximum):
    if value is None or minimum is None or maximum is None or maximum <= minimum:
        return None
    if value <= minimum:
        return 0
    if value >= maximum:
        return 100
    return round(((value - minimum) / (maximum - minimum)) * 100, 2)
