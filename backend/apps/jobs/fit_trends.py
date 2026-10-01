"""Fit trend and gap analytics derived from current application data."""
from collections import Counter
from .job_fit import JobFitAnalyzer
from .models import JobApplication

class FitTrendService:
    def __init__(self, user):
        self.user = user
        self.analyzer = JobFitAnalyzer(user)

    def snapshot(self, limit=100):
        applications = JobApplication.objects.filter(user=self.user).order_by("-updated_at", "-id")[:limit]
        items = []
        for application in applications:
            result = self.analyzer.analyze(application).to_dict()
            items.append({
                "application_id": application.id,
                "company": application.company,
                "role": application.role,
                "status": application.status,
                "score": result["score"],
                "required_gaps": result["required_gaps"],
            })
        return items

    def summary(self, limit=100):
        items = self.snapshot(limit)
        scores = [item["score"] for item in items]
        gaps = Counter(skill for item in items for skill in item["required_gaps"])
        by_status = {}
        for item in items:
            by_status.setdefault(item["status"], []).append(item["score"])
        status_summary = {
            status: {
                "count": len(values),
                "average_score": round(sum(values) / len(values), 1),
            }
            for status, values in sorted(by_status.items())
        }
        return {
            "applications": items,
            "count": len(items),
            "average_score": round(sum(scores) / len(scores), 1) if scores else 0,
            "highest_score": max(scores) if scores else 0,
            "lowest_score": min(scores) if scores else 0,
            "common_skill_gaps": [
                {"skill": skill, "count": count}
                for skill, count in gaps.most_common(10)
            ],
            "by_status": status_summary,
        }
