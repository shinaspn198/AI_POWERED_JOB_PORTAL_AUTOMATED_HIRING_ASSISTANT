"""
Unit & Integration Tests for Day 53 - Hiring Intelligence Report Generator
"""

import json
import pytest
from unified_scoring.hiring_report_generator import (
    HiringIntelligenceReportGenerator,
    CandidateProfileData
)


def test_hiring_report_generator_strong_hire():
    generator = HiringIntelligenceReportGenerator()
    
    stage_scores = {
        "ats": 88.0,
        "screening": 82.0,
        "hr": 90.0,
        "technical": 92.0,
        "machine_test": 95.0,
    }
    
    ats_details = {
        "skill_match": 90.0,
        "experience_relevance": 85.0,
        "education_alignment": 90.0,
        "matched_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        "missing_skills": [],
    }
    
    hr_details = {
        "behavioral_confidence": 88.0,
        "sentiment_score": 85.0,
        "stress_indicator": "Composed",
        "contradiction_detected": False,
        "culture_alignment": "High",
    }
    
    technical_details = {
        "test_cases_passed_ratio": 1.0,
        "execution_time_ms": 28.5,
    }
    
    integrity_details = {
        "integrity_score": 98.0,
        "risk_tag": "LOW_RISK",
        "tab_switches": 0,
        "looking_away_events": 1,
    }
    
    recommendation_details = {
        "hiring_fit_score": 90.45,
        "decision": "STRONG_HIRE",
        "decision_confidence": 92.0,
    }
    
    profile = generator.build_report(
        candidate_id="CAND-TEST-001",
        candidate_name="Alex Mercer",
        role="ai_engineer",
        experience_level="senior",
        stage_scores=stage_scores,
        ats_details=ats_details,
        hr_details=hr_details,
        technical_details=technical_details,
        integrity_details=integrity_details,
        recommendation_details=recommendation_details,
    )
    
    assert profile.candidate_id == "CAND-TEST-001"
    assert profile.candidate_name == "Alex Mercer"
    assert profile.hiring_fit_score == 90.45
    assert profile.hiring_recommendation == "STRONG_HIRE"
    assert len(profile.strengths) >= 1
    assert "Machine Test" in profile.strengths[0] or "coding ability" in profile.strengths[0]
    assert profile.behavioral_and_integrity_flags["integrity_score"] == 98.0
    assert profile.behavioral_and_integrity_flags["malpractice_detected"] is False
    
    # Test JSON Export
    json_out = generator.export_json(profile)
    parsed = json.loads(json_out)
    assert parsed["candidate_id"] == "CAND-TEST-001"
    assert parsed["hiring_fit_score"] == 90.45
    
    # Test Markdown Export
    md_out = generator.export_markdown(profile)
    assert "# Zecpath AI Hiring Intelligence Report" in md_out
    assert "Alex Mercer" in md_out
    assert "STRONG_HIRE" in md_out
    assert "| **Machine Test Sandbox** | 95.0% |" in md_out
    
    # Test HTML Export
    html_out = generator.export_html(profile)
    assert "<!DOCTYPE html>" in html_out
    assert "Alex Mercer" in html_out
    assert "Hiring Fit Score" in html_out
    assert "90.45%" in html_out


def test_hiring_report_generator_risk_flags():
    generator = HiringIntelligenceReportGenerator()
    
    stage_scores = {
        "ats": 60.0,
        "screening": 55.0,
        "hr": 62.0,
        "technical": 58.0,
        "machine_test": 50.0,
    }
    
    ats_details = {
        "missing_skills": ["Kubernetes", "Distributed Systems"],
    }
    
    hr_details = {
        "contradiction_detected": True,
    }
    
    integrity_details = {
        "integrity_score": 60.0,
        "risk_tag": "HIGH_RISK",
        "tab_switches": 5,
    }
    
    profile = generator.build_report(
        candidate_id="CAND-TEST-002",
        candidate_name="Risk Candidate",
        role="software_engineer",
        experience_level="entry",
        stage_scores=stage_scores,
        ats_details=ats_details,
        hr_details=hr_details,
        integrity_details=integrity_details,
    )
    
    assert profile.behavioral_and_integrity_flags["malpractice_detected"] is True
    assert any("contradiction" in r.lower() for r in profile.risk_indicators)
    assert any("tab switches" in r.lower() for r in profile.risk_indicators)
    assert any("Kubernetes" in w for w in profile.weaknesses)
