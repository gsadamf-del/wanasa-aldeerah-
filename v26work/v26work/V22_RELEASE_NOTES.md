# V22 Release Notes

## Added
- V22 models: rate-limit buckets, dead-letter events, metric samples, backup drills.
- V22 operations service with retry/dead-letter and metric recording.
- V22 API endpoints for health, readiness, capabilities, metrics, DLQ and backup drills.
- Outbox processing now moves exhausted events to DLQ instead of retrying forever.
- Production checklist and architecture documentation.

## Verification
- Backend test suite must pass in CI.
- ZIP integrity checked after packaging.
