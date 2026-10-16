"""
Tests for Day 65 — Feature Enhancements, Structured Error Handling, and Recruiter Card Polish
"""

import pytest
import asyncio
from fastapi import Request
from api.errors import (
    api_error_handler,
    ZecpathAPIException,
    ResourceNotFoundException,
    ModelInferenceException
)
from unified_scoring.hiring_report_generator import (
    HiringIntelligenceReportGenerator,
    CandidateProfileData
)


def test_custom_api_exceptions_and_error_handler():
    # Mock ASGI request
    class MockURL:
        path = "/api/v1/test-endpoint"
    
    class MockRequest:
        url = MockURL()

    req = MockRequest()

    # 1. Test ResourceNotFoundException
    exc_404 = ResourceNotFoundException("Candidate", "CAND-XYZ")
    resp_404 = asyncio.run(api_error_handler(req, exc_404))
    assert resp_404.status_code == 404
    body_404 = resp_404.body.decode("utf-8")
    assert "RESOURCE_NOT_FOUND" in body_404
    assert "Verify the requested ID exists" in body_404
    assert "/api/v1/test-endpoint" in body_404

    # 2. Test ModelInferenceException
    exc_502 = ModelInferenceException("ats_matcher", "Timeout after 5000ms")
    resp_502 = asyncio.run(api_error_handler(req, exc_502))
    assert resp_502.status_code == 502
    body_502 = resp_502.body.decode("utf-8")
    assert "MODEL_INFERENCE_FAILURE" in body_502
    assert "Retry request or use fallback" in body_502


def test_recruiter_scorecard_export():
    generator = HiringIntelligenceReportGenerator()
    
    profile = CandidateProfileData(
        candidate_id="CAND-TEST-65",
        candidate_name="Elena Rostova",
        role="senior_ai_engineer",
        experience_level="senior",
        hiring_fit_score=88.5,
        hiring_recommendation="HIRE",
        decision_confidence=92.0,
        strengths=["Exceptional system design", "Fluent communication", "Optimal algorithmic coding"],
        weaknesses=[],
        risk_indicators=[],
        executive_summary="Candidate demonstrated exceptional architectural expertise and strong communication.",
        recommended_action="Extend formal job offer.",
        ats_summary={"score": 90.0, "skill_match": 92.0},
        screening_summary={"score": 86.0},
        hr_insights={"score": 88.0},
        technical_performance={"interview_score": 90.0, "machine_test_score": 92.0},
        behavioral_and_integrity_flags={"integrity_score": 100.0, "risk_tag": "LOW_RISK"}
    )

    card = generator.export_recruiter_card(profile)
    assert card["candidate_id"] == "CAND-TEST-65"
    assert card["fit_tier"] == "EXCEPTIONAL"
    assert card["hiring_fit_score"] == 88.5
    assert card["recommendation"] == "HIRE"
    assert len(card["top_strengths"]) == 3
    assert card["stage_breakdown"]["ats"] == 90.0
    assert card["stage_breakdown"]["integrity"] == 100.0
