# وناسة الديرة V22 — Production Readiness & Observability Foundation

V22 تبني فوق V21 وتركّز على تحويل أساس التشغيل إلى طبقة قابلة للقياس والاسترداد:

- 📊 Metric samples للتشغيل والـoutbox.
- ☠️ Dead-letter queue للأحداث التي تتجاوز عدد المحاولات.
- 🔁 Retry/backoff أكثر وضوحًا مع حد محاولات.
- ❤️ Readiness يتضمن طبقة DLQ.
- 💾 Backup drill registry لتوثيق اختبارات الاستعادة.
- 🧭 Operations APIs للـmetrics والـDLQ والـbackup drills.
- 🔐 أساس جاهز لربط rate limiting موزع وsecrets manager خارجي.

V22 لا تدّعي أن telemetry أو rate limiting أصبحا موزعين فعليًا؛ ذلك يحتاج بنية الإنتاج المختارة.
