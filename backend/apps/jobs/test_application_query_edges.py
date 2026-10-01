from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from .models import JobApplication
from .application_query import ApplicationQueryService


class ApplicationQueryEdgeCaseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="edge-query", password="pass12345")
        self.service = ApplicationQueryService(self.user)
        self.applications = [
            JobApplication.objects.create(
                user=self.user, company="Alpha", role="Engineer",
                status="saved", location="", notes="", salary_min=None, salary_max=None,
            ),
            JobApplication.objects.create(
                user=self.user, company="Beta", role="Data Scientist",
                status="screening", location="Nairobi",
                notes="Research", salary_min=Decimal("60000"), salary_max=Decimal("80000"),
            ),
            JobApplication.objects.create(
                user=self.user, company="Gamma", role="Product Engineer",
                status="withdrawn", location="Remote",
                notes="Closed", next_action_date=date.today()-timedelta(days=2),
            ),
        ]

    def test_blank_company_list_keeps_queryset(self):
        self.assertEqual(self.service().companies(self.service.base, []).count(), 3)

    def test_blank_location_list_keeps_queryset(self):
        self.assertEqual(self.service().locations(self.service.base, []).count(), 3)

    def test_blank_status_list_keeps_queryset(self):
        self.assertEqual(self.service().statuses(self.service.base, []).count(), 3)

    def test_blank_role_keyword_keeps_queryset(self):
        self.assertEqual(self.service().with_role_keyword(self.service.base, "").count(), 3)

    def test_salary_presence_only_returns_records_with_any_salary(self):
        self.assertEqual(self.service().has_salary(self.service.base, True).count(), 1)

    def test_follow_up_filter_only_returns_records_with_dates(self):
        self.applications[0].next_action_date = date.today()+timedelta(days=1)
        self.applications[0].save()
        self.assertEqual(self.service().has_follow_up(self.service.base, True).count(), 1)

    def test_date_range_start(self):
        start = date.today()-timedelta(days=1)
        self.assertEqual(self.service().date_range(self.service.base, start=start).count(), 3)

    def test_date_range_future_excludes_existing_rows(self):
        end = date.today()-timedelta(days=30)
        self.assertEqual(self.service().date_range(self.service.base, end=end).count(), 0)

    def test_salary_range_accepts_decimal_values(self):
        rows = self.service().salary_range(self.service.base, Decimal("70000"), Decimal("90000"))
        self.assertEqual(rows.count(), 1)

    def test_overdue_excludes_closed_status(self):
        rows = self.service().overdue(self.service.base)
        self.assertEqual(rows.count(), 0)

    def test_due_between_defaults_to_next_week(self):
        self.applications[0].next_action_date = date.today()+timedelta(days=2)
        self.applications[0].save()
        self.assertEqual(self.service().due_between(self.service.base).count(), 1)

    def test_no_notes_only_matches_empty_notes(self):
        self.assertEqual(self.service().no_notes(self.service.base).count(), 1)

    def test_search_matches_notes(self):
        self.assertEqual(self.service().search("Research").count(), 1)

    def test_search_matches_location(self):
        self.assertEqual(self.service().search("Nairobi").count(), 1)

    def test_search_matches_company(self):
        self.assertEqual(self.service().search("Alpha").count(), 1)

    def test_search_matches_role(self):
        self.assertEqual(self.service().search("Scientist").count(), 1)

    def test_distinct_locations_omits_blank(self):
        self.assertEqual(list(self.service().distinct_locations(self.service.base)), ["Nairobi", "Remote"])

    def test_facets_include_every_status(self):
        self.assertEqual(set(self.service().facets()["statuses"]), {"saved", "screening", "withdrawn"})

    def test_counts_with_salary(self):
        self.assertEqual(self.service().counts()["with_salary"], 1)

    def test_counts_with_notes(self):
        self.assertEqual(self.service().counts()["with_notes"], 2)

    def test_counts_closed(self):
        self.assertEqual(self.service().counts()["closed"], 1)

    def test_serialize_limit_zero_returns_no_rows(self):
        self.assertEqual(self.service().serialize(self.service.base, limit=0), [])

    def test_serialize_preserves_company_and_role(self):
        row = self.service().serialize(self.service.base, limit=1)[0]
        self.assertIn("company", row)
        self.assertIn("role", row)

    def test_explorer_passes_query_to_counts(self):
        data = self.service().explorer(query="Nairobi")
        self.assertEqual(data["counts"]["total"], 1)

    def test_explorer_can_filter_active(self):
        data = self.service().explorer(active_only=True)
        self.assertEqual(data["counts"]["closed"], 0)

    def test_explorer_can_filter_salary(self):
        data = self.service().explorer(has_salary=True)
        self.assertEqual(data["counts"]["total"], 1)

    def test_sort_company_is_supported(self):
        rows = self.service().sort(self.service.base, "company")
        self.assertEqual(rows.first().company, "Alpha")

    def test_sort_role_is_supported(self):
        rows = self.service().sort(self.service.base, "role")
        self.assertEqual(rows.first().role, "Data Scientist")

    def test_sort_salary_low_is_supported(self):
        rows = self.service().sort(self.service.base, "salary_low")
        self.assertEqual(rows.first().salary_min, Decimal("60000"))

    def test_sort_follow_up_is_supported(self):
        self.applications[0].next_action_date = date.today()+timedelta(days=1)
        self.applications[0].save()
        rows = self.service().sort(self.service.base, "follow_up")
        self.assertEqual(rows.first().id, self.applications[0].id)

    def test_user_scope_is_always_applied(self):
        other = User.objects.create_user(username="edge-other", password="pass12345")
        JobApplication.objects.create(user=other, company="Hidden", role="Engineer", status="offer")
        self.assertEqual(self.service().base.count(), 3)
        self.assertNotIn("Hidden", list(self.service().distinct_companies(self.service.base)))

    def test_query_service_is_reusable(self):
        first = self.service().counts()
        second = self.service().counts()
        self.assertEqual(first, second)

    def test_query_without_filters_is_stable(self):
        rows = self.service().apply()
        self.assertEqual(rows.count(), 3)

    def test_status_filter_accepts_multiple_values(self):
        rows = self.service().statuses(self.service.base, ["saved", "screening"])
        self.assertEqual(rows.count(), 2)

    def test_company_filter_requires_exact_company_name(self):
        rows = self.service().companies(self.service.base, ["Alpha"])
        self.assertEqual(rows.count(), 1)

    def test_location_filter_supports_partial_value(self):
        rows = self.service().locations(self.service.base, ["Nai"])
        self.assertEqual(rows.count(), 1)

    def test_active_filter_keeps_saved_and_screening(self):
        rows = self.service().active_only(self.service.base, True)
        self.assertEqual(rows.count(), 2)
