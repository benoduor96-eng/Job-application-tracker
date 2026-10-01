from datetime import date, timedelta

from django.test import TestCase

from apps.jobs.models import JobApplication, CareerProfile
from apps.jobs.recommendations import RecommendationEngine


class RecommendationEngineTests(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.profile = CareerProfile.objects.create(
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
            requirements="python django postgres docker api system design aws",
            next_action_date=date.today() + timedelta(days=3),
        )

    def make_user(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.create_user(username="reco", password="secret123")

    def test_profile_summary(self):
        engine = RecommendationEngine(self.user)
        summary = engine.build_profile_summary()
        self.assertTrue(summary["exists"])

    def test_score_application_fit(self):
        engine = RecommendationEngine(self.user)
        score = engine.score_application_fit(self.app)
        self.assertGreater(score, 0)

    def test_rank_actions(self):
        engine = RecommendationEngine(self.user)
        actions = engine.rank_actions()
        self.assertTrue(actions)
