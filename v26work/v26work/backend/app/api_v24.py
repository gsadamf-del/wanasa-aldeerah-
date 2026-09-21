from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from .db.session import get_db
from .rbac import require_roles
from .core.config import settings

router = APIRouter(prefix="/api/v24", tags=["v24"])

EXPECTED_REVISION = "v24"


def migration_status(db: Session):
    if settings.environment.lower() not in {"production", "prod"}:
        return {"required_revision": EXPECTED_REVISION, "applied": True, "mode": "non-production"}
    try:
        row = db.execute(text("SELECT revision FROM v24_schema_migrations WHERE revision = :r"), {"r": EXPECTED_REVISION}).first()
        return {"required_revision": EXPECTED_REVISION, "applied": row is not None, "mode": "postgres-migration-gated"}
    except Exception as exc:
        db.rollback()
        return {"required_revision": EXPECTED_REVISION, "applied": False, "mode": "postgres-migration-gated", "error": type(exc).__name__}


@router.get("/health")
def health():
    return {"status": "ok", "service": "wanasa-aldeerah", "version": "24"}


@router.get("/readiness")
def readiness(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    migration = migration_status(db)
    return {
        "ready": bool(migration["applied"]),
        "database": "ok",
        "migration": migration,
        "version": "24",
    }


@router.get("/capabilities")
def capabilities():
    return {
        "version": "24",
        "release": "final-pre-postgresql-migration",
        "postgresql": "migration-gated",
        "migration_revision": EXPECTED_REVISION,
        "production_create_all": False,
        "outbox_worker": True,
        "dead_letter": True,
        "rate_limiting": True,
        "structured_logging": True,
    }


@router.get("/admin/migration-status")
def admin_migration_status(db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    return migration_status(db)
