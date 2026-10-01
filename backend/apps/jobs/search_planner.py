"""Planning and prioritization services for an active job search."""
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import date, timedelta
from django.utils import timezone
from .models import CareerContact, CareerTask, Interview, JobApplication

ACTIVE_STATUSES={"saved","applied","screening","interview","offer"}
TERMINAL_STATUSES={"rejected","withdrawn"}
TASK_OPEN_STATUSES={"todo","in_progress"}

@dataclass(frozen=True)
class PlanningItem:
    kind:str
    title:str
    priority:int
    due_date:date|None
    application_id:int|None=None
    contact_id:int|None=None
    task_id:int|None=None
    reason:str=""
    def to_dict(self): return asdict(self)

class JobSearchPlanner:
    """Build explainable work queues from existing tracker records."""
    def __init__(self,user,today=None): self.user=user; self.today=today or timezone.localdate()
    def applications(self): return JobApplication.objects.filter(user=self.user)
    def open_tasks(self): return CareerTask.objects.filter(user=self.user,status__in=TASK_OPEN_STATUSES).select_related("application")
    def contacts(self): return CareerContact.objects.filter(user=self.user)
    def interviews(self): return Interview.objects.filter(application__user=self.user).select_related("application")
    def overdue_actions(self):
        items=[]
        for app in self.applications().exclude(status__in=TERMINAL_STATUSES):
            due=app.next_action_date
            if due and due<self.today:
                days=(self.today-due).days
                items.append(PlanningItem("application_follow_up",app.next_action or f"Follow up with {app.company}",min(100,55+days*4),due,application_id=app.id,reason=f"Next action is {days} day(s) overdue."))
        for task in self.open_tasks():
            if task.due_date and task.due_date.date()<self.today:
                days=(self.today-task.due_date.date()).days
                items.append(PlanningItem("task",task.title,min(100,50+days*5),task.due_date.date(),application_id=task.application_id,task_id=task.id,reason=f"Task is {days} day(s) overdue."))
        return sorted(items,key=lambda x:(-x.priority,x.due_date or self.today))
    def upcoming_interviews(self,horizon=14):
        end=self.today+timedelta(days=horizon); items=[]
        for interview in self.interviews().filter(scheduled_date__date__gte=self.today,scheduled_date__date__lte=end).exclude(outcome__in=["failed","passed"]):
            due=interview.scheduled_date.date(); days=(due-self.today).days; urgency=90 if days<=1 else 75 if days<=3 else 60; app=interview.application
            items.append(PlanningItem("interview",f"Prepare for {interview.get_interview_type_display()} at {app.company}",urgency,due,application_id=app.id,reason=f"Interview scheduled in {days} day(s)."))
        return sorted(items,key=lambda x:(x.due_date,-x.priority))
    def contact_follow_ups(self,horizon=7):
        end=timezone.now()+timedelta(days=horizon); items=[]
        for contact in self.contacts().filter(next_follow_up__isnull=False,next_follow_up__lte=end):
            due=contact.next_follow_up.date(); overdue=due<self.today
            items.append(PlanningItem("contact_follow_up",f"Follow up with {contact.name}",85 if overdue else 65,due,application_id=contact.application_id,contact_id=contact.id,reason="Contact follow-up is overdue." if overdue else "Contact follow-up is due."))
        return sorted(items,key=lambda x:(-x.priority,x.due_date or self.today))
    def stale_applications(self,stale_days=10):
        cutoff=timezone.now()-timedelta(days=stale_days); items=[]
        for app in self.applications().filter(updated_at__lt=cutoff).exclude(status__in=TERMINAL_STATUSES):
            age=(timezone.now()-app.updated_at).days
            items.append(PlanningItem("stale_application",f"Review {app.role} at {app.company}",min(95,45+age*3),self.today,application_id=app.id,reason=f"No update recorded for {age} day(s)."))
        return sorted(items,key=lambda x:-x.priority)
    def application_quality(self):
        rows=[]
        for app in self.applications().exclude(status__in=TERMINAL_STATUSES):
            score=0; missing=[]
            if app.job_url: score+=10
            else: missing.append("add the job URL")
            if app.applied_date: score+=15
            elif app.status!="saved": missing.append("record the application date")
            if app.location: score+=5
            if app.notes: score+=10
            else: missing.append("add useful notes")
            if app.next_action: score+=20
            else: missing.append("set a next action")
            if app.next_action_date: score+=20
            else: missing.append("set a next-action date")
            if app.salary_min or app.salary_max: score+=10
            if app.status in ACTIVE_STATUSES: score+=10
            rows.append({"application_id":app.id,"company":app.company,"role":app.role,"score":min(score,100),"missing":missing})
        return sorted(rows,key=lambda x:(x["score"],x["company"].lower()))
    def pipeline_balance(self):
        counts=Counter(self.applications().values_list("status",flat=True))
        return {"total":sum(counts.values()),"active":sum(counts.get(s,0) for s in ACTIVE_STATUSES),"by_status":{s:counts.get(s,0) for s,_ in JobApplication.STATUS_CHOICES},"attention":[s for s in ("saved","applied","screening","interview") if counts.get(s,0)==0]}
    def weekly_capacity(self,target_applications=10,target_followups=5):
        start=self.today-timedelta(days=self.today.weekday()); end=start+timedelta(days=6)
        submitted=self.applications().filter(applied_date__gte=start,applied_date__lte=end).count()
        followups=self.applications().filter(next_action_date__gte=start,next_action_date__lte=end).exclude(status__in=TERMINAL_STATUSES).count()
        return {"week_start":start,"week_end":end,"applications_target":target_applications,"applications_completed":submitted,"applications_remaining":max(0,target_applications-submitted),"followups_target":target_followups,"followups_planned":followups,"followups_remaining":max(0,target_followups-followups)}
    def daily_plan(self,limit=12):
        candidates=self.overdue_actions()+self.upcoming_interviews()+self.contact_follow_ups()+self.stale_applications(); seen=set(); result=[]
        for item in sorted(candidates,key=lambda x:(-x.priority,x.due_date or self.today)):
            key=(item.kind,item.application_id,item.contact_id,item.task_id)
            if key in seen: continue
            seen.add(key); result.append(item)
            if len(result)>=limit: break
        return result
    def summary(self):
        quality=self.application_quality()
        return {"date":self.today,"plan":[x.to_dict() for x in self.daily_plan()],"overdue_count":len(self.overdue_actions()),"interview_count":len(self.upcoming_interviews()),"contact_follow_up_count":len(self.contact_follow_ups()),"stale_count":len(self.stale_applications()),"quality_average":round(sum(x["score"] for x in quality)/len(quality),2) if quality else 0,"pipeline":self.pipeline_balance(),"weekly_capacity":self.weekly_capacity()}
