"""
AI Monitoring & Observability System
Day 61 Implementation: Comprehensive logging, metrics tracking, alerting, and decision audit logs.
"""

import time
import json
import os
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from collections import deque


class AIMonitoringSystem:
    """
    Centralized Observability & Monitoring Engine for Zecpath AI System.
    Captures API logs, model latency/performance, error rates, decision audits, and triggers alerts.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AIMonitoringSystem, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, logs_dir: str = "logs"):
        if getattr(self, "_initialized", False):
            return

        self.logs_dir = logs_dir
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Buffer sizes
        self.max_buffer = 1000
        self.api_logs: deque = deque(maxlen=self.max_buffer)
        self.model_logs: deque = deque(maxlen=self.max_buffer)
        self.error_logs: deque = deque(maxlen=self.max_buffer)
        self.audit_logs: deque = deque(maxlen=self.max_buffer)
        
        # Alerting thresholds
        self.alert_rules = {
            "max_latency_ms": 2000.0,
            "max_failure_rate_pct": 5.0,
            "min_confidence_pct": 65.0,
            "max_memory_mb": 1024.0
        }
        
        # Internal counters
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_latency_ms": 0.0,
            "model_invocations": 0,
            "candidate_counts": {
                "total_processed": 0,
                "ats_screened": 0,
                "interviewed": 0,
                "offered": 0,
                "rejected": 0
            }
        }
        self._initialized = True

    def reset(self):
        """Reset buffers and metrics (useful for testing)."""
        self.api_logs.clear()
        self.model_logs.clear()
        self.error_logs.clear()
        self.audit_logs.clear()
        self.metrics["total_requests"] = 0
        self.metrics["successful_requests"] = 0
        self.metrics["failed_requests"] = 0
        self.metrics["total_latency_ms"] = 0.0
        self.metrics["model_invocations"] = 0
        self.metrics["candidate_counts"] = {
            "total_processed": 0,
            "ats_screened": 0,
            "interviewed": 0,
            "offered": 0,
            "rejected": 0
        }

    def log_api_request(
        self,
        method: str,
        endpoint: str,
        status_code: int,
        latency_ms: float,
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """Record an incoming API request with its execution telemetry."""
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "method": method.upper(),
            "endpoint": endpoint,
            "status_code": status_code,
            "latency_ms": round(latency_ms, 2),
            "is_success": 200 <= status_code < 400,
            "error": error
        }
        self.api_logs.append(record)
        
        self.metrics["total_requests"] += 1
        self.metrics["total_latency_ms"] += latency_ms
        if record["is_success"]:
            self.metrics["successful_requests"] += 1
        else:
            self.metrics["failed_requests"] += 1
            if error:
                self.log_error("API", f"HTTP_{status_code}", error)

        return record

    def log_model_output(
        self,
        model_name: str,
        input_summary: str,
        output_score: float,
        latency_ms: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Record an AI model inference output and performance metrics."""
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_name": model_name,
            "input_summary": input_summary[:200],
            "output_score": round(output_score, 2),
            "latency_ms": round(latency_ms, 2),
            "metadata": metadata or {}
        }
        self.model_logs.append(record)
        self.metrics["model_invocations"] += 1
        return record

    def log_error(
        self,
        component: str,
        error_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Capture an internal error with context."""
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "component": component,
            "error_type": error_type,
            "message": message,
            "details": details or {}
        }
        self.error_logs.append(record)
        return record

    def record_decision_audit(
        self,
        candidate_id: str,
        job_id: str,
        stage: str,
        scores: Dict[str, Any],
        verdict: str,
        model_version: str = "1.0.0",
        operator: str = "AI_DECISION_ENGINE"
    ) -> Dict[str, Any]:
        """
        Record a tamper-evident audit record for candidate evaluation decisions.
        Uses SHA-256 integrity hash across candidate, scores, verdict, and timestamp.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        content_for_hash = f"{candidate_id}:{job_id}:{stage}:{json.dumps(scores, sort_keys=True)}:{verdict}:{timestamp}"
        integrity_hash = hashlib.sha256(content_for_hash.encode("utf-8")).hexdigest()

        audit_entry = {
            "timestamp": timestamp,
            "candidate_id": candidate_id,
            "job_id": job_id,
            "stage": stage,
            "scores": scores,
            "verdict": verdict,
            "model_version": model_version,
            "operator": operator,
            "integrity_hash": integrity_hash
        }
        self.audit_logs.append(audit_entry)

        # Update candidate pipeline counters
        self.metrics["candidate_counts"]["total_processed"] += 1
        if stage == "ATS":
            self.metrics["candidate_counts"]["ats_screened"] += 1
        elif stage in ["INTERVIEW", "HR", "TECHNICAL"]:
            self.metrics["candidate_counts"]["interviewed"] += 1
        
        if verdict in ["HIRE", "OFFER", "SHORTLIST"]:
            self.metrics["candidate_counts"]["offered"] += 1
        elif verdict in ["REJECT", "NO_HIRE"]:
            self.metrics["candidate_counts"]["rejected"] += 1

        return audit_entry

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Compute system telemetry, error rates, average latency, and check active alerts."""
        total = self.metrics["total_requests"]
        failed = self.metrics["failed_requests"]
        failure_rate = (failed / total * 100.0) if total > 0 else 0.0
        avg_latency = (self.metrics["total_latency_ms"] / total) if total > 0 else 0.0

        # Model accuracy / score averages
        recent_scores = [m["output_score"] for m in self.model_logs]
        avg_model_score = sum(recent_scores) / len(recent_scores) if recent_scores else 0.0

        alerts = self.check_alerts(avg_latency, failure_rate, avg_model_score)

        return {
            "total_requests": total,
            "successful_requests": self.metrics["successful_requests"],
            "failed_requests": failed,
            "failure_rate_pct": round(failure_rate, 2),
            "avg_latency_ms": round(avg_latency, 2),
            "model_invocations": self.metrics["model_invocations"],
            "avg_model_score": round(avg_model_score, 2),
            "active_alerts": alerts,
            "system_status": "CRITICAL" if len(alerts) > 1 else ("WARNING" if len(alerts) == 1 else "HEALTHY")
        }

    def check_alerts(self, avg_latency: float, failure_rate: float, avg_model_score: float) -> List[Dict[str, Any]]:
        """Evaluate telemetry against configured threshold rules."""
        active = []
        if avg_latency > self.alert_rules["max_latency_ms"]:
            active.append({
                "rule": "HIGH_LATENCY",
                "severity": "WARNING",
                "message": f"Average latency {round(avg_latency, 2)}ms exceeds threshold {self.alert_rules['max_latency_ms']}ms"
            })
        if failure_rate > self.alert_rules["max_failure_rate_pct"]:
            active.append({
                "rule": "HIGH_FAILURE_RATE",
                "severity": "CRITICAL",
                "message": f"Failure rate {round(failure_rate, 2)}% exceeds threshold {self.alert_rules['max_failure_rate_pct']}%"
            })
        if self.model_logs and avg_model_score < self.alert_rules["min_confidence_pct"]:
            active.append({
                "rule": "LOW_MODEL_CONFIDENCE",
                "severity": "WARNING",
                "message": f"Average model evaluation score {round(avg_model_score, 2)}% is below expected quality threshold"
            })
        return active

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Aggregate stats for UI Monitoring Dashboard."""
        counts = self.metrics["candidate_counts"]
        total = counts["total_processed"]
        offered = counts["offered"]
        interview_pass_rate = round((offered / total * 100.0), 1) if total > 0 else 0.0

        return {
            "candidate_stats": {
                "total_candidates": total,
                "ats_screened": counts["ats_screened"],
                "interviewed": counts["interviewed"],
                "offered": offered,
                "rejected": counts["rejected"],
                "interview_success_rate_pct": interview_pass_rate
            },
            "recent_audit_decisions": list(self.audit_logs)[-5:],
            "recent_errors": list(self.error_logs)[-5:],
            "system_telemetry": self.get_metrics_summary()
        }

    def get_audit_trail(self, candidate_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Query immutable decision audit logs, optionally filtered by candidate ID."""
        if candidate_id:
            return [log for log in self.audit_logs if log["candidate_id"] == candidate_id]
        return list(self.audit_logs)


# Singleton accessor
ai_monitor = AIMonitoringSystem()
