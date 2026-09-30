from datetime import date, timedelta
from django.db.models import Avg, Count, Max, Min, Q
from .models import JobApplication, Interview


class JobApplicationService:
    """Application-domain operations kept outside the HTTP layer."""
    VALID_STATUSES = {choice[0] for choice in JobApplication.STATUS_CHOICES}

    def __init__(self, user):
        self.user = user

    def queryset(self):
        return JobApplication.objects.filter(user=self.user)

    def create(self, **data):
        data['user'] = self.user
        return JobApplication.objects.create(**data)

    def update_status(self, application, status):
        self._owned(application)
        if status not in self.VALID_STATUSES:
            raise ValueError('Unsupported application status')
        application.status = status
        application.save(update_fields=['status', 'updated_at'])
        return application

    def search(self, query='', status=None):
        qs = self.queryset()
        if query:
            qs = qs.filter(Q(company__icontains=query) | Q(role__icontains=query) |
                           Q(location__icontains=query) | Q(notes__icontains=query) |
                           Q(status__icontains=query))
        if status in self.VALID_STATUSES:
            qs = qs.filter(status=status)
        return qs

    def bulk_status(self, application_ids, status):
        if status not in self.VALID_STATUSES:
            raise ValueError('Unsupported application status')
        queryset = self.queryset().filter(id__in=list(application_ids))
        changed = queryset.update(status=status)
        return changed

    def counts_by_status(self):
        counts = {status: 0 for status in self.VALID_STATUSES}
        for row in self.queryset().values('status').annotate(total=Count('id')):
            counts[row['status']] = row['total']
        return counts

    def upcoming(self, days=14, limit=10):
        end = date.today() + timedelta(days=days)
        return self.queryset().filter(next_action_date__gte=date.today(), next_action_date__lte=end).order_by('next_action_date', 'company')[:limit]

    def overdue(self, limit=20):
        return self.queryset().filter(next_action_date__lt=date.today()).exclude(status__in=['rejected', 'withdrawn', 'offer']).order_by('next_action_date')[:limit]

    def dashboard(self):
        counts = self.counts_by_status()
        qs = self.queryset()
        return {'total': qs.count(), 'active': qs.exclude(status__in=['rejected', 'withdrawn']).count(),
                'offers': counts.get('offer', 0), 'interviews': counts.get('interview', 0),
                'by_status': counts, 'upcoming': self.upcoming(), 'overdue': self.overdue()}

    def pipeline_health(self):
        counts = self.counts_by_status()
        applied = counts.get('applied', 0)
        return {'screening_rate': self._rate(counts.get('screening', 0), applied),
                'interview_rate': self._rate(counts.get('interview', 0), applied),
                'offer_rate': self._rate(counts.get('offer', 0), applied),
                'total_tracked': sum(counts.values())}

    @staticmethod
    def _rate(numerator, denominator):
        return round(numerator / denominator * 100, 2) if denominator else 0.0

    def salary_statistics(self):
        rows = self.queryset().filter(salary_min__isnull=False, salary_max__isnull=False)
        result = rows.aggregate(avg_min=Avg('salary_min'), avg_max=Avg('salary_max'),
                                highest_min=Max('salary_min'), lowest_max=Min('salary_max'))
        return {'count': rows.count(), **{key: value or 0 for key, value in result.items()}}

    def interviews_summary(self, application):
        self._owned(application)
        interviews = Interview.objects.filter(application=application)
        return {'total': interviews.count(), 'pending': interviews.filter(outcome='pending').count(),
                'passed': interviews.filter(outcome='passed').count(), 'failed': interviews.filter(outcome='failed').count(),
                'interviews': list(interviews.values('interview_type', 'outcome', 'scheduled_date'))}

    def application_timeline(self, application):
        self._owned(application)
        timeline = [{'date': application.created_at, 'event': 'Application created', 'type': 'created'}]
        if application.applied_date:
            timeline.append({'date': application.applied_date, 'event': 'Applied', 'type': 'applied'})
        for interview in Interview.objects.filter(application=application).order_by('scheduled_date'):
            if interview.scheduled_date:
                timeline.append({'date': interview.scheduled_date, 'event': f'{interview.get_interview_type_display()} - {interview.get_outcome_display()}', 'type': 'interview'})
        if application.next_action_date:
            timeline.append({'date': application.next_action_date, 'event': f'Follow-up: {application.next_action}', 'type': 'followup'})
        return sorted(timeline, key=lambda item: item['date'], reverse=True)

    def export_rows(self):
        fields = ('company', 'role', 'location', 'status', 'job_url', 'applied_date', 'next_action', 'next_action_date', 'notes')
        return list(self.queryset().values(*fields).order_by('company', 'role'))

    def _owned(self, application):
        if application.user_id != self.user.id:
            raise PermissionError('Application does not belong to this user')
