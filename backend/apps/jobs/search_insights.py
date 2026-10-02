from collections import Counter, defaultdict
from decimal import Decimal
from django.db.models import Q
from .models import JobApplication, SavedSearch


class SearchInsights:
    """Compare saved-search intent with the applications the user actually tracks."""

    def __init__(self, user):
        self.user = user
        self.searches = SavedSearch.objects.filter(user=user)
        self.applications = JobApplication.objects.filter(user=user)

    @staticmethod
    def _tokens(value):
        if not value:
            return set()
        normalized = "".join(ch.lower() if ch.isalnum() else " " for ch in str(value))
        return {token for token in normalized.split() if len(token) > 1}

    def _matches_query(self, search, application):
        query = (search.query or "").strip().lower()
        if not query:
            return True
        haystack = " ".join([
            application.role or "",
            application.company or "",
            application.location or "",
            application.notes or "",
        ]).lower()
        query_tokens = self._tokens(query)
        if query in haystack:
            return True
        return bool(query_tokens & self._tokens(haystack))

    def _matches_location(self, search, application):
        if not search.location:
            return True
        wanted = self._tokens(search.location)
        actual = self._tokens(application.location)
        return not wanted or bool(wanted & actual)

    def _matches_status(self, search, application):
        wanted = (search.status or "").strip().lower()
        return not wanted or (application.status or "").strip().lower() == wanted

    def _matches_salary(self, search, application):
        if search.min_salary is not None:
            maximum = application.salary_max or application.salary_min
            if maximum is None or Decimal(str(maximum)) < Decimal(str(search.min_salary)):
                return False
        if search.max_salary is not None:
            minimum = application.salary_min or application.salary_max
            if minimum is not None and Decimal(str(minimum)) > Decimal(str(search.max_salary)):
                return False
        return True

    def matches(self, search, application):
        return (
            self._matches_query(search, application)
            and self._matches_location(search, application)
            and self._matches_status(search, application)
            and self._matches_salary(search, application)
        )

    def search_summary(self, search):
        apps = list(self.applications)
        matched = [a for a in apps if self.matches(search, a)]
        active = [a for a in matched if a.status not in {"rejected", "withdrawn"}]
        return {
            "id": search.id,
            "name": search.name,
            "query": search.query,
            "location": search.location,
            "status": search.status,
            "remote_only": search.remote_only,
            "min_salary": str(search.min_salary) if search.min_salary is not None else None,
            "max_salary": str(search.max_salary) if search.max_salary is not None else None,
            "alerts_enabled": search.alerts_enabled,
            "applications": len(matched),
            "active_applications": len(active),
            "statuses": dict(Counter(a.status for a in matched)),
            "companies": len({a.company.strip().lower() for a in matched}),
            "roles": len({a.role.strip().lower() for a in matched}),
        }

    def all_summaries(self):
        return [self.search_summary(search) for search in self.searches]

    def coverage(self):
        searches = list(self.searches)
        apps = list(self.applications)
        covered = [a for a in apps if any(self.matches(search, a) for search in searches)]
        uncovered = [a for a in apps if a not in covered]
        return {
            "saved_searches": len(searches),
            "applications": len(apps),
            "covered_applications": len(covered),
            "uncovered_applications": len(uncovered),
            "coverage_rate": round(len(covered) / len(apps) * 100, 1) if apps else 0.0,
        }

    def role_clusters(self):
        groups = defaultdict(lambda: {"applications": 0, "active": 0, "companies": set()})
        for app in self.applications:
            tokens = self._tokens(app.role)
            key = " ".join(sorted(tokens)) or "unspecified"
            groups[key]["applications"] += 1
            if app.status not in {"rejected", "withdrawn"}:
                groups[key]["active"] += 1
            groups[key]["companies"].add(app.company.strip())
        rows = []
        for role, data in groups.items():
            rows.append({
                "role_key": role,
                "applications": data["applications"],
                "active": data["active"],
                "companies": sorted(data["companies"]),
            })
        return sorted(rows, key=lambda row: (-row["applications"], row["role_key"]))

    def location_clusters(self):
        groups = defaultdict(lambda: {"applications": 0, "active": 0})
        for app in self.applications:
            key = app.location.strip() or "Unspecified"
            groups[key]["applications"] += 1
            if app.status not in {"rejected", "withdrawn"}:
                groups[key]["active"] += 1
        return [
            {"location": key, **value}
            for key, value in sorted(groups.items(), key=lambda item: (-item[1]["applications"], item[0].lower()))
        ]

    def recommendations(self):
        summaries = self.all_summaries()
        recommendations = []
        for item in summaries:
            if item["applications"] == 0:
                recommendations.append({
                    "type": "no_matches",
                    "search_id": item["id"],
                    "priority": "high",
                    "title": f"No tracked applications match {item['name']}",
                    "detail": "Review the query, location, salary or status filters.",
                })
            elif item["active_applications"] == 0:
                recommendations.append({
                    "type": "inactive",
                    "search_id": item["id"],
                    "priority": "medium",
                    "title": f"{item['name']} has no active applications",
                    "detail": "Consider adding a new opportunity or retiring the search.",
                })
            elif item["active_applications"] >= 5:
                recommendations.append({
                    "type": "attention",
                    "search_id": item["id"],
                    "priority": "low",
                    "title": f"{item['name']} has a large active pipeline",
                    "detail": "Keep follow-up dates current for this search.",
                })
        coverage = self.coverage()
        if coverage["uncovered_applications"] and not summaries:
            recommendations.append({
                "type": "missing_search",
                "search_id": None,
                "priority": "medium",
                "title": "Create saved searches for your existing pipeline",
                "detail": "Saved searches make recurring role and location patterns easier to review.",
            })
        return recommendations

    def dashboard(self):
        return {
            "coverage": self.coverage(),
            "searches": self.all_summaries(),
            "role_clusters": self.role_clusters(),
            "location_clusters": self.location_clusters(),
            "recommendations": self.recommendations(),
        }
