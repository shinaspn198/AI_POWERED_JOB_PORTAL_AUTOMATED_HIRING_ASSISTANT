"""
Day 51 - Cross-Round Aggregation Engine

Combines all evaluation stages into a unified hiring intelligence score:
- ATS
- Screening
- HR Interview
- Technical Interview
- Machine Test

Supports role-based weighting, experience profile normalization,
and granular transparency audit trails.
"""

from typing import Dict, Any, Optional
from unified_scoring.models import UnifiedCandidateScore, RoundScoreBreakdown
from unified_scoring.weight_config import (
    STAGES,
    get_weights_for_role,
    EXPERIENCE_PROFILE_NORMALIZERS
)
from unified_scoring.hiring_fit import calculate_hiring_fit


class CrossRoundAggregationEngine:
    """Aggregates and normalizes multi-stage interview evaluation scores."""

    def __init__(self):
        pass

    def _validate_score(self, stage_name: str, score: float) -> float:
        """Validate numeric score within 0 - 100 range."""
        if not isinstance(score, (int, float)):
            raise TypeError(f"{stage_name} score must be a number, got {type(score).__name__}")
        if score < 0 or score > 100:
            raise ValueError(f"{stage_name} score must be between 0 and 100, got {score}")
        return float(score)

    def normalize_profile(
        self,
        raw_scores: Dict[str, float],
        experience_level: str
    ) -> Dict[str, float]:
        """
        Applies profile normalization based on candidate experience level
        to ensure equitable evaluation across career stages.
        """
        exp_key = experience_level.lower()
        normalizers = EXPERIENCE_PROFILE_NORMALIZERS.get(
            exp_key,
            EXPERIENCE_PROFILE_NORMALIZERS["mid"]
        )

        multiplier_map = {
            "ats": normalizers["ats_multiplier"],
            "screening": normalizers["screening_multiplier"],
            "hr_interview": normalizers["hr_multiplier"],
            "technical_interview": normalizers["tech_multiplier"],
            "machine_test": normalizers["machine_test_multiplier"],
        }

        normalized = {}
        for stage, score in raw_scores.items():
            mult = multiplier_map.get(stage, 1.0)
            # Normalization adjustments are clamped between 0 and 100
            adjusted = min(100.0, max(0.0, score * mult))
            normalized[stage] = round(adjusted, 2)

        return normalized

    def aggregate_candidate_score(
        self,
        candidate_id: str,
        candidate_name: str,
        role: str,
        experience_level: str,
        ats_score: float,
        screening_score: float,
        hr_interview_score: float,
        technical_interview_score: float,
        machine_test_score: float,
        custom_weights: Optional[Dict[str, float]] = None
    ) -> UnifiedCandidateScore:
        """
        Executes cross-round aggregation across all 5 evaluation stages.
        """
        # 1. Validation
        raw_scores = {
            "ats": self._validate_score("ATS", ats_score),
            "screening": self._validate_score("Screening", screening_score),
            "hr_interview": self._validate_score("HR Interview", hr_interview_score),
            "technical_interview": self._validate_score("Technical Interview", technical_interview_score),
            "machine_test": self._validate_score("Machine Test", machine_test_score),
        }

        # 2. Retrieve Role Weights
        weights = custom_weights or get_weights_for_role(role)

        # 3. Profile Normalization
        normalized_scores = self.normalize_profile(raw_scores, experience_level)

        # 4. Weighted Calculation & Breakdown
        stage_breakdown: Dict[str, RoundScoreBreakdown] = {}
        weighted_sum = 0.0

        for stage_key, raw in raw_scores.items():
            norm = normalized_scores[stage_key]
            wt = weights.get(stage_key, 0.20)
            contribution = round(norm * wt, 2)
            weighted_sum += contribution

            stage_breakdown[stage_key] = RoundScoreBreakdown(
                stage_key=stage_key,
                stage_name=STAGES.get(stage_key, stage_key),
                raw_score=raw,
                normalized_score=norm,
                weight=wt,
                weighted_contribution=contribution,
            )

        weighted_base_score = round(weighted_sum, 2)

        # 5. Hiring Fit Score Calculation
        hiring_fit_score, recommendation = calculate_hiring_fit(weighted_base_score)

        # 6. Transparency Audit Trail
        transparency_audit = {
            "role_weight_profile": role,
            "experience_level_adjustment": experience_level,
            "weights_applied": weights,
            "formula": "Sum(Normalized_Score[i] * Role_Weight[i])",
            "explanation": (
                f"Candidate achieved a weighted score of {hiring_fit_score}%. "
                f"Evaluation emphasized role requirements for '{role}' "
                f"with profile adjustments for '{experience_level}' tier."
            ),
        }

        return UnifiedCandidateScore(
            candidate_id=candidate_id,
            candidate_name=candidate_name,
            role=role,
            experience_level=experience_level,
            ats_score=raw_scores["ats"],
            screening_score=raw_scores["screening"],
            hr_interview_score=raw_scores["hr_interview"],
            technical_interview_score=raw_scores["technical_interview"],
            machine_test_score=raw_scores["machine_test"],
            weighted_base_score=weighted_base_score,
            profile_adjustment_factor=1.0,
            hiring_fit_score=hiring_fit_score,
            hiring_recommendation=recommendation,
            stage_breakdown=stage_breakdown,
            transparency_audit=transparency_audit,
        )


def create_unified_candidate_score(
    candidate_id: str,
    candidate_name: str,
    role: str,
    experience_level: str,
    ats_score: float,
    screening_score: float,
    hr_interview_score: float,
    technical_interview_score: float,
    machine_test_score: float,
) -> UnifiedCandidateScore:
    """Convenience helper to instantiate and run cross-round aggregation."""
    engine = CrossRoundAggregationEngine()
    return engine.aggregate_candidate_score(
        candidate_id=candidate_id,
        candidate_name=candidate_name,
        role=role,
        experience_level=experience_level,
        ats_score=ats_score,
        screening_score=screening_score,
        hr_interview_score=hr_interview_score,
        technical_interview_score=technical_interview_score,
        machine_test_score=machine_test_score,
    )
