from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from .db.session import Base

class Payment(Base):
    __tablename__ = "v19_payments"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(8), default="SAR")
    provider = Column(String(64), nullable=False)
    status = Column(String(32), default="PENDING")
    reference = Column(String(128))
    created_at = Column(DateTime, default=datetime.utcnow)

class PaymentEvent(Base):
    __tablename__ = "v19_payment_events"
    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, nullable=False, index=True)
    event_type = Column(String(64), nullable=False)
    payload = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class DeviceToken(Base):
    __tablename__ = "v19_device_tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    token = Column(String(512), nullable=False, unique=True)
    platform = Column(String(16), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class MediaAsset(Base):
    __tablename__ = "v19_media_assets"
    id = Column(Integer, primary_key=True)
    owner_type = Column(String(32), nullable=False)
    owner_id = Column(Integer, nullable=False, index=True)
    url = Column(String(1024), nullable=False)
    kind = Column(String(32), default="image")
    created_at = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "v19_notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    body = Column(String(1000), nullable=False)
    event = Column(String(64), nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
