"""
Tests for Day 63 — Demo Dataset & Simulation Environment
"""

import pytest
import os
import json
from simulation.demo_pipeline_simulation import DemoPipelineSimulation
from performance.ai_monitoring import ai_monitor


def test_demo_dataset_schema():
    candidates_file = "data/demo_dataset/demo_candidates.json"
    jobs_file = "data/demo_dataset/job_descriptions.json"

    assert os.path.exists(candidates_file), "Candidates dataset file missing"
    assert os.path.exists(jobs_file), "Job descriptions file missing"

    with open(candidates_file, "r", encoding="utf-8") as f:
        candidates = json.load(f)
    assert len(candidates) >= 4

    tiers = {c["profile_tier"] for c in candidates}
    assert "TOP_TALENT" in tiers
    assert "AVERAGE_ACCEPTABLE" in tiers
    assert "MISMATCHED_UNQUALIFIED" in tiers
    assert "INTEGRITY_VIOLATION" in tiers

    with open(jobs_file, "r", encoding="utf-8") as f:
        jobs = json.load(f)
    assert len(jobs) >= 2


def test_demo_pipeline_simulation_execution():
    ai_monitor.reset()
    sim = DemoPipelineSimulation()
    results = sim.run_simulation()

    assert len(results) == 4
    results_map = {r["candidate_id"]: r for r in results}

    # 1. Top Talent candidate (Sarah Chen) should be HIRE
    top_cand = results_map["CAND-DEMO-01"]
    assert top_cand["ai_decision"] in ["HIRE", "Selected"]
    assert top_cand["ats_score"] >= 85.0
    assert top_cand["hiring_fit_score"] >= 85.0

    # 2. Average candidate (Marcus Brody) should be SHORTLIST / Hold
    avg_cand = results_map["CAND-DEMO-02"]
    assert avg_cand["ai_decision"] in ["SHORTLIST", "Hold / Review"]
    assert 60.0 <= avg_cand["hiring_fit_score"] <= 85.0

    # 3. Mismatched candidate (David Miller) should be REJECT
    mismatch_cand = results_map["CAND-DEMO-03"]
    assert mismatch_cand["ai_decision"] in ["REJECT", "Rejected"]
    assert mismatch_cand["ats_score"] < 65.0

    # 4. Integrity violation candidate (Evan Vance) should be REJECT
    flagged_cand = results_map["CAND-DEMO-04"]
    assert flagged_cand["ai_decision"] in ["REJECT", "Rejected"]
    assert flagged_cand["integrity_score"] < 50.0

    # Verify audit logs in ai_monitor
    dash = ai_monitor.get_dashboard_stats()
    assert dash["candidate_stats"]["total_candidates"] == 4
    assert len(ai_monitor.audit_logs) == 4
