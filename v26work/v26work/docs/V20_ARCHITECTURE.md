# V20 Architecture

## 1. Commerce
`POST /api/v20/orders` يتطلب `Idempotency-Key` ويستخدم transaction و`SELECT ... FOR UPDATE` عبر خدمة المخزون.

## 2. Payments
- Provider adapter منفصل.
- HMAC SHA-256 webhook verification.
- `PaymentWebhook.event_id` لمنع معالجة event مكرر.
- ما زال Mock provider في V20؛ لا يوجد ربط مالي حقيقي افتراضيًا.

## 3. Notifications
`DeviceToken` للتسجيل، و`Notification` لصندوق الإشعارات. FCM/APNs يبقيان خلف adapter خارجي.

## 4. Media
`MediaAsset` يسجل روابط الملفات؛ رفع الملفات الفعلي إلى object storage يحتاج provider/storage integration.

## 5. Delivery
`DeliveryLocation` يسجل آخر مواقع التوصيل. لا يوجد تتبع حي أو خرائط provider في هذه النسخة.

## 6. Settlement
`SettlementEntry` يحسب العمولة وصافي التاجر للطلبات المسلّمة/المكتملة. التسوية البنكية الفعلية ليست جزءًا من V20.

## 7. Operational APIs
- `/api/v20/health`
- `/api/v20/readiness`
- `/api/v20/capabilities`
