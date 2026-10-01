from collections import Counter
from datetime import timedelta
from django.utils import timezone
from .models import JobApplication, Interview, ApplicationActivity, CareerTask


class ApplicationTimeline:
    """Merge application, interview, activity and task events into one timeline."""

    EVENT_LABELS = {
        "created": "Application created",
        "status_change": "Status changed",
        "note": "Note added",
        "email": "Email",
        "call": "Call",
        "interview": "Interview",
        "follow_up": "Follow-up",
        "document": "Document",
        "task": "Career task",
        "interview_scheduled": "Interview scheduled",
        "interview_completed": "Interview completed",
    }

    def __init__(self, user):
        self.user = user

    def _application(self, application_id):
        return JobApplication.objects.filter(user=self.user, id=application_id).first()

    def _application_events(self, application):
        events = [{
            "id": f"application-created-{application.id}",
            "kind": "created",
            "occurred_at": application.created_at.isoformat(),
            "title": self.EVENT_LABELS["created"],
            "description": f"{application.company} · {application.role}",
            "application_id": application.id,
            "company": application.company,
            "role": application.role,
            "status": application.status,
            "source": "application",
        }]
        activities = ApplicationActivity.objects.filter(
            user=self.user, application=application
        ).order_by("occurred_at", "id")
        for activity in activities:
            events.append({
                "id": f"activity-{activity.id}",
                "kind": activity.activity_type,
                "occurred_at": activity.occurred_at.isoformat(),
                "title": activity.title or self.EVENT_LABELS.get(activity.activity_type, activity.activity_type),
                "description": activity.description,
                "application_id": application.id,
                "company": application.company,
                "role": application.role,
                "status": application.status,
                "source": "activity",
                "metadata": activity.metadata or {},
            })
        interviews = Interview.objects.filter(application=application).order_by("created_at")
        for interview in interviews:
            if interview.scheduled_date:
                events.append({
                    "id": f"interview-scheduled-{interview.id}",
                    "kind": "interview_scheduled",
                    "occurred_at": interview.scheduled_date.isoformat(),
                    "title": self.EVENT_LABELS["interview_scheduled"],
                    "description": interview.get_interview_type_display(),
                    "application_id": application.id,
                    "company": application.company,
                    "role": application.role,
                    "status": application.status,
                    "source": "interview",
                    "metadata": {"outcome": interview.outcome, "interviewer": interview.interviewer_name},
                })
            if interview.completed_date:
                events.append({
                    "id": f"interview-completed-{interview.id}",
                    "kind": "interview_completed",
                    "occurred_at": interview.completed_date.isoformat(),
                    "title": self.EVENT_LABELS["interview_completed"],
                    "description": interview.feedback or interview.notes,
                    "application_id": application.id,
                    "company": application.company,
                    "role": application.role,
                    "status": application.status,
                    "source": "interview",
                    "metadata": {"outcome": interview.outcome, "interviewer": interview.interviewer_name},
                })
        tasks = CareerTask.objects.filter(user=self.user, application=application).order_by("created_at")
        for task in tasks:
            occurred = task.completed_at or task.due_date or task.created_at
            events.append({
                "id": f"task-{task.id}",
                "kind": "task",
                "occurred_at": occurred.isoformat(),
                "title": task.title,
                "description": task.description,
                "application_id": application.id,
                "company": application.company,
                "role": application.role,
                "status": application.status,
                "source": "task",
                "metadata": {"priority": task.priority, "task_status": task.status},
            })
        return events

    def events_for_application(self, application_id, limit=100):
        application = self._application(application_id)
        if not application:
            return None
        events = self._application_events(application)
        events.sort(key=lambda item: item["occurred_at"], reverse=True)
        return events[:limit]

    def all_events(self, limit=100):
        applications = JobApplication.objects.filter(user=self.user).order_by("-updated_at")
        events = []
        for application in applications:
            events.extend(self._application_events(application))
        events.sort(key=lambda item: item["occurred_at"], reverse=True)
        return events[:limit]

    def filter_events(self, kind=None, source=None, application_id=None, limit=100):
        events = self.all_events(limit=max(limit * 4, 200))
        if kind:
            events = [event for event in events if event["kind"] == kind]
        if source:
            events = [event for event in events if event["source"] == source]
        if application_id:
            try:
                target = int(application_id)
                events = [event for event in events if event["application_id"] == target]
            except (TypeError, ValueError):
                return []
        return events[:limit]

    def activity_counts(self):
        events = self.all_events(limit=1000)
        return {
            "total": len(events),
            "by_kind": dict(Counter(event["kind"] for event in events)),
            "by_source": dict(Counter(event["source"] for event in events)),
        }

    def recent_window(self, days=30):
        cutoff = timezone.now() - timedelta(days=days)
        events = self.all_events(limit=2000)
        recent = [event for event in events if event["occurred_at"] >= cutoff.isoformat()]
        return {
            "days": days,
            "events": len(recent),
            "items": recent,
        }

    def application_summary(self):
        rows = []
        applications = JobApplication.objects.filter(user=self.user).order_by("-updated_at")
        for application in applications:
            events = self._application_events(application)
            rows.append({
                "application_id": application.id,
                "company": application.company,
                "role": application.role,
                "status": application.status,
                "event_count": len(events),
                "last_event": events[-1]["occurred_at"] if events else None,
                "activity_count": sum(1 for event in events if event["source"] == "activity"),
                "interview_count": sum(1 for event in events if event["source"] == "interview"),
                "task_count": sum(1 for event in events if event["source"] == "task"),
            })
        return rows

    def dashboard(self):
        recent = self.recent_window()
        counts = self.activity_counts()
        return {
            "recent": recent,
            "counts": counts,
            "applications": self.application_summary(),
            "events": self.all_events(limit=100),
        }
