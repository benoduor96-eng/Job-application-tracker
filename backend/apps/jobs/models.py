from django.conf import settings
from django.db import models


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('saved', 'Saved'),
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    job_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='saved')
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    applied_date = models.DateField(null=True, blank=True)
    next_action = models.CharField(max_length=255, blank=True)
    next_action_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['user', 'status']),
        ]

    def __str__(self):
        return f'{self.company} - {self.role}'


class Interview(models.Model):
    INTERVIEW_TYPE_CHOICES = [
        ('phone', 'Phone Screen'), ('technical', 'Technical'),
        ('behavioral', 'Behavioral'), ('system_design', 'System Design'),
        ('panel', 'Panel'), ('final', 'Final Round'), ('other', 'Other')
    ]
    OUTCOME_CHOICES = [
        ('pending', 'Pending'), ('passed', 'Passed'),
        ('failed', 'Failed'), ('scheduled', 'Scheduled')
    ]

    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='interviews')
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPE_CHOICES, default='phone')
    scheduled_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES, default='pending')
    interviewer_name = models.CharField(max_length=200, blank=True)
    interviewer_title = models.CharField(max_length=200, blank=True)
    feedback = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheduled_date']
        indexes = [
            models.Index(fields=['application', 'outcome']),
            models.Index(fields=['scheduled_date']),
        ]

    def __str__(self):
        return f'{self.get_interview_type_display()} for {self.application}'


class CareerContact(models.Model):
    CONTACT_TYPES = [
        ("recruiter", "Recruiter"),
        ("hiring_manager", "Hiring Manager"),
        ("referral", "Referral"),
        ("interviewer", "Interviewer"),
        ("career_coach", "Career Coach"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="career_contacts")
    application = models.ForeignKey(JobApplication, on_delete=models.SET_NULL, null=True, blank=True, related_name="contacts")
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    contact_type = models.CharField(max_length=30, choices=CONTACT_TYPES, default="recruiter")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    profile_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    last_contacted_at = models.DateTimeField(null=True, blank=True)
    next_follow_up = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["user", "contact_type"]),
            models.Index(fields=["user", "next_follow_up"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.company})"