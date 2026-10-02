"""Company-level intelligence for the job-search pipeline."""
from collections import Counter, defaultdict
from decimal import Decimal
from .models import CareerContact, CareerTask, Interview, JobApplication, JobDescription

ACTIVE = {"saved", "applied", "screening", "interview", "offer"}
CLOSED = {"rejected", "withdrawn"}

class CompanyIntelligenceService:
    def __init__(self, user, now=None):
        from django.utils import timezone
        self.user = user
        self.now = now or timezone.now()
        self.apps = JobApplication.objects.filter(user=user)
        self.interviews = Interview.objects.filter(application__user=user)
        self.contacts = CareerContact.objects.filter(user=user)
        self.tasks = CareerTask.objects.filter(user=user)
        self.descriptions = JobDescription.objects.filter(user=user)

    @staticmethod
    def _key(value):
        return (value or "").strip().lower()

    def _groups(self):
        groups = defaultdict(list)
        for app in self.apps:
            groups[self._key(app.company)].append(app)
        return groups

    def _contacts_for(self, company):
        return list(self.contacts.filter(company__iexact=company))

    def _interviews_for(self, ids):
        return list(self.interviews.filter(application_id__in=ids))

    def _tasks_for(self, ids):
        return list(self.tasks.filter(application_id__in=ids))

    def _descriptions_for(self, ids):
        return list(self.descriptions.filter(application_id__in=ids))

    def _status_mix(self, apps):
        counts = Counter(app.status for app in apps)
        return {s: counts.get(s, 0) for s in ["saved","applied","screening","interview","offer","rejected","withdrawn"]}

    def _salary(self, apps):
        values = []
        for app in apps:
            if app.salary_min is not None and app.salary_max is not None:
                values.append((Decimal(app.salary_min) + Decimal(app.salary_max)) / 2)
            elif app.salary_min is not None:
                values.append(Decimal(app.salary_min))
            elif app.salary_max is not None:
                values.append(Decimal(app.salary_max))
        if not values:
            return {"count": 0, "minimum": None, "maximum": None, "average": None}
        return {"count": len(values), "minimum": format(min(values).normalize(), "f"), "maximum": format(max(values).normalize(), "f"),
                "average": str((sum(values) / len(values)).quantize(Decimal("0.01")))}

    def _activity(self, apps):
        if not apps:
            return {"first_applied": None, "last_updated": None, "days_since_update": None}
        applied = [a.applied_date for a in apps if a.applied_date]
        latest = max(a.updated_at for a in apps)
        return {"first_applied": min(applied).isoformat() if applied else None,
                "last_updated": latest.isoformat(), "days_since_update": max(0, (self.now-latest).days)}

    def _relationship(self, contacts):
        return {
            "contacts": len(contacts),
            "linked_contacts": sum(bool(c.application_id) for c in contacts),
            "recent_contacts": sum(bool(c.last_contacted_at and (self.now-c.last_contacted_at).days <= 30) for c in contacts),
            "overdue_followups": sum(bool(c.next_follow_up and c.next_follow_up < self.now) for c in contacts),
            "contact_types": dict(Counter(c.contact_type for c in contacts)),
        }

    def _attention(self, apps, interviews, contacts, tasks, descriptions):
        items = []
        for app in apps:
            if app.status in ACTIVE and not app.next_action_date:
                items.append({"priority":80,"type":"missing_next_action","application_id":app.id,"title":"Plan the next step for "+app.role})
            elif app.status in ACTIVE and app.next_action_date and app.next_action_date < self.now.date():
                items.append({"priority":100,"type":"overdue_followup","application_id":app.id,"title":"Overdue follow-up for "+app.role})
            if app.status in {"screening","interview"} and not (app.notes or "").strip():
                items.append({"priority":60,"type":"missing_notes","application_id":app.id,"title":"Add preparation notes for "+app.role})
        for interview in interviews:
            if interview.outcome in {"scheduled","pending"} and not interview.scheduled_date:
                items.append({"priority":90,"type":"missing_interview_time","application_id":interview.application_id,"title":"Add the interview schedule"})
        for contact in contacts:
            if contact.next_follow_up and contact.next_follow_up < self.now:
                items.append({"priority":95,"type":"overdue_contact","application_id":contact.application_id,"title":"Follow up with "+contact.name})
        for task in tasks:
            if task.status in {"todo","in_progress"} and task.due_date and task.due_date < self.now:
                items.append({"priority":85,"type":"overdue_task","application_id":task.application_id,"title":task.title})
        if apps and not descriptions:
            items.append({"priority":50,"type":"missing_description","application_id":apps[0].id,"title":"Add a job description for this company"})
        return sorted(items, key=lambda x:(-x["priority"],x["title"]))[:20]

    def company_detail(self, company):
        apps = list(self.apps.filter(company__iexact=company).order_by("-updated_at"))
        if not apps:
            return None
        ids = [a.id for a in apps]
        interviews = self._interviews_for(ids)
        tasks = self._tasks_for(ids)
        descriptions = self._descriptions_for(ids)
        contacts = self._contacts_for(apps[0].company)
        active = [a for a in apps if a.status in ACTIVE]
        return {
            "company": apps[0].company, "applications": len(apps), "active_applications": len(active),
            "closed_applications": len(apps)-len(active), "offers": sum(a.status=="offer" for a in apps),
            "interviews": len(interviews), "contacts": len(contacts), "job_descriptions": len(descriptions),
            "open_tasks": sum(t.status in {"todo","in_progress"} for t in tasks),
            "status_mix": self._status_mix(apps), "salary": self._salary(apps), "activity": self._activity(apps),
            "relationship": self._relationship(contacts),
            "attention": self._attention(apps, interviews, contacts, tasks, descriptions),
            "roles": sorted({a.role for a in apps}),
            "applications_detail": [{"id":a.id,"role":a.role,"status":a.status,"location":a.location,
                "applied_date":a.applied_date.isoformat() if a.applied_date else None,
                "next_action":a.next_action,"next_action_date":a.next_action_date.isoformat() if a.next_action_date else None,
                "updated_at":a.updated_at.isoformat()} for a in apps],
        }

    def overview(self, limit=50):
        rows=[]
        for _, apps in self._groups().items():
            company=apps[0].company
            contacts=self._contacts_for(company)
            ids=[a.id for a in apps]
            interviews=self._interviews_for(ids)
            active=[a for a in apps if a.status in ACTIVE]
            rows.append({"company":company,"applications":len(apps),"active":len(active),
                "offers":sum(a.status=="offer" for a in apps),"interviews":len(interviews),"contacts":len(contacts),
                "roles":len({a.role.strip().lower() for a in apps}),
                "overdue_actions":sum(bool(a.next_action_date and a.next_action_date<self.now.date()) for a in active),
                "salary":self._salary(apps),"last_updated":max(a.updated_at for a in apps).isoformat()})
        return sorted(rows,key=lambda r:(-r["active"],-r["applications"],r["company"].lower()))[:limit]

    def status_distribution(self):
        counts=Counter(self.apps.values_list("status",flat=True))
        return {s:counts.get(s,0) for s in sorted(ACTIVE|CLOSED)}

    def relationship_gaps(self):
        rows=[]
        for row in self.overview(500):
            if row["active"] and row["contacts"]==0:
                rows.append({"company":row["company"],"reason":"No contact record","priority":"medium"})
            elif row["active"] and row["overdue_actions"]:
                rows.append({"company":row["company"],"reason":"Overdue application action","priority":"high"})
        return sorted(rows,key=lambda r:(r["priority"]!="high",r["company"].lower()))

    def pipeline(self):
        rows=[]
        for row in self.overview(500):
            rows.append({"company":row["company"],"active":row["active"],"interviews":row["interviews"],
                "offers":row["offers"],"conversion_signal":round(row["offers"]/row["applications"]*100,1) if row["applications"] else 0,
                "relationship_coverage":round(row["contacts"]/row["active"]*100,1) if row["active"] else 0})
        return rows

    def dashboard(self, limit=50):
        groups=self._groups()
        overview=self.overview(limit)
        return {"totals":{"companies":len(groups),"applications":self.apps.count(),
            "active_applications":self.apps.filter(status__in=ACTIVE).count(),"interviews":self.interviews.count(),"contacts":self.contacts.count()},
            "companies":overview,"status_distribution":self.status_distribution(),
            "relationship_gaps":self.relationship_gaps(),"pipeline":self.pipeline()[:limit]}
