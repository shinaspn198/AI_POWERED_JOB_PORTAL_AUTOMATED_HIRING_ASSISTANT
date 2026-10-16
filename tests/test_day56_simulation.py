"""
Unit & Integration Tests for Day 56 - Full System Simulation
"""

import pytest
from simulation.full_pipeline_simulation import (
    FullSystemSimulator,
    CandidateSimulationProfile
)


def test_full_system_simulation_archetypes():
    simulator = FullSystemSimulator()
    
    # 1. Strong Tech Lead
    lead = CandidateSimulationProfile(
        candidate_id="SIM-001",
        name="Elena Rostova",
        role="ai_engineer",
        experience_level="senior",
        resume_text="10 years leading deep learning and MLOps platforms...",
        screening_response="I architect high-throughput LLM pipelines and distributed inference systems.",
        hr_response="I prioritize servant leadership, open communication, and psychological safety.",
        coding_submission="def optimize_inference(): pass",
        expected_human_decision="Selected",
        expected_human_score=92.0,
        simulated_ats_raw=90.0,
        simulated_screening_raw=92.0,
        simulated_hr_raw=94.0,
        simulated_tech_raw=95.0,
        simulated_machine_raw=96.0,
    )
    
    # 2. Hidden Gem
    gem = CandidateSimulationProfile(
        candidate_id="SIM-002",
        name="Devon Vance",
        role="software_engineer",
        experience_level="mid",
        resume_text="Self-taught developer, built open source high-concurrency systems...",
        screening_response="I build asynchronous network services and database query engines.",
        hr_response="I focus on continuous learning, automated testing, and clean code.",
        coding_submission="class AsyncEngine: pass",
        expected_human_decision="Selected",
        expected_human_score=88.0,
        simulated_ats_raw=62.0,           # Low ATS keyword match
        simulated_screening_raw=82.0,
        simulated_hr_raw=80.0,
        simulated_tech_raw=88.0,
        simulated_machine_raw=98.0,       # Near-perfect coding
    )
    
    # 3. Resume Padder
    padder = CandidateSimulationProfile(
        candidate_id="SIM-003",
        name="Clayton Fluff",
        role="software_engineer",
        experience_level="entry",
        resume_text="Kubernetes, Docker, Python, PyTorch, React, Kafka, Redis, Golang, AWS, Microservices...",
        screening_response="I have listed many technologies on my resume.",
        hr_response="I am excited about jobs.",
        coding_submission="syntax error",
        expected_human_decision="Rejected",
        expected_human_score=50.0,
        simulated_ats_raw=92.0,           # High keyword stuffing
        simulated_screening_raw=70.0,
        simulated_hr_raw=65.0,
        simulated_tech_raw=45.0,
        simulated_machine_raw=40.0,       # Fails execution
    )
    
    cohort = [lead, gem, padder]
    cohort_results = simulator.run_cohort_simulation(cohort)
    
    assert cohort_results["total_candidates"] == 3
    assert cohort_results["decision_agreement_percentage"] == 100.0
    assert cohort_results["pearson_correlation"] > 0.90
    assert cohort_results["average_score_delta"] < 8.0
