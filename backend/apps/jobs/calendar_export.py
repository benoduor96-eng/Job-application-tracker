"""Build an iCalendar RFC 5545 feed from interviews and follow-up dates."""
from __future__ import annotations
from datetime import date, datetime, timedelta, timezone
from typing import Iterable, Optional

CRLF = "\r\n"
PRODID = "-//Job Application Tracker//Calendar Export//EN"
UID_DOMAIN = "jobtracker.local"
TERMINAL_STAGES = frozenset({"rejected", "withdrawn"})
INTERVIEW_TYPE_LABELS = {
    "phone": "Phone screen", "technical": "Technical interview",
    "behavioral": "Behavioral interview", "system_design": "System design interview",
    "panel": "Panel interview", "final": "Final round", "other": "Interview",
}

def escape_text(value: Optional[str]) -> str:
    text = (value or "").replace("\\", "\\\\")
    text = text.replace(";", "\\;").replace(",", "\\,")
    return text.replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\n")

def fold_line(line: str, limit: int = 75) -> str:
    if len(line.encode("utf-8")) <= limit:
        return line
    parts, current, budget = [], b"", limit
    for char in line:
        encoded = char.encode("utf-8")
        if len(current) + len(encoded) > budget:
            parts.append(current.decode("utf-8"))
            current, budget = encoded, limit - 1
        else:
            current += encoded
    parts.append(current.decode("utf-8"))
    return (CRLF + " ").join(parts)

def to_utc(value: datetime) -> datetime:
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)

def format_utc(value: datetime) -> str:
    return to_utc(value).strftime("%Y%m%dT%H%M%SZ")

def format_date(value: date) -> str:
    return value.strftime("%Y%m%d")

def _event(lines: list[str]) -> list[str]:
    return ["BEGIN:VEVENT", *lines, "END:VEVENT"]

def interview_event(interview, stamp: datetime, duration_minutes: int = 60):
    start = getattr(interview, "scheduled_date", None)
    if start is None:
        return None
    application = interview.application
    kind = INTERVIEW_TYPE_LABELS.get(interview.interview_type, "Interview")
    details = []
    if interview.interviewer_name:
        who = interview.interviewer_name
        if interview.interviewer_title:
            who += f" ({interview.interviewer_title})"
        details.append(f"Interviewer: {who}")
    if interview.notes:
        details.append(f"Notes: {interview.notes}")
    end = to_utc(start) + timedelta(minutes=duration_minutes)
    summary = f"{kind}: {application.role} at {application.company}"
    lines = [
        f"UID:interview-{interview.id}@{UID_DOMAIN}", f"DTSTAMP:{format_utc(stamp)}",
        f"DTSTART:{format_utc(start)}", f"DTEND:{format_utc(end)}",
        f"SUMMARY:{escape_text(summary)}",
    ]
    if details:
        lines.append(f"DESCRIPTION:{escape_text(chr(10).join(details))}")
    return to_utc(start), _event(lines)

def follow_up_event(application, stamp: datetime):
    due = getattr(application, "next_action_date", None)
    if due is None or application.status in TERMINAL_STAGES:
        return None
    action = application.next_action or "Follow up"
    summary = f"{action}: {application.role} at {application.company}"
    lines = [
        f"UID:follow-up-{application.id}@{UID_DOMAIN}", f"DTSTAMP:{format_utc(stamp)}",
        f"DTSTART;VALUE=DATE:{format_date(due)}",
        f"DTEND;VALUE=DATE:{format_date(due + timedelta(days=1))}",
        f"SUMMARY:{escape_text(summary)}",
    ]
    start = datetime(due.year, due.month, due.day, tzinfo=timezone.utc)
    return start, _event(lines)

def build_ics(interviews: Iterable, applications: Iterable, now: Optional[datetime] = None,
              duration_minutes: int = 60, include_past: bool = False,
              calendar_name: str = "Job Application Tracker") -> str:
    now = to_utc(now) if now else datetime.now(timezone.utc)
    dated = []
    for interview in interviews:
        built = interview_event(interview, now, duration_minutes)
        if built:
            dated.append(built)
    for application in applications:
        built = follow_up_event(application, now)
        if built:
            dated.append(built)
    if not include_past:
        cutoff = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
        dated = [(start, lines) for start, lines in dated if start >= cutoff]
    dated.sort(key=lambda pair: pair[0])
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", f"PRODID:{PRODID}",
             "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
             f"X-WR-CALNAME:{escape_text(calendar_name)}"]
    for _, event_lines in dated:
        lines.extend(event_lines)
    lines.append("END:VCALENDAR")
    return CRLF.join(fold_line(line) for line in lines) + CRLF

def parse_duration(raw: Optional[str], default: int = 60) -> int:
    if raw in (None, ""):
        return default
    try:
        minutes = int(raw)
    except (TypeError, ValueError):
        raise ValueError("duration must be an integer number of minutes.")
    if not 15 <= minutes <= 480:
        raise ValueError("duration must be between 15 and 480 minutes.")
    return minutes

def parse_bool(raw: Optional[str], default: bool = False) -> bool:
    if raw in (None, ""):
        return default
    value = str(raw).strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off"}:
        return False
    raise ValueError("Boolean parameters must be true or false.")
