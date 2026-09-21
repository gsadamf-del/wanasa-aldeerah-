# V23 Architecture — Production Integration & Reliability

V23 moves the V22 foundation toward an operational deployment model.

## Included
- configurable request rate limiting middleware (single-process foundation)
- structured JSON HTTP request logs with request IDs
- production configuration validation for JWT/webhook secrets and CORS
- dedicated outbox worker entrypoint with retry/dead-letter behavior
- Prometheus-compatible text endpoint backed by V22 metric samples
- DLQ requeue/resolve operations
- worker/incident persistence models
- reviewed PostgreSQL migration SQL
- CI tests and compile validation

## Important boundary
The rate limiter is intentionally single-process. Multi-instance deployments should place a shared gateway/Redis limiter in front of the API. The worker is a runnable process, but real payment/notification delivery connectors still require provider credentials and connector implementations.
