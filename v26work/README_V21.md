# وناسة الديرة V21 — Production Control Plane Foundation

V21 تبني فوق V20 مع تركيز على التشغيل الآمن والقابل للمراقبة:

- 🧾 Audit trail مستقل للأحداث الحساسة.
- 📤 Transactional Outbox لتقليل فقدان الأحداث بين DB والأنظمة الخارجية.
- 🔁 Outbox claim/retry/complete lifecycle.
- 💳 Payment reconciliation runs قابلة لإعادة التشغيل بواسطة run key.
- 🛡️ Security events.
- 🆔 X-Request-Id + security response headers.
- 📊 Operations summary / audit / security feeds للإدارة.
- 🧪 اختبارات V21 مع lifecycle للـ outbox وaudit.
- 🔧 إصلاح compatibility في V19 model import حتى يعمل التطبيق الكامل.

> V21 ليست ادعاءً بأن البنية أصبحت Production نهائية. ما زالت تحتاج migrations مدققة، rate limiting موزع، secrets manager، observability stack حقيقي، workers خارجيين، ومراجعة أمنية قبل الإطلاق العام.
