"""
Unit & Integration Tests for Day 55 - Security & AI Governance Framework
"""

import pytest
from datetime import datetime, timedelta
from security_governance.governance_engine import (
    UserRole,
    Permission,
    AccessControlGuard,
    AuditTrailSystem,
    ConsentGatekeeper,
    PIIScrubber,
    DataRetentionPolicy,
)


def test_rbac_access_control():
    # Recruiter permissions
    assert AccessControlGuard.check_permission(UserRole.RECRUITER, Permission.VIEW_CANDIDATE_LIST) is True
    assert AccessControlGuard.check_permission(UserRole.RECRUITER, Permission.OVERRIDE_AI_DECISION) is False
    
    # Hiring manager can override
    assert AccessControlGuard.check_permission(UserRole.HIRING_MANAGER, Permission.OVERRIDE_AI_DECISION) is True
    
    # Candidate cannot view candidate list
    assert AccessControlGuard.check_permission(UserRole.CANDIDATE, Permission.VIEW_CANDIDATE_LIST) is False
    
    # Enforcement raises error
    with pytest.raises(PermissionError):
        AccessControlGuard.enforce_permission(UserRole.CANDIDATE, Permission.ACCESS_AUDIT_LOGS)


def test_audit_trail_tamper_evidence():
    audit = AuditTrailSystem()
    
    # Log scores and decisions
    audit.log_score_calculation(candidate_id="CAND-001", stage="ats", score=85.0)
    audit.log_score_calculation(candidate_id="CAND-001", stage="technical", score=90.0)
    audit.log_decision(
        candidate_id="CAND-001",
        decision="STRONG_HIRE",
        hiring_fit_score=88.5,
        actor_id="recruiter_1",
        actor_role="recruiter",
        rationale="Strong performance across all rounds."
    )
    
    valid, err = audit.verify_integrity()
    assert valid is True
    assert err is None
    
    # Tamper with an entry
    audit.audit_log[1].details["score"] = 99.0
    valid_after_tamper, err_after_tamper = audit.verify_integrity()
    assert valid_after_tamper is False
    assert "Tampered" in err_after_tamper or "Hash chain broken" in err_after_tamper


def test_consent_gatekeeper():
    gatekeeper = ConsentGatekeeper()
    
    # No consent initially
    assert gatekeeper.verify_consent("CAND-002", "screening") is False
    
    # Grant partial consent (only ATS)
    gatekeeper.record_consent("CAND-002", resume_parsing=True, voice_recording=False, ai_evaluation=False)
    assert gatekeeper.verify_consent("CAND-002", "ats") is True
    assert gatekeeper.verify_consent("CAND-002", "screening") is False
    
    # Grant full consent
    gatekeeper.record_consent(
        "CAND-002",
        resume_parsing=True,
        voice_recording=True,
        video_proctoring=True,
        ai_evaluation=True
    )
    assert gatekeeper.verify_consent("CAND-002", "screening") is True
    assert gatekeeper.verify_consent("CAND-002", "machine_test") is True


def test_pii_scrubber():
    raw_transcript = (
        "Hello, my name is John and you can reach me at john.doe@example.com or "
        "call my cell +1 (555) 234-5678. My SSN is 123-45-6789."
    )
    cleaned = PIIScrubber.sanitize_transcript(raw_transcript)
    assert "john.doe@example.com" not in cleaned
    assert "[REDACTED_EMAIL]" in cleaned
    assert "555" not in cleaned
    assert "[REDACTED_PHONE]" in cleaned
    assert "123-45-6789" not in cleaned
    assert "[REDACTED_ID]" in cleaned


def test_data_retention_and_anonymization():
    policy = DataRetentionPolicy(retention_days=90)
    
    fresh_date = datetime.utcnow() - timedelta(days=30)
    old_date = datetime.utcnow() - timedelta(days=120)
    
    assert policy.is_expired(fresh_date) is False
    assert policy.is_expired(old_date) is True
    
    candidate_record = {
        "candidate_id": "CAND-123",
        "candidate_name": "Jane Smith",
        "email": "jane@smith.com",
        "phone": "+1-800-555-0199",
        "hiring_fit_score": 85.0
    }
    anonymized = policy.anonymize_candidate_record(candidate_record)
    assert "Jane Smith" not in anonymized["candidate_name"]
    assert anonymized["email"] == "anonymized@gdpr.internal"
    assert anonymized["hiring_fit_score"] == 85.0
