from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, UniqueConstraint, Index
from app.db.session import Base

class AuditEventV21(Base):
    __tablename__ = "v21_audit_events"
    id = Column(Integer, primary_key=True)
    actor_user_id = Column(Integer, nullable=True, index=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=True, index=True)
    request_id = Column(String(64), nullable=True, index=True)
    ip_address = Column(String(64), nullable=True)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

class OutboxEventV21(Base):
    __tablename__ = "v21_outbox_events"
    id = Column(Integer, primary_key=True)
    event_id = Column(String(128), nullable=False, unique=True)
    topic = Column(String(128), nullable=False, index=True)
    aggregate_type = Column(String(100), nullable=False)
    aggregate_id = Column(Integer, nullable=True, index=True)
    payload_json = Column(Text, nullable=False)
    status = Column(String(24), nullable=False, default="PENDING", index=True)
    attempts = Column(Integer, nullable=False, default=0)
    available_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    processed_at = Column(DateTime, nullable=True)
    last_error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    __table_args__ = (Index("ix_v21_outbox_pending", "status", "available_at"),)

class ReconciliationRunV21(Base):
    __tablename__ = "v21_reconciliation_runs"
    id = Column(Integer, primary_key=True)
    run_key = Column(String(128), nullable=False, unique=True)
    scope = Column(String(64), nullable=False)
    status = Column(String(24), nullable=False, default="RUNNING")
    checked_count = Column(Integer, nullable=False, default=0)
    mismatch_count = Column(Integer, nullable=False, default=0)
    summary_json = Column(Text, nullable=False, default="{}")
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    finished_at = Column(DateTime, nullable=True)

class SecurityEventV21(Base):
    __tablename__ = "v21_security_events"
    id = Column(Integer, primary_key=True)
    event_type = Column(String(100), nullable=False, index=True)
    severity = Column(String(16), nullable=False, default="INFO")
    actor_user_id = Column(Integer, nullable=True, index=True)
    request_id = Column(String(64), nullable=True, index=True)
    detail = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
