"""Tests for application lifecycle transitions and audit history."""
from datetime import date, timedelta
import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from apps.jobs.models import ApplicationActivity, JobApplication
from apps.jobs.lifecycle_service import ApplicationLifecycleService

@pytest.fixture
def user(db): return User.objects.create_user(username="lifecycle",password="pass")

@pytest.fixture
def application(user): return JobApplication.objects.create(user=user,company="Acme",role="Engineer",status="saved")

def test_applied_transition_records_date_followup_and_activity(application):
    service=ApplicationLifecycleService(application.user)
    now=timezone.now()
    result=service.transition(application,"applied",note="Submitted application",occurred_at=now)
    result.refresh_from_db()
    assert result.status=="applied"
    assert result.applied_date==now.date()
    assert result.next_action_date==now.date()+timedelta(days=7)
    activity=ApplicationActivity.objects.get(application=result)
    assert activity.activity_type=="status_change"
    assert activity.metadata=={"from":"saved","to":"applied"}

def test_terminal_transition_clears_followup(application):
    application.next_action="Follow up"
    application.next_action_date=date.today()+timedelta(days=3)
    application.save()
    ApplicationLifecycleService(application.user).transition(application,"rejected")
    application.refresh_from_db()
    assert application.next_action==""
    assert application.next_action_date is None

def test_invalid_status_is_rejected(application):
    with pytest.raises(ValueError):
        ApplicationLifecycleService(application.user).transition(application,"unknown")

def test_other_users_application_is_protected(application,db):
    other=User.objects.create_user(username="other-lifecycle",password="pass")
    with pytest.raises(PermissionError):
        ApplicationLifecycleService(other).transition(application,"applied")

def test_record_follow_up_creates_history(application):
    next_date=date.today()+timedelta(days=5)
    ApplicationLifecycleService(application.user).record_follow_up(application,note="Recruiter contacted",next_date=next_date)
    application.refresh_from_db()
    assert application.next_action_date==next_date
    assert ApplicationActivity.objects.filter(application=application,activity_type="follow_up").count()==1

def test_history_is_newest_first(application):
    service=ApplicationLifecycleService(application.user)
    service.transition(application,"applied")
    service.transition(application,"screening")
    history=service.history(application)
    assert len(history)==2
    assert history[0]["metadata"]["to"]=="screening"

def test_history_rejects_invalid_limit(application):
    with pytest.raises(ValueError):
        ApplicationLifecycleService(application.user).history(application,0)

def test_transition_options_describe_terminal_states(application):
    options=ApplicationLifecycleService(application.user).transition_options(application)
    rejected=next(item for item in options if item["status"]=="rejected")
    assert rejected["terminal"] is True
    assert rejected["forward"] is True

@pytest.mark.parametrize("status,days", [("applied",7),("screening",4),("interview",2)])
def test_active_statuses_schedule_different_followups(application,status,days):
    ApplicationLifecycleService(application.user).transition(application,status)
    application.refresh_from_db()
    assert application.next_action_date==date.today()+timedelta(days=days)
