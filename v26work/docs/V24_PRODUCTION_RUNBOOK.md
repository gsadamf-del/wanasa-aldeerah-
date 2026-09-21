# V24 Production Migration Runbook

1. Freeze the V24 artifact checksum and database backup.
2. Verify PostgreSQL version and connection credentials.
3. Run the V21 migration.
4. Run the V22 migration.
5. Run the V23 migration.
6. Run the V24 migration.
7. Execute data/constraint/index checks and application smoke tests.
8. Confirm `/api/v24/readiness` reports `ready: true`.
9. Only then enable production traffic.
10. Record the migration checksum in `v24_schema_migrations`.

## Rollback principle
Do not use destructive automatic rollback for financial/order tables. Restore from the verified backup or execute a reviewed forward migration.

## Important
The V24 release artifact does not execute these migrations automatically. The production database remains the source of truth and must be migrated under operational change control.
