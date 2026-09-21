# V23 Production Checklist

- [x] V23 migration SQL added
- [x] configurable rate-limit middleware foundation
- [x] structured request logging
- [x] request ID propagation
- [x] production secret/CORS validation
- [x] dedicated outbox worker entrypoint
- [x] DLQ requeue/resolve API
- [x] Prometheus-compatible metrics endpoint
- [x] CI + automated tests

Before production:
- [ ] Run migration against a staging PostgreSQL database and review SQL
- [ ] Use a shared rate limiter/gateway for multiple API replicas
- [ ] Configure secrets through a secrets manager
- [ ] Set restrictive HTTPS CORS origins
- [ ] Connect real payment/notification providers
- [ ] Run worker as a supervised service with monitoring
- [ ] Configure external Prometheus/alerting
- [ ] Execute backup + restore drill
- [ ] Security/penetration review
- [ ] Android/Windows signed release builds
