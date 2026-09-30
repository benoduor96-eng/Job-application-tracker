from django.contrib.auth import get_user_model
from django.test import TestCase

from .application_matching import find_possible_duplicates
from .models import JobApplication


class ApplicationMatchingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="matcher",
            password="test-password",
        )

    def test_detects_same_job_url(self):
        first = JobApplication.objects.create(
            user=self.user,
            company="Acme Labs",
            role="Backend Engineer",
            job_url="https://jobs.example.com/acme/backend",
        )
        duplicate = JobApplication.objects.create(
            user=self.user,
            company="Acme Labs",
            role="Backend Engineer",
            job_url="https://jobs.example.com/acme/backend",
        )

        matches = find_possible_duplicates(first, JobApplication.objects.all())

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].application_id, duplicate.id)
        self.assertIn("same job URL", matches[0].reasons)

    def test_does_not_compare_other_users(self):
        other = get_user_model().objects.create_user(
            username="other-matcher",
            password="test-password",
        )
        first = JobApplication.objects.create(
            user=self.user,
            company="Acme Labs",
            role="Backend Engineer",
        )
        JobApplication.objects.create(
            user=other,
            company="Acme Labs",
            role="Backend Engineer",
        )

        matches = find_possible_duplicates(
            first,
            JobApplication.objects.filter(user=self.user),
        )
        self.assertEqual(matches, [])
