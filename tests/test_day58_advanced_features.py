"""
Unit & Integration Tests for Day 58 - Advanced Features (Coaching, Analytics, Multimodal)
"""

import pytest
from advanced_features.coaching_and_analytics import (
    CandidateAICoachingEngine,
    InterviewAnalyticsDashboardEngine,
    MultimodalPerceptionSimulator
)


def test_candidate_coaching_engine():
    engine = CandidateAICoachingEngine()
    
    stage_scores = {
        "ats": 70.0,
        "screening": 82.0,
        "hr": 78.0,
        "technical": 65.0,        # Needs work
        "machine_test": 92.0,     # Strong
    }
    
    plan = engine.generate_coaching_plan(
        candidate_id="CAND-COACH-01",
        candidate_name="Marcus Aurelius",
        role="ai_engineer",
        stage_scores=stage_scores,
        missing_skills=["Kubernetes", "Ray"],
        hr_contradiction=False,
    )
    
    assert plan.candidate_id == "CAND-COACH-01"
    assert len(plan.strengths_observed) >= 1
    assert "hands-on coding" in plan.strengths_observed[0].lower() or "machine test" in plan.strengths_observed[0].lower()
    assert len(plan.critical_skill_gaps) >= 1
    assert any("Kubernetes" in tip for tip in plan.resume_improvement_suggestions)
    assert len(plan.recommended_learning_path) >= 1


def test_interview_analytics_funnel_computation():
    mock_cohort = [
        {"role": "software_engineer", "ats_score": 85.0, "screening_score": 80.0, "hr_score": 85.0, "machine_test_score": 90.0, "recommendation": "STRONG_HIRE", "status": "shortlisted"},
        {"role": "software_engineer", "ats_score": 75.0, "screening_score": 70.0, "hr_score": 75.0, "machine_test_score": 75.0, "recommendation": "HIRE", "status": "shortlisted"},
        {"role": "ai_engineer", "ats_score": 90.0, "screening_score": 85.0, "hr_score": 60.0, "machine_test_score": 50.0, "recommendation": "REJECT", "status": "rejected"},
        {"role": "ai_engineer", "ats_score": 50.0, "screening_score": 40.0, "hr_score": 50.0, "machine_test_score": 40.0, "recommendation": "REJECT", "status": "rejected"},
    ]
    
    metrics = InterviewAnalyticsDashboardEngine.compute_funnel_metrics(mock_cohort)
    
    assert metrics.total_applicants == 4
    assert metrics.offers_extended == 2
    assert metrics.funnel_conversion_rates["end_to_end_conversion"] == 50.0
    assert metrics.average_scores_by_stage["ats_avg"] == 75.0
    assert "software_engineer" in metrics.role_pass_rates
    assert metrics.role_pass_rates["software_engineer"] == 100.0


def test_multimodal_perception_simulator():
    # Candidate looking at camera, low hesitations, positive sentiment
    profile = MultimodalPerceptionSimulator.analyze_audio_visual_stream(
        duration_sec=120.0,
        looking_away_events=1,
        hesitation_pauses=1,
        sentiment_polarity=0.6
    )
    
    assert profile.gaze_stability_ratio > 0.85
    assert profile.dominant_emotion == "Confident"
    assert profile.emotion_confidence >= 0.85
