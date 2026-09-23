import 'package:flutter/material.dart';
import 'core/app_config.dart';
import 'core/push_service.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await PushService.initialize();
  runApp(const WanasaApp());
}

class WanasaApp extends StatelessWidget {
  const WanasaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'وناسة الديرة',
      theme: ThemeData(useMaterial3: true),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.rtl,
      child: Scaffold(
        appBar: AppBar(title: const Text('وناسة الديرة V26')),
        body: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            const Text('منصة التجارة والتصفية السريعة', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text('API: ${AppConfig.apiBaseUrl}'),
            const SizedBox(height: 20),
            _card(context, 'حساب العميل', 'تصفح المنتجات والعروض والسلة والطلبات'),
            _card(context, 'حساب التاجر', 'إدارة المنتجات والأسعار والمخزون والعروض والطلبات'),
            _card(context, 'لقطة الديرة', 'منتجات قريبة الصلاحية ضمن محرك التصفية'),
            _card(context, 'الأغذية الجافة', 'تصنيفات ومنتجات الأغذية'),
            _card(context, 'التجميل والعناية', 'منتجات التجميل والعناية'),
          ],
        ),
      ),
    );
  }

  Widget _card(BuildContext context, String title, String subtitle) {
    return Card(
      child: ListTile(
        title: Text(title),
        subtitle: Text(subtitle),
        trailing: const Icon(Icons.arrow_back_ios_new),
      ),
    );
  }
}
