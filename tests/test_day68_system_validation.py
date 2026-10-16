"""
Tests for Day 68 — System Stability, Edge Cases, and Bug Fix Validation
"""

import pytest
import math
from score_normalizer import normalize_score
from hr_score_normalizer import normalize_interview_score
from edge_case_handler import handle_edge_case, detect_language_mixing
from unified_scoring.recommendation_ai import RecommendationAIEngine, DecisionCategory


def test_score_normalizer_bugfixes():
    # Regular values
    assert normalize_score(85.5) == 85.5
    assert normalize_score(120) == 100.0
    assert normalize_score(-15) == 0.0

    # Edge cases & Bug Fixes
    assert normalize_score(None) == 0.0
    assert normalize_score("95.2") == 95.2
    assert normalize_score("invalid_str") == 0.0
    assert normalize_score(float("nan")) == 0.0
    assert normalize_score(float("inf")) == 0.0
    assert normalize_score(float("-inf")) == 0.0


def test_hr_score_normalizer_bugfixes():
    # Regular values
    assert normalize_interview_score(800, 10) == 80.0
    assert normalize_interview_score(950, 10) == 95.0

    # Zero & Negative Question Counts
    assert normalize_interview_score(100, 0) == 0.0
    assert normalize_interview_score(100, -2) == 0.0
    assert normalize_interview_score(None, 5) == 0.0
    assert normalize_interview_score("750", 10) == 75.0
    assert normalize_interview_score(float("nan"), 5) == 0.0


def test_edge_case_handler_stability():
    # Empty and whitespace text
    res_empty = handle_edge_case("", retry_count=0)
    assert res_empty["status"] == "retry"
    
    res_fallback = handle_edge_case(None, retry_count=3)
    assert res_fallback["status"] == "fallback"

    # Filler word handling
    res_filler = handle_edge_case("uh", retry_count=0)
    assert res_filler["status"] == "retry"

    # Language mixing detector
    res_lang = detect_language_mixing("This is a standard English interview answer.")
    assert "status" in res_lang


def test_recommendation_engine_boundary_resilience():
    engine = RecommendationAIEngine()

    # Extreme low boundary
    low_res = engine.evaluate_decision(
        candidate_id="CAND-ZERO",
        candidate_name="Zero Test",
        role="tester",
        hiring_fit_score=0.0,
        scores={"ats": 0.0, "technical": 0.0, "hr": 0.0, "screening": 0.0, "machine_test": 0.0},
        integrity_score=0.0,
        risk_tag="CRITICAL_RISK"
    )
    assert low_res.decision == DecisionCategory.REJECTED

    # Extreme high boundary
    high_res = engine.evaluate_decision(
        candidate_id="CAND-PERFECT",
        candidate_name="Perfect Test",
        role="ai_lead",
        hiring_fit_score=100.0,
        scores={"ats": 100.0, "technical": 100.0, "hr": 100.0, "screening": 100.0, "machine_test": 100.0},
        integrity_score=100.0,
        risk_tag="LOW_RISK"
    )
    assert high_res.decision == DecisionCategory.SELECTED
