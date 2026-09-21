from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .models import Product, Order, OrderItem, User
from .db.session import get_db
from .rbac import current_user
from .services.commerce import can_transition
from .services.notifications import build_notification

router = APIRouter(prefix="/api/v18", tags=["v18"])

class OrderCreate(BaseModel):
    product_id: int
    quantity: int
    delivery_fee: float = 0

class OrderStatusUpdate(BaseModel):
    status: str

@router.get("/commerce/status")
def status():
    return {"version": "18", "commerce": "ready", "notifications": "foundation"}

@router.post("/orders")
def create_order(payload: OrderCreate, db: Session = Depends(get_db),
                 user: User = Depends(current_user)):
    if payload.quantity <= 0:
        raise HTTPException(400, "quantity must be positive")
    product = db.get(Product, payload.product_id)
    if not product:
        raise HTTPException(404, "product not found")
    stock = int(product.stock or 0)
    if stock < payload.quantity:
        raise HTTPException(409, "insufficient stock")
    price = float(product.price or 0)
    subtotal = price * payload.quantity
    vat = round(subtotal * 0.15, 2)
    total = round(subtotal + vat + payload.delivery_fee, 2)
    product.stock = stock - payload.quantity
    order = Order(customer_id=user.id, status="PENDING", subtotal=subtotal,
                  vat=vat, delivery_fee=payload.delivery_fee, total=total)
    db.add(order); db.flush()
    db.add(OrderItem(order_id=order.id, product_id=product.id,
                     quantity=payload.quantity, unit_price=price))
    db.commit(); db.refresh(order)
    return {"id": order.id, "status": order.status, "subtotal": subtotal,
            "vat": vat, "delivery_fee": payload.delivery_fee, "total": total}

@router.patch("/orders/{order_id}/status")
def update_status(order_id: int, payload: OrderStatusUpdate,
                  db: Session = Depends(get_db),
                  user: User = Depends(current_user)):
    order = db.get(Order, order_id)
    if not order: raise HTTPException(404, "order not found")
    target = payload.status.upper()
    if not can_transition(order.status, target):
        raise HTTPException(409, f"invalid transition: {order.status} -> {target}")
    order.status = target; db.commit()
    n = build_notification(order.customer_id, "تحديث الطلب",
                           f"تم تحديث حالة الطلب إلى {target}",
                           "ORDER_STATUS_CHANGED")
    return {"order_id": order.id, "status": order.status,
            "notification": {"title": n.title, "body": n.body, "event": n.event}}

@router.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db),
              user: User = Depends(current_user)):
    order = db.get(Order, order_id)
    if not order: raise HTTPException(404, "order not found")
    return {"id": order.id, "status": order.status, "subtotal": order.subtotal,
            "vat": order.vat, "delivery_fee": order.delivery_fee, "total": order.total}

@router.get("/admin/control")
def admin_control(db: Session = Depends(get_db), user=Depends(current_user)):
    if getattr(user, "role", "") != "admin":
        raise HTTPException(403, "admin only")
    return {"orders": db.query(Order).count(),
            "products": db.query(Product).count(),
            "users": db.query(User).count(),
            "module": "v18-control-center"}
