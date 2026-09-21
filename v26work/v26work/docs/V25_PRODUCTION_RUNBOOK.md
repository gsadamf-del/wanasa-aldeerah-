# V25 Production Runbook

## 1. PostgreSQL
1. Provision PostgreSQL 16+.
2. Apply V21, V22, V23, V24, then V25 SQL migrations in order.
3. Verify `/api/v24/readiness` reports the required migration.
4. Keep `ENVIRONMENT=production`; `create_all()` is disabled in production.

## 2. Payments
Set `PAYMENT_PROVIDER=stripe` or `paypal` and provide live credentials through a secret manager. Configure provider webhooks and verify signatures before enabling real money flows. No production credential is bundled in this release.

## 3. Notifications
Configure Firebase FCM HTTP v1 and Apple APNs credentials. Register device tokens through the existing device-token APIs. Test both Android and iOS devices before rollout.

## 4. External monitoring
Set `EXTERNAL_MONITORING_URL` and API key to the team's Sentry/Datadog/Elastic/custom ingest endpoint. Run `POST /api/v25/admin/monitoring/test` with an admin token.

## 5. Backups and restore
Run a scheduled `pg_dump` to encrypted storage. Execute `infra/restore_drill.sh` against an isolated PostgreSQL database at least once per release cycle. Record the drill result in `v25_restore_drills`.

## 6. Mobile release
Run `mobile/tool/bootstrap_platforms.sh`, add Firebase config files, configure Android signing and Apple signing/App Store credentials, then use `.github/workflows/mobile-v25.yml`.

Never commit live API keys, signing keys, Firebase production files, or APNs private keys.

## 7. Payment webhooks
The existing V20 webhook storage/idempotency remains in place. For Stripe, validate the provider's `Stripe-Signature` using `StripeProviderV25.verify_webhook` before changing payment state. PayPal webhook verification must use the PayPal certificate/signature verification flow before changing state. Do not mark an order paid merely because a browser returned from checkout.
