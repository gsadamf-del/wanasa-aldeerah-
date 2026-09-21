# V23 Release Notes

- Added V23 production middleware and rate limiting foundation.
- Added structured JSON request logging.
- Added production secret/CORS configuration validation.
- Added dedicated `backend/worker.py` outbox worker.
- Added Prometheus-compatible metrics endpoint.
- Added DLQ requeue/resolve operations.
- Added worker heartbeat and operational incident models.
- Added PostgreSQL V23 migration SQL.
- Added V23 tests and CI workflow.

V23 remains a production integration foundation; provider credentials, shared distributed rate limiting, external observability, restore drills, and signed client releases remain deployment tasks.
