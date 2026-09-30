from apps.jobs.interview_catalog import INTERVIEW_PROMPTS, find_interview_prompts, prompts_for_role
from apps.jobs.role_catalog import ROLES, roles_for_skills, search_roles


def test_role_catalog_has_substantial_coverage():
    assert len(ROLES) >= 400
    assert len({role.title for role in ROLES}) >= 100


def test_role_catalog_has_complete_metadata():
    for role in ROLES[:100]:
        assert role.domain
        assert role.seniority
        assert role.skills
        assert role.keywords
        assert role.responsibilities
        assert role.interview_focus


def test_role_search_returns_ranked_results():
    results = search_roles("python django backend", limit=10)
    assert results
    assert len(results) <= 10
    assert any("Backend" in role.title for role in results)


def test_role_skill_overlap_is_bounded():
    for role in ROLES[:50]:
        score = role.skill_overlap(["python", "django", "unknown"])
        assert 0.0 <= score <= 1.0


def test_role_matching_uses_keywords():
    role = ROLES[0]
    assert role.matches("experienced " + role.keywords[0])


def test_skill_search_returns_only_matching_roles():
    results = roles_for_skills(["python", "django"], limit=25)
    assert results
    assert all(role.skill_overlap(["python", "django"]) > 0 for role in results)


def test_interview_catalog_has_substantial_coverage():
    assert len(INTERVIEW_PROMPTS) >= 1000


def test_interview_prompts_have_required_signals():
    for prompt in INTERVIEW_PROMPTS[:100]:
        assert prompt.category
        assert prompt.role
        assert prompt.seniority
        assert prompt.question
        assert len(prompt.signals) >= 3
        assert len(prompt.follow_ups) >= 2


def test_interview_search_is_limited():
    results = find_interview_prompts("backend senior architecture", limit=12)
    assert len(results) <= 12
    assert results


def test_interview_search_returns_relevant_text():
    results = find_interview_prompts("security", limit=20)
    assert any("security" in item.search_text() for item in results)


def test_role_specific_interview_lookup():
    results = prompts_for_role("backend", "senior", limit=15)
    assert len(results) <= 15
    assert results
    assert all(item.role == "backend" for item in results)


def test_role_specific_interview_lookup_without_seniority():
    results = prompts_for_role("frontend", limit=20)
    assert results
    assert all(item.role == "frontend" for item in results)


def test_interview_search_handles_unknown_terms():
    assert find_interview_prompts("zzzz-not-a-real-career-term", limit=5) == []


def test_role_search_handles_unknown_terms():
    assert search_roles("zzzz-not-a-real-role", limit=5) == []


def test_catalog_records_are_immutable():
    role = ROLES[0]
    prompt = INTERVIEW_PROMPTS[0]
    assert role.title
    assert prompt.question
