from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from .models import JobApplication
from .application_query import ApplicationQueryService


class ApplicationQueryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="query", password="pass12345")
        self.other = User.objects.create_user(username="other-query", password="pass12345")
        self.make("Acme", "Backend Engineer", "applied", "Remote", 90000, 110000, "Email recruiter")
        self.make("Beta", "Frontend Engineer", "screening", "Nairobi", 70000, 90000, "Prepare portfolio")
        self.make("Gamma", "Data Engineer", "rejected", "Remote", None, None, "")
        self.make("Acme", "Senior Python Engineer", "offer", "Remote", 100000, 130000, "Negotiate")
        JobApplication.objects.create(user=self.other, company="Private", role="Engineer", status="offer")

    def make(self, company, role, status, location, minimum, maximum, notes):
        return JobApplication.objects.create(
            user=self.user, company=company, role=role, status=status,
            location=location, salary_min=minimum, salary_max=maximum, notes=notes,
            next_action_date=date.today() + timedelta(days=2) if status in {"applied","screening"} else None,
        )

    def service(self):
        return ApplicationQueryService(self.user)

    def test_search_matches_multiple_text_fields(self):
        self.assertEqual(self.service().search("Python").count(), 1)
        self.assertEqual(self.service().search("Remote").count(), 3)

    def test_status_filter(self):
        rows=self.service().statuses(self.service().base,["offer","applied"])
        self.assertEqual(rows.count(),2)

    def test_company_filter(self):
        self.assertEqual(self.service().companies(self.service().base,["Acme"]).count(),2)

    def test_location_filter_is_case_insensitive(self):
        self.assertEqual(self.service().locations(self.service().base,["remote"]).count(),3)

    def test_active_only_excludes_closed(self):
        self.assertEqual(self.service().active_only(self.service().base,True).count(),3)

    def test_salary_presence(self):
        self.assertEqual(self.service().has_salary(self.service().base,True).count(),3)

    def test_follow_up_presence(self):
        self.assertEqual(self.service().has_follow_up(self.service().base,True).count(),2)

    def test_salary_range(self):
        self.assertEqual(self.service().salary_range(self.service().base,100000,None).count(),1)
        self.assertEqual(self.service().salary_range(self.service().base,None,80000).count(),2)

    def test_overdue(self):
        old=self.make("Old","Engineer","applied","Remote",50000,60000,"")
        old.next_action_date=date.today()-timedelta(days=1);old.save()
        self.assertEqual(self.service().overdue(self.service().base).count(),1)

    def test_due_between(self):
        rows=self.service().due_between(self.service().base,date.today(),date.today()+timedelta(days=3))
        self.assertEqual(rows.count(),2)

    def test_no_follow_up(self):
        self.assertEqual(self.service().no_follow_up(self.service().base).count(),2)

    def test_no_notes(self):
        self.assertEqual(self.service().no_notes(self.service().base).count(),1)

    def test_role_keyword(self):
        self.assertEqual(self.service().with_role_keyword(self.service().base,"Python").count(),1)

    def test_sort_keys_are_valid(self):
        for key in self.service().VALID_SORTS:
            self.assertEqual(self.service().sort(self.service().base,key).count(),4)

    def test_distinct_companies(self):
        self.assertEqual(list(self.service().distinct_companies(self.service().base)),["Acme","Beta","Gamma"])

    def test_distinct_locations(self):
        self.assertEqual(list(self.service().distinct_locations(self.service().base)),["Nairobi","Remote"])

    def test_apply_combines_filters(self):
        rows=self.service().apply(query="Engineer",active_only=True,has_salary=True,sort="salary_high")
        self.assertEqual(rows.count(),3)
        self.assertEqual(rows.first().company,"Acme")

    def test_facets_are_user_scoped(self):
        facets=self.service().facets()
        self.assertNotIn("Private",facets["companies"])

    def test_counts_are_consistent(self):
        counts=self.service().counts()
        self.assertEqual(counts["total"],4)
        self.assertEqual(counts["active"],3)
        self.assertEqual(counts["closed"],1)

    def test_serialize_is_json_friendly(self):
        rows=self.service().serialize(self.service().base)
        self.assertEqual(len(rows),4)
        self.assertIsInstance(rows[0]["updated_at"],str)

    def test_explorer_contains_all_sections(self):
        data=self.service().explorer(active_only=True)
        self.assertEqual(set(data),{"filters","counts","facets","applications"})
        self.assertEqual(data["counts"]["active"],3)

    def test_invalid_sort_falls_back_to_updated(self):
        rows=self.service().sort(self.service().base,"unknown")
        self.assertEqual(rows.count(),4)

    def test_empty_search_returns_all_user_records(self):
        self.assertEqual(self.service().search("").count(),4)
