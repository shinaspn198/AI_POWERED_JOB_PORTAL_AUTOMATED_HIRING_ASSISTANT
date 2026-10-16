"""
Day 51 - Hiring Fit Calculator

Calculates final hiring fit percentage and categorical recommendations.
"""

from typing import Tuple


def calculate_hiring_fit(unified_score: float) -> Tuple[float, str]:
    """
    Clamps the unified score between 0.0 and 100.0% and derives
    the final hiring recommendation tier.
    """
    score = max(0.0, min(100.0, round(unified_score, 2)))

    if score >= 85.0:
        recommendation = "STRONG_HIRE"
    elif score >= 70.0:
        recommendation = "HIRE"
    elif score >= 55.0:
        recommendation = "BORDERLINE_REVIEW"
    else:
        recommendation = "REJECT"

    return score, recommendation