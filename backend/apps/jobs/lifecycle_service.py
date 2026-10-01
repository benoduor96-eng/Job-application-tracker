"""Transactional application lifecycle operations and audit history."""
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from .models import ApplicationActivity, JobApplication

FOLLOW_UP_DAYS={"applied":7,"screening":4,"interview":2,"offer":2}
TERMINAL_STATUSES={"rejected","withdrawn"}

class ApplicationLifecycleService:
    VALID_STATUSES={value for value,_ in JobApplication.STATUS_CHOICES}

    def __init__(self,user): self.user=user

    def _owned(self,application):
        if application.user_id!=self.user.id: raise PermissionError("Application does not belong to this user")

    @transaction.atomic
    def transition(self,application,status,*,note="",occurred_at=None,schedule_follow_up=True):
        self._owned(application)
        if status not in self.VALID_STATUSES: raise ValueError("Unsupported application status")
        previous=application.status; now=occurred_at or timezone.now()
        application.status=status; fields=["status","updated_at"]
        if status=="applied" and not application.applied_date:
            application.applied_date=now.date(); fields.append("applied_date")
        if schedule_follow_up and status in FOLLOW_UP_DAYS and status!="offer":
            application.next_action_date=now.date()+timedelta(days=FOLLOW_UP_DAYS[status])
            application.next_action=application.next_action or "Follow up on application"
            fields += ["next_action_date","next_action"]
        elif status in TERMINAL_STATUSES:
            application.next_action=""; application.next_action_date=None
            fields += ["next_action","next_action_date"]
        application.save(update_fields=list(dict.fromkeys(fields)))
        ApplicationActivity.objects.create(application=application,user=self.user,activity_type="status_change",title=f"Status changed to {application.get_status_display()}",description=note,metadata={"from":previous,"to":status},occurred_at=now)
        return application

    @transaction.atomic
    def record_follow_up(self,application,*,title="Follow-up",note="",next_date=None):
        self._owned(application); now=timezone.now()
        ApplicationActivity.objects.create(application=application,user=self.user,activity_type="follow_up",title=title,description=note,metadata={"status":application.status},occurred_at=now)
        application.next_action_date=next_date
        application.next_action="Follow up again" if next_date else ""
        application.save(update_fields=["next_action_date","next_action","updated_at"])
        return application

    def history(self,application,limit=50):
        self._owned(application)
        if limit<1: raise ValueError("limit must be positive")
        return list(ApplicationActivity.objects.filter(application=application).order_by("-occurred_at","-created_at")[:limit].values("id","activity_type","title","description","metadata","occurred_at"))

    def transition_options(self,application):
        self._owned(application)
        order=["saved","applied","screening","interview","offer","rejected","withdrawn"]
        current=order.index(application.status); labels=dict(JobApplication.STATUS_CHOICES)
        return [{"status":s,"label":labels[s],"forward":order.index(s)>current,"terminal":s in TERMINAL_STATUSES} for s in order if s!=application.status]
