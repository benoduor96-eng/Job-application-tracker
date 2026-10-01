"""Interview preparation analytics built from existing interview records."""
from datetime import timedelta
from django.utils import timezone
from .models import Interview, CareerTask, JobDescription

class InterviewPreparationService:
    TYPES = {
        "phone": ["role summary", "recruiter questions", "availability"],
        "technical": ["core technical skills", "coding examples", "system fundamentals"],
        "behavioral": ["STAR stories", "conflict example", "achievement example"],
        "system_design": ["architecture tradeoffs", "scalability", "failure handling"],
        "panel": ["stakeholder stories", "role-specific examples", "questions for panel"],
        "final": ["impact examples", "role motivation", "closing questions"],
        "other": ["role requirements", "recent achievements", "questions"],
    }

    def __init__(self, user, now=None):
        self.user=user
        self.now=now or timezone.now()
        self.interviews=Interview.objects.filter(application__user=user).select_related("application")
        self.tasks=CareerTask.objects.filter(user=user)
        self.descriptions=JobDescription.objects.filter(user=user)

    def _checklist(self, interview, description):
        items=list(self.TYPES.get(interview.interview_type, self.TYPES["other"]))
        if description:
            required=description.required_skills or []
            preferred=description.preferred_skills or []
            if required: items.append("review required skills: "+", ".join(map(str,required[:8])))
            if preferred: items.append("review preferred skills: "+", ".join(map(str,preferred[:6])))
        if interview.interviewer_name: items.append("research interviewer context")
        items.append("prepare two questions for the interviewer")
        return items

    def upcoming(self, days=45):
        start=self.now
        end=self.now+timedelta(days=days)
        rows=[]
        for interview in self.interviews.filter(scheduled_date__gte=start,scheduled_date__lte=end).order_by("scheduled_date"):
            app=interview.application
            description=self.descriptions.filter(application=app).first()
            delta=interview.scheduled_date-start
            rows.append({
                "id":interview.id,"application_id":app.id,"company":app.company,"role":app.role,
                "type":interview.interview_type,"type_label":interview.get_interview_type_display(),
                "scheduled_date":interview.scheduled_date.isoformat(),
                "days_until":max(0,delta.days),"hours_until":max(0,int(delta.total_seconds()//3600)),
                "interviewer":{"name":interview.interviewer_name,"title":interview.interviewer_title},
                "outcome":interview.outcome,"notes":interview.notes,"feedback":interview.feedback,
                "checklist":self._checklist(interview,description),
                "job_description_attached":bool(description),
                "next_action":app.next_action,"next_action_date":app.next_action_date.isoformat() if app.next_action_date else None,
            })
        return rows

    def stats(self):
        upcoming=self.upcoming()
        return {
            "upcoming":len(upcoming),
            "next_7_days":sum(x["days_until"]<7 for x in upcoming),
            "next_30_days":sum(x["days_until"]<30 for x in upcoming),
            "missing_interviewer":sum(not x["interviewer"]["name"] for x in upcoming),
            "missing_notes":sum(not x["notes"] for x in upcoming),
            "missing_description":sum(not x["job_description_attached"] for x in upcoming),
            "types":{k:sum(x["type"]==k for x in upcoming) for k in self.TYPES},
        }

    def preparation_tasks(self):
        rows=[]
        for item in self.upcoming():
            existing=list(self.tasks.filter(application_id=item["application_id"],status__in=["todo","in_progress"]).values_list("title",flat=True))
            missing=[x for x in item["checklist"] if not any(x.lower() in e.lower() for e in existing)]
            rows.append({"interview_id":item["id"],"application_id":item["application_id"],"company":item["company"],
                         "role":item["role"],"missing_items":missing,"existing_tasks":existing})
        return rows

    def dashboard(self):
        upcoming=self.upcoming()
        return {"generated_at":self.now.isoformat(),"stats":self.stats(),"upcoming":upcoming,
                "preparation_tasks":self.preparation_tasks()}
