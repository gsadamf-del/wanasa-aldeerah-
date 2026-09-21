from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Product
from app.models_v20 import InventoryEvent

def reserve_stock(db: Session, product_id: int, quantity: int, order_id: int | None = None, idempotency_key: str | None = None):
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    stmt = select(Product).where(Product.id == product_id).with_for_update()
    product = db.execute(stmt).scalar_one_or_none()
    if not product:
        raise LookupError("product not found")
    if product.stock < quantity:
        raise ValueError("insufficient stock")
    product.stock -= quantity
    db.add(InventoryEvent(product_id=product_id, order_id=order_id, event_type="RESERVE",
                          quantity=quantity, balance_after=product.stock,
                          idempotency_key=idempotency_key))
    return product

def release_stock(db: Session, product_id: int, quantity: int, order_id: int | None = None):
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    stmt = select(Product).where(Product.id == product_id).with_for_update()
    product = db.execute(stmt).scalar_one_or_none()
    if not product:
        raise LookupError("product not found")
    product.stock += quantity
    db.add(InventoryEvent(product_id=product_id, order_id=order_id, event_type="RELEASE",
                          quantity=quantity, balance_after=product.stock))
    return product
