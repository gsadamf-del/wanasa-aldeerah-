-- V24 release gate. This migration is intentionally NOT executed by the application.
-- Apply only after reviewing V21, V22 and V23 migrations against the target database.
CREATE TABLE IF NOT EXISTS v24_schema_migrations (
  id SERIAL PRIMARY KEY,
  revision VARCHAR(64) NOT NULL UNIQUE,
  applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  checksum VARCHAR(128) NOT NULL,
  notes TEXT,
  CONSTRAINT uq_v24_schema_revision UNIQUE(revision)
);
CREATE TABLE IF NOT EXISTS v24_migration_preflights (
  id SERIAL PRIMARY KEY,
  run_key VARCHAR(128) NOT NULL UNIQUE,
  status VARCHAR(24) NOT NULL DEFAULT 'PENDING',
  checked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  detail TEXT,
  passed BOOLEAN NOT NULL DEFAULT FALSE
);
-- Record the release only after all preceding migrations have been verified.
-- INSERT INTO v24_schema_migrations(revision, checksum, notes)
-- VALUES ('v24', '<REVIEWED_SHA256>', 'Wanasa Al Deerah V24 production release');
