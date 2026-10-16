"""
FastAPI Monitoring & Observability Routes
Day 61 Implementation: Endpoints for system telemetry, monitoring dashboard, and decision audit logs.
"""

from fastapi import APIRouter, Query, Body, HTTPException
from typing import Optional, Dict, Any
from performance.ai_monitoring import ai_monitor

router = APIRouter(prefix="/api/monitoring", tags=["AI Monitoring & Observability"])


@router.get("/metrics")
def get_metrics():
    """Retrieve operational metrics: response times, error rates, model invocations, and active alerts."""
    return {
        "success": True,
        "data": ai_monitor.get_metrics_summary()
    }


@router.get("/dashboard")
def get_dashboard():
    """Retrieve candidate processing statistics, interview success rates, and live system health."""
    return {
        "success": True,
        "data": ai_monitor.get_dashboard_stats()
    }


@router.get("/audit-trail")
def get_audit_trail(candidate_id: Optional[str] = Query(None, description="Optional candidate ID filter")):
    """Retrieve tamper-evident audit logs for hiring decisions."""
    logs = ai_monitor.get_audit_trail(candidate_id=candidate_id)
    return {
        "success": True,
        "count": len(logs),
        "data": logs
    }


@router.post("/audit-decision")
def record_decision_audit(payload: Dict[str, Any] = Body(...)):
    """Record an official decision audit log with SHA-256 integrity hash."""
    required = ["candidate_id", "job_id", "stage", "scores", "verdict"]
    for req in required:
        if req not in payload:
            raise HTTPException(status_code=400, detail=f"Missing required field: '{req}'")

    entry = ai_monitor.record_decision_audit(
        candidate_id=payload["candidate_id"],
        job_id=payload["job_id"],
        stage=payload["stage"],
        scores=payload["scores"],
        verdict=payload["verdict"],
        model_version=payload.get("model_version", "1.0.0"),
        operator=payload.get("operator", "AI_DECISION_ENGINE")
    )
    return {
        "success": True,
        "message": "Decision audit successfully recorded with integrity signature",
        "data": entry
    }
