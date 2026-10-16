"""
Day 54 - Scoring Optimization & Consistency Refinement Engine

Enhances decision accuracy:
1. False Positive (Resume Padder) & False Negative (Hidden Gem) Mitigation
2. Seniority-Aware Dynamic Threshold Calibration
3. Cross-Round Consistency & Discrepancy Scoring
4. Ultra-Low Latency In-Memory Execution
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
import math
import time


@dataclass
class CalibratedScoreResult:
    original_fit_score: float
    calibrated_fit_score: float
    adjustment_applied: float
    consistency_score: float           # 0 - 100% consistency across rounds
    discrepancy_flag: bool
    archetype_detected: str            # NORMAL, HIDDEN_GEM, RESUME_PADDER, VOLATILE_CANDIDATE
    explanation: str
    calibrated_weights: Dict[str, float]
    execution_latency_ms: float


class ScoringOptimizationEngine:
    """Optimizes scoring accuracy, mitigates bias/errors, and ensures cross-round consistency."""

    def __init__(self):
        # Role threshold benchmarks
        self.role_thresholds = {
            "entry": {"pass_min": 65.0, "strong_min": 80.0, "machine_weight_boost": 0.05},
            "mid": {"pass_min": 70.0, "strong_min": 82.0, "machine_weight_boost": 0.0},
            "senior": {"pass_min": 75.0, "strong_min": 85.0, "machine_weight_boost": -0.05},
            "lead": {"pass_min": 80.0, "strong_min": 88.0, "machine_weight_boost": -0.05},
        }

    def calibrate_scores(
        self,
        candidate_id: str,
        role: str,
        experience_level: str,
        stage_scores: Dict[str, float],
        base_weights: Dict[str, float],
        contradiction_detected: bool = False,
        integrity_score: float = 100.0,
    ) -> CalibratedScoreResult:
        """Applies refinement algorithms to eliminate false positives and false negatives."""
        start_time = time.perf_counter()

        ats = stage_scores.get("ats", 0.0)
        screening = stage_scores.get("screening", 0.0)
        hr = stage_scores.get("hr", 0.0)
        tech = stage_scores.get("technical", 0.0)
        machine = stage_scores.get("machine_test", 0.0)

        tier = experience_level.lower() if experience_level.lower() in self.role_thresholds else "mid"
        tier_cfg = self.role_thresholds[tier]

        # 1. Calculate Base Weighted Score
        base_fit = sum(stage_scores.get(st, 0.0) * base_weights.get(st, 0.20) for st in base_weights)

        # 2. Cross-Round Consistency & Variance Analysis
        scores_list = [ats, screening, hr, tech, machine]
        mean_score = sum(scores_list) / len(scores_list)
        variance = sum((s - mean_score) ** 2 for s in scores_list) / len(scores_list)
        std_dev = math.sqrt(variance)

        # Consistency score: 100% when std_dev is 0, down to 50% when std_dev is 25+
        consistency_score = max(0.0, min(100.0, round(100.0 - (std_dev * 2.0), 1)))
        discrepancy_flag = std_dev > 22.0

        # 3. Archetype & Anomaly Detection (False Positive / False Negative)
        adjustment = 0.0
        archetype = "NORMAL"
        rationale = []

        # Archetype A: The "Hidden Gem" (False Negative Avoidance)
        # Low/Moderate ATS (e.g. <= 68) but Outstanding Machine Test (>= 88) and Solid Tech (>= 75)
        if ats <= 68.0 and machine >= 88.0 and tech >= 75.0:
            archetype = "HIDDEN_GEM"
            boost = round(min(8.0, (machine - 70.0) * 0.25), 2)
            adjustment += boost
            rationale.append(
                f"Candidate recognized as 'Hidden Gem': Non-traditional resume (ATS: {ats}%) overridden by "
                f"stellar hands-on coding ability (Machine Test: {machine}%). Calibrated +{boost}% upward."
            )

        # Archetype B: The "Resume Padder" (False Positive Elimination)
        # High ATS (>= 82) but severely underperforms in Machine Test (<= 58) or Tech (<= 55)
        elif ats >= 82.0 and (machine <= 58.0 or tech <= 55.0):
            archetype = "RESUME_PADDER"
            penalty = -round(min(12.0, max(4.0, (60.0 - machine) * 0.35 + (60.0 - tech) * 0.25)), 2)
            adjustment += penalty
            rationale.append(
                f"Candidate flagged as 'Resume Padder': High keyword density in resume (ATS: {ats}%) refuted by "
                f"poor hands-on engineering execution (Machine Test: {machine}%, Tech: {tech}%). Penalized {penalty}%."
            )

        # Archetype C: Volatile / Inconsistent Candidate
        elif discrepancy_flag:
            archetype = "VOLATILE_CANDIDATE"
            volatility_penalty = -4.0
            adjustment += volatility_penalty
            rationale.append(
                f"Cross-round score volatility detected (std dev: {std_dev:.1f}, consistency: {consistency_score}%). "
                f"Applied consistency damping penalty of {volatility_penalty}%."
            )

        # Contradiction and Integrity adjustments
        if contradiction_detected:
            adjustment -= 6.0
            rationale.append("Contradiction penalty of -6.0% applied due to conflicting interview assertions.")

        if integrity_score < 70.0:
            integrity_penalty = -10.0
            adjustment += integrity_penalty
            rationale.append(f"Malpractice risk penalty of {integrity_penalty}% applied due to low proctoring integrity ({integrity_score}%).")

        # 4. Seniority Weight Calibration
        calibrated_weights = dict(base_weights)
        if tier == "entry":
            # Boost machine test, reduce ATS weight
            calibrated_weights["machine_test"] = calibrated_weights.get("machine_test", 0.30) + 0.05
            calibrated_weights["ats"] = max(0.05, calibrated_weights.get("ats", 0.15) - 0.05)
        elif tier in ("senior", "lead"):
            # Boost technical interview, reduce ATS weight
            calibrated_weights["technical"] = calibrated_weights.get("technical", 0.25) + 0.05
            calibrated_weights["ats"] = max(0.05, calibrated_weights.get("ats", 0.15) - 0.05)

        # Normalize weights to sum exactly to 1.0
        w_sum = sum(calibrated_weights.values())
        calibrated_weights = {k: round(v / w_sum, 4) for k, v in calibrated_weights.items()}

        # 5. Final Calibrated Score
        calibrated_score = round(max(0.0, min(100.0, base_fit + adjustment)), 2)

        if not rationale:
            explanation = f"Standard calibration passed with {consistency_score}% consistency across 5 stages."
        else:
            explanation = " ".join(rationale)

        latency_ms = round((time.perf_counter() - start_time) * 1000, 3)

        return CalibratedScoreResult(
            original_fit_score=round(base_fit, 2),
            calibrated_fit_score=calibrated_score,
            adjustment_applied=round(adjustment, 2),
            consistency_score=consistency_score,
            discrepancy_flag=discrepancy_flag,
            archetype_detected=archetype,
            explanation=explanation,
            calibrated_weights=calibrated_weights,
            execution_latency_ms=latency_ms,
        )
