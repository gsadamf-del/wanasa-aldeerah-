import 'package:shared_preferences/shared_preferences.dart';

class TokenStore {
  static const key = 'access_token';

  static Future<void> save(String token) async {
    final p = await SharedPreferences.getInstance();
    await p.setString(key, token);
  }

  static Future<String?> read() async {
    final p = await SharedPreferences.getInstance();
    return p.getString(key);
  }

  static Future<void> clear() async {
    final p = await SharedPreferences.getInstance();
    await p.remove(key);
  }
}
