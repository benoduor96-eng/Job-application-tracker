from django.conf import settings
from django.db import models
class JobApplication(models.Model):
    STATUS_CHOICES=[('saved','Saved'),('applied','Applied'),('screening','Screening'),('interview','Interview'),('offer','Offer'),('rejected','Rejected'),('withdrawn','Withdrawn')]
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='job_applications')
    company=models.CharField(max_length=200)
    role=models.CharField(max_length=200)
    location=models.CharField(max_length=200,blank=True)
    job_url=models.URLField(blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='saved')
    salary_min=models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    salary_max=models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    applied_date=models.DateField(null=True,blank=True)
    next_action=models.CharField(max_length=255,blank=True)
    next_action_date=models.DateField(null=True,blank=True)
    notes=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['-updated_at']