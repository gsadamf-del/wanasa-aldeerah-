# V25 Release Notes

## Production Integration
- Stripe PaymentIntent adapter + webhook signature verification.
- PayPal Orders adapter with sandbox/live endpoint selection.
- FCM HTTP v1 push adapter.
- APNs token-auth push adapter.
- External monitoring HTTP event sink.
- Restore drill command using pg_restore.
- V25 PostgreSQL schema migration.

## Mobile
- Flutter app version 25.0.0.
- Firebase Core/Messaging integration.
- Android/iOS platform bootstrap script.
- Android signing and iOS export templates.
- GitHub Actions for Android APK and iOS build artifact.

## Security
- Production configuration requires real payment integration and external monitoring configuration.
- No credentials or private keys are included.
