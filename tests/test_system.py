import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)
from parsers.resume_parser import parse_resume
from ats_engine.ats_model import calculate_ats_score
from scoring.score_engine import final_score


def test_resume_parser():
    sample_path = "data/sample_resumes/sample_resume.pdf" if os.path.exists("data/sample_resumes/sample_resume.pdf") else "sample.pdf"
    result = parse_resume(sample_path)
    assert "skills" in result



def test_ats_score():

    score = calculate_ats_score(
        ["Python", "AI"]
    )

    assert score == 40



def test_final_score():

    result = final_score(
        80,
        90
    )

    assert result == 85