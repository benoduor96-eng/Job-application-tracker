"""Unit tests for the pipeline board helpers."""
from datetime import date, datetime
from decimal import Decimal
from types import SimpleNamespace
import pytest
from apps.jobs.pipeline_board import STAGES, build_board, is_stale, parse_move_request, plan_moves

TODAY = date(2026, 10, 1)

def app(id, status="applied", company="Acme", role="Engineer", location="Remote", **extra):
    data = dict(id=id, status=status, company=company, role=role, location=location,
                salary_min=None, salary_max=None, applied_date=None, next_action="",
                next_action_date=None, updated_at=datetime(2026, 9, 28, 12))
    data.update(extra)
    return SimpleNamespace(**data)

def column(board, status):
    return next(c for c in board["columns"] if c["status"] == status)

def test_all_stages_and_totals():
    board = build_board([app(1), app(2, "offer"), app(3, "rejected")], today=TODAY)
    assert [c["status"] for c in board["columns"]] == STAGES
    assert board["totals"] == {"applications": 3, "active": 2, "stale": 0}

def test_search_salary_and_sorting():
    apps = [app(1, company="Globex", location="Nairobi", salary_min=Decimal("100")),
            app(2, company="Alpha", salary_min=Decimal("200"), next_action_date=date(2026,10,3)),
            app(3, company="Beta", salary_min=Decimal("300"))]
    board = build_board(apps, today=TODAY, query="nairobi")
    assert board["totals"]["applications"] == 1
    board = build_board(apps, today=TODAY)
    assert column(board, "applied")["avg_salary_min"] == 200.0
    assert [c["id"] for c in column(board, "applied")["cards"]] == [2, 3, 1]

def test_stale_only_waiting_stages():
    old = datetime(2026, 9, 1)
    assert is_stale(app(1, updated_at=old), TODAY)
    assert not is_stale(app(2, "offer", updated_at=old), TODAY)
    assert not is_stale(app(3, updated_at=None, applied_date=None), TODAY)

def test_parse_and_plan_moves():
    assert parse_move_request({"ids":[3,1,3],"status":"interview"}) == ([3,1],"interview")
    assert plan_moves({1:"applied",2:"interview"}, [1,2,9], "interview") == {"moved":[1],"unchanged":[2],"missing":[9]}
    with pytest.raises(ValueError): parse_move_request({"ids":["1"],"status":"offer"})
