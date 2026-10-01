from collections import Counter
from datetime import timedelta
from django.utils import timezone
from .models import JobApplication, Interview, JobDescription, ApplicationActivity, CareerTask


class InterviewPacket:
    """Create a structured preparation packet from an interview and its application."""

    TOPIC_GROUPS = {
        "role": {"role", "responsibility", "responsibilities", "experience"},
        "technical": {"python", "django", "java", "sql", "api", "backend", "frontend", "react", "testing", "cloud"},
        "delivery": {"project", "deliver", "team", "collaborate", "communication", "stakeholder"},
        "domain": {"industry", "domain", "customer", "product", "market"},
    }

    def __init__(self, user, application_id=None):
        self.user = user
        self.application_id = application_id

    def application(self):
        queryset = JobApplication.objects.filter(user=self.user)
        if self.application_id:
            queryset = queryset.filter(id=self.application_id)
        return queryset.order_by("-updated_at").first()

    def _description(self, application):
        return JobDescription.objects.filter(
            user=self.user, application=application
        ).first()

    def upcoming_interviews(self, days=30):
        now = timezone.now()
        end = now + timedelta(days=days)
        rows = []
        queryset = Interview.objects.filter(
            application__user=self.user,
            scheduled_date__gte=now,
            scheduled_date__lte=end,
        ).select_related("application").order_by("scheduled_date")
        for item in queryset:
            rows.append({
                "id": item.id,
                "application_id": item.application_id,
                "company": item.application.company,
                "role": item.application.role,
                "type": item.get_interview_type_display(),
                "scheduled_date": item.scheduled_date.isoformat() if item.scheduled_date else None,
                "outcome": item.outcome,
                "interviewer": item.interviewer_name,
                "interviewer_title": item.interviewer_title,
            })
        return rows

    def _skills(self, description):
        if not description:
            return []
        required = description.required_skills or []
        preferred = description.preferred_skills or []
        result = []
        for value in required + preferred:
            text = str(value).strip()
            if text and text.lower() not in {x["name"].lower() for x in result}:
                result.append({"name": text, "required": value in required})
        return result

    def _topics(self, description, application):
        text = " ".join([
            description.raw_text if description else "",
            description.title if description else "",
            application.role,
            application.notes,
        ]).lower()
        topics = {}
        for group, keywords in self.TOPIC_GROUPS.items():
            found = sorted(keyword for keyword in keywords if keyword in text)
            topics[group] = found
        return topics

    def _activity_context(self, application):
        rows = ApplicationActivity.objects.filter(
            user=self.user, application=application
        ).order_by("-occurred_at")[:12]
        return [{
            "type": row.activity_type,
            "title": row.title,
            "description": row.description,
            "occurred_at": row.occurred_at.isoformat(),
        } for row in rows]

    def _task_context(self, application):
        rows = CareerTask.objects.filter(
            user=self.user, application=application
        ).exclude(status__in=["done", "cancelled"]).order_by("due_date")
        return [{
            "id": row.id,
            "title": row.title,
            "priority": row.priority,
            "status": row.status,
            "due_date": row.due_date.isoformat() if row.due_date else None,
        } for row in rows]

    def preparation_score(self, application, interview):
        score = 0
        checks = []
        if application.notes.strip():
            score += 15
            checks.append({"key": "notes", "label": "Application notes available", "complete": True})
        else:
            checks.append({"key": "notes", "label": "Application notes available", "complete": False})

        description = self._description(application)
        if description:
            score += 20
            checks.append({"key": "job_description", "label": "Job description attached", "complete": True})
        else:
            checks.append({"key": "job_description", "label": "Job description attached", "complete": False})

        if description and (description.required_skills or description.responsibilities):
            score += 20
            checks.append({"key": "requirements", "label": "Requirements extracted", "complete": True})
        else:
            checks.append({"key": "requirements", "label": "Requirements extracted", "complete": False})

        if interview.feedback.strip():
            score += 15
            checks.append({"key": "feedback", "label": "Previous feedback captured", "complete": True})
        else:
            checks.append({"key": "feedback", "label": "Previous feedback captured", "complete": False})

        if application.next_action_date:
            score += 10
            checks.append({"key": "next_action", "label": "Next action scheduled", "complete": True})
        else:
            checks.append({"key": "next_action", "label": "Next action scheduled", "complete": False})

        tasks = self._task_context(application)
        if tasks:
            score += 10
            checks.append({"key": "prep_tasks", "label": "Preparation tasks exist", "complete": True})
        else:
            checks.append({"key": "prep_tasks", "label": "Preparation tasks exist", "complete": False})

        if interview.interviewer_name:
            score += 5
            checks.append({"key": "interviewer", "label": "Interviewer recorded", "complete": True})
        else:
            checks.append({"key": "interviewer", "label": "Interviewer recorded", "complete": False})

        if interview.notes.strip():
            score += 5
            checks.append({"key": "interview_notes", "label": "Interview notes started", "complete": True})
        else:
            checks.append({"key": "interview_notes", "label": "Interview notes started", "complete": False})

        return {"score": score, "checks": checks}

    def packet_for_interview(self, interview):
        if interview.application.user_id != self.user.id:
            return None
        application = interview.application
        description = self._description(application)
        return {
            "interview": {
                "id": interview.id,
                "type": interview.get_interview_type_display(),
                "scheduled_date": interview.scheduled_date.isoformat() if interview.scheduled_date else None,
                "outcome": interview.outcome,
                "interviewer": interview.interviewer_name,
                "interviewer_title": interview.interviewer_title,
                "feedback": interview.feedback,
                "notes": interview.notes,
            },
            "application": {
                "id": application.id,
                "company": application.company,
                "role": application.role,
                "location": application.location,
                "status": application.status,
                "applied_date": application.applied_date.isoformat() if application.applied_date else None,
                "salary_min": str(application.salary_min) if application.salary_min is not None else None,
                "salary_max": str(application.salary_max) if application.salary_max is not None else None,
                "notes": application.notes,
                "next_action": application.next_action,
                "next_action_date": application.next_action_date.isoformat() if application.next_action_date else None,
            },
            "job_description": {
                "title": description.title if description else None,
                "company": description.company if description else None,
                "source": description.source if description else None,
                "required_skills": description.required_skills if description else [],
                "preferred_skills": description.preferred_skills if description else [],
                "responsibilities": description.responsibilities if description else [],
                "keywords": description.extracted_keywords if description else [],
            },
            "skills": self._skills(description),
            "topics": self._topics(description, application),
            "activity": self._activity_context(application),
            "tasks": self._task_context(application),
            "preparation": self.preparation_score(application, interview),
        }

    def packet_for_application(self, application):
        interview = Interview.objects.filter(
            application=application,
            scheduled_date__isnull=False,
        ).order_by("-scheduled_date").first()
        if not interview:
            interview = Interview.objects.filter(application=application).order_by("-updated_at").first()
        if not interview:
            return {
                "application_id": application.id,
                "interview": None,
                "message": "No interview record is attached to this application yet.",
            }
        return self.packet_for_interview(interview)

    def dashboard(self):
        interviews = self.upcoming_interviews()
        packets = []
        for row in interviews:
            interview = Interview.objects.select_related("application").get(id=row["id"])
            packet = self.packet_for_interview(interview)
            if packet:
                packets.append({
                    "interview": packet["interview"],
                    "application": packet["application"],
                    "preparation": packet["preparation"],
                })
        return {
            "upcoming": interviews,
            "packets": packets,
            "summary": {
                "interviews": len(interviews),
                "prepared": sum(1 for item in packets if item["preparation"]["score"] >= 70),
                "needs_preparation": sum(1 for item in packets if item["preparation"]["score"] < 70),
                "average_score": round(
                    sum(item["preparation"]["score"] for item in packets) / len(packets), 1
                ) if packets else 0,
            },
        }
