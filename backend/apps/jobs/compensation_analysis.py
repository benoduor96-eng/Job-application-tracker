from dataclasses import dataclass
from decimal import Decimal

from .models import JobApplication


@dataclass
class CompensationResult:
    application_id: int
    company: str
    role: str
    salary_min: Decimal | None
    salary_max: Decimal | None
    midpoint: Decimal | None
    target_salary: Decimal | None
    minimum_salary: Decimal | None
    midpoint_vs_target: Decimal | None
    midpoint_vs_minimum: Decimal | None
    position: str

    def to_dict(self):
        def number(value):
            return float(value) if value is not None else None

        return {
            "application_id": self.application_id,
            "company": self.company,
            "role": self.role,
            "salary_min": number(self.salary_min),
            "salary_max": number(self.salary_max),
            "midpoint": number(self.midpoint),
            "target_salary": number(self.target_salary),
            "minimum_salary": number(self.minimum_salary),
            "midpoint_vs_target": number(self.midpoint_vs_target),
            "midpoint_vs_minimum": number(self.midpoint_vs_minimum),
            "position": self.position,
        }


class CompensationAnalysisService:
    def __init__(self, user):
        self.user = user

    def analyze(self, application_id):
        application = JobApplication.objects.filter(
            id=application_id, user=self.user
        ).first()
        if not application:
            return None

        profile = getattr(self.user, "career_profile", None)
        minimum = profile.minimum_salary if profile else None
        target = profile.target_salary if profile else None

        salary_min = application.salary_min
        salary_max = application.salary_max
        midpoint = None
        if salary_min is not None and salary_max is not None:
            midpoint = (salary_min + salary_max) / Decimal("2")
        elif salary_min is not None:
            midpoint = salary_min
        elif salary_max is not None:
            midpoint = salary_max

        vs_target = None
        vs_minimum = None
        if midpoint is not None and target:
            vs_target = ((midpoint - target) / target) * Decimal("100")
        if midpoint is not None and minimum:
            vs_minimum = ((midpoint - minimum) / minimum) * Decimal("100")

        if midpoint is None:
            position = "unknown"
        elif minimum and midpoint < minimum:
            position = "below_minimum"
        elif target and midpoint >= target:
            position = "at_or_above_target"
        elif target:
            position = "between_minimum_and_target"
        else:
            position = "meets_minimum"

        return CompensationResult(
            application_id=application.id,
            company=application.company,
            role=application.role,
            salary_min=salary_min,
            salary_max=salary_max,
            midpoint=midpoint,
            target_salary=target,
            minimum_salary=minimum,
            midpoint_vs_target=vs_target,
            midpoint_vs_minimum=vs_minimum,
            position=position,
        )

    def summary(self, limit=50):
        applications = JobApplication.objects.filter(
            user=self.user,
            status__in=["applied", "screening", "interview", "offer"],
        ).order_by("-updated_at")[:limit]
        results = [self.analyze(item.id) for item in applications]
        results = [item for item in results if item]

        with_salary = [item for item in results if item.midpoint is not None]
        average = (
            sum(item.midpoint for item in with_salary) / len(with_salary)
            if with_salary else None
        )
        return {
            "count": len(results),
            "with_salary": len(with_salary),
            "average_midpoint": float(average) if average is not None else None,
            "at_or_above_target": sum(
                item.position == "at_or_above_target" for item in results
            ),
            "below_minimum": sum(
                item.position == "below_minimum" for item in results
            ),
            "applications": [item.to_dict() for item in results],
        }
