import 'api_client.dart';

class V21Api {
  final ApiClient api;
  V21Api(this.api);

  Uri health() => api.endpoint('/api/v21/health');
  Uri readiness() => api.endpoint('/api/v21/readiness');
  Uri capabilities() => api.endpoint('/api/v21/capabilities');
  Future<dynamic> operationsSummary() => api.getJson('/api/v21/operations/summary');
  Future<dynamic> audit({int limit = 100}) => api.getJson('/api/v21/admin/audit?limit=$limit');
  Future<dynamic> securityEvents({int limit = 100}) => api.getJson('/api/v21/admin/security-events?limit=$limit');
  Future<dynamic> reconcilePayments(String runKey) => api.postJson('/api/v21/admin/reconciliation/payments', {'run_key': runKey, 'scope': 'payments'});
  Future<dynamic> processOutbox({int limit = 50}) => api.postJson('/api/v21/operations/outbox/process', {'limit': limit});
}
