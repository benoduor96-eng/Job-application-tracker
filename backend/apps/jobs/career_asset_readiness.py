from collections import Counter
from .models import Resume, CareerProfile, JobApplication, JobDescription


class CareerAssetReadiness:
    """Measure how complete the user's reusable career assets are."""

    def __init__(self, user):
        self.user = user

    def profile(self):
        profile = CareerProfile.objects.filter(user=self.user).first()
        if not profile:
            return {
                "exists": False, "score": 0, "missing": [
                    "headline", "professional_summary", "skills", "preferred_roles",
                    "preferred_locations", "portfolio_url", "github_url",
                ],
            }
        checks = {
            "headline": bool(profile.headline.strip()),
            "professional_summary": bool(profile.professional_summary.strip()),
            "skills": bool(profile.skills),
            "preferred_roles": bool(profile.preferred_roles),
            "preferred_locations": bool(profile.preferred_locations),
            "work_preference": bool(profile.work_preference),
            "salary_target": profile.target_salary is not None,
            "portfolio_url": bool(profile.portfolio_url),
            "linkedin_url": bool(profile.linkedin_url),
            "github_url": bool(profile.github_url),
        }
        missing = [key for key, complete in checks.items() if not complete]
        return {
            "exists": True,
            "score": round(sum(checks.values()) / len(checks) * 100, 1),
            "checks": checks,
            "missing": missing,
        }

    def resumes(self):
        rows = []
        for resume in Resume.objects.filter(user=self.user).order_by("-updated_at"):
            checks = {
                "name": bool(resume.name.strip()),
                "summary": bool(resume.summary.strip()),
                "content": bool(resume.content.strip()),
                "target_role": bool(resume.target_role.strip()),
                "skills": bool(resume.skills),
                "active_or_draft": resume.status in {"active", "draft"},
            }
            missing = [key for key, complete in checks.items() if not complete]
            rows.append({
                "id": resume.id,
                "name": resume.name,
                "version": resume.version,
                "status": resume.status,
                "target_role": resume.target_role,
                "score": round(sum(checks.values()) / len(checks) * 100, 1),
                "missing": missing,
                "updated_at": resume.updated_at.isoformat(),
            })
        return rows

    def application_coverage(self):
        applications = list(JobApplication.objects.filter(user=self.user))
        covered = 0
        for application in applications:
            has_description = JobDescription.objects.filter(
                user=self.user, application=application
            ).exists()
            if has_description:
                covered += 1
        return {
            "applications": len(applications),
            "with_job_description": covered,
            "without_job_description": len(applications) - covered,
            "coverage_rate": round(covered / len(applications) * 100, 1) if applications else 0,
        }

    def asset_summary(self):
        profile = self.profile()
        resumes = self.resumes()
        return {
            "profile_score": profile["score"],
            "resume_count": len(resumes),
            "best_resume_score": max((item["score"] for item in resumes), default=0),
            "active_resumes": sum(item["status"] == "active" for item in resumes),
            "draft_resumes": sum(item["status"] == "draft" for item in resumes),
            "application_coverage": self.application_coverage(),
        }

    def recommendations(self):
        recommendations = []
        profile = self.profile()
        if not profile["exists"]:
            recommendations.append({"priority": "high", "type": "profile", "title": "Create your career profile", "detail": "A reusable profile stores the skills, roles and preferences used across the workspace."})
        else:
            for field in profile["missing"][:5]:
                recommendations.append({"priority": "medium", "type": "profile", "title": f"Complete profile: {field.replace('_', ' ')}", "detail": "Adding this information improves the completeness of your reusable career context."})
        resumes = self.resumes()
        if not resumes:
            recommendations.append({"priority": "high", "type": "resume", "title": "Add a resume", "detail": "Create at least one reusable resume asset for applications."})
        elif not any(item["status"] == "active" for item in resumes):
            recommendations.append({"priority": "medium", "type": "resume", "title": "Mark a resume active", "detail": "An active resume makes the current version explicit in your workspace."})
        coverage = self.application_coverage()
        if coverage["without_job_description"]:
            recommendations.append({"priority": "low", "type": "application", "title": "Attach missing job descriptions", "detail": f'{coverage["without_job_description"]} tracked application(s) have no attached job description.'})
        return recommendations

    def dashboard(self):
        return {
            "profile": self.profile(),
            "resumes": self.resumes(),
            "summary": self.asset_summary(),
            "recommendations": self.recommendations(),
        }
