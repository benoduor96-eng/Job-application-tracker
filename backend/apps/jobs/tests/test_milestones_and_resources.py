"""Tests for milestone dependencies and learning-resource planning."""
from datetime import date
from django.test import SimpleTestCase
from apps.jobs.application_milestones import (
    dependency_report, milestone_progress, milestone_review, propose_milestones, validate_milestone,
)
from apps.jobs.career_resource_library import (
    rank_resources, resource_learning_queue, resource_progress, validate_resource,
)

class MilestoneTests(SimpleTestCase):
    def test_milestone_requires_title_and_known_status(self):
        with self.assertRaises(ValueError):
            validate_milestone({"title": ""})
        with self.assertRaises(ValueError):
            validate_milestone({"title": "Apply", "status": "done"})

    def test_progress_counts_completed_and_overdue(self):
        result = milestone_progress([
            {"id": 1, "title": "Old", "due_date": "2026-01-01", "status": "planned"},
            {"id": 2, "title": "Done", "due_date": "2026-01-01", "status": "completed"},
        ], today=date(2026, 1, 5))
        self.assertEqual(result["overdue_count"], 1)
        self.assertEqual(result["completion_percent"], 50)

    def test_dependency_report_finds_missing_dependency(self):
        result = dependency_report([{"id": 1, "title": "Task", "dependencies": [2]}])
        self.assertFalse(result["valid"])
        self.assertEqual(result["errors"][0]["code"], "missing_dependency")

    def test_dependency_report_finds_cycle(self):
        result = dependency_report([
            {"id": 1, "title": "A", "dependencies": [2]},
            {"id": 2, "title": "B", "dependencies": [1]},
        ])
        self.assertFalse(result["valid"])
        self.assertTrue(any(error["code"] == "dependency_cycle" for error in result["errors"]))

    def test_proposal_is_not_persisted(self):
        result = propose_milestones(5, "Acme", "Analyst", date(2026, 1, 1))
        self.assertEqual(len(result), 5)
        self.assertFalse(result[0]["persisted"])

    def test_review_does_not_update_records(self):
        result = milestone_review([{"id": 1, "title": "Task", "status": "blocked"}])
        self.assertFalse(result["automatic_updates_performed"])
        self.assertEqual(len(result["blocked"]), 1)

class ResourceLibraryTests(SimpleTestCase):
    def test_resource_validates_url_type_and_rating(self):
        with self.assertRaises(ValueError):
            validate_resource({"title": "Unsafe", "url": "javascript:alert(1)"})
        with self.assertRaises(ValueError):
            validate_resource({"title": "Book", "rating": 8})

    def test_rank_resources_matches_skills_and_type(self):
        result = rank_resources([
            {"id": 1, "title": "Python guide", "skills": ["python"], "resource_type": "article"},
            {"id": 2, "title": "SQL book", "skills": ["sql"], "resource_type": "book"},
        ], ["python"], ["article"])
        self.assertEqual(result[0]["resource"]["id"], 1)

    def test_queue_respects_time_budget(self):
        result = resource_learning_queue([
            {"id": 1, "title": "Short", "estimated_minutes": 30},
            {"id": 2, "title": "Long", "estimated_minutes": 90},
        ], available_minutes=60)
        self.assertEqual(result["planned_minutes"], 30)
        self.assertEqual(len(result["deferred"]), 1)

    def test_progress_counts_completed_skills(self):
        result = resource_progress([
            {"title": "Guide", "skills": ["python"], "status": "completed", "estimated_minutes": 60},
            {"title": "Course", "skills": ["sql"], "status": "saved", "estimated_minutes": 90},
        ])
        self.assertEqual(result["completed_hours"], 1)
        self.assertEqual(result["skills_touched"], ["python"])

    def test_queue_rejects_invalid_budget(self):
        with self.assertRaises(ValueError):
            resource_learning_queue([], available_minutes=-1)
