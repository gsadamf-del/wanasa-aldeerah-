from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from .db.session import get_db

router = APIRouter(prefix="/api/v19", tags=["v19"])

@router.get("/health")
def health():
    return {"status": "ok", "version": "19"}

@router.get("/readiness")
def readiness(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"ready": True, "database": "ok"}

@router.get("/capabilities")
def capabilities():
    return {
        "inventory_transactions": "foundation",
        "payments": "adapter",
        "push_notifications": "adapter",
        "media_assets": "foundation",
        "audit": "foundation",
    }
