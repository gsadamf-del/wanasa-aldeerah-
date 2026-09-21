-- Wanasa Al Deerah V25 production integration schema.
-- Run only after V21, V22, V23 and V24 revisions are applied.
CREATE TABLE IF NOT EXISTS v25_external_provider_health (
 id SERIAL PRIMARY KEY, provider VARCHAR(64) NOT NULL UNIQUE, status VARCHAR(24) NOT NULL DEFAULT 'UNKNOWN',
 latency_ms DOUBLE PRECISION, checked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, detail TEXT
);
CREATE TABLE IF NOT EXISTS v25_restore_drills (
 id SERIAL PRIMARY KEY, drill_key VARCHAR(128) NOT NULL UNIQUE, source_backup VARCHAR(512) NOT NULL,
 target_database VARCHAR(256) NOT NULL, status VARCHAR(32) NOT NULL DEFAULT 'PLANNED',
 started_at TIMESTAMP NULL, completed_at TIMESTAMP NULL, verified BOOLEAN NOT NULL DEFAULT FALSE, notes TEXT
);
CREATE TABLE IF NOT EXISTS v25_monitoring_events (
 id SERIAL PRIMARY KEY, event_type VARCHAR(64) NOT NULL, severity VARCHAR(24) NOT NULL DEFAULT 'INFO',
 message TEXT NOT NULL, external_id VARCHAR(128), created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO v24_schema_migrations(revision, checksum, notes)
VALUES ('v25','v25-production-integration','payments notifications monitoring restore mobile release')
ON CONFLICT (revision) DO NOTHING;
