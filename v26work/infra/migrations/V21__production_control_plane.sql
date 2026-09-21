-- Review and apply through Alembic in production. This SQL is a reference migration.
CREATE TABLE IF NOT EXISTS v21_audit_events (
  id SERIAL PRIMARY KEY, actor_user_id INTEGER, action VARCHAR(100) NOT NULL,
  entity_type VARCHAR(100) NOT NULL, entity_id INTEGER, request_id VARCHAR(64),
  ip_address VARCHAR(64), metadata_json TEXT, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_v21_audit_events_actor_user_id ON v21_audit_events(actor_user_id);
CREATE INDEX IF NOT EXISTS ix_v21_audit_events_created_at ON v21_audit_events(created_at);

CREATE TABLE IF NOT EXISTS v21_outbox_events (
  id SERIAL PRIMARY KEY, event_id VARCHAR(128) NOT NULL UNIQUE, topic VARCHAR(128) NOT NULL,
  aggregate_type VARCHAR(100) NOT NULL, aggregate_id INTEGER, payload_json TEXT NOT NULL,
  status VARCHAR(24) NOT NULL DEFAULT 'PENDING', attempts INTEGER NOT NULL DEFAULT 0,
  available_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, processed_at TIMESTAMP,
  last_error TEXT, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_v21_outbox_status_available ON v21_outbox_events(status, available_at);

CREATE TABLE IF NOT EXISTS v21_reconciliation_runs (
  id SERIAL PRIMARY KEY, run_key VARCHAR(128) NOT NULL UNIQUE, scope VARCHAR(64) NOT NULL,
  status VARCHAR(24) NOT NULL DEFAULT 'RUNNING', checked_count INTEGER NOT NULL DEFAULT 0,
  mismatch_count INTEGER NOT NULL DEFAULT 0, summary_json TEXT NOT NULL DEFAULT '{}',
  started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, finished_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS v21_security_events (
  id SERIAL PRIMARY KEY, event_type VARCHAR(100) NOT NULL, severity VARCHAR(16) NOT NULL DEFAULT 'INFO',
  actor_user_id INTEGER, request_id VARCHAR(64), detail TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_v21_security_events_created_at ON v21_security_events(created_at);
