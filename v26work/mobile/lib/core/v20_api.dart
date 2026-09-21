import 'api_client.dart';

class V20Api {
  final ApiClient api;
  V20Api(this.api);

  Uri health() => api.endpoint('/api/v20/health');
  Uri readiness() => api.endpoint('/api/v20/readiness');
  Uri capabilities() => api.endpoint('/api/v20/capabilities');

  Future<dynamic> createOrder(List<Map<String, dynamic>> items, {String deliveryFee = '0', required String idempotencyKey}) {
    return api.postJson('/api/v20/orders', {
      'items': items,
      'delivery_fee': deliveryFee,
    }, idempotencyKey: idempotencyKey);
  }

  Future<dynamic> registerDevice(String token, String platform) {
    return api.postJson('/api/v20/devices', {'token': token, 'platform': platform});
  }

  Future<dynamic> notifications() => api.getJson('/api/v20/notifications');
}
