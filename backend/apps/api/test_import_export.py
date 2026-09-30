import io
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from apps.jobs.models import JobApplication


User = get_user_model()


class ImportExportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="csv", password="pass12345")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_export_contains_only_current_users_records(self):
        JobApplication.objects.create(user=self.user, company="Visible", role="Engineer")
        other = User.objects.create_user(username="othercsv", password="pass12345")
        JobApplication.objects.create(user=other, company="Private", role="Engineer")
        response = self.client.get("/api/applications/export/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Visible", response.content)
        self.assertNotIn(b"Private", response.content)

    def test_import_creates_user_owned_records(self):
        content = (
            "company,role,location,job_url,status,salary_min,salary_max,applied_date,"
            "next_action,next_action_date,notes\n"
            "Imported Co,Engineer,Remote,https://example.com,applied,,,,,,Imported\n"
        )
        upload = SimpleUploadedFile("applications.csv", content.encode(), content_type="text/csv")
        response = self.client.post("/api/applications/import/", {"file": upload}, format="multipart")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["created"], 1)
        self.assertEqual(JobApplication.objects.filter(user=self.user).count(), 1)
