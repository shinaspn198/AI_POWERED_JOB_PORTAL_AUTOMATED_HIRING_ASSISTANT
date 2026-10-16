"""
Day 56 - Full Pipeline End-to-End Simulation Engine

Simulates the entire multi-stage hiring journey:
1. Resume Upload & ATS Scoring
2. Conversational Voice Screening
3. HR Behavioral Evaluation
4. Technical & Hands-on Machine Test
5. Real-time Proctoring & Integrity Telemetry
6. Unified Aggregation & Final AI Decision
7. Benchmarking Against Human Expert Judgment
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
import json
import math
import time

from unified_scoring.aggregation_engine import CrossRoundAggregationEngine
from unified_scoring.recommendation_ai import RecommendationAIEngine, DecisionCategory
from unified_scoring.optimization_engine import ScoringOptimizationEngine
from unified_scoring.hiring_report_generator import HiringIntelligenceReportGenerator


@dataclass
class CandidateSimulationProfile:
    candidate_id: str
    name: str
    role: str
    experience_level: str
    resume_text: str
    screening_response: str
    hr_response: str
    coding_submission: str
    expected_human_decision: str       # "Selected", "Hold / Review", "Rejected"
    expected_human_score: float
    simulated_ats_raw: float
    simulated_screening_raw: float
    simulated_hr_raw: float
    simulated_tech_raw: float
    simulated_machine_raw: float
    integrity_score: float = 100.0
    risk_tag: str = "LOW_RISK"
    tab_switches: int = 0
    contradiction_detected: bool = False


@dataclass
class SimulationResult:
    candidate_id: str
    candidate_name: str
    role: str
    ai_fit_score: float
    ai_decision: str
    ai_confidence: float
    human_score: float
    human_decision: str
    decision_matches: bool
    score_delta: float
    archetype: str
    inconsistency_notes: List[str]


class FullSystemSimulator:
    """Executes end-to-end recruitment pipeline simulations across candidate cohorts."""

    def __init__(self):
        self.aggregation_engine = CrossRoundAggregationEngine()
        self.optimization_engine = ScoringOptimizationEngine()
        self.recommendation_engine = RecommendationAIEngine()
        self.report_generator = HiringIntelligenceReportGenerator()

    def run_candidate_journey(self, candidate: CandidateSimulationProfile) -> SimulationResult:
        """Runs the entire 5-stage recruitment journey for a single candidate."""
        stage_scores = {
            "ats": candidate.simulated_ats_raw,
            "screening": candidate.simulated_screening_raw,
            "hr": candidate.simulated_hr_raw,
            "technical": candidate.simulated_tech_raw,
            "machine_test": candidate.simulated_machine_raw,
        }

        # 1. Base Aggregation
        unified_score = self.aggregation_engine.aggregate_candidate_score(
            candidate_id=candidate.candidate_id,
            candidate_name=candidate.name,
            role=candidate.role,
            experience_level=candidate.experience_level,
            ats_score=candidate.simulated_ats_raw,
            screening_score=candidate.simulated_screening_raw,
            hr_interview_score=candidate.simulated_hr_raw,
            technical_interview_score=candidate.simulated_tech_raw,
            machine_test_score=candidate.simulated_machine_raw,
        )

        # 2. Optimization & Calibrated Correction (Day 54)
        base_weights = {
            "ats": 0.15,
            "screening": 0.15,
            "hr": 0.15,
            "technical": 0.25,
            "machine_test": 0.30,
        }
        calibrated = self.optimization_engine.calibrate_scores(
            candidate_id=candidate.candidate_id,
            role=candidate.role,
            experience_level=candidate.experience_level,
            stage_scores=stage_scores,
            base_weights=base_weights,
            contradiction_detected=candidate.contradiction_detected,
            integrity_score=candidate.integrity_score,
        )

        final_fit_score = calibrated.calibrated_fit_score

        # 3. Final Recommendation AI (Day 52 / Day 54)
        decision_output = self.recommendation_engine.evaluate_decision(
            candidate_id=candidate.candidate_id,
            candidate_name=candidate.name,
            role=candidate.role,
            hiring_fit_score=final_fit_score,
            scores=stage_scores,
            integrity_score=candidate.integrity_score,
            risk_tag=candidate.risk_tag,
            behavioral_confidence=82.0 if not candidate.contradiction_detected else 45.0,
            contradiction_detected=candidate.contradiction_detected,
        )

        ai_decision_str = decision_output.decision.value

        # Normalize decision strings for comparison
        norm_ai = "Selected" if "SELECT" in ai_decision_str.upper() or "STRONG_HIRE" in ai_decision_str.upper() else (
            "Hold / Review" if "HOLD" in ai_decision_str.upper() or "REVIEW" in ai_decision_str.upper() or "BORDERLINE" in ai_decision_str.upper() else "Rejected"
        )
        norm_human = "Selected" if "SELECT" in candidate.expected_human_decision.upper() or "HIRE" in candidate.expected_human_decision.upper() else (
            "Hold / Review" if "HOLD" in candidate.expected_human_decision.upper() or "REVIEW" in candidate.expected_human_decision.upper() else "Rejected"
        )

        matches = (norm_ai == norm_human)
        score_delta = round(abs(final_fit_score - candidate.expected_human_score), 2)

        inconsistencies = []
        if not matches:
            inconsistencies.append(f"Decision divergence: AI awarded '{norm_ai}', Human gave '{norm_human}'.")
        if score_delta > 12.0:
            inconsistencies.append(f"Score spread delta of {score_delta}% exceeds 12% tolerance.")
        if calibrated.discrepancy_flag:
            inconsistencies.append(f"Inter-round variance flag: std_dev exceeded threshold.")

        return SimulationResult(
            candidate_id=candidate.candidate_id,
            candidate_name=candidate.name,
            role=candidate.role,
            ai_fit_score=final_fit_score,
            ai_decision=norm_ai,
            ai_confidence=decision_output.decision_confidence,
            human_score=candidate.expected_human_score,
            human_decision=norm_human,
            decision_matches=matches,
            score_delta=score_delta,
            archetype=calibrated.archetype_detected,
            inconsistency_notes=inconsistencies,
        )

    def run_cohort_simulation(self, cohort: List[CandidateSimulationProfile]) -> Dict[str, Any]:
        """Simulates an entire cohort and computes statistical alignment."""
        results: List[SimulationResult] = []
        total = len(cohort)
        matches_count = 0
        deltas = []

        for cand in cohort:
            res = self.run_candidate_journey(cand)
            results.append(res)
            if res.decision_matches:
                matches_count += 1
            deltas.append(res.score_delta)

        accuracy_rate = round((matches_count / total) * 100, 2) if total > 0 else 0.0
        avg_delta = round(sum(deltas) / total, 2) if total > 0 else 0.0

        # Pearson correlation between AI score and Human score
        ai_scores = [r.ai_fit_score for r in results]
        human_scores = [r.human_score for r in results]

        mean_ai = sum(ai_scores) / total
        mean_human = sum(human_scores) / total

        numerator = sum((a - mean_ai) * (h - mean_human) for a, h in zip(ai_scores, human_scores))
        denom_a = math.sqrt(sum((a - mean_ai) ** 2 for a in ai_scores))
        denom_h = math.sqrt(sum((h - mean_human) ** 2 for h in human_scores))

        correlation = round(numerator / (denom_a * denom_h), 4) if (denom_a * denom_h) > 0 else 1.0

        return {
            "total_candidates": total,
            "decision_agreement_count": matches_count,
            "decision_agreement_percentage": accuracy_rate,
            "average_score_delta": avg_delta,
            "pearson_correlation": correlation,
            "detailed_results": [
                {
                    "candidate_id": r.candidate_id,
                    "name": r.candidate_name,
                    "ai_score": r.ai_fit_score,
                    "human_score": r.human_score,
                    "ai_decision": r.ai_decision,
                    "human_decision": r.human_decision,
                    "agreed": r.decision_matches,
                    "archetype": r.archetype,
                    "inconsistencies": r.inconsistency_notes,
                }
                for r in results
            ],
        }
