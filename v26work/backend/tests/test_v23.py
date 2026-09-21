import os, sys
os.environ["DATABASE_URL"] = "sqlite:///./v23_test.db"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.db.session import Base, engine, SessionLocal
from app.models_v21 import OutboxEventV21
from app.models_v22 import DeadLetterEventV22
from app.services.production_v23 import InMemoryRateLimiterV23, validate_production_settings


def setup_function(): Base.metadata.create_all(bind=engine)
def teardown_function(): Base.metadata.drop_all(bind=engine)

def test_rate_limiter_blocks_after_limit():
    limiter=InMemoryRateLimiterV23(limit=2, window_seconds=60)
    assert limiter.allow("x")[0] is True
    assert limiter.allow("x")[0] is True
    assert limiter.allow("x")[0] is False

def test_production_secret_validation():
    class S: environment="production"; jwt_secret_key="change-me"; payment_webhook_secret="change-me-webhook"; cors_origins="*"
    errors=validate_production_settings(S())
    assert len(errors)>=3

def test_worker_processes_valid_json():
    db=SessionLocal()
    row=OutboxEventV21(event_id="v23-worker-1",topic="test",aggregate_type="order",payload_json="{}",attempts=0,status="PENDING")
    db.add(row); db.commit()
    from app.services.production_v23 import process_outbox_batch
    result=process_outbox_batch(db,10)
    assert result["processed"] == 1
    assert db.query(OutboxEventV21).one().status == "PROCESSED"
    db.close()
