"""Unit tests for calendar_export.py."""
from datetime import date, datetime, timedelta, timezone
from types import SimpleNamespace
import pytest
from apps.jobs.calendar_export import build_ics, escape_text, fold_line, follow_up_event, format_utc, interview_event, parse_bool, parse_duration

NOW = datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc)

def application(id=1, status="interview", company="Acme", role="Backend Engineer", next_action="", next_action_date=None):
    return SimpleNamespace(id=id, status=status, company=company, role=role, next_action=next_action, next_action_date=next_action_date)

def interview(id=1, when=None, kind="technical", app=None, name="", title="", notes=""):
    return SimpleNamespace(id=id, scheduled_date=when, interview_type=kind, interviewer_name=name, interviewer_title=title, notes=notes, application=app or application())

def unfold(text): return text.replace("\r\n ", "")
def lines_of(text): return unfold(text).split("\r\n")

def test_escape_text_handles_special_characters():
    assert escape_text("a,b;c\\d") == "a\\,b\\;c\\\\d"
    assert escape_text("line1\nline2\r\nline3") == "line1\\nline2\\nline3"
    assert escape_text(None) == ""

def test_fold_line_leaves_short_lines_alone():
    assert fold_line("SUMMARY:short") == "SUMMARY:short"

def test_fold_line_limits_octets_and_round_trips():
    original = "DESCRIPTION:" + "word " * 60
    folded = fold_line(original)
    assert all(len(p.encode("utf-8")) <= 75 for p in folded.split("\r\n"))
    assert unfold(folded) == original

def test_format_utc_converts_timezones_and_assumes_naive_is_utc():
    nairobi = timezone(timedelta(hours=3))
    assert format_utc(datetime(2026, 10, 5, 14, 30, tzinfo=nairobi)) == "20261005T113000Z"
    assert format_utc(datetime(2026, 10, 5, 14, 30)) == "20261005T143000Z"

def test_interview_event_fields():
    when = datetime(2026, 10, 5, 14, 0, tzinfo=timezone.utc)
    item = interview(7, when, name="Jane Smith", title="Engineering Manager", notes="System design, caching")
    start, lines = interview_event(item, NOW, duration_minutes=45)
    text = "\r\n".join(lines)
    assert start == when
    assert "UID:interview-7@jobtracker.local" in lines
    assert "DTSTART:20261005T140000Z" in lines
    assert "DTEND:20261005T144500Z" in lines
    assert "SUMMARY:Technical interview: Backend Engineer at Acme" in lines
    assert "Jane Smith (Engineering Manager)" in text
    assert "System design\\, caching" in text

def test_follow_up_event():
    item = application(3, status="applied", next_action="Email recruiter", next_action_date=date(2026, 10, 9))
    start, lines = follow_up_event(item, NOW)
    assert "DTSTART;VALUE=DATE:20261009" in lines
    assert "DTEND;VALUE=DATE:20261010" in lines

def test_calendar_structure_and_past_filter():
    when = datetime(2026, 10, 5, 14, 0, tzinfo=timezone.utc)
    text = build_ics([interview(1, when)], [application(next_action_date=date(2026, 10, 9))], now=NOW)
    parts = lines_of(text)
    assert parts[0] == "BEGIN:VCALENDAR" and parts[-2] == "END:VCALENDAR"
    assert parts.count("BEGIN:VEVENT") == 2
    past = interview(2, datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc))
    assert "interview-2@" not in build_ics([past], [], now=NOW)

def test_parse_duration_and_bool():
    assert parse_duration(None) == 60
    assert parse_duration("90") == 90
    with pytest.raises(ValueError): parse_duration("14")
    assert parse_bool("TRUE") is True and parse_bool("0") is False
    with pytest.raises(ValueError): parse_bool("maybe")
