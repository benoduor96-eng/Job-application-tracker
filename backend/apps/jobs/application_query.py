from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Q
from .models import JobApplication


class ApplicationQueryService:
    """Composable, user-scoped application filtering and sorting."""

    VALID_SORTS = {
        "updated": "-updated_at",
        "created": "-created_at",
        "company": "company",
        "role": "role",
        "applied": "-applied_date",
        "follow_up": "next_action_date",
        "salary_high": "-salary_max",
        "salary_low": "salary_min",
    }

    def __init__(self, user):
        self.user = user
        self.base = JobApplication.objects.filter(user=user)

    def search(self, query=""):
        value = (query or "").strip()
        if not value:
            return self.base
        return self.base.filter(
            Q(company__icontains=value)
            | Q(role__icontains=value)
            | Q(location__icontains=value)
            | Q(notes__icontains=value)
            | Q(next_action__icontains=value)
        )

    def statuses(self, queryset, values):
        selected = [value.strip() for value in (values or []) if value and value.strip()]
        return queryset.filter(status__in=selected) if selected else queryset

    def companies(self, queryset, values):
        selected = [value.strip() for value in (values or []) if value and value.strip()]
        return queryset.filter(company__in=selected) if selected else queryset

    def locations(self, queryset, values):
        selected = [value.strip() for value in (values or []) if value and value.strip()]
        if not selected:
            return queryset
        condition = Q()
        for value in selected:
            condition |= Q(location__icontains=value)
        return queryset.filter(condition)

    def active_only(self, queryset, enabled=False):
        if not enabled:
            return queryset
        return queryset.exclude(status__in=["rejected", "withdrawn"])

    def has_salary(self, queryset, enabled=False):
        if not enabled:
            return queryset
        return queryset.filter(status__in=["saved", "applied", "screening", "interview", "offer"]).filter(Q(salary_min__isnull=False) | Q(salary_max__isnull=False))

    def has_follow_up(self, queryset, enabled=False):
        if not enabled:
            return queryset
        return queryset.filter(status__in=["saved", "applied", "screening", "interview", "offer"], next_action_date__isnull=False)

    def date_range(self, queryset, start=None, end=None, field="created_at"):
        if start:
            queryset = queryset.filter(**{f"{field}__date__gte": start})
        if end:
            queryset = queryset.filter(**{f"{field}__date__lte": end})
        return queryset

    def salary_range(self, queryset, minimum=None, maximum=None):
        """Filter advertised salary ranges using inclusive search bounds."""
        if minimum is not None:
            queryset = queryset.filter(
                Q(salary_min__gte=minimum)
                | Q(salary_min__isnull=True, salary_max__gte=minimum)
            )
        if maximum is not None:
            queryset = queryset.filter(
                Q(salary_max__gte=maximum)
                | Q(salary_max__isnull=True, salary_min__lte=maximum)
            )
        return queryset

    def overdue(self, queryset, today=None):
        today = today or date.today()
        return queryset.filter(
            status__in=["saved", "applied", "screening", "interview", "offer"],
            next_action_date__lt=today,
        )

    def due_between(self, queryset, start=None, end=None):
        start = start or date.today()
        end = end or start + timedelta(days=7)
        return queryset.filter(next_action_date__gte=start, next_action_date__lte=end)

    def no_follow_up(self, queryset):
        return queryset.filter(next_action_date__isnull=True)

    def no_notes(self, queryset):
        return queryset.filter(notes="")

    def with_role_keyword(self, queryset, keyword):
        value = (keyword or "").strip()
        return queryset.filter(role__icontains=value) if value else queryset

    def sort(self, queryset, key="updated"):
        field = self.VALID_SORTS.get(key, "-updated_at")
        if key in {"follow_up", "salary_low"}:
            from django.db.models import Case, When, Value, IntegerField
            nullable_field = "next_action_date" if key == "follow_up" else "salary_min"
            annotations = {
                "_null_sort": Case(
                    When(**{f"{nullable_field}__isnull": True}, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            }
            if key == "follow_up":
                annotations["_closed_sort"] = Case(
                    When(status__in=["rejected", "withdrawn"], then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            order_fields = (["_closed_sort"] if key == "follow_up" else []) + ["_null_sort", field]
            return queryset.annotate(**annotations).order_by(*order_fields)
        return queryset.order_by(field)

    def distinct_companies(self, queryset):
        return queryset.values_list("company", flat=True).distinct().order_by("company")

    def distinct_locations(self, queryset):
        return queryset.exclude(location="").values_list("location", flat=True).distinct().order_by("location")

    def apply(self, **filters):
        queryset = self.base
        queryset = self.search(filters.get("query"))
        queryset = self.statuses(queryset, filters.get("statuses"))
        queryset = self.companies(queryset, filters.get("companies"))
        queryset = self.locations(queryset, filters.get("locations"))
        queryset = self.active_only(queryset, filters.get("active_only", False))
        queryset = self.has_salary(queryset, filters.get("has_salary", False))
        queryset = self.has_follow_up(queryset, filters.get("has_follow_up", False))
        queryset = self.salary_range(queryset, filters.get("salary_min"), filters.get("salary_max"))
        queryset = self.with_role_keyword(queryset, filters.get("role_keyword"))
        queryset = self.date_range(queryset, filters.get("created_start"), filters.get("created_end"), "created_at")
        return self.sort(queryset, filters.get("sort", "updated"))

    def facets(self):
        return {
            "statuses": list(self.base.values_list("status", flat=True).distinct().order_by("status")),
            "companies": list(self.distinct_companies(self.base)),
            "locations": list(self.distinct_locations(self.base)),
            "sorts": sorted(self.VALID_SORTS),
        }

    def counts(self, queryset=None):
        queryset = queryset or self.base
        return {
            "total": queryset.count(),
            "active": queryset.exclude(status__in=["rejected", "withdrawn"]).count(),
            "closed": queryset.filter(status__in=["rejected", "withdrawn"]).count(),
            "with_salary": queryset.filter(Q(salary_min__isnull=False) | Q(salary_max__isnull=False)).count(),
            "with_follow_up": queryset.filter(next_action_date__isnull=False).count(),
            "with_notes": queryset.exclude(notes="").count(),
        }

    def serialize(self, queryset, limit=100):
        rows = []
        for application in queryset[:limit]:
            rows.append({
                "id": application.id,
                "company": application.company,
                "role": application.role,
                "location": application.location,
                "status": application.status,
                "salary_min": str(application.salary_min) if application.salary_min is not None else None,
                "salary_max": str(application.salary_max) if application.salary_max is not None else None,
                "applied_date": application.applied_date.isoformat() if application.applied_date else None,
                "next_action": application.next_action,
                "next_action_date": application.next_action_date.isoformat() if application.next_action_date else None,
                "updated_at": application.updated_at.isoformat(),
            })
        return rows

    def explorer(self, **filters):
        queryset = self.apply(**filters)
        return {
            "filters": filters,
            "counts": self.counts(queryset),
            "facets": self.facets(),
            "applications": self.serialize(queryset),
        }
