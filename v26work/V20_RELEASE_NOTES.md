# V20 Release Notes

## From V19
- Fixed V18/V19 router import mismatches against `app.db.session` and `rbac`.
- Added V20 API and domain models.
- Added transactional inventory reservation with row-lock intent.
- Added request idempotency for order creation.
- Added payment webhook HMAC verification and event replay protection.
- Added device registration and notification inbox endpoints.
- Added media asset registry.
- Added delivery location foundation.
- Added merchant settlement/commission foundation.
- Added Flutter API client and V20 client.
- Added V20 CI and tests.
- Added production checklist and V21 roadmap.

## Validation
- Source archive was structurally valid before upgrade (`ZipFile.testzip() == None`).
- V20 backend tests: **6 passed** using an isolated SQLite test database in the build environment.
- Production PostgreSQL integration, real payment provider, FCM/APNs, object storage, and APK/EXE packaging still require their real build/deployment environments.
