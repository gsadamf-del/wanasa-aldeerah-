from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User, Merchant, Product, Offer, PlatformSetting, Banner, Order, OrderItem, AuditLog
from app.security import hash_password, verify_password, create_token
from app.rbac import current_user, require_roles
from app.services.expiry import sellable

router = APIRouter(prefix="/api/v1")

class RegisterIn(BaseModel):
    name: str
    phone: str
    password: str
    role: str = "customer"

class LoginIn(BaseModel):
    phone: str
    password: str

class ProductIn(BaseModel):
    name: str
    category: str | None = None
    description: str | None = None
    price: Decimal = Field(ge=0)
    stock: int = Field(ge=0)
    expiry_date: str | None = None
    merchant_id: int | None = None

class OfferIn(BaseModel):
    product_id: int
    title: str
    discount_percent: Decimal = Field(ge=0, le=100)
    is_active: bool = True

class SettingIn(BaseModel):
    key: str
    value: str | None = None

class BannerIn(BaseModel):
    title: str
    image_url: str | None = None
    link_url: str | None = None
    is_active: bool = True
    sort_order: int = 0

class OrderIn(BaseModel):
    items: list[dict]
    delivery_fee: Decimal = Field(default=0, ge=0)

@router.get("/health")
def health():
    return {"status": "ok", "version": "v17"}

@router.post("/auth/register")
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if data.role not in {"customer", "merchant"}:
        raise HTTPException(400, "Invalid public role")
    if db.query(User).filter(User.phone == data.phone).first():
        raise HTTPException(409, "Phone already registered")
    user = User(name=data.name, phone=data.phone, password_hash=hash_password(data.password), role=data.role)
    db.add(user); db.commit(); db.refresh(user)
    if data.role == "merchant":
        db.add(Merchant(user_id=user.id, name=data.name, status="pending")); db.commit()
    return {"access_token": create_token(user.id, user.role), "role": user.role}

@router.post("/auth/login")
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == data.phone).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": create_token(user.id, user.role), "role": user.role}

@router.get("/me")
def me(user=Depends(current_user)):
    return {"id": user.id, "name": user.name, "phone": user.phone, "role": user.role}

@router.get("/products")
def products(db: Session = Depends(get_db)):
    rows = db.query(Product).filter(Product.is_active == True).all()
    return [{"id": p.id, "name": p.name, "category": p.category, "price": str(p.price), "stock": p.stock, "expiry_date": str(p.expiry_date) if p.expiry_date else None} for p in rows if sellable(p.expiry_date)]

@router.post("/admin/products")
def create_product(data: ProductIn, db: Session = Depends(get_db), user=Depends(require_roles("admin","merchant"))):
    expiry = datetime.strptime(data.expiry_date, "%Y-%m-%d").date() if data.expiry_date else None
    p = Product(name=data.name, category=data.category, description=data.description, price=data.price, stock=data.stock, expiry_date=expiry, merchant_id=data.merchant_id)
    db.add(p); db.commit(); db.refresh(p)
    return {"id": p.id, "name": p.name}

@router.post("/admin/offers")
def create_offer(data: OfferIn, db: Session = Depends(get_db), user=Depends(require_roles("admin","merchant"))):
    if not db.get(Product, data.product_id):
        raise HTTPException(404, "Product not found")
    offer = Offer(**data.model_dump())
    db.add(offer); db.commit(); db.refresh(offer)
    return {"id": offer.id}

@router.get("/offers")
def offers(db: Session = Depends(get_db)):
    rows = db.query(Offer).filter(Offer.is_active == True).all()
    return [{"id": x.id, "product_id": x.product_id, "title": x.title, "discount_percent": str(x.discount_percent)} for x in rows]

@router.post("/admin/settings")
def set_setting(data: SettingIn, db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    row = db.query(PlatformSetting).filter(PlatformSetting.key == data.key).first()
    if not row:
        row = PlatformSetting(key=data.key)
        db.add(row)
    row.value = data.value
    db.commit()
    return {"key": row.key, "value": row.value}

@router.get("/settings/public")
def public_settings(db: Session = Depends(get_db)):
    return [{"key": x.key, "value": x.value} for x in db.query(PlatformSetting).all()]

@router.post("/admin/banners")
def create_banner(data: BannerIn, db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    b = Banner(**data.model_dump())
    db.add(b); db.commit(); db.refresh(b)
    return {"id": b.id}

@router.get("/banners")
def banners(db: Session = Depends(get_db)):
    rows = db.query(Banner).filter(Banner.is_active == True).order_by(Banner.sort_order).all()
    return [{"id": x.id, "title": x.title, "image_url": x.image_url, "link_url": x.link_url} for x in rows]

@router.get("/admin/overview")
def overview(db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    return {
        "users": db.query(User).count(),
        "merchants": db.query(Merchant).count(),
        "products": db.query(Product).count(),
        "offers": db.query(Offer).count(),
        "orders": db.query(Order).count(),
    }
