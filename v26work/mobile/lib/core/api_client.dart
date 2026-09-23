import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiException implements Exception {
  final int? statusCode;
  final String message;

  const ApiException(
    this.message, {
    this.statusCode,
  });

  @override
  String toString() {
    if (statusCode == null) {
      return 'ApiException: $message';
    }

    return 'ApiException($statusCode): $message';
  }
}

class ApiClient {
  final String baseUrl;
  final String? token;

  static const Duration _timeout = Duration(seconds: 20);

  ApiClient(
    this.baseUrl, {
    this.token,
  });

  Uri endpoint(String path, [Map<String, dynamic>? query]) {
    final cleanBase = baseUrl.trim().replaceAll(RegExp(r'/$'), '');
    final cleanPath = path.startsWith('/') ? path : '/$path';

    final uri = Uri.parse('$cleanBase$cleanPath');

    if (query == null || query.isEmpty) {
      return uri;
    }

    return uri.replace(
      queryParameters: {
        ...uri.queryParameters,
        ...query.map(
          (key, value) => MapEntry(key, value.toString()),
        ),
      },
    );
  }

  Future<dynamic> getJson(
    String path, {
    Map<String, dynamic>? query,
  }) async {
    try {
      final response = await http
          .get(
            endpoint(path, query),
            headers: _headers(),
          )
          .timeout(_timeout);

      return _decode(response);
    } on TimeoutException {
      throw const ApiException(
        'انتهت مهلة الاتصال بالخادم',
      );
    } on ApiException {
      rethrow;
    } catch (e) {
      throw ApiException(
        'تعذر الاتصال بالخادم: $e',
      );
    }
  }

  Future<dynamic> postJson(
    String path,
    Map<String, dynamic> body, {
    String? idempotencyKey,
  }) async {
    try {
      final headers = _headers();

      if (idempotencyKey != null &&
          idempotencyKey.trim().isNotEmpty) {
        headers['Idempotency-Key'] = idempotencyKey.trim();
      }

      final response = await http
          .post(
            endpoint(path),
            headers: headers,
            body: jsonEncode(body),
          )
          .timeout(_timeout);

      return _decode(response);
    } on TimeoutException {
      throw const ApiException(
        'انتهت مهلة الاتصال بالخادم',
      );
    } on ApiException {
      rethrow;
    } catch (e) {
      throw ApiException(
        'تعذر الاتصال بالخادم: $e',
      );
    }
  }

  Map<String, String> _headers() {
    final headers = <String, String>{
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    };

    final currentToken = token?.trim();

    if (currentToken != null && currentToken.isNotEmpty) {
      headers['Authorization'] = 'Bearer $currentToken';
    }

    return headers;
  }

  dynamic _decode(http.Response response) {
    dynamic body;

    if (response.body.trim().isEmpty) {
      body = null;
    } else {
      try {
        body = jsonDecode(response.body);
      } catch (_) {
        body = response.body;
      }
    }

    if (response.statusCode >= 200 &&
        response.statusCode < 300) {
      return body;
    }

    switch (response.statusCode) {
      case 400:
        throw ApiException(
          _message(body, 'الطلب غير صحيح'),
          statusCode: response.statusCode,
        );

      case 401:
        throw ApiException(
          _message(body, 'انتهت جلسة تسجيل الدخول'),
          statusCode: response.statusCode,
        );

      case 403:
        throw ApiException(
          _message(body, 'ليس لديك صلاحية لهذا الإجراء'),
          statusCode: response.statusCode,
        );

      case 404:
        throw ApiException(
          _message(body, 'المورد المطلوب غير موجود'),
          statusCode: response.statusCode,
        );

      case 409:
        throw ApiException(
          _message(body, 'حدث تعارض في البيانات'),
          statusCode: response.statusCode,
        );

      case 422:
        throw ApiException(
          _message(body, 'البيانات المدخلة غير صالحة'),
          statusCode: response.statusCode,
        );

      case 429:
        throw ApiException(
          _message(body, 'تم تجاوز عدد الطلبات المسموح بها'),
          statusCode: response.statusCode,
        );

      default:
        if (response.statusCode >= 500) {
          throw ApiException(
            _message(body, 'الخادم غير متاح حاليًا'),
            statusCode: response.statusCode,
          );
        }

        throw ApiException(
          _message(body, 'حدث خطأ غير متوقع'),
          statusCode: response.statusCode,
        );
    }
  }

  String _message(
    dynamic body,
    String fallback,
  ) {
    if (body is Map<String, dynamic>) {
      final detail = body['detail'];

      if (detail is String && detail.trim().isNotEmpty) {
        return detail.trim();
      }

      final message = body['message'];

      if (message is String && message.trim().isNotEmpty) {
        return message.trim();
      }
    }

    if (body is String && body.trim().isNotEmpty) {
      return body.trim();
    }

    return fallback;
  }
}
