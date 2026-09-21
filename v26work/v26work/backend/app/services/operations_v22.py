from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models_v21 import OutboxEventV21
from app.models_v22 import DeadLetterEventV22, MetricSampleV22

def record_metric(db: Session, metric: str, value: int = 1, bucket: str | None = None):
    bucket = bucket or datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
    row = db.query(MetricSampleV22).filter_by(metric=metric, bucket=bucket).first()
    if row:
        row.value += value
    else:
        row = MetricSampleV22(metric=metric, value=value, bucket=bucket)
        db.add(row)
        db.flush()
    return row

def move_to_dead_letter(db: Session, row: OutboxEventV21, error: str):
    dlq = DeadLetterEventV22(source_event_id=row.event_id, topic=row.topic,
                              payload_json=row.payload_json, attempts=row.attempts,
                              error=error[:8000])
    db.add(dlq)
    row.status = "DEAD_LETTER"
    row.last_error = error[:4000]
    return dlq

def retry_or_dead_letter(db: Session, row: OutboxEventV21, error: str, max_attempts: int = 8):
    if row.attempts >= max_attempts:
        return move_to_dead_letter(db, row, error)
    row.status = "PENDING"
    row.last_error = error[:4000]
    row.available_at = datetime.utcnow() + timedelta(seconds=min(900, 2 ** min(row.attempts, 10)))
    return None
