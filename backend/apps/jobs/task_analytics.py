from collections import Counter
from datetime import timedelta
from django.utils import timezone
from .models import CareerTask


class TaskAnalytics:
    """Analyze the user's career-task workload without changing task state."""

    PRIORITY_ORDER = ["urgent", "high", "medium", "low"]
    ACTIVE = {"todo", "in_progress"}
    TERMINAL = {"done", "cancelled"}

    def __init__(self, user, now=None):
        self.user = user
        self.now = now or timezone.now()
        self.tasks = CareerTask.objects.filter(user=user)

    def summary(self):
        tasks = list(self.tasks)
        open_tasks = [task for task in tasks if task.status in self.ACTIVE]
        overdue = [task for task in open_tasks if task.due_date and task.due_date < self.now]
        due_today = [task for task in open_tasks if task.due_date and task.due_date.date() == self.now.date()]
        return {
            "total": len(tasks),
            "open": len(open_tasks),
            "done": sum(task.status == "done" for task in tasks),
            "cancelled": sum(task.status == "cancelled" for task in tasks),
            "overdue": len(overdue),
            "due_today": len(due_today),
            "completion_rate": round(sum(task.status == "done" for task in tasks) / len(tasks) * 100, 1) if tasks else 0,
            "by_priority": dict(Counter(task.priority for task in open_tasks)),
            "by_status": dict(Counter(task.status for task in tasks)),
        }

    def priority_breakdown(self):
        counts = Counter(self.tasks.filter(status__in=self.ACTIVE).values_list("priority", flat=True))
        return [{"priority": priority, "count": counts.get(priority, 0)} for priority in self.PRIORITY_ORDER]

    def due_window(self, days=14):
        end = self.now + timedelta(days=days)
        rows = self.tasks.filter(
            status__in=self.ACTIVE,
            due_date__isnull=False,
            due_date__gte=self.now,
            due_date__lte=end,
        ).order_by("due_date")
        return [{
            "id": task.id,
            "title": task.title,
            "priority": task.priority,
            "status": task.status,
            "due_date": task.due_date.isoformat(),
            "application_id": task.application_id,
        } for task in rows]

    def overdue(self, limit=50):
        rows = self.tasks.filter(status__in=self.ACTIVE, due_date__lt=self.now).order_by("due_date")[:limit]
        return [{
            "id": task.id,
            "title": task.title,
            "priority": task.priority,
            "status": task.status,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "application_id": task.application_id,
        } for task in rows]

    def application_load(self):
        counts = Counter(
            task.application_id
            for task in self.tasks.filter(status__in=self.ACTIVE)
            if task.application_id
        )
        return [{"application_id": key, "open_tasks": value} for key, value in counts.most_common()]

    def tags(self):
        counts = Counter()
        for task in self.tasks:
            seen = set()
            for tag in task.tags or []:
                value = str(tag).strip().lower()
                if value and value not in seen:
                    counts[value] += 1
                    seen.add(value)
        return [{"tag": tag, "count": count} for tag, count in counts.most_common()]

    def dashboard(self):
        return {
            "summary": self.summary(),
            "priorities": self.priority_breakdown(),
            "due_window": self.due_window(),
            "overdue": self.overdue(),
            "application_load": self.application_load(),
            "tags": self.tags(),
        }
