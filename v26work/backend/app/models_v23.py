from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from .db.session import Base

class WorkerHeartbeatV23(Base):
    __tablename__ = "v23_worker_heartbeats"
    id = Column(Integer, primary_key=True)
    worker_name = Column(String(128), unique=True, nullable=False)
    status = Column(String(32), nullable=False, default="STARTING")
    last_seen_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    detail = Column(Text, nullable=True)

class OperationalIncidentV23(Base):
    __tablename__ = "v23_operational_incidents"
    id = Column(Integer, primary_key=True)
    incident_key = Column(String(128), unique=True, nullable=False)
    severity = Column(String(32), nullable=False, default="INFO")
    status = Column(String(32), nullable=False, default="OPEN")
    detail = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    resolved = Column(Boolean, default=False, nullable=False)
