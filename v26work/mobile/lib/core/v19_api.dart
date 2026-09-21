import 'api_client.dart';

class V19Api {
  final ApiClient api;
  V19Api(this.api);

  Uri health() => api.endpoint('/api/v19/health');
  Uri readiness() => api.endpoint('/api/v19/readiness');
  Uri capabilities() => api.endpoint('/api/v19/capabilities');
}
