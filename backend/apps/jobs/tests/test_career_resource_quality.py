"""Tests for learning-resource quality and duplicate-review helpers."""
from django.test import SimpleTestCase
from apps.jobs.career_resource_quality import duplicate_resource_groups, resource_quality, resource_review_queue

class CareerResourceQualityTests(SimpleTestCase):
    def test_quality_flags_missing_metadata(self):
        result = resource_quality({"id": 1, "title": "Python course"})
        self.assertIn("missing_url", result["issues"])
        self.assertTrue(result["review_recommended"])

    def test_complete_resource_has_no_issues(self):
        result = resource_quality({"title": "Guide", "url": "https://example.test",
                                   "skills": ["python"], "provider": "Public docs", "notes": "Useful reference"})
        self.assertEqual(result["issues"], [])
        self.assertEqual(result["quality_percent"], 100)

    def test_duplicate_groups_require_manual_review(self):
        result = duplicate_resource_groups([
            {"id": 1, "title": "Python Guide", "url": "https://example.test/"},
            {"id": 2, "title": "Python Guide", "url": "https://example.test/"},
        ])
        self.assertEqual(result[0]["count"], 2)
        self.assertTrue(result[0]["manual_review_required"])

    def test_review_queue_never_deletes(self):
        result = resource_review_queue([{"title": "Draft"}])
        self.assertFalse(result["automatic_deletions_performed"])
        self.assertEqual(result["resource_count"], 1)
