from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, UniqueConstraint, Index
from app.db.session import Base

class RateLimitBucketV22(Base):
    __tablename__ = "v22_rate_limit_buckets"
    id = Column(Integer, primary_key=True)
    bucket_key = Column(String(255), nullable=False, unique=True)
    window_started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    request_count = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class DeadLetterEventV22(Base):
    __tablename__ = "v22_dead_letter_events"
    id = Column(Integer, primary_key=True)
    source_event_id = Column(String(128), nullable=False, index=True)
    topic = Column(String(128), nullable=False, index=True)
    payload_json = Column(Text, nullable=False)
    attempts = Column(Integer, nullable=False, default=0)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    resolved = Column(Boolean, nullable=False, default=False, index=True)

class MetricSampleV22(Base):
    __tablename__ = "v22_metric_samples"
    id = Column(Integer, primary_key=True)
    metric = Column(String(100), nullable=False, index=True)
    value = Column(Integer, nullable=False, default=0)
    bucket = Column(String(64), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    __table_args__ = (UniqueConstraint("metric", "bucket", name="uq_v22_metric_bucket"),)

class BackupDrillV22(Base):
    __tablename__ = "v22_backup_drills"
    id = Column(Integer, primary_key=True)
    drill_key = Column(String(128), nullable=False, unique=True)
    status = Column(String(24), nullable=False, default="PLANNED")
    verified_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
