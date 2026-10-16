"""
Tests for Day 61 — AI Monitoring & Observability System
"""

import pytest
from performance.ai_monitoring import AIMonitoringSystem, ai_monitor


@pytest.fixture(autouse=True)
def reset_monitor():
    ai_monitor.reset()
    yield
    ai_monitor.reset()


def test_api_logging_and_metrics():
    ai_monitor.log_api_request("GET", "/api/jobs", 200, 45.5)
    ai_monitor.log_api_request("POST", "/api/scoring/evaluate", 200, 150.2)
    ai_monitor.log_api_request("POST", "/api/resume/upload", 500, 320.0, error="Corrupt PDF")

    metrics = ai_monitor.get_metrics_summary()
    assert metrics["total_requests"] == 3
    assert metrics["successful_requests"] == 2
    assert metrics["failed_requests"] == 1
    assert metrics["failure_rate_pct"] == pytest.approx(33.33, 0.1)
    assert metrics["avg_latency_ms"] == pytest.approx((45.5 + 150.2 + 320.0) / 3, 0.1)


def test_model_logging_and_alerts():
    # Log model outputs
    ai_monitor.log_model_output("ats_semantic_matcher", "Resume snippet", 88.5, 35.0)
    ai_monitor.log_model_output("hr_behavioral_scorer", "Interview response", 82.0, 42.0)

    metrics = ai_monitor.get_metrics_summary()
    assert metrics["model_invocations"] == 2
    assert metrics["avg_model_score"] == pytest.approx(85.25, 0.1)

    # Check alert rules when values are normal
    alerts = ai_monitor.check_alerts(avg_latency=200.0, failure_rate=1.0, avg_model_score=85.0)
    assert len(alerts) == 0

    # Check alert rules when thresholds are breached
    breached_alerts = ai_monitor.check_alerts(avg_latency=2500.0, failure_rate=12.0, avg_model_score=50.0)
    alert_names = [a["rule"] for a in breached_alerts]
    assert "HIGH_LATENCY" in alert_names
    assert "HIGH_FAILURE_RATE" in alert_names
    assert "LOW_MODEL_CONFIDENCE" in alert_names


def test_decision_audit_log_and_integrity_hash():
    audit_entry = ai_monitor.record_decision_audit(
        candidate_id="CAND-TEST-001",
        job_id="JOB-AI-ENG",
        stage="FINAL_DECISION",
        scores={"ats": 85.0, "technical": 90.0, "hr": 88.0},
        verdict="HIRE"
    )

    assert audit_entry["candidate_id"] == "CAND-TEST-001"
    assert audit_entry["verdict"] == "HIRE"
    assert "integrity_hash" in audit_entry
    assert len(audit_entry["integrity_hash"]) == 64  # SHA-256 length

    trail = ai_monitor.get_audit_trail(candidate_id="CAND-TEST-001")
    assert len(trail) == 1
    assert trail[0]["integrity_hash"] == audit_entry["integrity_hash"]


def test_monitoring_api_routes():
    from api.routes.monitoring import (
        get_metrics,
        get_dashboard,
        get_audit_trail,
        record_decision_audit
    )

    # 1. Test metrics endpoint
    metrics_resp = get_metrics()
    assert metrics_resp["success"] is True
    assert "data" in metrics_resp

    # 2. Test dashboard endpoint
    dash_resp = get_dashboard()
    assert dash_resp["success"] is True
    dash_data = dash_resp["data"]
    assert "candidate_stats" in dash_data
    assert "system_telemetry" in dash_data

    # 3. Test post audit decision endpoint
    audit_payload = {
        "candidate_id": "CAND-API-002",
        "job_id": "JOB-DEV-002",
        "stage": "ATS",
        "scores": {"ats_score": 92.0},
        "verdict": "SHORTLIST"
    }
    audit_post_resp = record_decision_audit(audit_payload)
    assert audit_post_resp["success"] is True
    res_data = audit_post_resp["data"]
    assert res_data["candidate_id"] == "CAND-API-002"
    assert res_data["integrity_hash"] is not None

    # 4. Verify audit query endpoint
    audit_get_resp = get_audit_trail(candidate_id="CAND-API-002")
    assert audit_get_resp["success"] is True
    assert audit_get_resp["count"] == 1
    assert audit_get_resp["data"][0]["candidate_id"] == "CAND-API-002"
