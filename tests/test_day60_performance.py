"""
Unit & Integration Tests for Day 60 - Performance Tuning & Batch Processing
"""

import pytest
import time
from performance.cache_manager import TTLCache
from performance.batch_processor import (
    BatchResumeProcessor,
    CandidateBatchItem
)
from performance.benchmark_suite import run_synthetic_load_benchmark


def test_ttl_cache_operations():
    cache = TTLCache(maxsize=3, default_ttl_sec=1.0)
    
    cache.set("a", 100)
    cache.set("b", 200)
    assert cache.get("a") == 100
    assert cache.get("b") == 200
    
    # Eviction on maxsize
    cache.set("c", 300)
    cache.set("d", 400)  # Should evict oldest
    
    stats = cache.get_stats()
    assert stats["size"] <= 3
    assert stats["hits"] >= 2


def test_batch_resume_processor():
    processor = BatchResumeProcessor(default_workers=4)
    
    sample_resumes = [
        CandidateBatchItem(
            candidate_id=f"BATCH-{i:03d}",
            role="software_engineer",
            raw_resume_text=f"Candidate {i}\nEmail: c{i}@test.com\nSKILLS\nPython\nFastAPI\nSQL\nEXPERIENCE\nDev at Org"
        )
        for i in range(12)
    ]
    
    report = processor.process_batch(sample_resumes, max_workers=4)
    
    assert report.total_items == 12
    assert report.succeeded_count == 12
    assert report.failed_count == 0
    assert report.throughput_items_per_second > 5.0
    assert report.p50_latency_ms >= 0


def test_synthetic_load_benchmark():
    res = run_synthetic_load_benchmark(concurrency=8, total_requests=40)
    
    assert res["total_requests"] == 40
    assert res["throughput_rps"] > 50.0
    assert res["p50_latency_ms"] < 25.0
    assert res["error_rate_pct"] == 0.0
