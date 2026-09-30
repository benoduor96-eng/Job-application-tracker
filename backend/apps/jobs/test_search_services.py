"""Tests for search services."""
from datetime import date, timedelta
import pytest
from .job_comparison_service import *

def test_rule_5_0():
    service = JobComparisonService()
    record = {"score": 20, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(20) == 20

def test_rule_5_1():
    service = JobComparisonService()
    record = {"score": 24, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(24) == 24

def test_rule_5_2():
    service = JobComparisonService()
    record = {"score": 28, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(28) == 28

def test_rule_5_3():
    service = JobComparisonService()
    record = {"score": 32, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(32) == 32

def test_rule_5_4():
    service = JobComparisonService()
    record = {"score": 36, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(36) == 36

def test_rule_5_5():
    service = JobComparisonService()
    record = {"score": 40, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(40) == 40

def test_rule_5_6():
    service = JobComparisonService()
    record = {"score": 44, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(44) == 44

def test_rule_5_7():
    service = JobComparisonService()
    record = {"score": 48, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(48) == 48

def test_rule_5_8():
    service = JobComparisonService()
    record = {"score": 52, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(52) == 52

def test_rule_5_9():
    service = JobComparisonService()
    record = {"score": 56, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(56) == 56

def test_rule_5_10():
    service = JobComparisonService()
    record = {"score": 60, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(60) == 60

def test_rule_5_11():
    service = JobComparisonService()
    record = {"score": 64, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(64) == 64

def test_rule_5_12():
    service = JobComparisonService()
    record = {"score": 68, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(68) == 68

def test_rule_5_13():
    service = JobComparisonService()
    record = {"score": 72, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(72) == 72

def test_rule_5_14():
    service = JobComparisonService()
    record = {"score": 76, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(76) == 76

def test_rule_5_15():
    service = JobComparisonService()
    record = {"score": 80, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(80) == 80

def test_rule_5_16():
    service = JobComparisonService()
    record = {"score": 84, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(84) == 84

def test_rule_5_17():
    service = JobComparisonService()
    record = {"score": 88, "status": "active", "name": "Example"}
    result = service.evaluate(record)
    assert result.code in {"risk","watch","healthy","strong"}
    assert 0 <= result.score <= 100
    assert service.normalize("  Example  Value ") == "example value"
    assert service.clamp(88) == 88

@pytest.mark.parametrize("value,expected",[(0,"risk"),(39,"risk"),(40,"watch"),(59,"watch"),(60,"healthy"),(79,"healthy"),(80,"strong"),(100,"strong")])
def test_threshold_boundaries(value,expected):
    service=JobComparisonService()
    assert service.classify(value)==expected

def test_empty_inputs_are_safe():
    service=JobComparisonService()
    assert service.avg([])==0
    assert service.unique([None,""," A ","a"])==["a"]
    assert service.overlap([],["a"])==0.0
    assert service.summary([])["count"]==0
    assert service.status_counts([])=={}
    assert service.bucket([])=={"strong":0,"healthy":0,"watch":0,"risk":0}

def test_dates_are_deterministic():
    service=JobComparisonService()
    start=date(2026,1,1)
    assert service.next_date(start,10)==date(2026,1,11)
    assert service.age_days(start,date(2026,1,11))==10
    assert service.overdue(start,date(2026,1,11))
