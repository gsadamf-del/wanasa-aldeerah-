import os, time, logging
from app.db.session import SessionLocal
from app.services.production_v23 import process_outbox_batch

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(message)s")
log = logging.getLogger("wanasa.worker")

if __name__ == "__main__":
    limit = int(os.getenv("OUTBOX_BATCH_SIZE", "50"))
    interval = int(os.getenv("OUTBOX_POLL_SECONDS", "5"))
    once = os.getenv("WORKER_ONCE", "0") == "1"
    while True:
        db = SessionLocal()
        try:
            result = process_outbox_batch(db, limit)
            log.info('{"event":"outbox_worker","result":%s}', result)
        except Exception as exc:
            db.rollback()
            log.exception('{"event":"outbox_worker_error","error":%r}', exc)
        finally:
            db.close()
        if once:
            break
        time.sleep(interval)
