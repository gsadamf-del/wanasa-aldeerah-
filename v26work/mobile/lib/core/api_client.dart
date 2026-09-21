import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiClient {
  final String baseUrl;
  final String? token;
  ApiClient(this.baseUrl, {this.token});

  Uri endpoint(String path) => Uri.parse('$baseUrl$path');

  Future<dynamic> getJson(String path) async {
    final r = await http.get(endpoint(path), headers: _headers());
    return _decode(r);
  }

  Future<dynamic> postJson(String path, Map<String, dynamic> body, {String? idempotencyKey}) async {
    final h = _headers();
    if (idempotencyKey != null) h['Idempotency-Key'] = idempotencyKey;
    final r = await http.post(endpoint(path), headers: h, body: jsonEncode(body));
    return _decode(r);
  }

  Map<String, String> _headers() => {
    'Content-Type': 'application/json',
    if (token != null) 'Authorization': 'Bearer $token',
  };

  dynamic _decode(http.Response r) {
    final body = r.body.isEmpty ? {} : jsonDecode(r.body);
    if (r.statusCode >= 400) throw Exception('API ${r.statusCode}: $body');
    return body;
  }
}
