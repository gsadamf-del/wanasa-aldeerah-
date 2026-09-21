import os, sys
os.environ["DATABASE_URL"] = "sqlite:///./v24_test.db"
os.environ["ENVIRONMENT"] = "test"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.db.session import Base, engine, SessionLocal
from app.models_v24 import SchemaMigrationV24, MigrationPreflightV24


def setup_function(): Base.metadata.create_all(bind=engine)
def teardown_function(): Base.metadata.drop_all(bind=engine)


def test_schema_revision_is_unique():
    db = SessionLocal()
    db.add(SchemaMigrationV24(revision="v24", checksum="test")); db.commit()
    assert db.query(SchemaMigrationV24).filter_by(revision="v24").count() == 1
    db.close()


def test_preflight_registry():
    db = SessionLocal()
    row = MigrationPreflightV24(run_key="preflight-1", status="PASSED", passed=True, detail="ok")
    db.add(row); db.commit()
    assert db.query(MigrationPreflightV24).one().passed is True
    db.close()
