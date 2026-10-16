"""
Day 51 - Unified Scoring Engine Bridge

Exposes cross-round score generation and legacy scoring functions.
"""

from unified_scoring.aggregation_engine import (
    CrossRoundAggregationEngine,
    create_unified_candidate_score
)


def final_score(ats_score, interview_score):
    """Legacy 2-round average calculator."""
    scores = {
        "ATS score": ats_score,
        "Interview score": interview_score
    }

    for name, score in scores.items():
        if not isinstance(score, (int, float)):
            raise TypeError(f"{name} must be a number.")
        if score < 0 or score > 100:
            raise ValueError(f"{name} must be between 0 and 100.")

    return round((ats_score + interview_score) / 2, 2)


def create_candidate_score(
    candidate_id: str,
    role: str,
    ats_score: float,
    screening_score: float,
    interview_score: float,
    hr_interview_score: float = None,
    technical_interview_score: float = None,
    machine_test_score: float = None,
    candidate_name: str = "Candidate",
    experience_level: str = "mid"
):
    """Bridge for cross-round aggregation supporting both 3-stage and 5-stage inputs."""
    hr_score = hr_interview_score if hr_interview_score is not None else interview_score
    tech_score = technical_interview_score if technical_interview_score is not None else interview_score
    mach_score = machine_test_score if machine_test_score is not None else interview_score

    return create_unified_candidate_score(
        candidate_id=candidate_id,
        candidate_name=candidate_name,
        role=role,
        experience_level=experience_level,
        ats_score=ats_score,
        screening_score=screening_score,
        hr_interview_score=hr_score,
        technical_interview_score=tech_score,
        machine_test_score=mach_score
    )