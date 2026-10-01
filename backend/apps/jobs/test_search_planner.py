"""Tests for job-search planning rules."""
from datetime import timedelta
from decimal import Decimal
import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from apps.jobs.models import CareerContact, CareerTask, Interview, JobApplication
from apps.jobs.search_planner import JobSearchPlanner

@pytest.fixture
def user(db): return User.objects.create_user(username="planner-user",password="pass")

@pytest.fixture
def application(user):
    return JobApplication.objects.create(user=user,company="Acme",role="Backend Engineer",location="Remote",job_url="https://example.com/job",status="applied",applied_date=timezone.localdate(),next_action="Send follow-up",next_action_date=timezone.localdate()+timedelta(days=2),notes="Strong match",salary_min=Decimal("70000"),salary_max=Decimal("90000"))

def test_overdue_action_is_prioritized(user):
    app=JobApplication.objects.create(user=user,company="Acme",role="Engineer",status="applied",next_action="Follow up",next_action_date=timezone.localdate()-timedelta(days=3))
    items=JobSearchPlanner(user).overdue_actions()
    assert items[0].application_id==app.id and items[0].priority>=60

def test_terminal_applications_are_excluded(user):
    JobApplication.objects.create(user=user,company="Closed",role="Engineer",status="rejected",next_action="Follow up",next_action_date=timezone.localdate()-timedelta(days=5))
    assert JobSearchPlanner(user).overdue_actions()==[]

def test_interview_is_prioritized(application):
    interview=Interview.objects.create(application=application,interview_type="technical",scheduled_date=timezone.now()+timedelta(days=1))
    item=JobSearchPlanner(application.user).upcoming_interviews()[0]
    assert item.application_id==application.id and interview.application_id==application.id

def test_contact_follow_up_is_visible(user,application):
    contact=CareerContact.objects.create(user=user,application=application,name="Jane",company="Acme",next_follow_up=timezone.now()+timedelta(days=2))
    assert JobSearchPlanner(user).contact_follow_ups()[0].contact_id==contact.id

def test_stale_application_is_detected(user):
    app=JobApplication.objects.create(user=user,company="Stale",role="Engineer",status="screening")
    JobApplication.objects.filter(pk=app.pk).update(updated_at=timezone.now()-timedelta(days=30))
    assert JobSearchPlanner(user).stale_applications()[0].application_id==app.id

def test_complete_application_scores_one_hundred(application):
    assert JobSearchPlanner(application.user).application_quality()[0]["score"]==100

def test_quality_explains_missing_data(user):
    JobApplication.objects.create(user=user,company="Sparse",role="Engineer",status="saved")
    row=JobSearchPlanner(user).application_quality()[0]
    assert "add the job URL" in row["missing"] and "set a next action" in row["missing"]

def test_pipeline_balance_counts_statuses(user,application):
    JobApplication.objects.create(user=user,company="Offer",role="Engineer",status="offer")
    result=JobSearchPlanner(user).pipeline_balance()
    assert result["total"]==2 and result["by_status"]["offer"]==1

def test_weekly_capacity_counts_application(application):
    result=JobSearchPlanner(application.user).weekly_capacity(target_applications=4)
    assert result["applications_completed"]==1 and result["applications_remaining"]==3

def test_daily_plan_deduplicates(user,application):
    CareerTask.objects.create(user=user,application=application,title="Follow up",due_date=timezone.now()-timedelta(days=1),status="todo")
    items=JobSearchPlanner(user).daily_plan()
    keys=[(x.kind,x.application_id,x.contact_id,x.task_id) for x in items]
    assert len(keys)==len(set(keys))

def test_summary_has_operational_sections(user):
    result=JobSearchPlanner(user).summary()
    assert {"date","plan","pipeline","weekly_capacity"}<=set(result)

@pytest.mark.parametrize("value",[0,1,5,100])
def test_weekly_targets_are_supported(user,value):
    result=JobSearchPlanner(user).weekly_capacity(value,value)
    assert result["applications_target"]==value and result["followups_target"]==value
