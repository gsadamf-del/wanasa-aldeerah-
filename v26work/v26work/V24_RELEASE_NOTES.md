# V24 Release Notes

## Final application release before PostgreSQL migration

V24 converts PostgreSQL migration from a future checklist item into an explicit production readiness gate without executing the migration itself.

### Changes
- Application version: `24.0.0`.
- Added V24 schema migration registry and preflight registry.
- Added `/api/v24/health`, `/api/v24/readiness`, `/api/v24/capabilities` and admin migration status.
- Production startup no longer uses `Base.metadata.create_all()`.
- Added the previously missing V22 PostgreSQL migration.
- Added V24 migration gate SQL.
- Preserved V23 reliability, worker, DLQ, rate limiting and structured logging foundations.
- Added V24 tests and documentation.

### Required next operation
Apply the reviewed PostgreSQL migrations in a controlled environment, verify backup/restore, run smoke tests, then record V24 as applied.
