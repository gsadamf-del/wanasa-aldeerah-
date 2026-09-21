import json
import logging
import time
from collections import defaultdict, deque
from threading import Lock
from datetime import datetime
from sqlalchemy.orm import Session
from app.models_v21 import OutboxEventV21
from app.services.operations_v22 import retry_or_dead_letter, record_metric

logger = logging.getLogger("wanasa")

class InMemoryRateLimiterV23:
    """Single-process limiter. Use a shared gateway/Redis adapter for multi-instance deployments."""
    def __init__(self, limit: int = 120, window_seconds: int = 60):
        self.limit = max(1, limit)
        self.window_seconds = max(1, window_seconds)
        self._hits = defaultdict(deque)
        self._lock = Lock()

    def allow(self, key: str) -> tuple[bool, int]:
        now = time.monotonic()
        with self._lock:
            q = self._hits[key]
            cutoff = now - self.window_seconds
            while q and q[0] <= cutoff:
                q.popleft()
            if len(q) >= self.limit:
                retry_after = max(1, int(self.window_seconds - (now - q[0])))
                return False, retry_after
            q.append(now)
            return True, 0


def process_outbox_batch(db: Session, limit: int = 50) -> dict:
    from app.services.operations_v21 import claim_outbox, complete_outbox
    rows = claim_outbox(db, limit)
    processed = 0
    failed = 0
    for row in rows:
        try:
            json.loads(row.payload_json)
            complete_outbox(db, row)
            processed += 1
        except Exception as exc:
            failed += 1
            retry_or_dead_letter(db, row, str(exc))
    record_metric(db, "worker_claimed", len(rows))
    record_metric(db, "worker_processed", processed)
    record_metric(db, "worker_failed", failed)
    db.commit()
    return {"claimed": len(rows), "processed": processed, "failed": failed}


def validate_production_settings(settings) -> list[str]:
    errors = []
    if settings.environment.lower() in {"production", "prod"}:
        if settings.jwt_secret_key in {"change-me", ""} or len(settings.jwt_secret_key) < 32:
            errors.append("JWT_SECRET_KEY must be a strong secret (32+ chars)")
        if settings.payment_webhook_secret in {"change-me-webhook", ""} or len(settings.payment_webhook_secret) < 32:
            errors.append("PAYMENT_WEBHOOK_SECRET must be a strong secret (32+ chars)")
        if settings.cors_origins.strip() == "*":
            errors.append("CORS_ORIGINS must not be '*' in production")
        if getattr(settings, "payment_provider", "mock").lower() == "stripe" and not getattr(settings, "stripe_secret_key", ""):
            errors.append("STRIPE_SECRET_KEY is required when PAYMENT_PROVIDER=stripe")
        if getattr(settings, "payment_provider", "mock").lower() == "paypal" and (not getattr(settings, "paypal_client_id", "") or not getattr(settings, "paypal_client_secret", "")):
            errors.append("PAYPAL_CLIENT_ID/PAYPAL_CLIENT_SECRET are required when PAYMENT_PROVIDER=paypal")
        if not getattr(settings, "external_monitoring_url", ""):
            errors.append("EXTERNAL_MONITORING_URL is required in production")
    return errors
