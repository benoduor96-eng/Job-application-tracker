from datetime import date, timedelta

from django.test import TestCase

from apps.jobs.models import JobApplication, CareerProfile, JobDescription
from apps.jobs.recommendations import RecommendationEngine


class RecommendationEngineTests(TestCase):
    def setUp(self):
        self.user = self.make_user()
        CareerProfile.objects.create(
            user=self.user,
            headline="Senior Python engineer",
            professional_summary="Python, Django, APIs, team leadership",
            skills=["python", "django", "postgresql", "docker", "aws"],
            preferred_roles=["backend engineer", "platform engineer"],
            preferred_locations=["remote", "london"],
            work_preference="remote",
        )
        self.app = JobApplication.objects.create(
            user=self.user,
            company="Acme",
            role="Backend Engineer",
            status="applied",
            next_action_date=date.today() + timedelta(days=3),
        )
        JobDescription.objects.create(
            user=self.user,
            application=self.app,
            title="Backend Engineer",
            company="Acme",
            raw_text="python django postgres docker api system design aws",
            required_skills=["python", "django", "postgresql", "docker", "aws"],
        )

    def make_user(self):
        from django.contrib.auth import get_user_model
        return get_user_model().objects.create_user(username="reco", password="secret123")

    def test_profile_summary(self):
        summary = RecommendationEngine(self.user).build_profile_summary()
        self.assertTrue(summary["exists"])

    def test_score_application_fit(self):
        score = RecommendationEngine(self.user).score_application_fit(self.app)
        self.assertGreater(score, 0)

    def test_rank_actions(self):
        actions = RecommendationEngine(self.user).rank_actions()
        self.assertTrue(actions)
