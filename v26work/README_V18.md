# وناسة الديرة V18 — Full Platform Foundation

امتداد V17 بطبقة تجارة وتشغيل موحدة:
- دورة الطلب: PENDING → CONFIRMED → PREPARING → READY → OUT_FOR_DELIVERY → DELIVERED.
- الإلغاء في الحالات المسموح بها.
- أساس خصم/حجز المخزون.
- API للتجارة والطلبات ومركز الإدارة.
- أساس الإشعارات.
- أساس مركز تحكم Windows.
- Flutter قابل للبناء Android/iOS/Web/Windows.

هذه Foundation وليست نسخة إنتاجية نهائية. يلزم للإنتاج: transactions/row locking للمخزون، بوابات دفع، FCM/APNs، تخزين ملفات، أسرار CI، مراقبة، نسخ احتياطي واختبارات أمن وتكامل.
