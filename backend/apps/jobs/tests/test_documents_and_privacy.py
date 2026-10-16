"""Tests for career document packet checks and privacy minimization."""
from django.test import SimpleTestCase
from apps.jobs.career_document_checklist import (
    application_packet_check, document_maintenance_queue, document_readiness, document_status_summary,
    validate_document,
)
from apps.jobs.job_search_privacy import (
    allowed_share_fields, classify_field, privacy_review, sanitize_share_payload,
    sharing_risk_report, validate_share_options,
)

class DocumentChecklistTests(SimpleTestCase):
    def test_document_requires_title_and_supported_status(self):
        with self.assertRaises(ValueError):
            validate_document({})
        with self.assertRaises(ValueError):
            validate_document({"title": "Resume", "status": "sent"})

    def test_ready_document_requires_reviews(self):
        result = document_readiness({"title": "Resume", "status": "ready",
                                     "confidentiality_reviewed": True, "personal_data_reviewed": True})
        self.assertTrue(result["ready"])

    def test_packet_requires_ready_document_type(self):
        result = application_packet_check([
            {"title": "Resume", "document_type": "resume", "status": "draft"}], ["resume", "cover_letter"])
        self.assertEqual(result["missing_ready_types"], ["cover_letter", "resume"])

    def test_maintenance_queue_identifies_blockers(self):
        result = document_maintenance_queue([{"id": 1, "title": "CV"}])
        self.assertGreaterEqual(len(result), 2)

    def test_summary_counts_status_and_type(self):
        result = document_status_summary([{"title": "CV", "document_type": "resume"}])
        self.assertEqual(result["by_type"]["resume"], 1)

class SharingPrivacyTests(SimpleTestCase):
    def test_classifier_detects_secrets_and_personal_fields(self):
        self.assertEqual(classify_field("refresh_token"), "sensitive")
        self.assertEqual(classify_field("contact_email"), "personal")
        self.assertEqual(classify_field("company"), "ordinary")

    def test_privacy_review_flags_sensitive_fields(self):
        result = privacy_review({"company": "Acme", "email": "a@example.test", "api_key": "secret"})
        self.assertEqual(result["sensitive_count"], 1)
        self.assertEqual(result["personal_count"], 1)

    def test_sanitization_is_recursive(self):
        result = sanitize_share_payload({"email": "a@example.test", "nested": {"password": "x", "company": "Acme"}})
        self.assertEqual(result["email"], "[REDACTED]")
        self.assertEqual(result["nested"]["password"], "[REDACTED]")
        self.assertEqual(result["nested"]["company"], "Acme")

    def test_share_options_require_a_category_and_reject_unknowns(self):
        with self.assertRaises(ValueError):
            validate_share_options({})
        with self.assertRaises(ValueError):
            validate_share_options({"include_everything": True})
        self.assertFalse(validate_share_options({"include_applications": True})["include_credentials"])

    def test_risk_report_never_shares_automatically(self):
        result = sharing_risk_report({"national_id": "123", "email": "a@example.test"})
        self.assertEqual(result["risk_level"], "high")
        self.assertFalse(result["automatic_sharing_performed"])

    def test_allowed_fields_excludes_credentials(self):
        result = allowed_share_fields(["company", "email", "password"], include_personal=True)
        self.assertEqual(result["included"], ["company", "email"])
        self.assertFalse(result["credentials_allowed"])
