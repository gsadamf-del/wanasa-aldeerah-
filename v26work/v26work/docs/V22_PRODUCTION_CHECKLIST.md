# V22 Production Checklist

- [ ] PostgreSQL + reviewed Alembic migrations applied.
- [ ] Secrets loaded from a production secrets manager; rotate defaults before launch.
- [ ] Strict CORS, HTTPS, secure cookies/tokens, and trusted proxy configuration.
- [ ] Distributed rate limiting at gateway/API edge.
- [ ] Structured logs exported with X-Request-Id.
- [ ] Metrics and traces exported to the selected observability stack.
- [ ] Dedicated outbox worker deployed; V22 DLQ monitored and alerted.
- [ ] Payment reconciliation connected to real provider reports/webhooks.
- [ ] Backup and restore drill verified in an isolated environment.
- [ ] Security review / penetration testing completed.
- [ ] Android/Windows signing and release builds configured.
- [ ] Alerting configured for readiness failures, payment mismatches, DLQ growth, and authentication anomalies.
