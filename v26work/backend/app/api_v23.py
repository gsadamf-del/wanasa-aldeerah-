import os
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .db.session import get_db
from .models_v22 import DeadLetterEventV22, MetricSampleV22
from .models_v21 import OutboxEventV21
from .rbac import require_roles
from .services.operations_v22 import move_to_dead_letter
from .services.production_v23 import validate_production_settings
from .core.config import settings

router = APIRouter(prefix="/api/v23", tags=["v23"])

class WorkerRunIn(BaseModel):
    limit: int = Field(default=50, ge=1, le=200)

class DlqActionIn(BaseModel):
    action: str = Field(pattern="^(REQUEUE|RESOLVE)$")

@router.get("/health")
def health():
    return {"status":"ok","version":"23","service":"wanasa-aldeerah"}

@router.get("/readiness")
def readiness(db: Session = Depends(get_db)):
    from sqlalchemy import text
    db.execute(text("SELECT 1"))
    errors = validate_production_settings(settings)
    return {"ready": not errors, "database":"ok", "worker":"enabled", "rate_limit":"enabled", "configuration":"ok" if not errors else "invalid", "errors":errors, "version":"23"}

@router.get("/capabilities")
def capabilities():
    return {"version":"23","worker":"batch-processing","dead_letter":"requeue-resolve","observability":"structured-logs-prometheus-text-db-samples","rate_limiting":"in-process-edge-compatible","security":"production-secret-validation","migrations":"v22-to-v23"}

@router.get("/metrics/prometheus")
def prometheus_metrics(db: Session = Depends(get_db)):
    rows = db.query(MetricSampleV22).order_by(MetricSampleV22.created_at.desc()).limit(500).all()
    latest = {}
    for r in rows:
        latest.setdefault(r.metric, r.value)
    lines = ["# HELP wanasa_metric Last recorded application metric sample", "# TYPE wanasa_metric gauge"]
    for metric, value in sorted(latest.items()):
        safe = "".join(c if c.isalnum() or c == "_" else "_" for c in metric)
        lines.append(f"wanasa_metric{{metric=\"{safe}\"}} {value}")
    return "\n".join(lines) + "\n"

@router.post("/admin/worker/run")
def worker_run(payload: WorkerRunIn, db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    from .services.production_v23 import process_outbox_batch
    return process_outbox_batch(db, payload.limit)

@router.post("/admin/dead-letter/{event_id}")
def dead_letter_action(event_id: str, payload: DlqActionIn, db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    dlq = db.query(DeadLetterEventV22).filter_by(source_event_id=event_id, resolved=False).order_by(DeadLetterEventV22.id.desc()).first()
    if not dlq:
        raise HTTPException(404, "dead-letter event not found")
    row = db.query(OutboxEventV21).filter_by(event_id=event_id).first()
    if payload.action == "REQUEUE":
        if row:
            row.status = "PENDING"
            row.available_at = None
            row.last_error = None
        dlq.resolved = True
        db.commit()
        return {"status":"REQUEUED","event_id":event_id}
    dlq.resolved = True
    db.commit()
    return {"status":"RESOLVED","event_id":event_id}

@router.get("/admin/config-check")
def config_check(user=Depends(require_roles("admin"))):
    errors = validate_production_settings(settings)
    return {"environment":settings.environment,"valid":not errors,"errors":errors}
