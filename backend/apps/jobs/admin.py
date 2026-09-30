from django.contrib import admin
from .models import CareerTask, CareerContact, CareerProfile, Interview, JobApplication, Resume
admin.site.register([JobApplication, Interview, CareerContact, CareerProfile, Resume, CareerTask])