import os, sys
os.environ["DATABASE_URL"] = "sqlite:///./v21_test.db"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.db.session import Base, engine, SessionLocal
from app.models_v21 import OutboxEventV21, AuditEventV21
from app.services.operations_v21 import enqueue, audit, claim_outbox, complete_outbox

def setup_function():
    Base.metadata.create_all(bind=engine)

def teardown_function():
    Base.metadata.drop_all(bind=engine)

def test_outbox_lifecycle():
    db = SessionLocal()
    row = enqueue(db, "orders.created", "order", 7, {"order_id": 7}, event_id="v21-test-1")
    db.commit()
    claimed = claim_outbox(db, 10)
    assert len(claimed) == 1
    assert claimed[0].status == "PROCESSING"
    complete_outbox(db, claimed[0])
    db.refresh(row)
    assert row.status == "PROCESSED"
    db.close()

def test_audit_event_persists():
    db = SessionLocal()
    row = audit(db, "TEST", "system", 1, actor_user_id=2, request_id="req-1")
    db.commit()
    assert row.id is not None
    assert db.query(AuditEventV21).count() == 1
    db.close()
