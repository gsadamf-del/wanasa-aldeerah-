import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';

class PushService {
  static Future<String?> initialize() async {
    try {
      await Firebase.initializeApp();
      final messaging = FirebaseMessaging.instance;
      await messaging.requestPermission(alert: true, badge: true, sound: true);
      return await messaging.getToken();
    } catch (_) {
      // Native Firebase configuration is intentionally environment-specific.
      return null;
    }
  }
}
