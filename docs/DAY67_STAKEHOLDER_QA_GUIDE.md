# Day 67 — Stakeholder Q&A Defense Guide

## 1. Overview
This document compiles the most frequent, challenging technical and strategic questions asked by executives, recruiters, compliance officers, and engineering managers, along with verified answers.

---

## 2. Strategic & Technical Questions

### Q1: How does Zecpath AI prevent algorithmic bias against underrepresented groups?
- **Answer:** "Zecpath enforces strict fairness and demographic parity controls:
  1. Personal identifiers (name, gender, age, photo, address) are anonymized before semantic matching.
  2. Scoring rubrics rely on demonstrated competency keywords, AST code correctness, and STAR-behavioral structures rather than proxy variables.
  3. Every decision includes an explainable rationale, and the system is continuously evaluated for adverse impact ratio ($\ge 0.80$ standard)."

### Q2: What happens if a candidate experiences a legitimate network glitch during an interview?
- **Answer:** "Our integrity system differentiates between transient packet loss and malicious intent. Single tab switches or momentary video drops are classified as `LOW_RISK`. A `CRITICAL_RISK` flag requires repeated, corroborated telemetry (e.g. 5+ tab switches, simultaneous massive clipboard pastes, and multiple face disappearances)."

### Q3: How does the system handle high concurrency during campus recruitment drives?
- **Answer:** "The backend is architected asynchronously on FastAPI ASGI. Time-intensive operations (PDF text extraction and model inference) run via background workers and async job polling (`/api/integration/resume/parse-job/{job_id}`). In Day 60 benchmarks, the platform processed 100 concurrent candidate streams with sub-second response times."

### Q4: Can a recruiter override the AI recommendation?
- **Answer:** "Yes, human-in-the-loop governance is a core pillar. Recruiters have full administrative override authority. When an override occurs, the system records the recruiter's ID, reason code, and timestamp into the immutable SHA-256 decision audit ledger for organizational accountability."
