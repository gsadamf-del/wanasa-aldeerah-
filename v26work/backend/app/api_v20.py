import json
from decimal import Decimal, ROUND_HALF_UP
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from pydantic import BaseModel, Field
from sqlalchemy import text, select
from sqlalchemy.orm import Session

from .db.session import get_db
from .models import Product, Order, OrderItem, User, Merchant
from .models_v19 import Payment, PaymentEvent, DeviceToken, Notification, MediaAsset
from .models_v20 import IdempotencyKey, PaymentWebhook, DeliveryLocation, SettlementEntry
from .rbac import current_user, require_roles
from .core.config import settings
from .services.inventory_v20 import reserve_stock
from .services.payments_v20 import verify_signature, MockPaymentProviderV20

router = APIRouter(prefix="/api/v20", tags=["v20"])

class OrderItemIn(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderCreateV20(BaseModel):
    items: list[OrderItemIn] = Field(min_length=1)
    delivery_fee: Decimal = Field(default=Decimal("0"), ge=0)

class DeviceTokenIn(BaseModel):
    token: str = Field(min_length=10, max_length=512)
    platform: str = Field(pattern="^(android|ios|web)$")

class ReadIn(BaseModel):
    read: bool = True

class PaymentCreateIn(BaseModel):
    order_id: int
    provider: str = "mock"

class MediaIn(BaseModel):
    owner_type: str
    owner_id: int
    url: str = Field(min_length=1, max_length=1024)
    kind: str = "image"

class LocationIn(BaseModel):
    latitude: Decimal = Field(ge=Decimal("-90"), le=Decimal("90"))
    longitude: Decimal = Field(ge=Decimal("-180"), le=Decimal("180"))

class SettlementRunIn(BaseModel):
    commission_percent: Decimal | None = Field(default=None, ge=0, le=100)

def _idem(db, user_id, key, endpoint):
    return db.query(IdempotencyKey).filter_by(user_id=user_id, key=key, endpoint=endpoint).first()

@router.get("/health")
def health():
    return {"status": "ok", "version": "20", "service": "wanasa-aldeerah"}

@router.get("/readiness")
def readiness(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"ready": True, "database": "ok", "version": "20"}

@router.get("/capabilities")
def capabilities():
    return {
        "version": "20",
        "inventory": "transactional-row-lock",
        "idempotency": "enabled",
        "payments": "provider-adapter-webhook-verification",
        "notifications": "device-token-inbox-foundation",
        "media": "asset-registry",
        "delivery_tracking": "location-stream-foundation",
        "settlements": "commission-foundation",
    }

@router.post("/orders")
def create_order(payload: OrderCreateV20, request: Request,
                 db: Session = Depends(get_db), user=Depends(current_user),
                 idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")):
    endpoint = "POST:/api/v20/orders"
    if not idempotency_key:
        raise HTTPException(400, "Idempotency-Key header is required")
    old = _idem(db, user.id, idempotency_key, endpoint)
    if old:
        return json.loads(old.response_json)

    try:
        subtotal = Decimal("0")
        order = Order(customer_id=user.id, status="PENDING", subtotal=0, vat=0,
                      delivery_fee=payload.delivery_fee, total=0)
        db.add(order); db.flush()
        for item in payload.items:
            product = db.get(Product, item.product_id)
            if not product:
                raise HTTPException(404, f"product {item.product_id} not found")
            reserve_stock(db, product.id, item.quantity, order.id,
                          f"{user.id}:{idempotency_key}:{product.id}")
            price = Decimal(product.price or 0)
            subtotal += price * item.quantity
            db.add(OrderItem(order_id=order.id, product_id=product.id,
                             quantity=item.quantity, unit_price=price))
        vat = (subtotal * Decimal("0.15")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total = subtotal + vat + payload.delivery_fee
        order.subtotal, order.vat, order.total = subtotal, vat, total
        db.commit(); db.refresh(order)
        result = {"id": order.id, "status": order.status, "subtotal": str(subtotal),
                  "vat": str(vat), "delivery_fee": str(payload.delivery_fee), "total": str(total)}
        db.add(IdempotencyKey(user_id=user.id, key=idempotency_key, endpoint=endpoint,
                              response_json=json.dumps(result), status_code=200))
        db.commit()
        return result
    except HTTPException:
        db.rollback(); raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(500, f"order transaction failed: {type(exc).__name__}")

@router.post("/payments")
def create_payment(payload: PaymentCreateIn, db: Session = Depends(get_db), user=Depends(current_user)):
    order = db.get(Order, payload.order_id)
    if not order or order.customer_id != user.id:
        raise HTTPException(404, "order not found")
    provider = MockPaymentProviderV20()
    result = provider.create_payment(float(order.total), "SAR", order.id)
    payment = Payment(order_id=order.id, amount=order.total, currency="SAR",
                      provider=result.provider, status="SUCCEEDED" if result.success else "FAILED",
                      reference=result.reference)
    db.add(payment); db.flush()
    db.add(PaymentEvent(payment_id=payment.id, event_type="PAYMENT_CREATED",
                        payload=json.dumps({"reference": result.reference})))
    db.commit()
    return {"payment_id": payment.id, "status": payment.status, "reference": payment.reference}

@router.post("/payments/webhook/{provider}")
async def payment_webhook(provider: str, request: Request,
                          x_signature: str | None = Header(default=None),
                          x_event_id: str | None = Header(default=None)):
    raw = await request.body()
    if not x_signature or not x_event_id:
        raise HTTPException(400, "X-Signature and X-Event-Id are required")
    valid = verify_signature(settings.payment_webhook_secret, raw, x_signature)
    db = next(get_db())
    try:
        if db.query(PaymentWebhook).filter_by(event_id=x_event_id).first():
            return {"accepted": True, "duplicate": True}
        db.add(PaymentWebhook(provider=provider, event_id=x_event_id,
                              signature_valid=valid, payload=raw.decode("utf-8", errors="replace")))
        db.commit()
        if not valid:
            raise HTTPException(401, "invalid webhook signature")
        return {"accepted": True, "duplicate": False}
    finally:
        db.close()

@router.post("/devices")
def register_device(payload: DeviceTokenIn, db: Session = Depends(get_db), user=Depends(current_user)):
    row = db.query(DeviceToken).filter_by(token=payload.token).first()
    if row:
        row.user_id, row.platform, row.active = user.id, payload.platform, True
    else:
        row = DeviceToken(user_id=user.id, token=payload.token, platform=payload.platform, active=True)
        db.add(row)
    db.commit()
    return {"id": row.id, "active": row.active}

@router.get("/notifications")
def notifications(db: Session = Depends(get_db), user=Depends(current_user)):
    rows = db.query(Notification).filter_by(user_id=user.id).order_by(Notification.created_at.desc()).limit(100).all()
    return [{"id": n.id, "title": n.title, "body": n.body, "event": n.event, "read": n.read,
             "created_at": n.created_at.isoformat()} for n in rows]

@router.patch("/notifications/{notification_id}")
def mark_notification(notification_id: int, payload: ReadIn, db: Session = Depends(get_db), user=Depends(current_user)):
    n = db.get(Notification, notification_id)
    if not n or n.user_id != user.id: raise HTTPException(404, "notification not found")
    n.read = payload.read; db.commit()
    return {"id": n.id, "read": n.read}

@router.post("/media")
def register_media(payload: MediaIn, db: Session = Depends(get_db), user=Depends(require_roles("admin","merchant"))):
    asset = MediaAsset(**payload.model_dump())
    db.add(asset); db.commit(); db.refresh(asset)
    return {"id": asset.id, "url": asset.url, "kind": asset.kind}

@router.post("/orders/{order_id}/location")
def update_location(order_id: int, payload: LocationIn, db: Session = Depends(get_db), user=Depends(require_roles("admin","merchant"))):
    order = db.get(Order, order_id)
    if not order: raise HTTPException(404, "order not found")
    row = DeliveryLocation(order_id=order_id, courier_user_id=user.id,
                           latitude=payload.latitude, longitude=payload.longitude)
    db.add(row); db.commit()
    return {"id": row.id, "order_id": order_id, "latitude": str(row.latitude), "longitude": str(row.longitude)}

@router.get("/orders/{order_id}/location")
def latest_location(order_id: int, db: Session = Depends(get_db), user=Depends(current_user)):
    row = db.query(DeliveryLocation).filter_by(order_id=order_id).order_by(DeliveryLocation.recorded_at.desc()).first()
    if not row: raise HTTPException(404, "location not found")
    return {"order_id": order_id, "latitude": str(row.latitude), "longitude": str(row.longitude),
            "recorded_at": row.recorded_at.isoformat()}

@router.post("/admin/settlements/run")
def run_settlements(payload: SettlementRunIn, db: Session = Depends(get_db),
                    user=Depends(require_roles("admin"))):
    pct = payload.commission_percent if payload.commission_percent is not None else Decimal(str(settings.platform_commission_percent))
    orders = db.query(Order).filter(Order.status.in_(["DELIVERED", "COMPLETED"])).all()
    created = 0
    for order in orders:
        items = db.query(OrderItem).filter_by(order_id=order.id).all()
        merchant_ids = {db.get(Product, i.product_id).merchant_id for i in items if db.get(Product, i.product_id)}
        for merchant_id in merchant_ids:
            if merchant_id is None: continue
            gross = Decimal(order.subtotal or 0)
            commission = (gross * pct / Decimal("100")).quantize(Decimal("0.01"))
            if db.query(SettlementEntry).filter_by(order_id=order.id, merchant_id=merchant_id).first():
                continue
            db.add(SettlementEntry(merchant_id=merchant_id, order_id=order.id,
                                   gross_amount=gross, commission_amount=commission,
                                   net_amount=gross-commission, status="PENDING"))
            created += 1
    db.commit()
    return {"created": created, "commission_percent": str(pct)}
