#!/usr/bin/env bash
set -euo pipefail
: "${BACKUP_FILE:?BACKUP_FILE is required}"
: "${TARGET_DATABASE_URL:?TARGET_DATABASE_URL is required}"
echo "Starting isolated PostgreSQL restore drill..."
pg_restore --exit-on-error --no-owner --clean --if-exists --dbname "$TARGET_DATABASE_URL" "$BACKUP_FILE"
psql "$TARGET_DATABASE_URL" -v ON_ERROR_STOP=1 -c "SELECT 1 AS restore_verified;"
echo "RESTORE DRILL PASSED"
