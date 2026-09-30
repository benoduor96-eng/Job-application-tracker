"""Tests for the expanded deterministic career domain engines."""

import importlib
import inspect
import pytest

MODULES = [
    "apps.jobs.workflow_engine",
    "apps.jobs.application_scoring",
    "apps.jobs.career_planner",
    "apps.jobs.resume_optimizer",
    "apps.jobs.interview_scheduler",
    "apps.jobs.offer_evaluator",
    "apps.jobs.search_service",
    "apps.jobs.audit_service",
    "apps.jobs.notification_rules",
    "apps.jobs.reporting_engine",
    "apps.jobs.contact_strategy",
    "apps.jobs.job_quality",
    "apps.jobs.pipeline_metrics",
    "apps.jobs.application_templates",
    "apps.jobs.skill_gap_engine",
    "apps.jobs.task_planner",
    "apps.jobs.company_research",
    "apps.jobs.application_validator",
    "apps.jobs.career_goals",
    "apps.jobs.followup_engine",
    "apps.jobs.analytics_segments",
    "apps.jobs.data_quality",
    "apps.jobs.import_pipeline",
    "apps.jobs.export_pipeline",
    "apps.jobs.security_rules",
    "apps.jobs.recommendation_engine",
]

@pytest.mark.parametrize("module_name", MODULES)
def test_domain_module_imports(module_name):
    module = importlib.import_module(module_name)
    assert module is not None

@pytest.mark.parametrize("module_name", MODULES)
def test_domain_engine_exposes_evaluation_api(module_name):
    module = importlib.import_module(module_name)
    engines = [obj for _, obj in inspect.getmembers(module, inspect.isclass) if obj.__module__ == module.__name__ and obj.__name__.endswith(("Service","Engine"))]
    assert engines
    engine = engines[0]()
    result = engine.evaluate({"follow_up_due": True, "missing_information": False})
    assert 0 <= result.score <= 100
    assert result.status

@pytest.mark.parametrize("module_name", MODULES)
def test_domain_engine_handles_empty_records(module_name):
    module = importlib.import_module(module_name)
    engines = [obj for _, obj in inspect.getmembers(module, inspect.isclass) if obj.__module__ == module.__name__ and obj.__name__.endswith(("Service","Engine"))]
    engine = engines[0]()
    summary = engine.summarize(engine.evaluate_many([]))
    assert summary["count"] == 0
    assert summary["average"] == 0.0

@pytest.mark.parametrize("module_name", MODULES)
def test_domain_engine_is_deterministic(module_name):
    module = importlib.import_module(module_name)
    engines = [obj for _, obj in inspect.getmembers(module, inspect.isclass) if obj.__module__ == module.__name__ and obj.__name__.endswith(("Service","Engine"))]
    engine = engines[0]()
    context = {"follow_up_due": True, "missing_information": False, "role_fit": "strong", "role_fit_complete": True}
    first = engine.evaluate(context)
    second = engine.evaluate(context)
    assert first == second
