import 'package:flutter/material.dart';
import 'core/app_config.dart';
import 'core/api_client.dart';
import 'core/push_service.dart';
import 'core/token_store.dart';

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
        appBar: AppBar(
          title: const Text('وناسة الديرة V26'),
        ),
        body: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            const Text(
              'منصة التجارة والتصفية السريعة',
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text('API: ${AppConfig.apiBaseUrl}'),
            const SizedBox(height: 20),

            _card(
              context,
              'حساب العميل',
              'تصفح المنتجات والعروض والسلة والطلبات',
              const CustomerLoginPage(),
            ),

            _card(
              context,
              'حساب التاجر',
              'إدارة المنتجات والأسعار والمخزون والعروض والطلبات',
              const PlaceholderPage(title: 'حساب التاجر'),
            ),

            _card(
              context,
              'لقطة الديرة',
              'منتجات قريبة الصلاحية ضمن محرك التصفية',
              const PlaceholderPage(title: 'لقطة الديرة'),
            ),

            _card(
              context,
              'الأغذية الجافة',
              'تصنيفات ومنتجات الأغذية',
              const PlaceholderPage(title: 'الأغذية الجافة'),
            ),

            _card(
              context,
              'التجميل والعناية',
              'منتجات التجميل والعناية',
              const PlaceholderPage(title: 'التجميل والعناية'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _card(
    BuildContext context,
    String title,
    String subtitle,
    Widget page,
  ) {
    return Card(
      child: ListTile(
        title: Text(title),
        subtitle: Text(subtitle),
        trailing: const Icon(Icons.arrow_back_ios_new),
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => page),
          );
        },
      ),
    );
  }
}

class CustomerLoginPage extends StatefulWidget {
  const CustomerLoginPage({super.key});

  @override
  State<CustomerLoginPage> createState() => _CustomerLoginPageState();
}

class _CustomerLoginPageState extends State<CustomerLoginPage> {
  final phoneController = TextEditingController();
  final passwordController = TextEditingController();

  bool loading = false;

  Future<void> login() async {
    setState(() => loading = true);

    try {
      final api = ApiClient(AppConfig.apiBaseUrl);

      final result = await api.postJson(
        '/api/v1/auth/login',
        {
          'phone': phoneController.text.trim(),
          'password': passwordController.text,
        },
      );

      await TokenStore.save(result['access_token']);

      if (!mounted) return;

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => const CustomerHomePage(),
        ),
      );
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('فشل تسجيل الدخول: $e'),
        ),
      );
    } finally {
      if (mounted) {
        setState(() => loading = false);
      }
    }
  }

  @override
  void dispose() {
    phoneController.dispose();
    passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('حساب العميل'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const Text(
            'تسجيل دخول العميل',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 24),

          TextField(
            controller: phoneController,
            keyboardType: TextInputType.phone,
            decoration: const InputDecoration(
              labelText: 'رقم الهاتف',
              border: OutlineInputBorder(),
            ),
          ),

          const SizedBox(height: 16),

          TextField(
            controller: passwordController,
            obscureText: true,
            decoration: const InputDecoration(
              labelText: 'كلمة المرور',
              border: OutlineInputBorder(),
            ),
          ),

          const SizedBox(height: 24),

          FilledButton(
            onPressed: loading ? null : login,
            child: Text(
              loading ? 'جاري الدخول...' : 'دخول',
            ),
          ),

          const SizedBox(height: 12),

          OutlinedButton(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const PlaceholderPage(
                    title: 'تسجيل عميل جديد',
                  ),
                ),
              );
            },
            child: const Text('إنشاء حساب جديد'),
          ),
        ],
      ),
    );
  }
}

class CustomerHomePage extends StatelessWidget {
  const CustomerHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('حساب العميل'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _item(context, 'المنتجات', Icons.shopping_bag),
          _item(context, 'العروض', Icons.local_offer),
          _item(context, 'السلة', Icons.shopping_cart),
          _item(context, 'الطلبات', Icons.receipt_long),
        ],
      ),
    );
  }

  Widget _item(
    BuildContext context,
    String title,
    IconData icon,
  ) {
    return Card(
      child: ListTile(
        leading: Icon(icon),
        title: Text(title),
        trailing: const Icon(Icons.arrow_back_ios_new),
        onTap: () {},
      ),
    );
  }
}

class PlaceholderPage extends StatelessWidget {
  final String title;

  const PlaceholderPage({
    super.key,
    required this.title,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: Center(
        child: Text(
          title,
          style: const TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}
