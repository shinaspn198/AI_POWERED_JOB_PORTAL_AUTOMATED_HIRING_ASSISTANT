"""
Unit & Integration Tests for Day 54 - Scoring Optimization & Intent Refinement
"""

import pytest
from unified_scoring.optimization_engine import ScoringOptimizationEngine
from interview_ai.intent_refiner import ConversationalIntentRefiner


def test_optimization_hidden_gem():
    engine = ScoringOptimizationEngine()
    
    # Low ATS (60.0) but stellar machine test (95.0) and strong tech (85.0)
    stage_scores = {
        "ats": 60.0,
        "screening": 78.0,
        "hr": 80.0,
        "technical": 85.0,
        "machine_test": 95.0,
    }
    base_weights = {
        "ats": 0.15,
        "screening": 0.15,
        "hr": 0.15,
        "technical": 0.25,
        "machine_test": 0.30,
    }
    
    res = engine.calibrate_scores(
        candidate_id="CAND-GEM-01",
        role="ai_engineer",
        experience_level="mid",
        stage_scores=stage_scores,
        base_weights=base_weights,
    )
    
    assert res.archetype_detected == "HIDDEN_GEM"
    assert res.adjustment_applied > 0
    assert res.calibrated_fit_score > res.original_fit_score
    assert "Hidden Gem" in res.explanation
    assert res.execution_latency_ms < 50.0  # Ultra-fast latency check


def test_optimization_resume_padder():
    engine = ScoringOptimizationEngine()
    
    # High ATS (90.0) but low machine test (45.0) and poor tech (48.0)
    stage_scores = {
        "ats": 90.0,
        "screening": 75.0,
        "hr": 70.0,
        "technical": 48.0,
        "machine_test": 45.0,
    }
    base_weights = {
        "ats": 0.15,
        "screening": 0.15,
        "hr": 0.15,
        "technical": 0.25,
        "machine_test": 0.30,
    }
    
    res = engine.calibrate_scores(
        candidate_id="CAND-PADDER-01",
        role="software_engineer",
        experience_level="entry",
        stage_scores=stage_scores,
        base_weights=base_weights,
    )
    
    assert res.archetype_detected == "RESUME_PADDER"
    assert res.adjustment_applied < 0
    assert res.calibrated_fit_score < res.original_fit_score
    assert "Resume Padder" in res.explanation


def test_intent_refinement_negation():
    refiner = ConversationalIntentRefiner()
    
    # Negated production experience but admitted tutorial/study
    text = "I have not used Kubernetes in production, but I studied it in academic tutorials."
    res = refiner.classify_intent(text)
    
    assert res.is_negated is True
    assert res.primary_intent == "QUALIFIED_EXPERIENCE"
    assert "kubernetes" in res.detected_entities


def test_intent_refinement_clarification():
    refiner = ConversationalIntentRefiner()
    text = "Could you please clarify what you mean by distributed transactions?"
    res = refiner.classify_intent(text)
    
    assert res.primary_intent == "CLARIFICATION_REQUEST"
    assert res.confidence >= 0.85
