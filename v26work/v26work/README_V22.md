# وناسة الديرة V22 — Production Readiness & Observability Foundation

V22 تبني فوق V21 مع:
- Dead-letter handling للـOutbox بعد محاولات فاشلة متكررة.
- Metrics تشغيلية بسيطة قابلة للقراءة عبر API.
- Backup drill registry.
- V22 health/readiness/capabilities.
- Operations APIs للـDLQ والـmetrics واختبارات النسخ الاحتياطي.
- تحديث CI والاختبارات.

الحالة: Foundation تشغيلية متقدمة، وليست إطلاق Production نهائيًا. يجب ربط PostgreSQL/migrations وsecrets manager وrate limiting موزع وobservability stack وworkers الحقيقية قبل الإطلاق العام.
