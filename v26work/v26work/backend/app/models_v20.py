from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric, Text, ForeignKey, UniqueConstraint
from app.db.session import Base

class InventoryEvent(Base):
    __tablename__ = "v20_inventory_events"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True, index=True)
    event_type = Column(String(32), nullable=False)  # RESERVE/RELEASE/ADJUST
    quantity = Column(Integer, nullable=False)
    balance_after = Column(Integer, nullable=False)
    idempotency_key = Column(String(128), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class IdempotencyKey(Base):
    __tablename__ = "v20_idempotency_keys"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    key = Column(String(128), nullable=False)
    endpoint = Column(String(160), nullable=False)
    response_json = Column(Text, nullable=False)
    status_code = Column(Integer, nullable=False, default=200)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    __table_args__ = (UniqueConstraint("user_id", "key", "endpoint", name="uq_v20_idempotency"),)

class PaymentWebhook(Base):
    __tablename__ = "v20_payment_webhooks"
    id = Column(Integer, primary_key=True)
    provider = Column(String(64), nullable=False)
    event_id = Column(String(128), nullable=False, unique=True)
    signature_valid = Column(Boolean, nullable=False)
    payload = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class DeliveryLocation(Base):
    __tablename__ = "v20_delivery_locations"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    courier_user_id = Column(Integer, nullable=False, index=True)
    latitude = Column(Numeric(10, 7), nullable=False)
    longitude = Column(Numeric(10, 7), nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class SettlementEntry(Base):
    __tablename__ = "v20_settlement_entries"
    id = Column(Integer, primary_key=True)
    merchant_id = Column(Integer, nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    gross_amount = Column(Numeric(12,2), nullable=False)
    commission_amount = Column(Numeric(12,2), nullable=False)
    net_amount = Column(Numeric(12,2), nullable=False)
    status = Column(String(24), nullable=False, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
