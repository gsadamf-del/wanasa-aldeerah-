-- V22 PostgreSQL migration. Apply after V21 control-plane migration.
CREATE TABLE IF NOT EXISTS v22_rate_limit_buckets (
  id SERIAL PRIMARY KEY,
  bucket_key VARCHAR(255) NOT NULL UNIQUE,
  window_started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  request_count INTEGER NOT NULL DEFAULT 0,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS v22_dead_letter_events (
  id SERIAL PRIMARY KEY,
  source_event_id VARCHAR(128) NOT NULL,
  topic VARCHAR(128) NOT NULL,
  payload_json TEXT NOT NULL,
  attempts INTEGER NOT NULL DEFAULT 0,
  error TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  resolved BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE INDEX IF NOT EXISTS ix_v22_dlq_source_event ON v22_dead_letter_events(source_event_id);
CREATE INDEX IF NOT EXISTS ix_v22_dlq_topic ON v22_dead_letter_events(topic);
CREATE INDEX IF NOT EXISTS ix_v22_dlq_created ON v22_dead_letter_events(created_at);
CREATE INDEX IF NOT EXISTS ix_v22_dlq_resolved ON v22_dead_letter_events(resolved);
CREATE TABLE IF NOT EXISTS v22_metric_samples (
  id SERIAL PRIMARY KEY,
  metric VARCHAR(100) NOT NULL,
  value INTEGER NOT NULL DEFAULT 0,
  bucket VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_v22_metric_bucket UNIQUE(metric, bucket)
);
CREATE INDEX IF NOT EXISTS ix_v22_metric ON v22_metric_samples(metric);
CREATE INDEX IF NOT EXISTS ix_v22_metric_bucket ON v22_metric_samples(bucket);
CREATE INDEX IF NOT EXISTS ix_v22_metric_created ON v22_metric_samples(created_at);
CREATE TABLE IF NOT EXISTS v22_backup_drills (
  id SERIAL PRIMARY KEY,
  drill_key VARCHAR(128) NOT NULL UNIQUE,
  status VARCHAR(24) NOT NULL DEFAULT 'PLANNED',
  verified_at TIMESTAMP,
  notes TEXT
);
