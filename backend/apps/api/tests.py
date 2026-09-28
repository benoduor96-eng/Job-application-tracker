import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from apps.jobs.models import JobApplication, Interview
from apps.jobs.services import JobApplicationService
from datetime import date, timedelta


class JobApplicationModelTests(TestCase):
    """Test JobApplication model."""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pass1234')
        self.app = JobApplication.objects.create(
            user=self.user,
            company='Acme Corp',
            role='Backend Engineer',
            location='San Francisco',
            status='applied',
            job_url='https://example.com/job/123',
            applied_date=date.today(),
        )
    
    def test_create_job_application(self):
        """Test creating a job application."""
        self.assertEqual(self.app.company, 'Acme Corp')
        self.assertEqual(self.app.status, 'applied')
        self.assertIsNotNone(self.app.created_at)
    
    def test_job_application_string_representation(self):
        """Test model string representation."""
        self.assertEqual(str(self.app), 'Acme Corp - Backend Engineer')
    
    def test_update_application_status(self):
        """Test updating application status."""
        self.app.status = 'interview'
        self.app.save()
        self.app.refresh_from_db()
        self.assertEqual(self.app.status, 'interview')
    
    def test_salary_range(self):
        """Test salary range fields."""
        self.app.salary_min = 100000
        self.app.salary_max = 150000
        self.app.save()
        self.app.refresh_from_db()
        self.assertEqual(self.app.salary_min, 100000)
        self.assertEqual(self.app.salary_max, 150000)


class InterviewModelTests(TestCase):
    """Test Interview model."""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pass1234')
        self.app = JobApplication.objects.create(
            user=self.user,
            company='Acme Corp',
            role='Backend Engineer',
        )
        self.interview = Interview.objects.create(
            application=self.app,
            interview_type='phone',
            outcome='passed',
        )
    
    def test_create_interview(self):
        """Test creating an interview."""
        self.assertEqual(self.interview.interview_type, 'phone')
        self.assertEqual(self.interview.outcome, 'passed')
    
    def test_interview_relationship(self):
        """Test interview-application relationship."""
        self.assertEqual(self.interview.application, self.app)
        self.assertIn(self.interview, self.app.interviews.all())


class JobApplicationServiceTests(TestCase):
    """Test JobApplicationService business logic."""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pass1234')
        self.service = JobApplicationService(self.user)
        self.app1 = JobApplication.objects.create(
            user=self.user,
            company='Acme',
            role='Backend',
            status='applied',
            salary_min=100000,
            salary_max=150000,
        )
        self.app2 = JobApplication.objects.create(
            user=self.user,
            company='TechCorp',
            role='Frontend',
            status='interview',
            salary_min=80000,
            salary_max=120000,
        )
    
    def test_search_by_company(self):
        """Test searching applications by company."""
        results = self.service.search(query='Acme')
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().company, 'Acme')
    
    def test_filter_by_status(self):
        """Test filtering by status."""
        results = self.service.search(status='interview')
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().role, 'Frontend')
    
    def test_counts_by_status(self):
        """Test status counts."""
        counts = self.service.counts_by_status()
        self.assertEqual(counts['applied'], 1)
        self.assertEqual(counts['interview'], 1)
    
    def test_upcoming_applications(self):
        """Test getting upcoming follow-ups."""
        today = date.today()
        self.app1.next_action_date = today + timedelta(days=3)
        self.app1.next_action = 'Follow up with recruiter'
        self.app1.save()
        
        upcoming = self.service.upcoming(days=7)
        self.assertEqual(upcoming.count(), 1)
    
    def test_overdue_applications(self):
        """Test getting overdue follow-ups."""
        self.app1.next_action_date = date.today() - timedelta(days=5)
        self.app1.next_action = 'Follow up'
        self.app1.save()
        
        overdue = self.service.overdue()
        self.assertEqual(overdue.count(), 1)
    
    def test_pipeline_health(self):
        """Test pipeline health metrics."""
        health = self.service.pipeline_health()
        self.assertIn('screening_rate', health)
        self.assertIn('interview_rate', health)
        self.assertIn('offer_rate', health)
    
    def test_salary_statistics(self):
        """Test salary statistics."""
        stats = self.service.salary_statistics()
        self.assertGreater(stats['count'], 0)
    
    def test_export_rows(self):
        """Test exporting application data."""
        rows = self.service.export_rows()
        self.assertEqual(len(rows), 2)
        self.assertIn('company', rows[0])
        self.assertIn('role', rows[0])


@pytest.mark.django_db
class APITests:
    """Test API endpoints."""
    
    def setup_method(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pass1234')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_register(self):
        """Test user registration."""
        client = APIClient()
        response = client.post('/api/auth/register/', {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'new@example.com'
        }, format='json')
        assert response.status_code == 201
    
    def test_create_application(self):
        """Test creating an application via API."""
        response = self.client.post('/api/applications/', {
            'company': 'TechCorp',
            'role': 'DevOps Engineer',
            'status': 'applied',
        }, format='json')
        assert response.status_code == 201
        assert response.data['company'] == 'TechCorp'
    
    def test_list_applications(self):
        """Test listing applications."""
        JobApplication.objects.create(
            user=self.user,
            company='Acme',
            role='Backend',
        )
        response = self.client.get('/api/applications/')
        assert response.status_code == 200
        assert len(response.data) == 1
    
    def test_search_applications(self):
        """Test searching applications."""
        JobApplication.objects.create(
            user=self.user,
            company='Acme Corp',
            role='Backend Engineer',
        )
        response = self.client.get('/api/applications/?q=Acme')
        assert response.status_code == 200
        assert len(response.data) == 1
    
    def test_dashboard_endpoint(self):
        """Test dashboard endpoint."""
        response = self.client.get('/api/applications/dashboard/')
        assert response.status_code == 200
        assert 'total' in response.data
        assert 'by_status' in response.data
    
    def test_health_metrics(self):
        """Test health metrics endpoint."""
        response = self.client.get('/api/applications/health_metrics/')
        assert response.status_code == 200
        assert 'interview_rate' in response.data
    
    def test_export_endpoint(self):
        """Test export endpoint."""
        JobApplication.objects.create(
            user=self.user,
            company='Acme',
            role='Backend',
        )
        response = self.client.get('/api/applications/export/')
        assert response.status_code == 200
        assert isinstance(response.data, list)
    
    def test_salary_stats_endpoint(self):
        """Test salary statistics endpoint."""
        response = self.client.get('/api/applications/salary_stats/')
        assert response.status_code == 200
