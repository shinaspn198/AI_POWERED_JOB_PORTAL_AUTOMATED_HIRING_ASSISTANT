"""
Day 52 - Final Recommendation AI Engine

Purpose:
Autonomous decision-making engine for hiring outcomes using a hybrid
rule + score model, decision confidence evaluation, risk factor synthesis
(behavioral + integrity), and transparent explainable reasoning.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


# =========================================================
# 1. DECISION CATEGORIES
# =========================================================

class DecisionCategory(str, Enum):
    SELECTED = "Selected"
    HOLD_REVIEW = "Hold / Review"
    REJECTED = "Rejected"


@dataclass
class CandidateDecisionOutput:
    candidate_id: str
    candidate_name: str
    role: str
    decision: DecisionCategory
    decision_confidence: float          # 0 - 100% confidence in the decision
    hiring_fit_score: float             # 0 - 100% composite score
    risk_summary: Dict[str, Any]        # Behavioral & integrity risk factors
    key_strengths: List[str]            # Corroborated positive signals
    risk_factors: List[str]             # Flags, discrepancies, warnings
    explainable_rationale: str          # Transparent reasoning narrative
    recommended_action: str             # Specific recruiter next step


# =========================================================
# 2. HYBRID RULE + SCORE LOGIC ENGINE
# =========================================================

class RecommendationAIEngine:
    """Hybrid decision-making engine combining quantitative scoring with rule guardrails."""

    def __init__(self):
        # Minimum threshold rules for automatic selection
        self.selection_fit_threshold = 80.0
        self.selection_machine_test_min = 70.0
        self.selection_tech_min = 70.0

        # Hard rejection thresholds
        self.rejection_fit_threshold = 55.0
        self.rejection_machine_test_min = 45.0
        self.rejection_integrity_min = 40.0

    def evaluate_decision(
        self,
        candidate_id: str,
        candidate_name: str,
        role: str,
        hiring_fit_score: float,
        scores: Dict[str, float],
        integrity_score: float = 100.0,
        risk_tag: str = "LOW_RISK",
        behavioral_confidence: float = 80.0,
        contradiction_detected: bool = False
    ) -> CandidateDecisionOutput:
        """
        Executes hybrid rule + score evaluation to derive the final hiring decision,
        decision confidence score, risk factors, and explainable rationale.
        """
        ats = scores.get("ats", 70.0)
        screening = scores.get("screening", 70.0)
        hr = scores.get("hr", 70.0)
        tech = scores.get("technical", 70.0)
        machine_test = scores.get("machine_test", 70.0)

        strengths = []
        risks = []
        rule_triggers = []

        # --- A. Positive Signal Extraction ---
        if machine_test >= 85.0:
            strengths.append(f"Outstanding hands-on machine test performance ({machine_test}/100)")
        if tech >= 85.0:
            strengths.append(f"Strong technical interview reasoning & architectural depth ({tech}/100)")
        if hr >= 85.0:
            strengths.append(f"High cultural alignment and behavioral resilience ({hr}/100)")
        if ats >= 85.0:
            strengths.append(f"Comprehensive resume qualification and skill alignment ({ats}/100)")
        if screening >= 85.0:
            strengths.append(f"Clear, relevant, and articulate initial screening ({screening}/100)")

        # --- B. Risk Factor Synthesis ---
        # Integrity Risk
        if integrity_score < self.rejection_integrity_min or risk_tag == "CRITICAL_RISK":
            risks.append("Critical malpractice / cheating signals detected during session")
            rule_triggers.append("HARD_REJECT_INTEGRITY")
        elif risk_tag in ("HIGH_RISK", "MEDIUM_RISK"):
            risks.append(f"Proctoring anomaly tagged: {risk_tag} (Integrity Score: {integrity_score}/100)")

        # Behavioral Risk
        if contradiction_detected:
            risks.append("Cross-round factual contradiction identified in interview responses")
        if behavioral_confidence < 60.0:
            risks.append(f"Elevated stress / severe hesitation pattern detected ({behavioral_confidence}/100)")

        # Performance Discrepancies
        if abs(ats - tech) >= 30.0 and ats > tech:
            risks.append(f"Significant qualification discrepancy: High ATS ({ats}) vs Lower Technical Score ({tech})")
        if machine_test < self.rejection_machine_test_min:
            risks.append(f"Failed hands-on programming execution benchmarks ({machine_test}/100)")
            rule_triggers.append("HARD_REJECT_MACHINE_TEST")

        # --- C. Hybrid Decision Rules ---
        decision = DecisionCategory.HOLD_REVIEW
        rec_action = "Conduct human technical review"

        # Rule 1: Hard Disqualification
        if "HARD_REJECT_INTEGRITY" in rule_triggers:
            decision = DecisionCategory.REJECTED
            rec_action = "Disqualify application due to integrity violation."
        elif "HARD_REJECT_MACHINE_TEST" in rule_triggers or hiring_fit_score < self.rejection_fit_threshold:
            decision = DecisionCategory.REJECTED
            rec_action = "Send standard candidate rejection notification."

        # Rule 2: Automatic Selection
        elif (
            hiring_fit_score >= self.selection_fit_threshold
            and machine_test >= self.selection_machine_test_min
            and tech >= self.selection_tech_min
            and risk_tag == "LOW_RISK"
            and not contradiction_detected
        ):
            decision = DecisionCategory.SELECTED
            rec_action = "Proceed directly to job offer and team matching."

        # Rule 3: Hold / Review Triggers
        else:
            decision = DecisionCategory.HOLD_REVIEW
            if risk_tag in ("HIGH_RISK", "MEDIUM_RISK"):
                rec_action = "Schedule proctoring audit review before proceeding."
            elif machine_test < self.selection_machine_test_min:
                rec_action = "Assign supplementary practical coding challenge."
            else:
                rec_action = "Conduct 15-minute hiring manager debrief to resolve borderline signals."

        # --- D. Decision Confidence Calculation ---
        # Confidence measures how decisive the signal set is (higher when signals agree)
        conf = 85.0
        if decision == DecisionCategory.SELECTED:
            if hiring_fit_score >= 90.0 and len(risks) == 0:
                conf = 96.0
            elif hiring_fit_score >= 85.0:
                conf = 90.0
            else:
                conf = 82.0
        elif decision == DecisionCategory.REJECTED:
            if "HARD_REJECT_INTEGRITY" in rule_triggers or hiring_fit_score < 45.0:
                conf = 98.0
            elif len(risks) >= 2:
                conf = 92.0
            else:
                conf = 84.0
        else: # HOLD_REVIEW
            # In borderline situations, confidence in the final hire/reject outcome is inherently lower
            conf = max(60.0, 75.0 - (len(risks) * 5.0))

        decision_confidence = round(conf, 1)

        # --- E. Explainable Output Generation ---
        rationale_parts = [
            f"Candidate was assigned '{decision.value}' status with {decision_confidence}% decision confidence.",
            f"Composite Hiring Fit Score reached {hiring_fit_score}%.",
        ]
        if strengths:
            rationale_parts.append(f"Key drivers: {'; '.join(strengths[:2])}.")
        if risks:
            rationale_parts.append(f"Risk considerations: {'; '.join(risks)}.")
        else:
            rationale_parts.append("Zero critical behavioral or proctoring risk factors detected.")

        explainable_rationale = " ".join(rationale_parts)

        return CandidateDecisionOutput(
            candidate_id=candidate_id,
            candidate_name=candidate_name,
            role=role,
            decision=decision,
            decision_confidence=decision_confidence,
            hiring_fit_score=hiring_fit_score,
            risk_summary={
                "integrity_score": integrity_score,
                "risk_tag": risk_tag,
                "behavioral_confidence": behavioral_confidence,
                "contradiction_detected": contradiction_detected,
                "total_risk_factors": len(risks)
            },
            key_strengths=strengths,
            risk_factors=risks,
            explainable_rationale=explainable_rationale,
            recommended_action=rec_action
        )


def evaluate_final_recommendation(
    candidate_id: str,
    candidate_name: str,
    role: str,
    hiring_fit_score: float,
    scores: Dict[str, float],
    integrity_score: float = 100.0,
    risk_tag: str = "LOW_RISK",
    behavioral_confidence: float = 80.0,
    contradiction_detected: bool = False
) -> CandidateDecisionOutput:
    """Convenience helper to run Day 52 Recommendation AI."""
    engine = RecommendationAIEngine()
    return engine.evaluate_decision(
        candidate_id=candidate_id,
        candidate_name=candidate_name,
        role=role,
        hiring_fit_score=hiring_fit_score,
        scores=scores,
        integrity_score=integrity_score,
        risk_tag=risk_tag,
        behavioral_confidence=behavioral_confidence,
        contradiction_detected=contradiction_detected
    )
