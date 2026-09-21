import os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .db.session import get_db
from .models_v21 import OutboxEventV21
from .models_v22 import DeadLetterEventV22, BackupDrillV22, MetricSampleV22
from .rbac import require_roles
from .services.operations_v22 import record_metric, move_to_dead_letter

router = APIRouter(prefix="/api/v22", tags=["v22"])

class BackupDrillIn(BaseModel):
    drill_key: str = Field(min_length=3, max_length=128)
    status: str = Field(default="VERIFIED", pattern="^(PLANNED|RUNNING|VERIFIED|FAILED)$")
    notes: str | None = Field(default=None, max_length=4000)

@router.get("/health")
def health():
    return {"status":"ok","version":"22","service":"wanasa-aldeerah"}

@router.get("/readiness")
def readiness(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"ready":True,"database":"ok","outbox":"enabled","dead_letter":"enabled","version":"22"}

@router.get("/capabilities")
def capabilities():
    return {"version":"22","observability":"metrics-request-id-security-headers","rate_limiting":"edge-ready-foundation",
            "outbox":"retry-dead-letter","operations":"backup-drill-readiness","security":"secret-validation-foundation"}

@router.get("/metrics")
def metrics(db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    rows = db.query(MetricSampleV22).order_by(MetricSampleV22.created_at.desc()).limit(200).all()
    return [{"metric":r.metric,"value":r.value,"bucket":r.bucket} for r in rows]

@router.get("/admin/dead-letter")
def dead_letter(limit: int = 100, db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    limit = min(max(limit,1),200)
    rows = db.query(DeadLetterEventV22).filter_by(resolved=False).order_by(DeadLetterEventV22.created_at.desc()).limit(limit).all()
    return [{"id":r.id,"source_event_id":r.source_event_id,"topic":r.topic,"attempts":r.attempts,
             "error":r.error,"created_at":r.created_at.isoformat()} for r in rows]

@router.post("/admin/outbox/{event_id}/dead-letter")
def dead_letter_event(event_id: str, db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    row = db.query(OutboxEventV21).filter_by(event_id=event_id).first()
    if not row: raise HTTPException(404,"outbox event not found")
    if row.status == "DEAD_LETTER": return {"status":"DEAD_LETTER","event_id":event_id}
    move_to_dead_letter(db,row,row.last_error or "manual dead-letter")
    db.commit()
    record_metric(db,"outbox_dead_lettered",1); db.commit()
    return {"status":"DEAD_LETTER","event_id":event_id}

@router.post("/admin/backup-drills")
def backup_drill(payload: BackupDrillIn, db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    row = db.query(BackupDrillV22).filter_by(drill_key=payload.drill_key).first()
    if not row:
        row=BackupDrillV22(drill_key=payload.drill_key); db.add(row)
    row.status=payload.status; row.notes=payload.notes
    row.verified_at=datetime.utcnow() if payload.status=="VERIFIED" else None
    db.commit()
    return {"id":row.id,"drill_key":row.drill_key,"status":row.status,"verified_at":row.verified_at.isoformat() if row.verified_at else None}
