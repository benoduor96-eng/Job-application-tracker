"""Deterministic networking and recruiter-contact intelligence."""

from __future__ import annotations

from datetime import timedelta

from django.utils import timezone

from apps.jobs.models import CareerContact


class ContactIntelligenceService:
    """Turn contact records into actionable, user-scoped networking signals."""

    def __init__(self, user, now=None):
        self.user = user
        self.now = now or timezone.now()

    def contacts(self):
        return CareerContact.objects.filter(user=self.user).select_related("application")

    def summary(self):
        contacts = list(self.contacts())
        upcoming_limit = self.now + timedelta(days=7)
        overdue = [
            c for c in contacts
            if c.next_follow_up and c.next_follow_up < self.now
        ]
        upcoming = [
            c for c in contacts
            if c.next_follow_up and self.now <= c.next_follow_up <= upcoming_limit
        ]
        never_contacted = [c for c in contacts if c.last_contacted_at is None]
        linked = [c for c in contacts if c.application_id]

        by_type = {}
        by_company = {}
        for contact in contacts:
            by_type[contact.contact_type] = by_type.get(contact.contact_type, 0) + 1
            if contact.company:
                by_company[contact.company] = by_company.get(contact.company, 0) + 1

        actions = []
        for contact in sorted(overdue, key=lambda item: item.next_follow_up)[:8]:
            actions.append({
                "contact_id": contact.id,
                "name": contact.name,
                "company": contact.company,
                "action": "Follow up",
                "priority": "high",
                "reason": "Scheduled follow-up is overdue.",
                "due_at": contact.next_follow_up.isoformat(),
            })
        for contact in sorted(never_contacted, key=lambda item: item.updated_at)[:5]:
            actions.append({
                "contact_id": contact.id,
                "name": contact.name,
                "company": contact.company,
                "action": "Make first contact",
                "priority": "medium",
                "reason": "No contact attempt has been recorded.",
                "due_at": None,
            })
        for contact in sorted(upcoming, key=lambda item: item.next_follow_up)[:5]:
            actions.append({
                "contact_id": contact.id,
                "name": contact.name,
                "company": contact.company,
                "action": "Prepare follow-up",
                "priority": "medium",
                "reason": "Follow-up is scheduled within seven days.",
                "due_at": contact.next_follow_up.isoformat(),
            })

        return {
            "total": len(contacts),
            "overdue": len(overdue),
            "upcoming": len(upcoming),
            "never_contacted": len(never_contacted),
            "linked_to_application": len(linked),
            "by_type": by_type,
            "by_company": dict(sorted(by_company.items(), key=lambda item: (-item[1], item[0]))[:8]),
            "actions": actions,
        }
