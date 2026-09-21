import json
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy.orm import Session
from app.models_v21 import AuditEventV21, OutboxEventV21, SecurityEventV21

def audit(db: Session, action: str, entity_type: str, entity_id=None, *, actor_user_id=None,
          request_id=None, ip_address=None, metadata=None):
    row = AuditEventV21(actor_user_id=actor_user_id, action=action, entity_type=entity_type,
                        entity_id=entity_id, request_id=request_id, ip_address=ip_address,
                        metadata_json=json.dumps(metadata or {}, ensure_ascii=False))
    db.add(row)
    return row

def enqueue(db: Session, topic: str, aggregate_type: str, aggregate_id=None, payload=None,
            *, event_id=None):
    row = OutboxEventV21(event_id=event_id or str(uuid4()), topic=topic,
                         aggregate_type=aggregate_type, aggregate_id=aggregate_id,
                         payload_json=json.dumps(payload or {}, ensure_ascii=False))
    db.add(row)
    return row

def security_event(db: Session, event_type: str, detail=None, *, severity="INFO",
                   actor_user_id=None, request_id=None):
    row = SecurityEventV21(event_type=event_type, severity=severity, detail=detail,
                           actor_user_id=actor_user_id, request_id=request_id)
    db.add(row)
    return row

def claim_outbox(db: Session, limit=50):
    now = datetime.utcnow()
    rows = (db.query(OutboxEventV21)
            .filter(OutboxEventV21.status == "PENDING", OutboxEventV21.available_at <= now)
            .order_by(OutboxEventV21.id).limit(limit).all())
    for row in rows:
        row.status = "PROCESSING"
        row.attempts += 1
    db.commit()
    return rows

def fail_outbox(db: Session, row: OutboxEventV21, error: str):
    row.status = "PENDING"
    row.last_error = error[:4000]
    row.available_at = datetime.utcnow() + timedelta(seconds=min(300, 2 ** min(row.attempts, 8)))
    db.commit()

def complete_outbox(db: Session, row: OutboxEventV21):
    row.status = "PROCESSED"
    row.processed_at = datetime.utcnow()
    db.commit()
