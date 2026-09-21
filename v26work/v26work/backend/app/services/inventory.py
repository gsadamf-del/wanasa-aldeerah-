from sqlalchemy import select
from sqlalchemy.orm import Session

def reserve_product(db: Session, product, quantity: int):
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    stock = int(getattr(product, "stock", 0) or 0)
    if stock < quantity:
        raise ValueError("insufficient stock")
    product.stock = stock - quantity
    return product.stock

def release_product(product, quantity: int):
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    product.stock = int(getattr(product, "stock", 0) or 0) + quantity
    return product.stock
