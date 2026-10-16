"""Tests for structured career decision journaling."""
from datetime import date
from django.test import SimpleTestCase
from apps.jobs.career_decision_log import (
    decision_patterns, decision_review_queue, decision_template, validate_decision,
)

class CareerDecisionLogTests(SimpleTestCase):
    def test_decision_requires_supported_choice_and_rationale(self):
        with self.assertRaises(ValueError):
            validate_decision({"decision": "maybe", "rationale": "Some rationale"})
        with self.assertRaises(ValueError):
            validate_decision({"decision": "apply", "rationale": "no"})

    def test_decision_validates_certainty(self):
        with self.assertRaises(ValueError):
            validate_decision({"decision": "apply", "rationale": "I meet the requirements", "certainty": 9})

    def test_review_queue_includes_due_or_flagged_decisions(self):
        result = decision_review_queue([
            {"id": 1, "decision": "research", "rationale": "Need to check company", "review_date": "2026-01-01"},
            {"id": 2, "decision": "pause", "rationale": "Wait for more details", "revisit": True},
            {"id": 3, "decision": "apply", "rationale": "Good match", "review_date": "2027-01-01"},
        ], today=date(2026, 2, 1))
        self.assertEqual({row["id"] for row in result}, {1, 2})

    def test_patterns_count_evidence_and_certainty(self):
        result = decision_patterns([
            {"decision": "apply", "rationale": "Strong skills match", "certainty": 4, "evidence": ["portfolio"]},
            {"decision": "pause", "rationale": "Need written contract", "certainty": 2},
        ])
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["average_certainty"], 3)
        self.assertEqual(result["with_evidence"], 1)

    def test_template_does_not_persist(self):
        self.assertFalse(decision_template(4)["saved"])
