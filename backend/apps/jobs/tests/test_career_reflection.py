"""Tests for weekly reflection prompts and progress trends."""
from datetime import date
from django.test import SimpleTestCase
from apps.jobs.career_reflection import (
    propose_next_steps, reflection_quality, reflection_trends, validate_reflection,
)

class CareerReflectionTests(SimpleTestCase):
    def test_week_start_normalizes_to_monday(self):
        result = validate_reflection({"week_start": "2026-01-07"})
        self.assertEqual(result["week_start"], date(2026, 1, 5))

    def test_invalid_energy_rating_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_reflection({"week_start": "2026-01-05", "energy_rating": 9})

    def test_quality_reports_missing_areas(self):
        result = reflection_quality({"week_start": "2026-01-05", "responses": {"progress": "Applied to two roles"}})
        self.assertEqual(result["answered_areas"], 1)
        self.assertIn("wellbeing", result["missing_areas"])

    def test_next_steps_are_bounded_and_contextual(self):
        result = propose_next_steps({"week_start": "2026-01-05",
                                     "responses": {"barriers": "Need a quiet place to study"}})
        self.assertEqual(result[0]["source_area"], "barriers")
        with self.assertRaises(ValueError):
            propose_next_steps({"week_start": "2026-01-05"}, limit=0)

    def test_trends_do_not_claim_health_assessment(self):
        result = reflection_trends([{"week_start": "2026-01-05", "energy_rating": 3, "completed": True}])
        self.assertEqual(result["average_energy_rating"], 3)
        self.assertIn("not health assessments", result["note"])
