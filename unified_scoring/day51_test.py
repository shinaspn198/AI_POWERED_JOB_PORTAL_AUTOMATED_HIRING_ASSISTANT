"""
Day 51 - Test Cross-Round Aggregation Engine
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_scoring.aggregation_engine import create_unified_candidate_score


def test_cross_round_aggregation():
    print("=" * 65)
    print("DAY 51 - CROSS-ROUND AGGREGATION ENGINE TEST")
    print("=" * 65)

    # Candidate 1: AI Engineer (Senior)
    c1 = create_unified_candidate_score(
        candidate_id="CAND-001",
        candidate_name="Alex Rivera",
        role="ai_engineer",
        experience_level="senior",
        ats_score=88.0,
        screening_score=82.0,
        hr_interview_score=90.0,
        technical_interview_score=94.0,
        machine_test_score=92.0
    )

    print(f"\n[CANDIDATE 1: {c1.candidate_name} ({c1.candidate_id})]")
    print(f"Role                     : {c1.role} | Tier: {c1.experience_level}")
    print(f"Hiring Fit Score         : {c1.hiring_fit_score}%")
    print(f"Recommendation           : {c1.hiring_recommendation}")
    print("\nStage Breakdown (Transparency):")
    for stage_key, b in c1.stage_breakdown.items():
        print(f" - {b.stage_name:<26}: Raw={b.raw_score:<5} Norm={b.normalized_score:<5} Weight={b.weight*100:>4.1f}% Contribution={b.weighted_contribution:>5.2f}")

    # Candidate 2: Software Engineer (Entry Level)
    c2 = create_unified_candidate_score(
        candidate_id="CAND-002",
        candidate_name="Priya Sharma",
        role="software_engineer",
        experience_level="entry",
        ats_score=72.0,   # Lower resume score
        screening_score=80.0,
        hr_interview_score=78.0,
        technical_interview_score=88.0,
        machine_test_score=95.0  # High practical coding skill
    )

    print(f"\n[CANDIDATE 2: {c2.candidate_name} ({c2.candidate_id})]")
    print(f"Role                     : {c2.role} | Tier: {c2.experience_level}")
    print(f"Hiring Fit Score         : {c2.hiring_fit_score}%")
    print(f"Recommendation           : {c2.hiring_recommendation}")
    print("\nStage Breakdown (Transparency):")
    for stage_key, b in c2.stage_breakdown.items():
        print(f" - {b.stage_name:<26}: Raw={b.raw_score:<5} Norm={b.normalized_score:<5} Weight={b.weight*100:>4.1f}% Contribution={b.weighted_contribution:>5.2f}")

    print("\nTransparency Audit Explanation:")
    print(f" - {c2.transparency_audit['explanation']}")
    print("=" * 65)


if __name__ == "__main__":
    test_cross_round_aggregation()
