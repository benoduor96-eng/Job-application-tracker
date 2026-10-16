"""Tests for interview practice and consent-aware networking helpers."""
from datetime import date
from django.test import SimpleTestCase
from apps.jobs.interview_practice import (
    answer_review, build_interview_agenda, follow_up_questions, generate_practice_set,
    parse_star_answer, preparation_checklist, question_bank, question_coverage,
)
from apps.jobs.networking_pipeline import (
    contact_health, find_contact_duplicates, networking_week_summary,
    outreach_message_outline, plan_touchpoint, rank_networking_contacts,
    relationship_maintenance_report, validate_contact,
)

class InterviewPracticeTests(SimpleTestCase):
    def test_question_bank_has_supported_categories(self):
        self.assertTrue(question_bank("technical"))
        with self.assertRaises(ValueError):
            question_bank("astrology")

    def test_practice_set_is_reproducible_with_seed(self):
        first = generate_practice_set(["behavioral", "technical"], 5, seed=12)
        second = generate_practice_set(["behavioral", "technical"], 5, seed=12)
        self.assertEqual(first["questions"], second["questions"])
        self.assertEqual(len(first["questions"]), 5)

    def test_practice_set_rejects_invalid_count(self):
        with self.assertRaises(ValueError):
            generate_practice_set(count=0)

    def test_star_parser_finds_missing_sections(self):
        result = parse_star_answer("Situation: outage\\nTask: restore service\\nAction: I checked logs")
        self.assertEqual(result["missing_sections"], ["result"])
        self.assertFalse(result["complete"])

    def test_star_template_reminds_truthful_evidence(self):
        result = parse_star_answer("Situation: x\\nTask: y\\nAction: z\\nResult: q")
        self.assertTrue(result["complete"])
        self.assertIn("truthful", str(__import__("apps.jobs.interview_practice", fromlist=["star_prompt_template"]).star_prompt_template()))

    def test_answer_review_returns_actionable_feedback(self):
        result = answer_review("I built a small service. I tested the endpoint, fixed a bug, and improved reliability.")
        self.assertIn("rubric_score", result)
        self.assertTrue(result["suggestions"])

    def test_agenda_minutes_sum_to_duration(self):
        for kind in ("behavioral", "technical", "mixed", "screening"):
            agenda = build_interview_agenda(47, kind)
            self.assertEqual(sum(item["minutes"] for item in agenda["agenda"]), 47)

    def test_agenda_rejects_invalid_duration(self):
        with self.assertRaises(ValueError):
            build_interview_agenda(10)

    def test_follow_up_questions_include_role_context(self):
        result = follow_up_questions("Data Analyst", "Acme", "technical")
        self.assertTrue(any("90 days" in item["question"] for item in result))
        self.assertTrue(any(item["topic"] == "engineering" for item in result))

    def test_question_coverage_finds_unpracticed_competencies(self):
        result = question_coverage([{"competencies": ["communication", "impact"]}])
        self.assertIn("problem_solving", result["uncovered_competencies"])
        self.assertEqual(result["competency_counts"]["impact"], 1)

    def test_checklist_includes_logistics_and_wellbeing(self):
        result = preparation_checklist()
        self.assertTrue(any(item["category"] == "logistics" for item in result))
        self.assertTrue(any(item["category"] == "wellbeing" for item in result))

class NetworkingPipelineTests(SimpleTestCase):
    def setUp(self):
        self.contact = {"id": 1, "name": "A Person", "company": "Acme", "role": "Recruiter",
                        "relationship": "recruiter", "next_follow_up_date": "2026-02-01",
                        "consent_status": "known"}

    def test_contact_validation_requires_name_and_known_relationship(self):
        with self.assertRaises(ValueError):
            validate_contact({"company": "Acme"})
        with self.assertRaises(ValueError):
            validate_contact({"name": "A", "relationship": "alien"})

    def test_contact_health_marks_overdue(self):
        result = contact_health(self.contact, today=date(2026, 2, 4))
        self.assertTrue(result["overdue"])
        self.assertEqual(result["state"], "follow_up_overdue")

    def test_opted_out_contacts_are_not_ranked(self):
        result = rank_networking_contacts([
            self.contact, {**self.contact, "id": 2, "consent_status": "opted_out"}], today=date(2026, 2, 4))
        self.assertEqual([item["id"] for item in result], [1])

    def test_touchpoint_rejects_opted_out_contact(self):
        with self.assertRaises(ValueError):
            plan_touchpoint({**self.contact, "consent_status": "do_not_contact"}, "message")

    def test_touchpoint_computes_date_without_persisting(self):
        result = plan_touchpoint(self.contact, "thank_you", occurred_on=date(2026, 1, 1))
        self.assertEqual(result["suggested_follow_up"], "2026-01-06")
        self.assertFalse(result["persistence_performed"])

    def test_networking_summary_counts_follow_ups_in_week(self):
        result = networking_week_summary([self.contact], start_date=date(2026, 2, 4))
        self.assertEqual(result["follow_ups_due"], 1)

    def test_duplicate_contacts_are_review_only(self):
        result = find_contact_duplicates([self.contact, {**self.contact, "id": 2}])
        self.assertEqual(result[0]["count"], 2)
        self.assertTrue(result[0]["requires_manual_review"])

    def test_outreach_requires_real_reason(self):
        with self.assertRaises(ValueError):
            outreach_message_outline(self.contact, "")
        result = outreach_message_outline(self.contact, "Ask about the public data analyst opening")
        self.assertIn("decline", " ".join(result["outline"]))

    def test_relationship_report_does_not_hide_unknown_consent(self):
        result = relationship_maintenance_report([self.contact, {**self.contact, "id": 2}], today=date(2026, 2, 4))
        self.assertEqual(result["consent_unknown"], 0)
        self.assertEqual(result["total_contacts"], 2)
