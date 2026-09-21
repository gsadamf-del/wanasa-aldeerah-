# V20 Production Checklist

## Database
- [ ] PostgreSQL production instance
- [ ] Alembic migration generated/reviewed/applied
- [ ] Transaction isolation and row-lock behavior tested under concurrency
- [ ] Backup + restore drill

## Security
- [ ] Rotate JWT secret
- [ ] Rotate payment webhook secret
- [ ] Restrictive CORS
- [ ] HTTPS only
- [ ] Rate limiting / abuse protection
- [ ] Audit logging policy
- [ ] Secret manager configured

## Payments
- [ ] Real provider credentials
- [ ] Real provider adapter
- [ ] Webhook endpoint exposed over HTTPS
- [ ] Signature verification tested with provider fixtures
- [ ] Replay/duplicate event handling tested
- [ ] Refund/cancel flows implemented

## Notifications
- [ ] FCM/APNs credentials
- [ ] Push adapter
- [ ] Token cleanup for invalid tokens
- [ ] Notification delivery metrics

## Media
- [ ] Object storage
- [ ] Signed upload/download URLs
- [ ] MIME/size validation
- [ ] Malware scanning policy
- [ ] CDN

## Delivery
- [ ] Courier role/model
- [ ] Location privacy/retention policy
- [ ] Live tracking provider
- [ ] Delivery state machine

## Finance
- [ ] Settlement reconciliation
- [ ] Commission policy approved
- [ ] Refund/chargeback accounting
- [ ] Merchant payout provider

## Release
- [ ] Backend CI green
- [ ] Flutter analyzer/tests green
- [ ] Android signing
- [ ] iOS signing
- [ ] Privacy/terms/compliance review
- [ ] Staged rollout
