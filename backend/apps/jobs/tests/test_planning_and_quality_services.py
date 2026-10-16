"""Regression tests for skill roadmaps, offer comparison, and timeline helpers."""
from django.test import SimpleTestCase
from apps.jobs.skill_roadmap import (
    detect_dependency_cycles, estimate_roadmap, evidence_portfolio_plan,
    skill_gap_report, topological_learning_order, validate_catalog, weekly_learning_review,
)
from apps.jobs.offer_evaluation import (
    compare_compensation, compare_offers, negotiation_preparation, offer_missing_information,
    validate_offer, weighted_offer_score,
)
from apps.jobs.application_timeline import (
    chronological_events, events_by_month, merge_timeline_preview, timeline_gaps,
    timeline_integrity_report, timeline_summary,
)

class SkillRoadmapTests(SimpleTestCase):
    def test_catalog_is_valid(self):
        self.assertTrue(validate_catalog()["valid"])

    def test_dependency_order_includes_prerequisites(self):
        result = topological_learning_order(["django"])
        self.assertLess(result["learning_order"].index("python"), result["learning_order"].index("django"))
        self.assertEqual(result["prerequisite_count"], 1)

    def test_unknown_skill_and_cycle_are_rejected(self):
        with self.assertRaises(ValueError):
            topological_learning_order(["unknown"])
        cycle = {"a": {"prerequisites": ["b"]}, "b": {"prerequisites": ["a"]}}
        self.assertTrue(detect_dependency_cycles(cycle))

    def test_roadmap_estimates_hours_and_weeks(self):
        result = estimate_roadmap(["django"], weekly_hours=5)
        self.assertGreater(result["total_hours"], 0)
        self.assertGreater(result["estimated_weeks"], 0)

    def test_roadmap_rejects_invalid_weekly_budget(self):
        with self.assertRaises(ValueError):
            estimate_roadmap(["python"], weekly_hours=0)

    def test_skill_gap_separates_gaps_and_strengths(self):
        result = skill_gap_report(["python", "django"], {"python": "advanced"}, target_level=2)
        self.assertEqual(result["strength_count"], 1)
        self.assertEqual(result["gap_count"], 1)
        self.assertEqual(result["gaps"][0]["skill"], "django")

    def test_evidence_plan_is_truthful_and_actionable(self):
        result = evidence_portfolio_plan(["python", "unknown"])
        self.assertTrue(result[0]["project_ideas"])
        self.assertTrue(any(row["catalog_missing"] for row in result))

    def test_weekly_review_sums_completed_hours(self):
        plan = {"items": [{"skill": "python", "estimated_hours": 10}]}
        result = weekly_learning_review(plan, [{"skill": "python", "hours": 2, "evidence": "small script"}], "week 1")
        self.assertEqual(result["total_completed_hours"], 2)
        self.assertFalse(result["skills"][0]["evidence_missing"])

class OfferEvaluationTests(SimpleTestCase):
    def setUp(self):
        self.offer_a = {"id": 1, "name": "Offer A", "currency": "USD", "annual_base_salary": 80000,
                        "compensation": 5, "benefits": 3, "growth": 4, "role_fit": 4,
                        "flexibility": 3, "stability": 4, "values": 4}
        self.offer_b = {"id": 2, "name": "Offer B", "currency": "USD", "annual_base_salary": 90000,
                        "compensation": 4, "benefits": 4, "growth": 3, "role_fit": 3,
                        "flexibility": 5, "stability": 3, "values": 4}

    def test_offer_validation_rejects_negative_salary(self):
        with self.assertRaises(ValueError):
            validate_offer({"name": "A", "annual_base_salary": -1})

    def test_weighted_score_discloses_missing_criteria(self):
        result = weighted_offer_score({"name": "A", "compensation": 5})
        self.assertIn("missing_weighted_criteria", result)
        self.assertLess(result["rated_weight_percent"], 100)

    def test_comparison_requires_two_offers(self):
        with self.assertRaises(ValueError):
            compare_offers([self.offer_a])

    def test_offer_comparison_uses_ratings(self):
        result = compare_offers([self.offer_a, self.offer_b])
        self.assertEqual(len(result["offers"]), 2)
        self.assertIn("decision aid", result["disclaimer"])

    def test_compensation_comparison_refuses_mixed_currencies(self):
        result = compare_compensation([self.offer_a, {**self.offer_b, "currency": "KES"}])
        self.assertFalse(result["comparable"])

    def test_negotiation_needs_priority_and_warns_against_misrepresentation(self):
        with self.assertRaises(ValueError):
            negotiation_preparation(self.offer_a, [])
        result = negotiation_preparation(self.offer_a, ["remote work"])
        self.assertIn("misrepresent", result["warning"])

    def test_missing_offer_information_is_exposed(self):
        result = offer_missing_information({"name": "Offer", "currency": "USD"})
        self.assertTrue(any(item["field"] == "annual_base_salary" for item in result))

class ApplicationTimelineTests(SimpleTestCase):
    def test_chronology_sorts_dated_events_before_undated(self):
        result = chronological_events([
            {"id": 2, "created_at": "2026-02-01", "type": "note"},
            {"id": 1, "created_at": "2026-01-01", "type": "status_change"},
            {"id": 3, "type": "note"},
        ])
        self.assertEqual([item["id"] for item in result], [1, 2, 3])

    def test_integrity_detects_discontinuous_status_chain(self):
        result = timeline_integrity_report([
            {"id": 1, "event_type": "status_change", "from_status": "saved", "to_status": "applied",
             "occurred_at": "2026-01-01"},
            {"id": 2, "event_type": "status_change", "from_status": "interview", "to_status": "offer",
             "occurred_at": "2026-01-02"},
        ], initial_status="saved")
        self.assertFalse(result["consistent"])
        self.assertTrue(any(item["code"] == "status_chain_discontinuity" for item in result["issues"]))

    def test_summary_counts_missing_timestamps(self):
        result = timeline_summary([{"id": 1, "created_at": "2026-01-01"}, {"id": 2}])
        self.assertEqual(result["undated_event_count"], 1)

    def test_monthly_report_groups_event_types(self):
        result = events_by_month([
            {"created_at": "2026-01-02", "type": "note"},
            {"created_at": "2026-01-03", "type": "note"},
            {"created_at": "2026-02-03", "type": "status_change"},
        ])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["by_type"]["note"], 2)

    def test_merge_preview_never_persists_and_flags_duplicates(self):
        event = {"type": "note", "created_at": "2026-01-01", "description": "Applied"}
        result = merge_timeline_preview([event], [event, {"type": "note", "created_at": "2026-01-02"}])
        self.assertEqual(len(result["possible_duplicates"]), 1)
        self.assertFalse(result["persisted"])

    def test_gaps_require_valid_threshold(self):
        result = timeline_gaps([
            {"id": 1, "created_at": "2026-01-01"},
            {"id": 2, "created_at": "2026-03-10"},
        ], threshold_days=30)
        self.assertEqual(len(result), 1)
        with self.assertRaises(ValueError):
            timeline_gaps([], threshold_days=0)
