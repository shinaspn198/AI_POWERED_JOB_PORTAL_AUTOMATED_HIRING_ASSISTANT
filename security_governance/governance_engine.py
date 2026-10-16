"""
Day 55 - Security & AI Governance Framework

Implements enterprise-grade AI compliance and security:
1. Tamper-evident Audit Trail System (Score Logs & Decision Logs with SHA-256 Hash Chaining)
2. Automated Data Retention & Anonymization Policies (GDPR / EEOC / CCPA)
3. Explicit Consent Verification Gatekeeper
4. Secure Storage & PII Redaction for Transcripts and Reports
5. Role-Based Access Control (RBAC) Logic
"""

import hashlib
import json
import re
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum


# =========================================================
# 1. RBAC (ROLE-BASED ACCESS CONTROL)
# =========================================================

class UserRole(str, Enum):
    CANDIDATE = "candidate"
    RECRUITER = "recruiter"
    HIRING_MANAGER = "hiring_manager"
    ADMIN = "admin"


class Permission(str, Enum):
    VIEW_OWN_ASSESSMENT = "view_own_assessment"
    VIEW_CANDIDATE_LIST = "view_candidate_list"
    VIEW_CANDIDATE_REPORT = "view_candidate_report"
    UPDATE_CANDIDATE_STATUS = "update_candidate_status"
    OVERRIDE_AI_DECISION = "override_ai_decision"
    ACCESS_AUDIT_LOGS = "access_audit_logs"
    EXECUTE_DATA_PURGE = "execute_data_purge"
    CONFIGURE_WEIGHTS = "configure_weights"


ROLE_PERMISSIONS: Dict[UserRole, Set[Permission]] = {
    UserRole.CANDIDATE: {
        Permission.VIEW_OWN_ASSESSMENT,
    },
    UserRole.RECRUITER: {
        Permission.VIEW_CANDIDATE_LIST,
        Permission.VIEW_CANDIDATE_REPORT,
        Permission.UPDATE_CANDIDATE_STATUS,
    },
    UserRole.HIRING_MANAGER: {
        Permission.VIEW_CANDIDATE_LIST,
        Permission.VIEW_CANDIDATE_REPORT,
        Permission.UPDATE_CANDIDATE_STATUS,
        Permission.OVERRIDE_AI_DECISION,
    },
    UserRole.ADMIN: {
        Permission.VIEW_OWN_ASSESSMENT,
        Permission.VIEW_CANDIDATE_LIST,
        Permission.VIEW_CANDIDATE_REPORT,
        Permission.UPDATE_CANDIDATE_STATUS,
        Permission.OVERRIDE_AI_DECISION,
        Permission.ACCESS_AUDIT_LOGS,
        Permission.EXECUTE_DATA_PURGE,
        Permission.CONFIGURE_WEIGHTS,
    },
}


class AccessControlGuard:
    """Enforces RBAC permissions across API endpoints and operations."""

    @staticmethod
    def check_permission(user_role: UserRole, required_permission: Permission) -> bool:
        """Returns True if user role possesses the required permission."""
        perms = ROLE_PERMISSIONS.get(user_role, set())
        return required_permission in perms

    @staticmethod
    def enforce_permission(user_role: UserRole, required_permission: Permission) -> None:
        """Raises PermissionError if unauthorized."""
        if not AccessControlGuard.check_permission(user_role, required_permission):
            raise PermissionError(
                f"Access Denied: Role '{user_role.value}' lacks permission '{required_permission.value}'."
            )


# =========================================================
# 2. TAMPER-EVIDENT AUDIT TRAIL (HASH-CHAINED LOGS)
# =========================================================

@dataclass
class AuditEntry:
    entry_id: str
    entry_type: str                  # SCORE_LOG or DECISION_LOG
    candidate_id: str
    actor_id: str
    actor_role: str
    timestamp: str
    action: str
    details: Dict[str, Any]
    prev_hash: str
    current_hash: str


class AuditTrailSystem:
    """Tamper-evident audit logger for score calculations and hiring decisions."""

    def __init__(self):
        self.audit_log: List[AuditEntry] = []
        self._last_hash = "GENESIS_HASH_0000000000000000000000000000000000000000000000000000000000"

    def _compute_hash(self, entry_data: Dict[str, Any], prev_hash: str) -> str:
        payload = f"{json.dumps(entry_data, sort_keys=True)}:{prev_hash}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def log_score_calculation(
        self,
        candidate_id: str,
        stage: str,
        score: float,
        actor_id: str = "ai_system",
        actor_role: str = "system",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AuditEntry:
        """Logs an immutable record of an AI score computation."""
        entry_id = f"SCORE-{len(self.audit_log) + 1:06d}"
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        data = {
            "entry_id": entry_id,
            "candidate_id": candidate_id,
            "stage": stage,
            "score": score,
            "metadata": metadata or {},
        }
        curr_hash = self._compute_hash(data, self._last_hash)

        entry = AuditEntry(
            entry_id=entry_id,
            entry_type="SCORE_LOG",
            candidate_id=candidate_id,
            actor_id=actor_id,
            actor_role=actor_role,
            timestamp=timestamp,
            action=f"Calculated {stage} score: {score}",
            details=data,
            prev_hash=self._last_hash,
            current_hash=curr_hash,
        )
        self.audit_log.append(entry)
        self._last_hash = curr_hash
        return entry

    def log_decision(
        self,
        candidate_id: str,
        decision: str,
        hiring_fit_score: float,
        actor_id: str,
        actor_role: str,
        rationale: str,
        override: bool = False,
    ) -> AuditEntry:
        """Logs a hiring recommendation or recruiter decision override."""
        entry_id = f"DECISION-{len(self.audit_log) + 1:06d}"
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        data = {
            "entry_id": entry_id,
            "candidate_id": candidate_id,
            "decision": decision,
            "hiring_fit_score": hiring_fit_score,
            "rationale": rationale,
            "override": override,
        }
        curr_hash = self._compute_hash(data, self._last_hash)

        entry = AuditEntry(
            entry_id=entry_id,
            entry_type="DECISION_LOG",
            candidate_id=candidate_id,
            actor_id=actor_id,
            actor_role=actor_role,
            timestamp=timestamp,
            action=f"Recorded decision '{decision}' (Override={override})",
            details=data,
            prev_hash=self._last_hash,
            current_hash=curr_hash,
        )
        self.audit_log.append(entry)
        self._last_hash = curr_hash
        return entry

    def verify_integrity(self) -> Tuple[bool, Optional[str]]:
        """Validates that no historical log entry has been altered."""
        last_hash = "GENESIS_HASH_0000000000000000000000000000000000000000000000000000000000"
        for i, entry in enumerate(self.audit_log):
            if entry.prev_hash != last_hash:
                return False, f"Hash chain broken at index {i} (entry {entry.entry_id})"
            expected_hash = self._compute_hash(entry.details, last_hash)
            if entry.current_hash != expected_hash:
                return False, f"Tampered content at entry {entry.entry_id}"
            last_hash = entry.current_hash
        return True, None


# =========================================================
# 3. CONSENT-BASED DATA USAGE ENFORCER
# =========================================================

@dataclass
class CandidateConsentRecord:
    candidate_id: str
    resume_parsing_consent: bool = False
    voice_recording_consent: bool = False
    video_proctoring_consent: bool = False
    ai_evaluation_consent: bool = False
    consent_timestamp: str = field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))


class ConsentGatekeeper:
    """Verifies candidate legal consent before any AI evaluation runs."""

    def __init__(self):
        self._consents: Dict[str, CandidateConsentRecord] = {}

    def record_consent(
        self,
        candidate_id: str,
        resume_parsing: bool = True,
        voice_recording: bool = True,
        video_proctoring: bool = True,
        ai_evaluation: bool = True,
    ) -> CandidateConsentRecord:
        record = CandidateConsentRecord(
            candidate_id=candidate_id,
            resume_parsing_consent=resume_parsing,
            voice_recording_consent=voice_recording,
            video_proctoring_consent=video_proctoring,
            ai_evaluation_consent=ai_evaluation,
        )
        self._consents[candidate_id] = record
        return record

    def verify_consent(self, candidate_id: str, stage: str) -> bool:
        """Ensures candidate granted mandatory consent for the given stage."""
        record = self._consents.get(candidate_id)
        if not record:
            return False

        if stage == "ats":
            return record.resume_parsing_consent
        elif stage in ("screening", "hr"):
            return record.voice_recording_consent and record.ai_evaluation_consent
        elif stage in ("technical", "machine_test"):
            return record.video_proctoring_consent and record.ai_evaluation_consent
        elif stage == "unified_decision":
            return record.ai_evaluation_consent
        return True


# =========================================================
# 4. PII SCRUBBER & SECURE STORAGE ENCRYPTION
# =========================================================

class PIIScrubber:
    """Anonymizes Personally Identifiable Information (PII) before storage."""

    EMAIL_PATTERN = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    PHONE_PATTERN = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    SSN_ID_PATTERN = r"\b\d{3}-\d{2}-\d{4}\b|\b\d{9,12}\b"

    @classmethod
    def sanitize_transcript(cls, text: str) -> str:
        """Redacts sensitive contact details, emails, and identifiers."""
        if not text:
            return ""
        clean = re.sub(cls.EMAIL_PATTERN, "[REDACTED_EMAIL]", text)
        clean = re.sub(cls.PHONE_PATTERN, "[REDACTED_PHONE]", clean)
        clean = re.sub(cls.SSN_ID_PATTERN, "[REDACTED_ID]", clean)
        return clean


# =========================================================
# 5. DATA RETENTION POLICY & ANONYMIZATION
# =========================================================

class DataRetentionPolicy:
    """Manages compliance retention periods and automated purging."""

    def __init__(self, retention_days: int = 180):
        self.retention_days = retention_days

    def is_expired(self, record_created_at: datetime) -> bool:
        """Checks if a record has exceeded legal retention duration."""
        cutoff = datetime.utcnow() - timedelta(days=self.retention_days)
        return record_created_at < cutoff

    def anonymize_candidate_record(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymizes demographic & personal data for historical bias telemetry without retaining PII."""
        anonymized = dict(candidate_data)
        anonymized["candidate_name"] = f"ANONYMIZED_CANDIDATE_{hashlib.md5(candidate_data.get('candidate_id', '').encode()).hexdigest()[:8]}"
        anonymized["email"] = "anonymized@gdpr.internal"
        anonymized["phone"] = "+0000000000"
        anonymized["anonymized_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        return anonymized
