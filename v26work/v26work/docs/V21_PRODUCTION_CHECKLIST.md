# V21 Production Checklist

- [ ] PostgreSQL + reviewed Alembic migrations.
- [ ] Unique indexes/constraints verified in production schema.
- [ ] Secrets in a secrets manager; no default secrets.
- [ ] Restrictive CORS and HTTPS.
- [ ] Distributed rate limiting at edge/API gateway.
- [ ] Structured logs with X-Request-Id.
- [ ] Metrics/traces exported to the chosen observability stack.
- [ ] Outbox worker deployed separately with retry/backoff and dead-letter handling.
- [ ] Payment reconciliation connected to the real provider's reports/webhooks.
- [ ] Backup + restore drill completed.
- [ ] Security review / penetration testing completed.
- [ ] Android/Windows signing keys and release builds configured.
