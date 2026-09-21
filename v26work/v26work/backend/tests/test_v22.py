import os, sys
os.environ["DATABASE_URL"] = "sqlite:///./v22_test.db"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.db.session import Base, engine, SessionLocal
from app.models_v21 import OutboxEventV21
from app.models_v22 import DeadLetterEventV22, MetricSampleV22, BackupDrillV22
from app.services.operations_v22 import retry_or_dead_letter, record_metric

def setup_function():
    Base.metadata.create_all(bind=engine)

def teardown_function():
    Base.metadata.drop_all(bind=engine)

def test_dead_letter_after_max_attempts():
    db=SessionLocal()
    row=OutboxEventV21(event_id="v22-dlq-1",topic="test",aggregate_type="order",payload_json="{}",attempts=8,status="PROCESSING")
    db.add(row); db.commit()
    dlq=retry_or_dead_letter(db,row,"boom",max_attempts=8)
    db.commit()
    assert dlq is not None
    assert row.status == "DEAD_LETTER"
    assert db.query(DeadLetterEventV22).count() == 1
    db.close()

def test_metric_accumulates():
    db=SessionLocal()
    record_metric(db,"requests",1,bucket="fixed")
    record_metric(db,"requests",2,bucket="fixed")
    db.commit()
    row=db.query(MetricSampleV22).filter_by(metric="requests",bucket="fixed").one()
    assert row.value == 3
    db.close()

def test_backup_drill_model():
    db=SessionLocal()
    row=BackupDrillV22(drill_key="restore-2026-01",status="VERIFIED")
    db.add(row); db.commit()
    assert db.query(BackupDrillV22).count() == 1
    db.close()
