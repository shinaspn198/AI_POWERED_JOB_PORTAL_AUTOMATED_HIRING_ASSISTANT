"""
Day 51 - Cross-Round Aggregation Engine Models

Data objects for representing cross-round scores, weight breakdowns,
and unified candidate hiring fit objects.
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class RoundScoreBreakdown:
    stage_key: str
    stage_name: str
    raw_score: float
    normalized_score: float
    weight: float
    weighted_contribution: float


@dataclass
class UnifiedCandidateScore:
    candidate_id: str
    candidate_name: str
    role: str
    experience_level: str

    # 5 evaluation stages
    ats_score: float
    screening_score: float
    hr_interview_score: float
    technical_interview_score: float
    machine_test_score: float

    # Aggregation & Normalization results
    weighted_base_score: float
    profile_adjustment_factor: float
    hiring_fit_score: float          # Final hiring fit percentage (0 - 100%)
    hiring_recommendation: str      # STRONG_HIRE, HIRE, BORDERLINE, REJECT

    # Transparency audit trail
    stage_breakdown: Dict[str, RoundScoreBreakdown] = field(default_factory=dict)
    transparency_audit: Dict[str, Any] = field(default_factory=dict)

    # Backward compatibility properties for Day 41 legacy callers
    @property
    def interview_score(self) -> float:
        return self.technical_interview_score

    @property
    def unified_score(self) -> float:
        return self.hiring_fit_score

    @property
    def hiring_fit_percentage(self) -> float:
        return self.hiring_fit_score