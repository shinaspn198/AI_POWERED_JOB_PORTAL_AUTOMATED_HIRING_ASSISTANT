from dataclasses import dataclass, field
from typing import List


@dataclass
class ScreeningReport:
    candidate_id: str
    screening_score: float
    decision: str

    key_answers: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    missing_information: List[str] = field(default_factory=list)

    salary_expectation: str = ""
    availability: str = ""
    confirmed_skills: List[str] = field(default_factory=list)

    recommendation: str = ""