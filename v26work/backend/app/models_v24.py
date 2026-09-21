from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, UniqueConstraint
from .db.session import Base


class SchemaMigrationV24(Base):
    __tablename__ = "v24_schema_migrations"
    id = Column(Integer, primary_key=True)
    revision = Column(String(64), nullable=False, unique=True)
    applied_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    checksum = Column(String(128), nullable=False)
    notes = Column(Text, nullable=True)
    __table_args__ = (UniqueConstraint("revision", name="uq_v24_schema_revision"),)


class MigrationPreflightV24(Base):
    __tablename__ = "v24_migration_preflights"
    id = Column(Integer, primary_key=True)
    run_key = Column(String(128), nullable=False, unique=True)
    status = Column(String(24), nullable=False, default="PENDING")
    checked_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    detail = Column(Text, nullable=True)
    passed = Column(Boolean, nullable=False, default=False)
