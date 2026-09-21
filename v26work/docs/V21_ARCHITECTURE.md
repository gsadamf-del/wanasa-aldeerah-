# V21 Architecture

## Control plane
- AuditEventV21: append-oriented operational audit records.
- SecurityEventV21: security signal stream.
- OutboxEventV21: durable DB-backed event handoff.
- ReconciliationRunV21: idempotent operational reconciliation runs.

## Request boundary
Every HTTP response gets a request ID and baseline security headers. A reverse proxy/load balancer should preserve or generate the canonical request ID and pass it downstream.

## Outbox contract
1. Business transaction writes domain changes and an outbox row in the same DB transaction.
2. Worker claims PENDING rows.
3. External delivery occurs outside the request transaction.
4. Worker marks PROCESSED or retries with backoff.

The included admin endpoint only exercises the durable lifecycle; it is not a substitute for a production worker or message broker.
