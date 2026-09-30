from datetime import date, timedelta
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from apps.jobs.career_intelligence import (
    CareerDashboardService,
    FollowUpPlanner,
    JobDescriptionAnalyzer,
    JobMatchingEngine,
    PipelinePrioritizer,
    extract_keywords,
    extract_skills,
    location_fit,
    normalize_skill,
    normalize_skills,
    salary_fit,
)
from apps.jobs.models import CareerProfile, CareerTask, JobApplication, JobDescription


User = get_user_model()


@pytest.mark.django_db
class TestSkillUtilities:
    def test_normalize_aliases(self):
        assert normalize_skill("SpringBoot") == "spring boot"
        assert normalize_skill("POSTGRES") == "postgresql"
        assert normalize_skill("ReactJS") == "react"

    def test_normalize_skills_accepts_text(self):
        result = normalize_skills("Python, Django; PostgreSQL")
        assert result == {"python", "django", "postgresql"}

    def test_extract_skills_is_deterministic(self):
        text = "We use Python, Django, PostgreSQL and Docker."
        assert extract_skills(text) == ["django", "docker", "postgresql", "python"]

    def test_extract_keywords_returns_repeated_terms_first(self):
        result = extract_keywords(
            "python python django testing testing testing api delivery"
        )
        assert result[0] == "testing"
        assert "python" in result


@pytest.mark.django_db
class TestScoringHelpers:
    def test_salary_fit_inside_range(self):
        assert salary_fit(50000, 80000, 65000) == 1.0

    def test_salary_fit_missing_target_is_neutral(self):
        assert salary_fit(50000, 80000, None) == 0.5

    def test_location_fit_exact_match(self):
        assert location_fit(["Nairobi"], "Nairobi, Kenya") == 1.0

    def test_remote_location_matches_remote_preference(self):
        assert location_fit([], "Remote - Africa", "remote") == 1.0


@pytest.mark.django_db
class TestMatchingEngine:
    def setup_user(self):
        return User.objects.create_user(username="matcher", password="test-pass-123")

    def test_required_skill_score_uses_profile(self):
        user = self.setup_user()
        profile = CareerProfile.objects.create(
            user=user,
            skills=["python", "django", "postgresql"],
            preferred_roles=["Backend Developer"],
            preferred_locations=["Nairobi"],
            target_salary=Decimal("70000"),
        )
        result = JobMatchingEngine(profile).score(
            ["python", "django"],
            ["docker"],
            role="Backend Developer",
            location="Nairobi",
            salary_min=Decimal("60000"),
            salary_max=Decimal("90000"),
        )
        assert result.required_score == 100.0
        assert result.missing_required == ()
        assert "docker" not in result.matched_required
        assert result.score > 70

    def test_missing_required_skills_are_reported(self):
        user = self.setup_user()
        profile = CareerProfile.objects.create(
            user=user,
            skills=["python"],
        )
        result = JobMatchingEngine(profile).score(
            ["python", "kubernetes"],
            [],
        )
        assert result.missing_required == ("kubernetes",)
        assert any("kubernetes" in item for item in result.recommendations)


@pytest.mark.django_db
class TestDescriptionAnalyzer:
    def setup_description(self):
        user = User.objects.create_user(username="analyst", password="test-pass-123")
        return JobDescription.objects.create(
            user=user,
            title="Backend Engineer",
            company="Example",
            raw_text="Python Django PostgreSQL Docker API testing",
        )

    def test_analyze_populates_skills_and_keywords(self):
        description = self.setup_description()
        result = JobDescriptionAnalyzer().analyze(description)
        assert "python" in result.required_skills
        assert "django" in result.required_skills
        assert result.extracted_keywords
        assert result.analyzed_at is not None

    def test_preview_does_not_require_database_record(self):
        result = JobDescriptionAnalyzer().preview(
            "Senior Python engineer working with Django and PostgreSQL"
        )
        assert result["skill_count"] >= 3
        assert "python" in result["skills"]


@pytest.mark.django_db
class TestFollowUpPlanner:
    def setup_application(self, status="applied"):
        user = User.objects.create_user(username="planner", password="test-pass-123")
        return JobApplication.objects.create(
            user=user,
            company="Example",
            role="Engineer",
            status=status,
            applied_date=date(2026, 9, 1),
        )

    def test_applied_application_gets_follow_up(self):
        application = self.setup_application()
        plan = FollowUpPlanner(today=date(2026, 9, 8)).plan_for(application)
        assert plan is not None
        assert plan.due_date == date(2026, 9, 8)
        assert plan.priority == "medium"

    def test_rejected_application_has_no_follow_up(self):
        application = self.setup_application(status="rejected")
        assert FollowUpPlanner().plan_for(application) is None

    def test_create_tasks_skips_duplicate_open_task(self):
        application = self.setup_application()
        application.user
        CareerTask.objects.create(
            user=application.user,
            application=application,
            title="Check application status",
            status="todo",
        )
        tasks = FollowUpPlanner(today=date(2026, 9, 8)).create_tasks([application])
        assert tasks == []


@pytest.mark.django_db
class TestPipelinePrioritizer:
    def setup_user(self):
        return User.objects.create_user(username="priority", password="test-pass-123")

    def test_offer_has_high_base_priority(self):
        user = self.setup_user()
        application = JobApplication.objects.create(
            user=user,
            company="Example",
            role="Engineer",
            status="offer",
        )
        result = PipelinePrioritizer().score(application)
        assert result.score >= 100
        assert result.urgency == "normal"

    def test_overdue_action_increases_priority(self):
        user = self.setup_user()
        application = JobApplication.objects.create(
            user=user,
            company="Example",
            role="Engineer",
            status="applied",
            next_action_date=date(2026, 9, 1),
        )
        result = PipelinePrioritizer().score(application, today=date(2026, 9, 10))
        assert result.urgency == "overdue"
        assert result.score > 55
        assert "next action is overdue" in result.reasons

    def test_prioritize_sorts_descending(self):
        user = self.setup_user()
        low = JobApplication.objects.create(
            user=user, company="A", role="Engineer", status="saved"
        )
        high = JobApplication.objects.create(
            user=user, company="B", role="Engineer", status="interview"
        )
        results = PipelinePrioritizer().prioritize([low, high])
        assert results[0].application_id == high.id


@pytest.mark.django_db
class TestCareerDashboard:
    def test_summary_counts_active_and_total(self):
        user = User.objects.create_user(username="dashboard", password="test-pass-123")
        JobApplication.objects.create(
            user=user, company="A", role="Engineer", status="applied"
        )
        JobApplication.objects.create(
            user=user, company="B", role="Engineer", status="rejected"
        )
        payload = CareerDashboardService(user).summary()
        assert payload["total_applications"] == 2
        assert payload["active_applications"] == 1
        assert payload["status_counts"]["applied"] == 1
        assert payload["status_counts"]["rejected"] == 1
        assert len(payload["priority_items"]) == 2
