# وناسة الديرة V20 — Production Operations Foundation

V20 تبني مباشرة فوق V19 وتحوّل الأساسات إلى مسارات تشغيلية أوضح:
- مخزون transactional مع row locking وInventoryEvent.
- Idempotency-Key لإنشاء الطلبات.
- Payment provider adapter + HMAC webhook verification + duplicate event protection.
- Device tokens + notification inbox API.
- Media asset registry.
- Delivery location foundation.
- Settlement/commission foundation.
- Health/readiness/capabilities V20.
- إصلاح تكامل V18/V19 مع طبقة DB الحالية.
- Flutter API client وV20 API.
- CI واختبارات V20.

> هذه النسخة لا تدّعي وجود بوابة دفع حقيقية أو FCM/APNs حقيقي أو تخزين Object Storage؛ هذه تبقى adapters/foundations حتى إضافة بيانات الاعتماد والمزود الفعلي ومراجعة الأمن.

## التشغيل
Backend:
```bash
cd backend
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```

Production:
1. PostgreSQL.
2. Alembic migrations reviewed/applied.
3. HTTPS + restrictive CORS.
4. `JWT_SECRET_KEY` و`PAYMENT_WEBHOOK_SECRET` من secrets manager.
5. مزود دفع حقيقي مع webhook verification.
6. Object storage وCDN للصور.
7. FCM/APNs credentials.
8. rate limiting، logs، metrics، backups/restore test.
