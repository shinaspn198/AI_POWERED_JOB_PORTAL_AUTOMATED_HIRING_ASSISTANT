"""
SQLAlchemy Model for Candidate Assessments & Cross-Round Results
"""

from datetime import datetime
from sqlalchemy import Float, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from api.database import Base


class CandidateAssessment(Base):
    __tablename__ = "candidate_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    candidate_id: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    candidate_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    experience_level: Mapped[str] = mapped_column(String(20), default="mid")

    # 5 Stage Scores
    ats_score: Mapped[float] = mapped_column(Float, default=0.0)
    screening_score: Mapped[float] = mapped_column(Float, default=0.0)
    hr_interview_score: Mapped[float] = mapped_column(Float, default=0.0)
    technical_interview_score: Mapped[float] = mapped_column(Float, default=0.0)
    machine_test_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Integrity & Malpractice Telemetry
    integrity_score: Mapped[float] = mapped_column(Float, default=100.0)
    risk_tag: Mapped[str] = mapped_column(String(30), default="LOW_RISK")

    # Aggregated Hiring Fit
    hiring_fit_score: Mapped[float] = mapped_column(Float, default=0.0)
    hiring_recommendation: Mapped[str] = mapped_column(String(30), default="PENDING")
    status: Mapped[str] = mapped_column(String(30), default="evaluated")  # evaluated, shortlisted, rejected, hired

    # Detailed Audit & Breakdown (JSON)
    breakdown_data: Mapped[dict] = mapped_column(JSON, default=dict)
    audit_notes: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
