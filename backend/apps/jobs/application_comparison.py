from collections import Counter
from decimal import Decimal
from .models import JobApplication, JobDescription, Interview, ApplicationActivity


class ApplicationComparison:
    """Compare two user-owned applications using explicit stored fields."""

    def __init__(self, user):
        self.user = user

    def _get(self, application_id):
        return JobApplication.objects.filter(user=self.user, id=application_id).first()

    @staticmethod
    def _salary_midpoint(application):
        if application.salary_min is not None and application.salary_max is not None:
            return (Decimal(application.salary_min) + Decimal(application.salary_max)) / Decimal("2")
        return application.salary_min or application.salary_max

    @staticmethod
    def _tokens(value):
        return {
            token.lower()
            for token in str(value or "").replace(",", " ").replace("/", " ").split()
            if len(token.strip()) > 1
        }

    def _description(self, application):
        return JobDescription.objects.filter(user=self.user, application=application).first()

    def _skills(self, description):
        if not description:
            return set()
        return self._tokens(" ".join(
            [str(x) for x in (description.required_skills or []) + (description.preferred_skills or [])]
        ))

    def _row(self, application):
        description = self._description(application)
        interviews = Interview.objects.filter(application=application)
        activities = ApplicationActivity.objects.filter(application=application, user=self.user)
        salary = self._salary_midpoint(application)
        skills = self._skills(description)
        return {
            "id": application.id,
            "company": application.company,
            "role": application.role,
            "location": application.location,
            "status": application.status,
            "salary_min": str(application.salary_min) if application.salary_min is not None else None,
            "salary_max": str(application.salary_max) if application.salary_max is not None else None,
            "salary_midpoint": str(salary) if salary is not None else None,
            "applied_date": application.applied_date.isoformat() if application.applied_date else None,
            "has_job_description": bool(description),
            "required_skills": description.required_skills if description else [],
            "preferred_skills": description.preferred_skills if description else [],
            "skill_count": len(skills),
            "interviews": interviews.count(),
            "passed_interviews": interviews.filter(outcome="passed").count(),
            "activities": activities.count(),
            "has_next_action": bool(application.next_action_date),
        }

    def compare(self, left_id, right_id):
        left = self._get(left_id)
        right = self._get(right_id)
        if not left or not right:
            return None
        left_row = self._row(left)
        right_row = self._row(right)
        left_skills = self._skills(self._description(left))
        right_skills = self._skills(self._description(right))
        shared = sorted(left_skills & right_skills)
        left_only = sorted(left_skills - right_skills)
        right_only = sorted(right_skills - left_skills)
        left_salary = self._salary_midpoint(left)
        right_salary = self._salary_midpoint(right)
        salary_delta = None
        if left_salary is not None and right_salary is not None:
            salary_delta = str(left_salary - right_salary)
        return {
            "left": left_row,
            "right": right_row,
            "differences": {
                "salary_midpoint_delta": salary_delta,
                "shared_skills": shared,
                "left_only_skills": left_only,
                "right_only_skills": right_only,
                "status_same": left.status == right.status,
                "location_same": left.location.strip().lower() == right.location.strip().lower(),
                "company_same": left.company.strip().lower() == right.company.strip().lower(),
                "activity_delta": left_row["activities"] - right_row["activities"],
                "interview_delta": left_row["interviews"] - right_row["interviews"],
            },
            "dimensions": [
                self._dimension("Salary midpoint", left_salary, right_salary),
                self._dimension("Skill coverage", left_row["skill_count"], right_row["skill_count"]),
                self._dimension("Interviews", left_row["interviews"], right_row["interviews"]),
                self._dimension("Activities", left_row["activities"], right_row["activities"]),
                self._dimension("Passed interviews", left_row["passed_interviews"], right_row["passed_interviews"]),
            ],
        }

    @staticmethod
    def _dimension(label, left, right):
        if left is None or right is None:
            relation = "unknown"
        elif left > right:
            relation = "left"
        elif right > left:
            relation = "right"
        else:
            relation = "equal"
        return {
            "label": label,
            "left": str(left) if left is not None else None,
            "right": str(right) if right is not None else None,
            "relation": relation,
        }

    def compare_many(self, application_ids):
        rows = []
        seen = set()
        for value in application_ids:
            try:
                application_id = int(value)
            except (TypeError, ValueError):
                continue
            if application_id in seen:
                continue
            seen.add(application_id)
            application = self._get(application_id)
            if application:
                rows.append(self._row(application))
        return rows

    def shortlist(self, limit=10):
        rows = [self._row(application) for application in self.user_applications()]
        rows.sort(
            key=lambda row: (
                -(1 if row["status"] == "offer" else 0),
                -(1 if row["status"] == "interview" else 0),
                -row["skill_count"],
                -row["interviews"],
                -row["activities"],
                row["company"].lower(),
            )
        )
        return rows[:limit]

    def user_applications(self):
        return JobApplication.objects.filter(user=self.user).order_by("-updated_at")

    def summary(self):
        applications = list(self.user_applications())
        salaries = [self._salary_midpoint(item) for item in applications if self._salary_midpoint(item) is not None]
        statuses = Counter(item.status for item in applications)
        described = sum(1 for item in applications if self._description(item))
        return {
            "applications": len(applications),
            "described": described,
            "without_description": len(applications) - described,
            "status_counts": dict(statuses),
            "salary_records": len(salaries),
            "average_salary_midpoint": str(round(sum(salaries) / len(salaries), 2)) if salaries else None,
            "shortlist": self.shortlist(),
        }
