import json
from datetime import datetime
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from .db.session import get_db
from .models import Order
from .models_v19 import Payment, PaymentEvent
from .models_v21 import OutboxEventV21, AuditEventV21, SecurityEventV21, ReconciliationRunV21
from .rbac import current_user, require_roles
from .services.operations_v21 import audit, enqueue, security_event, claim_outbox, complete_outbox, fail_outbox
from .services.operations_v22 import retry_or_dead_letter, record_metric

router = APIRouter(prefix="/api/v21", tags=["v21"])

class OutboxProcessIn(BaseModel):
    limit: int = Field(default=50, ge=1, le=200)

class ReconcileIn(BaseModel):
    run_key: str = Field(min_length=3, max_length=128)
    scope: str = Field(default="payments", min_length=3, max_length=64)

@router.get("/health")
def health():
    return {"status": "ok", "version": "21", "service": "wanasa-aldeerah"}

@router.get("/readiness")
def readiness(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"ready": True, "database": "ok", "version": "21", "outbox": "enabled"}

@router.get("/capabilities")
def capabilities():
    return {
        "version": "21",
        "operations": "audit-outbox-reconciliation-security-events",
        "observability": "request-id-security-headers",
        "payments": "idempotent-webhook-foundation",
        "inventory": "transactional-row-lock",
        "delivery": "location-foundation",
        "settlements": "commission-foundation",
    }

@router.get("/operations/summary")
def operations_summary(db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    pending = db.query(OutboxEventV21).filter(OutboxEventV21.status == "PENDING").count()
    processing = db.query(OutboxEventV21).filter(OutboxEventV21.status == "PROCESSING").count()
    security = db.query(SecurityEventV21).count()
    audits = db.query(AuditEventV21).count()
    return {"outbox_pending": pending, "outbox_processing": processing,
            "security_events": security, "audit_events": audits}

@router.post("/operations/outbox/process")
def process_outbox(payload: OutboxProcessIn, db: Session = Depends(get_db),
                   user=Depends(require_roles("admin"))):
    rows = claim_outbox(db, payload.limit)
    processed = 0
    # V21 deliberately stops at the durable outbox boundary. Actual delivery is delegated
    # to a worker/connector; claiming + completing here provides a deterministic foundation.
    for row in rows:
        try:
            json.loads(row.payload_json)
            complete_outbox(db, row)
            processed += 1
        except Exception as exc:
            retry_or_dead_letter(db, row, str(exc))
    audit(db, "OUTBOX_BATCH_PROCESSED", "outbox", None, actor_user_id=user.id,
          metadata={"claimed": len(rows), "processed": processed})
    record_metric(db, "outbox_processed", processed)
    record_metric(db, "outbox_claimed", len(rows))
    db.commit()
    return {"claimed": len(rows), "processed": processed}

@router.post("/admin/reconciliation/payments")
def reconcile_payments(payload: ReconcileIn, db: Session = Depends(get_db),
                       user=Depends(require_roles("admin"))):
    existing = db.query(ReconciliationRunV21).filter_by(run_key=payload.run_key).first()
    if existing:
        return {"id": existing.id, "run_key": existing.run_key, "status": existing.status,
                "checked_count": existing.checked_count, "mismatch_count": existing.mismatch_count}
    run = ReconciliationRunV21(run_key=payload.run_key, scope=payload.scope, status="RUNNING")
    db.add(run); db.flush()
    payments = db.query(Payment).all()
    mismatches = 0
    for payment in payments:
        if payment.status not in {"SUCCEEDED", "FAILED", "PENDING"}:
            mismatches += 1
    run.checked_count = len(payments)
    run.mismatch_count = mismatches
    run.status = "COMPLETED"
    run.finished_at = datetime.utcnow()
    run.summary_json = json.dumps({"scope": payload.scope, "mismatch_count": mismatches})
    audit(db, "PAYMENT_RECONCILIATION", "reconciliation", run.id, actor_user_id=user.id,
          metadata={"checked": len(payments), "mismatches": mismatches})
    db.commit()
    return {"id": run.id, "run_key": run.run_key, "status": run.status,
            "checked_count": run.checked_count, "mismatch_count": run.mismatch_count}

@router.get("/admin/reconciliation/{run_id}")
def get_reconciliation(run_id: int, db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    run = db.get(ReconciliationRunV21, run_id)
    if not run: raise HTTPException(404, "reconciliation run not found")
    return {"id": run.id, "run_key": run.run_key, "scope": run.scope, "status": run.status,
            "checked_count": run.checked_count, "mismatch_count": run.mismatch_count,
            "started_at": run.started_at.isoformat(),
            "finished_at": run.finished_at.isoformat() if run.finished_at else None}

@router.get("/admin/audit")
def audit_feed(limit: int = 100, db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    limit = min(max(limit, 1), 200)
    rows = db.query(AuditEventV21).order_by(AuditEventV21.created_at.desc()).limit(limit).all()
    return [{"id": r.id, "action": r.action, "entity_type": r.entity_type,
             "entity_id": r.entity_id, "actor_user_id": r.actor_user_id,
             "request_id": r.request_id, "created_at": r.created_at.isoformat()} for r in rows]

@router.get("/admin/security-events")
def security_feed(limit: int = 100, db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    limit = min(max(limit, 1), 200)
    rows = db.query(SecurityEventV21).order_by(SecurityEventV21.created_at.desc()).limit(limit).all()
    return [{"id": r.id, "event_type": r.event_type, "severity": r.severity,
             "actor_user_id": r.actor_user_id, "request_id": r.request_id,
             "detail": r.detail, "created_at": r.created_at.isoformat()} for r in rows]
