"""Application data-quality and audit analytics.

The audit service is intentionally read-only. It inspects the user's stored
applications, interviews, contacts, descriptions, tasks, and profile signals
and turns missing or inconsistent data into actionable findings.
"""
from collections import Counter
from datetime import timedelta
from django.db.models import Count, Q
from django.utils import timezone

from .models import (
    CareerContact,
    CareerProfile,
    CareerTask,
    Interview,
    JobApplication,
    JobDescription,
    Resume,
)


ACTIVE = {"saved", "applied", "screening", "interview", "offer"}
CLOSED = {"rejected", "withdrawn"}
KNOWN_STATUSES = ACTIVE | CLOSED


class ApplicationAuditService:
    """Produce deterministic, user-scoped data-quality findings."""

    SEVERITY_WEIGHT = {"critical": 40, "high": 25, "medium": 15, "low": 5, "info": 0}

    def __init__(self, user, now=None):
        self.user = user
        self.now = now or timezone.now()
        self.today = self.now.date()
        self.applications = JobApplication.objects.filter(user=user)
        self.interviews = Interview.objects.filter(application__user=user)
        self.contacts = CareerContact.objects.filter(user=user)
        self.tasks = CareerTask.objects.filter(user=user)
        self.descriptions = JobDescription.objects.filter(user=user)
        self.resumes = Resume.objects.filter(user=user)
        self.profile = CareerProfile.objects.filter(user=user).first()

    def _finding(self, code, severity, title, detail, application=None, field=None):
        return {
            "code": code,
            "severity": severity,
            "title": title,
            "detail": detail,
            "application_id": application.id if application else None,
            "company": application.company if application else None,
            "role": application.role if application else None,
            "field": field,
        }

    def missing_next_action(self):
        rows = []
        for app in self.applications.filter(status__in=ACTIVE).order_by("updated_at"):
            if not app.next_action_date:
                rows.append(self._finding(
                    "missing_next_action", "medium",
                    "Active application has no next action",
                    "Set a concrete follow-up date and action so the application remains actionable.",
                    app, "next_action_date",
                ))
        return rows

    def missing_job_url(self):
        rows = []
        for app in self.applications.filter(status__in=ACTIVE):
            if not (app.job_url or "").strip():
                rows.append(self._finding(
                    "missing_job_url", "low",
                    "Active application has no job URL",
                    "Add the original listing URL so the role can be revisited quickly.",
                    app, "job_url",
                ))
        return rows

    def missing_notes(self):
        rows = []
        for app in self.applications.filter(status__in={"screening", "interview", "offer"}):
            if not (app.notes or "").strip():
                rows.append(self._finding(
                    "missing_notes", "medium",
                    "Pipeline-stage application has no notes",
                    "Capture role-specific context, recruiter details, interview preparation, or decisions.",
                    app, "notes",
                ))
        return rows

    def applied_without_applied_date(self):
        rows = []
        for app in self.applications.filter(status__in=ACTIVE):
            if app.status != "saved" and not app.applied_date:
                rows.append(self._finding(
                    "missing_applied_date", "high",
                    "Application status is active but applied date is missing",
                    "Record when the application was submitted to make response-time and funnel analytics reliable.",
                    app, "applied_date",
                ))
        return rows

    def interview_without_schedule(self):
        rows = []
        for interview in self.interviews.select_related("application"):
            app = interview.application
            if app.user_id != self.user.id:
                continue
            if not interview.scheduled_date and interview.outcome in {"scheduled", "pending"}:
                rows.append(self._finding(
                    "interview_missing_schedule", "high",
                    "Pending interview has no scheduled time",
                    "Add the interview date and time so it appears in the calendar and preparation workflow.",
                    app, "scheduled_date",
                ))
        return rows

    def interview_without_application_context(self):
        rows = []
        for interview in self.interviews.select_related("application"):
            app = interview.application
            if not app:
                continue
            if not interview.interviewer_name and not interview.notes:
                rows.append(self._finding(
                    "interview_missing_context", "low",
                    "Interview record has little context",
                    "Add interviewer information or notes to improve preparation and follow-up.",
                    app, "interviewer_name",
                ))
        return rows

    def overdue_next_actions(self):
        rows = []
        for app in self.applications.filter(status__in=ACTIVE):
            if app.next_action_date and app.next_action_date < self.today:
                age = (self.today - app.next_action_date).days
                severity = "high" if age >= 7 else "medium"
                rows.append(self._finding(
                    "overdue_next_action", severity,
                    "Next action is overdue",
                    f"The recorded next action is {age} day(s) overdue.",
                    app, "next_action_date",
                ))
        return rows

    def stale_active_applications(self, days=30):
        cutoff = self.now - timedelta(days=days)
        rows = []
        for app in self.applications.filter(status__in={"saved", "applied"}):
            if app.updated_at < cutoff:
                age = (self.now - app.updated_at).days
                rows.append(self._finding(
                    "stale_application", "medium",
                    "Early-stage application is stale",
                    f"No application record update has been made for {age} day(s).",
                    app, "updated_at",
                ))
        return rows

    def duplicate_role_records(self):
        groups = {}
        for app in self.applications:
            key = (app.company.strip().lower(), app.role.strip().lower())
            groups.setdefault(key, []).append(app)
        rows = []
        for (company, role), apps in groups.items():
            if len(apps) < 2:
                continue
            active = [a for a in apps if a.status in ACTIVE]
            if len(active) > 1:
                rows.append(self._finding(
                    "duplicate_active_role", "high",
                    "Multiple active records target the same company and role",
                    f"{len(active)} active records share the normalized company/role pair.",
                    active[0],
                ))
        return rows

    def duplicate_company_records(self):
        groups = {}
        for app in self.applications:
            key = app.company.strip().lower()
            groups.setdefault(key, []).append(app)
        rows = []
        for company, apps in groups.items():
            roles = {a.role.strip().lower() for a in apps}
            if len(apps) >= 3 and len(roles) == 1:
                rows.append(self._finding(
                    "repeated_company_role", "low",
                    "Company has repeated records for one role",
                    f"{len(apps)} records exist for the same normalized role at this company.",
                    apps[0],
                ))
        return rows

    def contact_followup_gaps(self):
        rows = []
        for contact in self.contacts:
            if contact.last_contacted_at and not contact.next_follow_up:
                app = contact.application
                rows.append(self._finding(
                    "contact_missing_followup", "low",
                    "Contact has recent activity but no follow-up date",
                    "Add a follow-up date when continued relationship management is appropriate.",
                    app,
                    "next_follow_up",
                ))
        return rows

    def description_gaps(self):
        rows = []
        linked_ids = set(self.descriptions.values_list("application_id", flat=True))
        for app in self.applications.filter(status__in=ACTIVE):
            if app.id not in linked_ids:
                rows.append(self._finding(
                    "missing_job_description", "medium",
                    "Active application has no job description",
                    "Attach or record the job description to support fit and preparation analysis.",
                    app,
                    "job_description",
                ))
        return rows

    def asset_gaps(self):
        rows = []
        if not self.profile:
            rows.append(self._finding(
                "missing_profile", "high",
                "Career profile is missing",
                "Create a profile with skills, preferred roles, and work preferences.",
            ))
            return rows
        if not (self.profile.skills or []):
            rows.append(self._finding(
                "profile_missing_skills", "high",
                "Career profile has no skills",
                "Add the skills used by fit analysis and application matching.",
            ))
        if not (self.profile.preferred_roles or []):
            rows.append(self._finding(
                "profile_missing_roles", "medium",
                "Career profile has no preferred roles",
                "Add target roles to make role-fit analysis more useful.",
            ))
        if not self.resumes.exists():
            rows.append(self._finding(
                "missing_resume", "high",
                "No resume is stored",
                "Add at least one resume version for application readiness.",
            ))
        return rows

    def task_gaps(self):
        rows = []
        for task in self.tasks.filter(status__in={"todo", "in_progress"}):
            if task.due_date and task.due_date.date() < self.today:
                app = task.application
                rows.append(self._finding(
                    "overdue_task", "medium",
                    "Career task is overdue",
                    f"Task '{task.title}' is past its due date.",
                    app,
                    "due_date",
                ))
        return rows

    def all_findings(self):
        methods = (
            self.missing_next_action,
            self.missing_job_url,
            self.missing_notes,
            self.applied_without_applied_date,
            self.interview_without_schedule,
            self.interview_without_application_context,
            self.overdue_next_actions,
            self.stale_active_applications,
            self.duplicate_role_records,
            self.duplicate_company_records,
            self.contact_followup_gaps,
            self.description_gaps,
            self.asset_gaps,
            self.task_gaps,
        )
        findings = []
        for method in methods:
            findings.extend(method())
        findings.sort(key=lambda item: (
            -self.SEVERITY_WEIGHT.get(item["severity"], 0),
            item["company"] or "",
            item["role"] or "",
            item["title"],
        ))
        return findings

    def summary(self):
        findings = self.all_findings()
        severity = Counter(item["severity"] for item in findings)
        categories = Counter(item["code"] for item in findings)
        score = max(0, 100 - sum(self.SEVERITY_WEIGHT.get(item["severity"], 0) for item in findings))
        return {
            "score": score,
            "total_findings": len(findings),
            "by_severity": {key: severity.get(key, 0) for key in ("critical", "high", "medium", "low", "info")},
            "by_category": dict(categories),
            "applications": self.applications.count(),
            "active_applications": self.applications.filter(status__in=ACTIVE).count(),
            "interviews": self.interviews.count(),
            "contacts": self.contacts.count(),
            "tasks": self.tasks.count(),
            "job_descriptions": self.descriptions.count(),
            "resumes": self.resumes.count(),
        }

    def application_scores(self):
        findings = self.all_findings()
        grouped = {}
        for finding in findings:
            app_id = finding.get("application_id")
            if not app_id:
                continue
            grouped.setdefault(app_id, []).append(finding)
        rows = []
        for app in self.applications.filter(status__in=ACTIVE):
            items = grouped.get(app.id, [])
            penalty = sum(self.SEVERITY_WEIGHT.get(item["severity"], 0) for item in items)
            rows.append({
                "application_id": app.id,
                "company": app.company,
                "role": app.role,
                "status": app.status,
                "score": max(0, 100 - penalty),
                "finding_count": len(items),
                "high_priority": sum(item["severity"] in {"critical", "high"} for item in items),
                "codes": sorted({item["code"] for item in items}),
            })
        return sorted(rows, key=lambda row: (row["score"], row["company"].lower(), row["role"].lower()))

    def company_scores(self):
        grouped = {}
        for app in self.applications:
            key = app.company.strip().lower()
            grouped.setdefault(key, []).append(app)
        findings = self.all_findings()
        counts = Counter(item.get("company") for item in findings if item.get("company"))
        rows = []
        for key, apps in grouped.items():
            company = apps[0].company
            finding_count = counts.get(company, 0)
            rows.append({
                "company": company,
                "applications": len(apps),
                "active": sum(a.status in ACTIVE for a in apps),
                "findings": finding_count,
                "score": max(0, 100 - finding_count * 10),
            })
        return sorted(rows, key=lambda row: (-row["findings"], row["company"].lower()))

    def dashboard(self, limit=50):
        findings = self.all_findings()
        return {
            "summary": self.summary(),
            "findings": findings[:limit],
            "applications": self.application_scores()[:limit],
            "companies": self.company_scores()[:limit],
            "recommendations": self.recommendations(),
        }

    def recommendations(self):
        summary = self.summary()
        recommendations = []
        if summary["by_severity"]["high"]:
            recommendations.append({
                "priority": "high",
                "title": "Resolve high-priority data gaps",
                "detail": "Complete missing dates, profile information, interview scheduling, or other high-impact fields first.",
            })
        if summary["by_category"].get("missing_job_description"):
            recommendations.append({
                "priority": "medium",
                "title": "Attach job descriptions",
                "detail": "Job descriptions improve fit scoring, interview preparation, and opportunity review.",
            })
        if summary["by_category"].get("missing_next_action"):
            recommendations.append({
                "priority": "medium",
                "title": "Plan the next step",
                "detail": "Every active application should have a next action and a date.",
            })
        if summary["by_category"].get("overdue_next_action"):
            recommendations.append({
                "priority": "high",
                "title": "Clear overdue follow-ups",
                "detail": "Review overdue application actions and update their dates or outcomes.",
            })
        if summary["score"] >= 90:
            recommendations.append({
                "priority": "low",
                "title": "Keep the dataset healthy",
                "detail": "Continue recording dates, notes, descriptions, and follow-ups as the pipeline changes.",
            })
        return recommendations
