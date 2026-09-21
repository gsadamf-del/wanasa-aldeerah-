# V19 Architecture

## الوحدات الجديدة
1. Transactional inventory foundation
2. Payments abstraction
3. Push notification abstraction
4. Media assets
5. Audit/operational events
6. Health/readiness
7. Production configuration

## مبدأ المخزون
استخدم transaction وSELECT ... FOR UPDATE في PostgreSQL عند الحجز الفعلي.
الكود الموجود يوفر طبقة خدمة مرجعية ويجب ربطه بكل عملية checkout في الإنتاج.

## الدفع
PaymentProvider interface يسمح بإضافة Mada/STC Pay/بوابات أخرى دون ربط منطق الطلب بمزود واحد.

## الإشعارات
DeviceToken وNotification يفصلان تخزين الأجهزة عن مزود FCM/APNs.
