from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date, Boolean, ForeignKey, Text

from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False, default="customer")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Merchant(Base):
    __tablename__ = "merchants"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String(200), nullable=False)
    status = Column(String(30), nullable=False, default="pending")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=True)
    name = Column(String(250), nullable=False)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(12,2), nullable=False, default=0)
    stock = Column(Integer, nullable=False, default=0)
    expiry_date = Column(Date, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

class Offer(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    title = Column(String(250), nullable=False)
    discount_percent = Column(Numeric(5,2), nullable=False, default=0)
    start_at = Column(DateTime, nullable=True)
    end_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(40), nullable=False, default="pending")
    subtotal = Column(Numeric(12,2), nullable=False, default=0)
    vat = Column(Numeric(12,2), nullable=False, default=0)
    delivery_fee = Column(Numeric(12,2), nullable=False, default=0)
    total = Column(Numeric(12,2), nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12,2), nullable=False)

class PlatformSetting(Base):
    __tablename__ = "platform_settings"
    id = Column(Integer, primary_key=True)
    key = Column(String(150), unique=True, nullable=False)
    value = Column(Text, nullable=True)

class Banner(Base):
    __tablename__ = "banners"
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    image_url = Column(String(500), nullable=True)
    link_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    sort_order = Column(Integer, nullable=False, default=0)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    actor_user_id = Column(Integer, nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
