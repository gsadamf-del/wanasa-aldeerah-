# وناسة الديرة V25

V25 is the production-integration release built on V24. It includes:

- PostgreSQL V25 migration and production gate compatibility.
- Real payment adapters for Stripe and PayPal (credential/config driven).
- Real push adapters for Firebase FCM HTTP v1 and Apple APNs.
- External monitoring event sink integration.
- Backup/restore drill tooling.
- Android + iOS Flutter platform bootstrap and CI release workflows.
- Firebase configuration templates and signing templates.
- Existing V19–V24 inventory, payments foundation, outbox/DLQ, rate limiting, security, migration gate and operational controls.

## Important
Credentials are intentionally not included. A successful code/test build is not the same as a signed App Store/Google Play release. Production payment, push, monitoring and PostgreSQL connectivity must be validated with the deployment's real credentials and infrastructure.
