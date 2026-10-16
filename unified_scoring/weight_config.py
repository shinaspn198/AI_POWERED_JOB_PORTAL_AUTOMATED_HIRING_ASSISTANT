"""
Day 51 - Role-Based Weightage System and Profile Normalization Config

Defines evaluation weights across the 5 stages:
1. ATS
2. Screening
3. HR Interview
4. Technical Interview
5. Machine Test
"""

from typing import Dict, Any

STAGES = {
    "ats": "ATS Resume Match",
    "screening": "Candidate Screening",
    "hr_interview": "HR Behavioral Interview",
    "technical_interview": "Technical Skill Interview",
    "machine_test": "Hands-on Machine Test",
}

DEFAULT_WEIGHTS = {
    "ats": 0.20,
    "screening": 0.20,
    "hr_interview": 0.20,
    "technical_interview": 0.20,
    "machine_test": 0.20,
}

ROLE_WEIGHTS: Dict[str, Dict[str, float]] = {
    "software_engineer": {
        "ats": 0.15,
        "screening": 0.15,
        "hr_interview": 0.15,
        "technical_interview": 0.25,
        "machine_test": 0.30,
    },
    "ai_engineer": {
        "ats": 0.15,
        "screening": 0.15,
        "hr_interview": 0.15,
        "technical_interview": 0.25,
        "machine_test": 0.30,
    },
    "data_analyst": {
        "ats": 0.20,
        "screening": 0.15,
        "hr_interview": 0.15,
        "technical_interview": 0.25,
        "machine_test": 0.25,
    },
    "product_manager": {
        "ats": 0.20,
        "screening": 0.25,
        "hr_interview": 0.25,
        "technical_interview": 0.20,
        "machine_test": 0.10,
    },
    "hr_specialist": {
        "ats": 0.20,
        "screening": 0.25,
        "hr_interview": 0.35,
        "technical_interview": 0.10,
        "machine_test": 0.10,
    },
}

# Profile Normalization Adjustments across experience levels
# Compensates for structural resume differences (e.g., freshers vs seniors)
EXPERIENCE_PROFILE_NORMALIZERS: Dict[str, Dict[str, float]] = {
    "entry": {
        # Entry level: boost hands-on demonstration, relax heavy resume years requirement
        "ats_multiplier": 1.05,
        "screening_multiplier": 1.00,
        "hr_multiplier": 1.00,
        "tech_multiplier": 1.00,
        "machine_test_multiplier": 1.05,
    },
    "mid": {
        "ats_multiplier": 1.00,
        "screening_multiplier": 1.00,
        "hr_multiplier": 1.00,
        "tech_multiplier": 1.00,
        "machine_test_multiplier": 1.00,
    },
    "senior": {
        # Seniors: higher bar on architecture & technical interview
        "ats_multiplier": 1.00,
        "screening_multiplier": 1.00,
        "hr_multiplier": 1.02,
        "tech_multiplier": 1.00,
        "machine_test_multiplier": 0.98,
    },
}


def get_weights_for_role(role: str) -> Dict[str, float]:
    """Retrieve normalized weight configuration for a specified job role."""
    key = role.lower().replace(" ", "_")
    weights = ROLE_WEIGHTS.get(key, DEFAULT_WEIGHTS).copy()

    # Ensure total weights sum to 1.0
    total = sum(weights.values())
    return {k: round(v / total, 4) for k, v in weights.items()}