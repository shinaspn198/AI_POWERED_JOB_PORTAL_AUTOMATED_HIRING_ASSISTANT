"""
Unit & Integration Tests for Day 59 - Standardized API Integration Layer
"""

import pytest
from fastapi import BackgroundTasks
from api.routes.integration import (
    parse_candidate_resume,
    get_async_job_status,
    score_ats_candidate,
    evaluate_screening_dialogue,
    evaluate_interview_stage,
    recommend_final_decision,
    ResumeParseRequest,
    AtsScoringRequest,
    ScreeningEvaluateRequest,
    InterviewEvaluateRequest,
    DecisionRecommendRequest,
    ASYNC_JOB_STORE
)


def test_integration_resume_parse_sync():
    raw_resume = """
    Alice Walker
    alice@example.com
    
    SKILLS
    Python, FastAPI, Docker, Kubernetes
    
    EXPERIENCE
    Senior Backend Engineer at CloudScale
    """
    
    req = ResumeParseRequest(
        candidate_id="CAND-INT-01",
        raw_text=raw_resume,
        is_async=False
    )
    bg = BackgroundTasks()
    resp = parse_candidate_resume(req, bg)
    
    assert resp.status == "COMPLETED"
    assert resp.candidate_id == "CAND-INT-01"
    assert "Alice Walker" in resp.parsed_data["name"]
    assert resp.execution_time_ms >= 0


def test_integration_resume_parse_async():
    raw_resume = """
    Bob Builder
    bob@example.com
    
    SKILLS
    React, TypeScript, CSS
    """
    
    req = ResumeParseRequest(
        candidate_id="CAND-INT-02",
        raw_text=raw_resume,
        is_async=True
    )
    bg = BackgroundTasks()
    resp = parse_candidate_resume(req, bg)
    
    assert resp.status == "PROCESSING"
    assert resp.candidate_id == "CAND-INT-02"
    job_id = resp.job_id
    
    # Run the background tasks manually
    for task in bg.tasks:
        task.func(*task.args, **task.kwargs)
        
    poll_resp = get_async_job_status(job_id)
    assert poll_resp.status == "COMPLETED"
    assert poll_resp.candidate_id == "CAND-INT-02"
    assert "Bob Builder" in poll_resp.parsed_data["name"]


def test_integration_ats_scoring():
    req = AtsScoringRequest(
        candidate_id="CAND-INT-03",
        role="software_engineer",
        skill_match=85.0,
        experience_relevance=80.0,
        education_alignment=90.0,
        semantic_similarity=82.0
    )
    resp = score_ats_candidate(req)
    assert resp.ats_score > 80.0
    assert resp.is_shortlisted is True
    assert resp.candidate_id == "CAND-INT-03"


def test_integration_screening_evaluate():
    req = ScreeningEvaluateRequest(
        candidate_id="CAND-INT-04",
        role="software_engineer",
        question="Tell me about your experience with Docker.",
        answer="I have built and maintained multi-stage Docker containers in production."
    )
    resp = evaluate_screening_dialogue(req)
    assert resp.primary_intent == "CONFIRM_EXPERIENCE"
    assert "docker" in resp.detected_entities
    assert resp.screening_score >= 80.0


def test_integration_decision_recommend():
    req = DecisionRecommendRequest(
        candidate_id="CAND-INT-05",
        candidate_name="Diana Prince",
        role="ai_engineer",
        experience_level="senior",
        stage_scores={
            "ats": 88.0,
            "screening": 85.0,
            "hr": 90.0,
            "technical": 92.0,
            "machine_test": 95.0
        },
        integrity_score=100.0,
        risk_tag="LOW_RISK",
        contradiction_detected=False
    )
    resp = recommend_final_decision(req)
    assert resp.decision in ("Selected", "STRONG_HIRE", "HIRE")
    assert resp.hiring_fit_score >= 85.0
    assert len(resp.key_strengths) >= 1
