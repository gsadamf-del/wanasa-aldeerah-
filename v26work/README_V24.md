# Wanasa Al Deerah — V24

## Final release before the real PostgreSQL migration

V24 is the final application release gate before applying the reviewed PostgreSQL migrations to the production database.

### Production rules
- Production no longer calls `Base.metadata.create_all()`.
- Readiness remains false until `v24_schema_migrations` contains revision `v24`.
- Apply migrations in order: V21, V22, V23, then V24.
- Do not mark V24 applied until schema checks, backup/restore verification, and smoke tests pass.
- Local/test environments may still bootstrap with SQLAlchemy `create_all()`.

### Included
- V24 migration gate and preflight registry.
- V22 PostgreSQL migration that was previously missing from the migration directory.
- V24 migration SQL and release runbook.
- Production readiness endpoint with migration status.
- Existing V19–V23 payment, inventory, outbox, DLQ, worker, rate-limit and observability foundations.

This release does **not** claim that the production PostgreSQL database has already been migrated.
