from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from .db.session import Base

class ExternalProviderHealthV25(Base):
    __tablename__ = 'v25_external_provider_health'
    id = Column(Integer, primary_key=True)
    provider = Column(String(64), nullable=False, unique=True)
    status = Column(String(24), nullable=False, default='UNKNOWN')
    latency_ms = Column(Float, nullable=True)
    checked_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    detail = Column(Text, nullable=True)

class RestoreDrillV25(Base):
    __tablename__ = 'v25_restore_drills'
    id = Column(Integer, primary_key=True)
    drill_key = Column(String(128), nullable=False, unique=True)
    source_backup = Column(String(512), nullable=False)
    target_database = Column(String(256), nullable=False)
    status = Column(String(32), nullable=False, default='PLANNED')
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    verified = Column(Boolean, nullable=False, default=False)
    notes = Column(Text, nullable=True)

class MonitoringEventV25(Base):
    __tablename__ = 'v25_monitoring_events'
    id = Column(Integer, primary_key=True)
    event_type = Column(String(64), nullable=False)
    severity = Column(String(24), nullable=False, default='INFO')
    message = Column(Text, nullable=False)
    external_id = Column(String(128), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
