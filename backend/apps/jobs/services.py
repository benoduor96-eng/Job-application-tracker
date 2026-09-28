from datetime import date, timedelta

from django.db.models import Count, Q

from .models import JobApplication


class JobApplicationService:
    """Application-domain operations kept outside the HTTP layer."""

    VALID_STATUSES = {choice[0] for choice in JobApplication.STATUS_CHOICES}

    def __init__(self, user):
        self.user = user

    def queryset(self):
        return JobApplication.objects.filter(user=self.user)

    def create(self, **data):
        data["user"] = self.user
        return JobApplication.objects.create(**data)

    def update_status(self, application, status):
        if application.user_id != self.user.id:
            raise PermissionError("Application does not belong to this user")
        if status not in self.VALID_STATUSES:
            raise ValueError("Unsupported application status")
        application.status = status
        application.save(update_fields=["status", "updated_at"])
        return application

    def search(self, query="", status=None):
        qs = self.queryset()
        if query:
            qs = qs.filter(
                Q(company__icontains=query)
                | Q(role__icontains=query)
                | Q(location__icontains=query)
                | Q(notes__icontains=query)
            )
        if status and status in self.VALID_STATUSES:
            qs = qs.filter(status=status)
        return qs

    def counts_by_status(self):
        counts = {
            status: 0
            for status in self.VALID_STATUSES
        }
        rows = self.queryset().values("status").annotate(total=Count("id"))
        for row in rows:
            counts[row["status"]] = row["total"]
        return counts

    def upcoming(self, days=14, limit=10):
        today = date.today()
        end = today + timedelta(days=days)
        return self.queryset().filter(
            next_action_date__gte=today,
            next_action_date__lte=end,
        ).order_by("next_action_date", "company")[:limit]

    def overdue(self, limit=20):
        return self.queryset().filter(
            next_action_date__lt=date.today(),
        ).exclude(
            status__in=["rejected", "withdrawn", "offer"],
        ).order_by("next_action_date")[:limit]

    def dashboard(self):
        qs = self.queryset()
        counts = self.counts_by_status()
        return {
            "total": qs.count(),
            "active": qs.exclude(status__in=["rejected", "withdrawn"]).count(),
            "offers": counts.get("offer", 0),
            "interviews": counts.get("interview", 0),
            "by_status": counts,
            "upcoming": self.upcoming(),
            "overdue": self.overdue(),
        }

    def pipeline_health(self):
        counts = self.counts_by_status()
        applied = counts.get("applied", 0)
        interviews = counts.get("interview", 0)
        offers = counts.get("offer", 0)
        return {
            "screening_rate": self._rate(counts.get("screening", 0), applied),
            "interview_rate": self._rate(interviews, applied),
            "offer_rate": self._rate(offers, applied),
            "total_tracked": sum(counts.values()),
        }

    @staticmethod
    def _rate(numerator, denominator):
        if denominator == 0:
            return 0.0
        return round((numerator / denominator) * 100, 2)

    def bulk_status(self, application_ids, status):
        if status not in self.VALID_STATUSES:
            raise ValueError("Unsupported application status")
        return self.queryset().filter(id__in=application_ids).update(
            status=status,
        )

    def delete(self, application):
        if application.user_id != self.user.id:
            raise PermissionError("Application does not belong to this user")
        application.delete()

    def export_rows(self):
        fields = (
            "company",
            "role",
            "location",
            "status",
            "job_url",
            "applied_date",
            "next_action",
            "next_action_date",
            "notes",
        )
        return list(self.queryset().values(*fields).order_by("company", "role"))
