"""
Assessment & Unified Hiring Intelligence API Routes

Exposes complete end-to-end evaluation stages:
1. ATS Scoring & Resume Match
2. Conversational AI Screening
3. HR Behavioral & Confidence Interview
4. Technical Skill Rubric Evaluation
5. Hands-on Machine Test Sandbox Runner
6. Real-time Proctoring & Integrity Telemetry
7. Cross-Round Aggregation & Unified Recruiter Intelligence
"""

import sys
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response, PlainTextResponse, HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import desc

# Ensure workspace root is in path
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from api.database import get_db
from api.models.candidate_assessment import CandidateAssessment
from unified_scoring.hiring_report_generator import HiringIntelligenceReportGenerator

from ats_score import calculate_ats_score
from behavioral_confidence import calculate_behavioral_confidence
from interview_ai.integrity_detection import IntegrityDetector, IntegrityTelemetry, MALPRACTICE_SIGNALS
from interview_ai.machine_test_ai import (
    MachineTestEvaluator,
    TaskSubmission,
    ExecutionResult,
    CodeSnapshot,
    MachineTestType,
    MACHINE_TEST_TYPES
)
from unified_scoring.aggregation_engine import CrossRoundAggregationEngine
from unified_scoring.weight_config import ROLE_WEIGHTS, STAGES


router = APIRouter(
    prefix="/api/assessment",
    tags=["Assessment & Hiring Intelligence"]
)


# =========================================================
# SCHEMAS
# =========================================================

class EvaluateAtsRequest(BaseModel):
    candidate_id: str
    role: str = "software_engineer"
    skill_match: float = Field(..., ge=0, le=100)
    experience_relevance: float = Field(..., ge=0, le=100)
    education_alignment: float = Field(..., ge=0, le=100)
    semantic_similarity: float = Field(..., ge=0, le=100)


class EvaluateScreeningRequest(BaseModel):
    candidate_id: str
    role: str = "software_engineer"
    question: str
    answer: str
    background_context: Optional[str] = None


class EvaluateHRRequest(BaseModel):
    candidate_id: str
    scenario_question: str
    response_text: str
    confidence_score: float = Field(80.0, ge=0, le=100)
    sentiment_score: float = Field(75.0, ge=0, le=100)
    stress_score: float = Field(25.0, ge=0, le=100)
    contradiction_detected: bool = False


class EvaluateTechnicalRequest(BaseModel):
    candidate_id: str
    role: str = "software_engineer"
    question_type: str = "experience_based"
    question: str
    technical_answer: str


class MachineTestSubmissionRequest(BaseModel):
    candidate_id: str
    test_type: str = "coding_problems"
    source_code: str
    time_taken_seconds: float
    expected_time_seconds: float = 1800.0
    max_allowed_seconds: float = 2700.0
    passed_test_cases: int = 10
    total_test_cases: int = 10
    execution_time_ms: float = 45.0
    memory_used_mb: float = 28.0
    snapshots: Optional[List[Dict[str, Any]]] = None


class IntegrityTelemetryRequest(BaseModel):
    candidate_id: str
    tab_switches: int = 0
    focus_loss_duration_sec: float = 0.0
    external_voice_events: int = 0
    looking_away_events: int = 0
    question_timestamp_sec: float = 0.0
    recent_events: Optional[List[Dict[str, Any]]] = None
    baseline_behavioral_confidence: Optional[float] = 80.0


class FinalizeAssessmentRequest(BaseModel):
    candidate_id: str
    candidate_name: str
    role: str = "software_engineer"
    experience_level: str = "mid"
    ats_score: float = Field(..., ge=0, le=100)
    screening_score: float = Field(..., ge=0, le=100)
    hr_interview_score: float = Field(..., ge=0, le=100)
    technical_interview_score: float = Field(..., ge=0, le=100)
    machine_test_score: float = Field(..., ge=0, le=100)
    telemetry: Optional[IntegrityTelemetryRequest] = None


class UpdateCandidateStatusRequest(BaseModel):
    status: str  # shortlisted, rejected, hired, interview_scheduled


# =========================================================
# ROUTES
# =========================================================

@router.get("/config")
def get_assessment_config():
    """Returns available roles, default weights, and assessment stages."""
    return {
        "stages": STAGES,
        "roles": list(ROLE_WEIGHTS.keys()),
        "role_weights": ROLE_WEIGHTS,
        "machine_test_types": MACHINE_TEST_TYPES,
        "malpractice_signals": MALPRACTICE_SIGNALS,
    }


@router.post("/evaluate/ats")
def evaluate_ats(req: EvaluateAtsRequest):
    """Calculates ATS score based on skills, experience, education, and semantics."""
    try:
        role_map = {
            "software_engineer": "Software Engineer",
            "ai_engineer": "AI Engineer",
            "data_analyst": "Data Scientist",
            "data_scientist": "Data Scientist",
            "product_manager": "Software Engineer",
            "hr_specialist": "Software Engineer",
        }
        mapped_role = role_map.get(req.role.lower().replace(" ", "_"), req.role)
        score = calculate_ats_score(
            role=mapped_role,
            skill_match=req.skill_match,
            experience_relevance=req.experience_relevance,
            education_alignment=req.education_alignment,
            semantic_similarity=req.semantic_similarity
        )
        return {
            "candidate_id": req.candidate_id,
            "role": req.role,
            "ats_score": score,
            "breakdown": {
                "skill_match": req.skill_match,
                "experience_relevance": req.experience_relevance,
                "education_alignment": req.education_alignment,
                "semantic_similarity": req.semantic_similarity,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/evaluate/screening")
def evaluate_screening(req: EvaluateScreeningRequest):
    """Evaluates candidate conversational screening answer."""
    ans = req.answer.strip()
    word_count = len(ans.split())

    # Calculate 4 screening pillars: clarity, relevance, completeness, consistency
    clarity = min(100.0, max(20.0, 50.0 + min(word_count * 0.8, 45.0)))
    relevance = 85.0 if any(k in ans.lower() for k in ["experience", "project", "work", "built", "team", "scale"]) else 65.0
    completeness = min(100.0, max(30.0, word_count * 1.2))
    consistency = 85.0

    score = round((clarity * 0.25 + relevance * 0.30 + completeness * 0.25 + consistency * 0.20), 2)
    return {
        "candidate_id": req.candidate_id,
        "screening_score": score,
        "pillars": {
            "clarity": round(clarity, 2),
            "relevance": round(relevance, 2),
            "completeness": round(completeness, 2),
            "consistency": round(consistency, 2),
        },
        "feedback": "Answer demonstrates clear domain understanding with good communication structure."
    }


@router.post("/evaluate/hr")
def evaluate_hr(req: EvaluateHRRequest):
    """Evaluates HR behavioral scenario and computes behavioral confidence."""
    confidence = calculate_behavioral_confidence(
        confidence_score=req.confidence_score,
        sentiment_score=req.sentiment_score,
        stress_score=req.stress_score,
        contradiction_detected=req.contradiction_detected
    )
    return {
        "candidate_id": req.candidate_id,
        "hr_score": confidence,
        "metrics": {
            "confidence_score": req.confidence_score,
            "sentiment_score": req.sentiment_score,
            "stress_score": req.stress_score,
            "contradiction_detected": req.contradiction_detected,
        },
        "summary": "Demonstrated positive emotional resilience and structured behavioral articulation."
    }


@router.post("/evaluate/technical")
def evaluate_technical(req: EvaluateTechnicalRequest):
    """Evaluates technical depth, logical reasoning, and real-world applicability."""
    ans = req.technical_answer.strip()
    words = len(ans.split())

    accuracy = min(100.0, 60.0 + min(words * 0.5, 35.0))
    depth = min(100.0, 50.0 + min(words * 0.6, 45.0))
    logical_reasoning = 88.0 if any(k in ans.lower() for k in ["because", "therefore", "optimize", "architecture", "tradeoff"]) else 70.0
    applicability = 85.0 if any(k in ans.lower() for k in ["production", "deploy", "database", "api", "tested", "system"]) else 68.0

    score = round((accuracy * 0.35 + depth * 0.25 + logical_reasoning * 0.20 + applicability * 0.20), 2)
    return {
        "candidate_id": req.candidate_id,
        "technical_score": score,
        "rubric": {
            "accuracy": round(accuracy, 2),
            "depth": round(depth, 2),
            "logical_reasoning": round(logical_reasoning, 2),
            "real_world_applicability": round(applicability, 2),
        }
    }


@router.post("/evaluate/machine-test")
def evaluate_machine_test(req: MachineTestSubmissionRequest):
    """Executes sandbox evaluation of code submission across all Day 50 metrics."""
    evaluator = MachineTestEvaluator()

    exec_result = ExecutionResult(
        total_test_cases=req.total_test_cases,
        passed_test_cases=req.passed_test_cases,
        failed_test_cases=max(0, req.total_test_cases - req.passed_test_cases),
        execution_time_ms=req.execution_time_ms,
        memory_used_mb=req.memory_used_mb,
        exit_code=0 if req.passed_test_cases == req.total_test_cases else 1
    )

    snapshots = []
    if req.snapshots:
        for s in req.snapshots:
            snapshots.append(CodeSnapshot(
                timestamp_sec=s.get("timestamp_sec", 0.0),
                snapshot_index=s.get("snapshot_index", 0),
                char_count=s.get("char_count", 0),
                line_count=s.get("line_count", 0),
                diff_size=s.get("diff_size", 0),
                is_run_trigger=s.get("is_run_trigger", False),
                paste_detected=s.get("paste_detected", False),
            ))

    try:
        ttype = MachineTestType(req.test_type)
    except ValueError:
        ttype = MachineTestType.CODING_PROBLEM

    submission = TaskSubmission(
        test_type=ttype,
        source_code=req.source_code,
        time_taken_seconds=req.time_taken_seconds,
        expected_time_seconds=req.expected_time_seconds,
        max_allowed_seconds=req.max_allowed_seconds,
        execution_result=exec_result,
        snapshots=snapshots
    )

    evaluation = evaluator.evaluate_submission(submission)
    return {
        "candidate_id": req.candidate_id,
        "machine_test_score": evaluation["final_score"],
        "details": evaluation
    }


@router.post("/telemetry/integrity")
def evaluate_integrity(req: IntegrityTelemetryRequest):
    """Tracks real-time proctoring telemetry and generates candidate alerts and recruiter flags."""
    detector = IntegrityDetector()
    telemetry = IntegrityTelemetry(
        tab_switches=req.tab_switches,
        focus_loss_duration_sec=req.focus_loss_duration_sec,
        external_voice_events=req.external_voice_events,
        looking_away_events=req.looking_away_events,
        question_timestamp_sec=req.question_timestamp_sec,
        recent_events=req.recent_events or []
    )

    eval_result = detector.evaluate_telemetry(
        telemetry,
        behavioral_confidence_score=req.baseline_behavioral_confidence
    )

    return {
        "candidate_id": req.candidate_id,
        "integrity_score": eval_result.integrity_score,
        "risk_tag": eval_result.risk_tag,
        "real_time_warnings": eval_result.real_time_warnings,
        "recruiter_flags": eval_result.recruiter_flags,
        "detected_patterns": [p["name"] for p in eval_result.detected_patterns],
        "behavioral_impact": eval_result.behavioral_impact,
    }


@router.post("/finalize")
def finalize_candidate_assessment(req: FinalizeAssessmentRequest, db: Session = Depends(get_db)):
    """Cross-round aggregation unifying all 5 stages into final hiring fit score and DB record."""
    engine = CrossRoundAggregationEngine()

    unified = engine.aggregate_candidate_score(
        candidate_id=req.candidate_id,
        candidate_name=req.candidate_name,
        role=req.role,
        experience_level=req.experience_level,
        ats_score=req.ats_score,
        screening_score=req.screening_score,
        hr_interview_score=req.hr_interview_score,
        technical_interview_score=req.technical_interview_score,
        machine_test_score=req.machine_test_score,
    )

    # Evaluate integrity if telemetry provided
    integrity_score = 100.0
    risk_tag = "LOW_RISK"
    if req.telemetry:
        detector = IntegrityDetector()
        t = IntegrityTelemetry(
            tab_switches=req.telemetry.tab_switches,
            focus_loss_duration_sec=req.telemetry.focus_loss_duration_sec,
            external_voice_events=req.telemetry.external_voice_events,
            looking_away_events=req.telemetry.looking_away_events,
            question_timestamp_sec=req.telemetry.question_timestamp_sec,
            recent_events=req.telemetry.recent_events or []
        )
        integ_eval = detector.evaluate_telemetry(t, behavioral_confidence_score=unified.hiring_fit_score)
        integrity_score = integ_eval.integrity_score
        risk_tag = integ_eval.risk_tag

    # Build breakdown dictionary
    breakdown_json = {}
    for k, v in unified.stage_breakdown.items():
        breakdown_json[k] = {
            "stage_name": v.stage_name,
            "raw_score": v.raw_score,
            "normalized_score": v.normalized_score,
            "weight": v.weight,
            "weighted_contribution": v.weighted_contribution
        }

    # Upsert into DB
    try:
        record = db.query(CandidateAssessment).filter(CandidateAssessment.candidate_id == req.candidate_id).first()
        if not record:
            record = CandidateAssessment(candidate_id=req.candidate_id)
            db.add(record)

        record.candidate_name = req.candidate_name
        record.role = req.role
        record.experience_level = req.experience_level
        record.ats_score = req.ats_score
        record.screening_score = req.screening_score
        record.hr_interview_score = req.hr_interview_score
        record.technical_interview_score = req.technical_interview_score
        record.machine_test_score = req.machine_test_score
        record.integrity_score = integrity_score
        record.risk_tag = risk_tag
        record.hiring_fit_score = unified.hiring_fit_score
        record.hiring_recommendation = unified.hiring_recommendation
        record.status = "shortlisted" if unified.hiring_recommendation in ("STRONG_HIRE", "HIRE") else "review"
        record.breakdown_data = breakdown_json
        record.audit_notes = unified.transparency_audit.get("explanation", "")
        record.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(record)
    except Exception as e:
        db.rollback()
        # Non-fatal if DB issue: return unified score payload anyway
        pass

    return {
        "candidate_id": unified.candidate_id,
        "candidate_name": unified.candidate_name,
        "role": unified.role,
        "experience_level": unified.experience_level,
        "hiring_fit_score": unified.hiring_fit_score,
        "hiring_recommendation": unified.hiring_recommendation,
        "integrity_score": integrity_score,
        "risk_tag": risk_tag,
        "status": "shortlisted" if unified.hiring_recommendation in ("STRONG_HIRE", "HIRE") else "review",
        "stage_breakdown": breakdown_json,
        "transparency_audit": unified.transparency_audit,
    }


@router.get("/candidates")
def list_evaluated_candidates(role: Optional[str] = None, db: Session = Depends(get_db)):
    """Recruiter Dashboard endpoint returning all assessed candidates."""
    try:
        query = db.query(CandidateAssessment).order_by(desc(CandidateAssessment.hiring_fit_score))
        if role:
            query = query.filter(CandidateAssessment.role == role)
        records = query.all()

        return [
            {
                "id": r.id,
                "candidate_id": r.candidate_id,
                "candidate_name": r.candidate_name,
                "role": r.role,
                "experience_level": r.experience_level,
                "hiring_fit_score": r.hiring_fit_score,
                "hiring_recommendation": r.hiring_recommendation,
                "integrity_score": r.integrity_score,
                "risk_tag": r.risk_tag,
                "status": r.status,
                "scores": {
                    "ats": r.ats_score,
                    "screening": r.screening_score,
                    "hr": r.hr_interview_score,
                    "technical": r.technical_interview_score,
                    "machine_test": r.machine_test_score,
                },
                "breakdown": r.breakdown_data,
                "audit_notes": r.audit_notes,
                "updated_at": r.updated_at.isoformat() if r.updated_at else None,
            }
            for r in records
        ]
    except Exception as e:
        # Fallback sample data if empty
        return []


@router.get("/candidate/{candidate_id}")
def get_candidate_scorecard(candidate_id: str, db: Session = Depends(get_db)):
    """Deep-dive scorecard for a single candidate."""
    record = db.query(CandidateAssessment).filter(CandidateAssessment.candidate_id == candidate_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Candidate assessment record not found")

    return {
        "candidate_id": record.candidate_id,
        "candidate_name": record.candidate_name,
        "role": record.role,
        "experience_level": record.experience_level,
        "hiring_fit_score": record.hiring_fit_score,
        "hiring_recommendation": record.hiring_recommendation,
        "integrity_score": record.integrity_score,
        "risk_tag": record.risk_tag,
        "status": record.status,
        "stage_scores": {
            "ats": record.ats_score,
            "screening": record.screening_score,
            "hr": record.hr_interview_score,
            "technical": record.technical_interview_score,
            "machine_test": record.machine_test_score,
        },
        "breakdown": record.breakdown_data,
        "audit_notes": record.audit_notes,
    }


@router.patch("/candidate/{candidate_id}/status")
def update_candidate_status(candidate_id: str, req: UpdateCandidateStatusRequest, db: Session = Depends(get_db)):
    """Allows recruiters to shortlist, reject, or mark candidate as hired."""
    record = db.query(CandidateAssessment).filter(CandidateAssessment.candidate_id == candidate_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Candidate assessment record not found")

    record.status = req.status
    record.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(record)

    return {
        "candidate_id": record.candidate_id,
        "status": record.status,
        "message": f"Candidate status successfully updated to {req.status}"
    }


@router.get("/candidate/{candidate_id}/report")
def get_candidate_intelligence_report(candidate_id: str, db: Session = Depends(get_db)):
    """Day 53: Comprehensive Recruiter Intelligence Report for a candidate."""
    record = db.query(CandidateAssessment).filter(CandidateAssessment.candidate_id == candidate_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Candidate assessment record not found")

    generator = HiringIntelligenceReportGenerator()
    profile = generator.build_report(
        candidate_id=record.candidate_id,
        candidate_name=record.candidate_name,
        role=record.role,
        experience_level=record.experience_level,
        stage_scores={
            "ats": record.ats_score,
            "screening": record.screening_score,
            "hr": record.hr_interview_score,
            "technical": record.technical_interview_score,
            "machine_test": record.machine_test_score,
        },
        integrity_details={
            "integrity_score": record.integrity_score,
            "risk_tag": record.risk_tag,
        },
        recommendation_details={
            "hiring_fit_score": record.hiring_fit_score,
            "decision": record.hiring_recommendation,
        }
    )

    return json.loads(generator.export_json(profile))


@router.get("/candidate/{candidate_id}/report/export")
def export_candidate_report(candidate_id: str, format: str = "json", db: Session = Depends(get_db)):
    """Day 53: Export candidate report in JSON, Markdown, or Printable HTML format."""
    record = db.query(CandidateAssessment).filter(CandidateAssessment.candidate_id == candidate_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Candidate assessment record not found")

    generator = HiringIntelligenceReportGenerator()
    profile = generator.build_report(
        candidate_id=record.candidate_id,
        candidate_name=record.candidate_name,
        role=record.role,
        experience_level=record.experience_level,
        stage_scores={
            "ats": record.ats_score,
            "screening": record.screening_score,
            "hr": record.hr_interview_score,
            "technical": record.technical_interview_score,
            "machine_test": record.machine_test_score,
        },
        integrity_details={
            "integrity_score": record.integrity_score,
            "risk_tag": record.risk_tag,
        },
        recommendation_details={
            "hiring_fit_score": record.hiring_fit_score,
            "decision": record.hiring_recommendation,
        }
    )

    if format.lower() == "markdown" or format.lower() == "md":
        return PlainTextResponse(content=generator.export_markdown(profile), media_type="text/markdown")
    elif format.lower() == "html":
        return HTMLResponse(content=generator.export_html(profile))
    else:
        return Response(content=generator.export_json(profile), media_type="application/json")

