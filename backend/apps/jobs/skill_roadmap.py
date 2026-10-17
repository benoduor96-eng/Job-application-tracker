"""Skill-development roadmaps with explicit evidence, prerequisites, and time budgets."""
from collections import defaultdict, deque
from typing import Iterable, Mapping

SKILL_LEVELS = {"new": 0, "beginner": 1, "working": 2, "proficient": 3, "advanced": 4}
DEFAULT_CATALOG = {
    "python": {"category": "programming", "prerequisites": [], "estimated_hours": 35,
               "evidence": ["small scripts", "unit-tested functions", "documented project"]},
    "git": {"category": "engineering", "prerequisites": [], "estimated_hours": 8,
            "evidence": ["branch and merge workflow", "meaningful commits", "conflict resolution"]},
    "sql": {"category": "data", "prerequisites": [], "estimated_hours": 25,
            "evidence": ["joins and aggregation", "indexes and query plan", "transaction example"]},
    "testing": {"category": "engineering", "prerequisites": ["python"], "estimated_hours": 18,
                "evidence": ["unit tests", "integration tests", "edge-case regression tests"]},
    "django": {"category": "web", "prerequisites": ["python"], "estimated_hours": 30,
               "evidence": ["model and migration", "validated API", "permission tests"]},
    "rest api": {"category": "web", "prerequisites": ["python"], "estimated_hours": 20,
                 "evidence": ["documented endpoints", "input validation", "authentication tests"]},
    "postgresql": {"category": "data", "prerequisites": ["sql"], "estimated_hours": 18,
                   "evidence": ["schema design", "index rationale", "query optimization"]},
    "react": {"category": "web", "prerequisites": [], "estimated_hours": 30,
              "evidence": ["accessible component", "loading and error states", "component tests"]},
    "typescript": {"category": "programming", "prerequisites": ["javascript"], "estimated_hours": 18,
                   "evidence": ["typed API boundary", "strict compiler configuration", "generic utility"]},
    "javascript": {"category": "programming", "prerequisites": [], "estimated_hours": 24,
                   "evidence": ["async flow", "error handling", "browser interaction"]},
    "docker": {"category": "operations", "prerequisites": [], "estimated_hours": 16,
               "evidence": ["reproducible image", "health check", "non-root container"]},
    "ci/cd": {"category": "operations", "prerequisites": ["git", "testing"], "estimated_hours": 20,
              "evidence": ["automated checks", "build artifact", "failure visibility"]},
    "data analysis": {"category": "data", "prerequisites": ["sql"], "estimated_hours": 25,
                      "evidence": ["cleaning notebook", "reproducible chart", "caveated conclusions"]},
    "machine learning": {"category": "data", "prerequisites": ["python", "data analysis"], "estimated_hours": 45,
                         "evidence": ["baseline model", "holdout evaluation", "error analysis"]},
    "security": {"category": "security", "prerequisites": ["rest api"], "estimated_hours": 25,
                 "evidence": ["threat model", "authorization tests", "dependency review"]},
}

def normalize_skill(value):
    text = str(value or "").strip().lower()
    if not text:
        raise ValueError("Skill name cannot be empty")
    return " ".join(text.split())

def validate_catalog(catalog: Mapping | None = None) -> dict:
    catalog = catalog or DEFAULT_CATALOG
    normalized = {normalize_skill(key): value for key, value in catalog.items()}
    errors = []
    for name, item in normalized.items():
        if not isinstance(item, Mapping):
            errors.append({"skill": name, "error": "catalog_item_not_mapping"})
            continue
        hours = item.get("estimated_hours", 1)
        if not isinstance(hours, (int, float)) or hours <= 0:
            errors.append({"skill": name, "error": "invalid_estimated_hours"})
        for prerequisite in item.get("prerequisites", []):
            prerequisite = normalize_skill(prerequisite)
            if prerequisite not in normalized:
                errors.append({"skill": name, "error": "unknown_prerequisite", "prerequisite": prerequisite})
    if not errors:
        errors.extend(detect_dependency_cycles(normalized))
    return {"valid": not errors, "skill_count": len(normalized), "errors": errors}

def detect_dependency_cycles(catalog: Mapping | None = None) -> list[dict]:
    catalog = catalog or DEFAULT_CATALOG
    graph = {normalize_skill(name): [normalize_skill(value) for value in item.get("prerequisites", [])]
             for name, item in catalog.items()}
    visiting, visited, stack, cycles = set(), set(), [], []
    def visit(node):
        if node in visiting:
            start = stack.index(node) if node in stack else 0
            cycle = stack[start:] + [node]
            cycles.append({"error": "dependency_cycle", "path": cycle})
            return
        if node in visited:
            return
        visiting.add(node)
        stack.append(node)
        for dependency in graph.get(node, []):
            if dependency in graph:
                visit(dependency)
        stack.pop()
        visiting.remove(node)
        visited.add(node)
    for node in sorted(graph):
        visit(node)
    unique, result = set(), []
    for cycle in cycles:
        key = tuple(cycle["path"])
        if key not in unique:
            unique.add(key)
            result.append(cycle)
    return result

def topological_learning_order(skills: Iterable[str], catalog: Mapping | None = None) -> dict:
    catalog = catalog or DEFAULT_CATALOG
    catalog = {normalize_skill(name): value for name, value in catalog.items()}
    targets = {normalize_skill(skill) for skill in skills}
    unknown = sorted(targets - set(catalog))
    if unknown:
        raise ValueError("Unknown skills: " + ", ".join(unknown))
    closure = set()
    def add_with_prerequisites(skill):
        if skill in closure:
            return
        closure.add(skill)
        for dependency in catalog[skill].get("prerequisites", []):
            dependency = normalize_skill(dependency)
            if dependency not in catalog:
                raise ValueError(f"Unknown prerequisite {dependency} for {skill}")
            add_with_prerequisites(dependency)
    for target in targets:
        add_with_prerequisites(target)
    cycle_errors = detect_dependency_cycles({key: catalog[key] for key in closure})
    if cycle_errors:
        raise ValueError("Skill prerequisite graph contains a cycle")
    indegree = {skill: 0 for skill in closure}
    children = defaultdict(list)
    for skill in closure:
        for dependency in catalog[skill].get("prerequisites", []):
            dependency = normalize_skill(dependency)
            if dependency in closure:
                indegree[skill] += 1
                children[dependency].append(skill)
    queue = deque(sorted(skill for skill, degree in indegree.items() if degree == 0))
    order = []
    while queue:
        skill = queue.popleft()
        order.append(skill)
        for child in sorted(children[skill]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(closure):
        raise ValueError("Could not construct learning order")
    return {"requested_skills": sorted(targets), "learning_order": order,
            "prerequisite_count": len(closure - targets), "total_skill_count": len(closure)}

def estimate_roadmap(skills: Iterable[str], weekly_hours: float = 5,
                     current_levels: Mapping | None = None, catalog: Mapping | None = None) -> dict:
    if not isinstance(weekly_hours, (int, float)) or weekly_hours <= 0 or weekly_hours > 80:
        raise ValueError("weekly_hours must be greater than 0 and at most 80")
    catalog = catalog or DEFAULT_CATALOG
    order = topological_learning_order(skills, catalog)
    levels = current_levels or {}
    items, total_hours = [], 0.0
    for skill in order["learning_order"]:
        data = catalog[skill]
        current = levels.get(skill, "new")
        if isinstance(current, int):
            current_level = current
        else:
            if str(current).lower() not in SKILL_LEVELS:
                raise ValueError(f"Unknown proficiency level for {skill}")
            current_level = SKILL_LEVELS[str(current).lower()]
        if not 0 <= current_level <= 4:
            raise ValueError("Proficiency level must be between 0 and 4")
        base = float(data.get("estimated_hours", 1))
        remaining = round(base * (4 - current_level) / 4, 2)
        total_hours += remaining
        items.append({"skill": skill, "category": data.get("category", "general"),
                      "current_level": current_level, "estimated_hours": remaining,
                      "weeks_at_budget": round(remaining / weekly_hours, 2),
                      "prerequisites": list(data.get("prerequisites", [])),
                      "evidence_ideas": list(data.get("evidence", []))})
    return {"learning_order": order["learning_order"], "items": items, "total_hours": round(total_hours, 2),
            "weekly_hours": weekly_hours, "estimated_weeks": round(total_hours / weekly_hours, 2),
            "prerequisite_count": order["prerequisite_count"],
            "disclaimer": "Estimates vary by prior experience; demonstrate skill with real work rather than hours alone."}

def skill_gap_report(required_skills: Iterable[str], current_levels: Mapping,
                     target_level: int = 2, catalog: Mapping | None = None) -> dict:
    if not isinstance(target_level, int) or not 0 <= target_level <= 4:
        raise ValueError("target_level must be between 0 and 4")
    catalog = catalog or DEFAULT_CATALOG
    required = sorted({normalize_skill(skill) for skill in required_skills})
    known = {normalize_skill(key): value for key, value in current_levels.items()}
    gaps, strengths, unknown = [], [], []
    for skill in required:
        value = known.get(skill, "new")
        level = value if isinstance(value, int) else SKILL_LEVELS.get(str(value).lower(), None)
        if level is None or not 0 <= level <= 4:
            unknown.append(skill)
            continue
        item = {"skill": skill, "current_level": level, "target_level": target_level,
                "gap": max(0, target_level - level)}
        if item["gap"]:
            item["estimated_hours"] = round(float(catalog.get(skill, {}).get("estimated_hours", 10)) * item["gap"] / 4, 2)
            gaps.append(item)
        else:
            strengths.append(item)
    gaps.sort(key=lambda item: (-item["gap"], -item["estimated_hours"], item["skill"]))
    return {"required_count": len(required), "gap_count": len(gaps), "strength_count": len(strengths),
            "unknown_level_skills": unknown, "gaps": gaps, "strengths": strengths,
            "note": "Self-assessed levels are approximate and should be validated with evidence."}

def evidence_portfolio_plan(skills: Iterable[str], catalog: Mapping | None = None) -> list[dict]:
    catalog = catalog or DEFAULT_CATALOG
    output = []
    for skill in sorted({normalize_skill(value) for value in skills}):
        item = catalog.get(skill)
        if not item:
            output.append({"skill": skill, "project_ideas": [], "catalog_missing": True})
            continue
        evidence = item.get("evidence", [])
        output.append({"skill": skill, "project_ideas": [
            {"title": f"Demonstrate {skill}: {idea}", "evidence": idea,
             "verification": "Include a README, reproducible steps, and truthful notes about your contribution."}
            for idea in evidence], "catalog_missing": False})
    return output

def weekly_learning_review(plan: Mapping, completed: Iterable[Mapping], week_label: str = "") -> dict:
    planned = {item.get("skill"): item for item in plan.get("items", [])}
    completed_by_skill = defaultdict(list)
    for record in completed:
        skill = normalize_skill(record.get("skill"))
        hours = record.get("hours", 0)
        try:
            hours = float(hours)
        except (ValueError, TypeError):
            raise ValueError("Completed learning hours must be numeric")
        if hours < 0 or hours > 168:
            raise ValueError("Completed learning hours must be between 0 and 168")
        completed_by_skill[skill].append({"hours": hours, "evidence": str(record.get("evidence") or "")[:500]})
    result = []
    for skill, item in sorted(planned.items()):
        records = completed_by_skill.get(skill, [])
        hours = round(sum(row["hours"] for row in records), 2)
        result.append({"skill": skill, "planned_hours": item.get("estimated_hours", 0),
                       "completed_hours": hours, "evidence_entries": len(records),
                       "evidence_missing": bool(hours and not any(row["evidence"] for row in records))})
    return {"week": str(week_label)[:80], "skills_reviewed": len(result),
            "total_completed_hours": round(sum(row["completed_hours"] for row in result), 2),
            "skills": result, "note": "Log evidence and outcomes, not just time spent."}
