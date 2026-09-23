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
    const primary = Color(0xFF0F766E);
    const secondary = Color(0xFFF59E0B);

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'وناسة الديرة V26',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: primary,
          primary: primary,
          secondary: secondary,
          brightness: Brightness.light,
        ),
        scaffoldBackgroundColor: const Color(0xFFF7F9F8),
        appBarTheme: const AppBarTheme(
          centerTitle: false,
          elevation: 0,
          backgroundColor: Colors.transparent,
          foregroundColor: Color(0xFF17312F),
        ),
        cardTheme: CardThemeData(
          elevation: 0,
          margin: EdgeInsets.zero,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(22),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.white,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: BorderSide.none,
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: BorderSide.none,
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: const BorderSide(
              color: primary,
              width: 1.5,
            ),
          ),
        ),
      ),
      home: const MainShell(),
    );
  }
}

class MainShell extends StatefulWidget {
  const MainShell({super.key});

  @override
  State<MainShell> createState() => _MainShellState();
}

class _MainShellState extends State<MainShell> {
  int _index = 0;

  final List<Widget> _pages = const [
    HomePage(),
    CustomerHomePage(),
    MerchantHomePage(),
    MorePage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _index,
        children: _pages,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (value) {
          setState(() => _index = value);
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home),
            label: 'الرئيسية',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outline),
            selectedIcon: Icon(Icons.person),
            label: 'العميل',
          ),
          NavigationDestination(
            icon: Icon(Icons.storefront_outlined),
            selectedIcon: Icon(Icons.storefront),
            label: 'التاجر',
          ),
          NavigationDestination(
            icon: Icon(Icons.grid_view_outlined),
            selectedIcon: Icon(Icons.grid_view),
            label: 'المزيد',
          ),
        ],
      ),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: CustomScrollView(
        slivers: [
          SliverPadding(
            padding: const EdgeInsets.fromLTRB(20, 18, 20, 10),
            sliver: SliverToBoxAdapter(
              child: _Header(
                title: 'وناسة الديرة V26',
                subtitle: 'منصة التجارة والتصفية السريعة',
              ),
            ),
          ),
          SliverPadding(
            padding: const EdgeInsets.symmetric(horizontal: 20),
            sliver: SliverToBoxAdapter(
              child: _SearchBox(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const SearchPage(),
                    ),
                  );
                },
              ),
            ),
          ),
          SliverPadding(
            padding: const EdgeInsets.fromLTRB(20, 20, 20, 12),
            sliver: SliverToBoxAdapter(
              child: _HeroCard(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const SnapshotPage(),
                    ),
                  );
                },
              ),
            ),
          ),
          SliverPadding(
            padding: const EdgeInsets.fromLTRB(20, 8, 20, 12),
            sliver: SliverToBoxAdapter(
              child: Text(
                'الوصول السريع',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w800,
                    ),
              ),
            ),
          ),
          SliverPadding(
            padding: const EdgeInsets.symmetric(horizontal: 20),
            sliver: SliverGrid(
              delegate: SliverChildListDelegate([
                _HomeActionCard(
                  icon: Icons.person,
                  title: 'حساب العميل',
                  subtitle: 'المنتجات والسلة والطلبات',
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const CustomerHomePage(
                          standalone: true,
                        ),
                      ),
                    );
                  },
                ),
                _HomeActionCard(
                  icon: Icons.storefront,
                  title: 'حساب التاجر',
                  subtitle: 'المنتجات والمخزون والعروض',
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const MerchantHomePage(
                          standalone: true,
                        ),
                      ),
                    );
                  },
                ),
                _HomeActionCard(
                  icon: Icons.local_offer,
                  title: 'لقطة الديرة',
                  subtitle: 'عروض التصفية السريعة',
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const SnapshotPage(),
                      ),
                    );
                  },
                ),
                _HomeActionCard(
                  icon: Icons.category,
                  title: 'التصنيفات',
                  subtitle: 'تصفح الأقسام بسهولة',
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const CategoriesPage(),
                      ),
                    );
                  },
                ),
              ]),
              gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                maxCrossAxisExtent: 360,
                mainAxisSpacing: 14,
                crossAxisSpacing: 14,
                childAspectRatio: 1.45,
              ),
            ),
          ),
          SliverPadding(
            padding: const EdgeInsets.fromLTRB(20, 24, 20, 8),
            sliver: SliverToBoxAdapter(
              child: Text(
                'الأقسام الرئيسية',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w800,
                    ),
              ),
            ),
          ),
          SliverPadding(
            padding: const EdgeInsets.fromLTRB(20, 0, 20, 30),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                _CategoryTile(
                  icon: Icons.inventory_2,
                  title: 'الأغذية الجافة',
                  subtitle: 'منتجات وتصنيفات الأغذية',
                  onTap: () => _openCategory(
                    context,
                    'الأغذية الجافة',
                  ),
                ),
                const SizedBox(height: 12),
                _CategoryTile(
                  icon: Icons.spa,
                  title: 'التجميل والعناية',
                  subtitle: 'منتجات التجميل والعناية',
                  onTap: () => _openCategory(
                    context,
                    'التجميل والعناية',
                  ),
                ),
                const SizedBox(height: 12),
                _CategoryTile(
                  icon: Icons.local_shipping,
                  title: 'التصفية السريعة',
                  subtitle: 'عروض قريبة الصلاحية وأسعار خاصة',
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const SnapshotPage(),
                      ),
                    );
                  },
                ),
              ]),
            ),
          ),
        ],
      ),
    );
  }

  void _openCategory(BuildContext context, String title) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => ProductsPage(title: title),
      ),
    );
  }
}

class CustomerHomePage extends StatelessWidget {
  final bool standalone;

  const CustomerHomePage({
    super.key,
    this.standalone = false,
  });

  @override
  Widget build(BuildContext context) {
    final content = SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          if (standalone)
            const _SimpleBackHeader(title: 'حساب العميل')
          else
            const _SectionHeader(
              title: 'حساب العميل',
              subtitle: 'كل ما تحتاجه لتجربة شراء سهلة',
            ),
          const SizedBox(height: 18),
          _LargeAction(
            icon: Icons.shopping_bag,
            title: 'المنتجات',
            subtitle: 'استعراض المنتجات المتاحة',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const ProductsPage(
                    title: 'المنتجات',
                  ),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _LargeAction(
            icon: Icons.local_offer,
            title: 'العروض',
            subtitle: 'عروض وأسعار مميزة',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const OffersPage(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _LargeAction(
            icon: Icons.shopping_cart,
            title: 'السلة',
            subtitle: 'مراجعة المنتجات المختارة',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const PlaceholderPage(
                    title: 'السلة',
                    message: 'السلة جاهزة للربط مع نظام الطلبات.',
                  ),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _LargeAction(
            icon: Icons.receipt_long,
            title: 'الطلبات',
            subtitle: 'متابعة الطلبات وحالتها',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const PlaceholderPage(
                    title: 'الطلبات',
                    message: 'سيتم عرض الطلبات هنا عند ربط API الطلبات.',
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );

    return standalone ? Scaffold(body: content) : content;
  }
}

class MerchantHomePage extends StatelessWidget {
  final bool standalone;

  const MerchantHomePage({
    super.key,
    this.standalone = false,
  });

  @override
  Widget build(BuildContext context) {
    final content = SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          if (standalone)
            const _SimpleBackHeader(title: 'حساب التاجر')
          else
            const _SectionHeader(
              title: 'حساب التاجر',
              subtitle: 'إدارة المنتجات والمخزون والعروض',
            ),
          const SizedBox(height: 18),
          _LargeAction(
            icon: Icons.inventory,
            title: 'إدارة المنتجات',
            subtitle: 'إضافة وتعديل المنتجات',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const PlaceholderPage(
                    title: 'إدارة المنتجات',
                    message: 'واجهة إدارة المنتجات جاهزة للربط مع API.',
                  ),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _LargeAction(
            icon: Icons.price_change,
            title: 'الأسعار والمخزون',
            subtitle: 'متابعة الأسعار والكميات',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const PlaceholderPage(
                    title: 'الأسعار والمخزون',
                    message: 'واجهة المخزون جاهزة للربط مع API.',
                  ),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _LargeAction(
            icon: Icons.campaign,
            title: 'العروض',
            subtitle: 'إنشاء وإدارة العروض',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const OffersPage(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _LargeAction(
            icon: Icons.receipt_long,
            title: 'الطلبات',
            subtitle: 'متابعة طلبات العملاء',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const PlaceholderPage(
                    title: 'طلبات العملاء',
                    message: 'واجهة الطلبات جاهزة للربط مع API.',
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );

    return standalone ? Scaffold(body: content) : content;
  }
}

class MorePage extends StatelessWidget {
  const MorePage({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const _SectionHeader(
            title: 'المزيد',
            subtitle: 'إعدادات ومعلومات وناسة الديرة',
          ),
          const SizedBox(height: 18),
          _LargeAction(
            icon: Icons.category,
            title: 'التصنيفات',
            subtitle: 'استعراض جميع الأقسام',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const CategoriesPage(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _LargeAction(
            icon: Icons.search,
            title: 'البحث',
            subtitle: 'ابحث عن منتج أو عرض',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const SearchPage(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _LargeAction(
            icon: Icons.settings,
            title: 'الإعدادات',
            subtitle: 'إعدادات التطبيق',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const SettingsPage(),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _LargeAction(
            icon: Icons.info_outline,
            title: 'عن وناسة الديرة',
            subtitle: 'معلومات الإصدار',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const AboutPage(),
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}

class CategoriesPage extends StatelessWidget {
  const CategoriesPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('التصنيفات')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          _CategoryTile(
            icon: Icons.inventory_2,
            title: 'الأغذية الجافة',
            subtitle: 'أغذية ومنتجات متنوعة',
            onTap: () => _open(context, 'الأغذية الجافة'),
          ),
          const SizedBox(height: 12),
          _CategoryTile(
            icon: Icons.spa,
            title: 'التجميل والعناية',
            subtitle: 'منتجات العناية الشخصية',
            onTap: () => _open(context, 'التجميل والعناية'),
          ),
          const SizedBox(height: 12),
          _CategoryTile(
            icon: Icons.local_offer,
            title: 'لقطة الديرة',
            subtitle: 'تصفية وعروض خاصة',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const SnapshotPage(),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  void _open(BuildContext context, String title) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => ProductsPage(title: title),
      ),
    );
  }
}

class ProductsPage extends StatelessWidget {
  final String title;

  const ProductsPage({
    super.key,
    required this.title,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          _ProductCard(
            name: 'منتج تجريبي 01',
            subtitle: 'جاهز للربط مع قاعدة البيانات',
            price: 'السعر عند الربط',
            icon: Icons.inventory_2,
          ),
          const SizedBox(height: 12),
          _ProductCard(
            name: 'منتج تجريبي 02',
            subtitle: 'واجهة المنتج الجديدة',
            price: 'السعر عند الربط',
            icon: Icons.shopping_bag,
          ),
          const SizedBox(height: 12),
          _ProductCard(
            name: 'منتج تجريبي 03',
            subtitle: 'يمكن استبدال البيانات من API',
            price: 'السعر عند الربط',
            icon: Icons.local_mall,
          ),
        ],
      ),
    );
  }
}

class OffersPage extends StatelessWidget {
  const OffersPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('العروض')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          _OfferCard(
            title: 'عروض وناسة الديرة',
            subtitle: 'عروض خاصة وأسعار تصفية',
            onTap: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('سيتم تحميل العروض من الخادم عند الربط.'),
                ),
              );
            },
          ),
          const SizedBox(height: 12),
          _OfferCard(
            title: 'لقطة الديرة',
            subtitle: 'منتجات قريبة الصلاحية بأسعار خاصة',
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const SnapshotPage(),
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}

class SnapshotPage extends StatelessWidget {
  const SnapshotPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('لقطة الديرة')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Container(
            padding: const EdgeInsets.all(22),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(26),
              gradient: const LinearGradient(
                begin: Alignment.topRight,
                end: Alignment.bottomLeft,
                colors: [
                  Color(0xFF0F766E),
                  Color(0xFF115E59),
                ],
              ),
            ),
            child: const Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(
                  Icons.local_offer,
                  color: Colors.white,
                  size: 42,
                ),
                SizedBox(height: 16),
                Text(
                  'لقطة الديرة',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 26,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                SizedBox(height: 8),
                Text(
                  'محرك التصفية والعروض السريعة',
                  style: TextStyle(
                    color: Colors.white70,
                    fontSize: 16,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 18),
          _ProductCard(
            name: 'عروض التصفية',
            subtitle: 'منتجات قريبة الصلاحية',
            price: 'عرض خاص',
            icon: Icons.flash_on,
          ),
        ],
      ),
    );
  }
}

class SearchPage extends StatefulWidget {
  const SearchPage({super.key});

  @override
  State<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends State<SearchPage> {
  final controller = TextEditingController();
  String query = '';

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('البحث')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          TextField(
            controller: controller,
            textDirection: TextDirection.rtl,
            textInputAction: TextInputAction.search,
            onChanged: (value) {
              setState(() => query = value.trim());
            },
            decoration: const InputDecoration(
              hintText: 'ابحث عن منتج أو عرض...',
              prefixIcon: Icon(Icons.search),
            ),
          ),
          const SizedBox(height: 24),
          if (query.isEmpty)
            const Center(
              child: Padding(
                padding: EdgeInsets.all(30),
                child: Text(
                  'اكتب اسم المنتج للبحث',
                  style: TextStyle(fontSize: 17),
                ),
              ),
            )
          else
            _ProductCard(
              name: query,
              subtitle: 'نتيجة البحث - جاهزة للربط مع API',
              price: 'سيتم جلب السعر',
              icon: Icons.search,
            ),
        ],
      ),
    );
  }
}

class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('الإعدادات')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const _InfoTile(
            icon: Icons.cloud,
            title: 'عنوان الخادم',
            value: AppConfig.apiBaseUrl,
          ),
          const SizedBox(height: 12),
          const _InfoTile(
            icon: Icons.verified,
            title: 'الإصدار',
            value: '26.0.0',
          ),
          const SizedBox(height: 12),
          const _InfoTile(
            icon: Icons.security,
            title: 'حالة الواجهة',
            value: 'V26',
          ),
        ],
      ),
    );
  }
}

class AboutPage extends StatelessWidget {
  const AboutPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('عن وناسة الديرة')),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              Container(
                width: 92,
                height: 92,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(28),
                  color: Theme.of(context).colorScheme.primary,
                ),
                child: const Icon(
                  Icons.storefront,
                  color: Colors.white,
                  size: 48,
                ),
              ),
              const SizedBox(height: 22),
              const Text(
                'وناسة الديرة V26',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.w900,
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'منصة التجارة والتصفية السريعة',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 17),
              ),
              const SizedBox(height: 22),
              Text(
                'الإصدار 26.0.0',
                style: Theme.of(context).textTheme.bodyLarge,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class PlaceholderPage extends StatelessWidget {
  final String title;
  final String message;

  const PlaceholderPage({
    super.key,
    required this.title,
    required this.message,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(28),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                Icons.check_circle_outline,
                size: 64,
                color: Theme.of(context).colorScheme.primary,
              ),
              const SizedBox(height: 18),
              Text(
                title,
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.w800,
                ),
              ),
              const SizedBox(height: 10),
              Text(
                message,
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 16),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _Header extends StatelessWidget {
  final String title;
  final String subtitle;

  const _Header({
    required this.title,
    required this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 30,
            fontWeight: FontWeight.w900,
            color: Color(0xFF17312F),
          ),
        ),
        const SizedBox(height: 6),
        Text(
          subtitle,
          style: TextStyle(
            fontSize: 16,
            color: Colors.grey.shade700,
          ),
        ),
      ],
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final String title;
  final String subtitle;

  const _SectionHeader({
    required this.title,
    required this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 28,
            fontWeight: FontWeight.w900,
          ),
        ),
        const SizedBox(height: 6),
        Text(
          subtitle,
          style: TextStyle(
            color: Colors.grey.shade700,
            fontSize: 15,
          ),
        ),
      ],
    );
  }
}

class _SimpleBackHeader extends StatelessWidget {
  final String title;

  const _SimpleBackHeader({
    required this.title,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        IconButton(
          onPressed: () => Navigator.maybePop(context),
          icon: const Icon(Icons.arrow_back),
        ),
        Expanded(
          child: Text(
            title,
            style: const TextStyle(
              fontSize: 27,
              fontWeight: FontWeight.w900,
            ),
          ),
        ),
      ],
    );
  }
}

class _SearchBox extends StatelessWidget {
  final VoidCallback onTap;

  const _SearchBox({
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      borderRadius: BorderRadius.circular(18),
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(
          horizontal: 18,
          vertical: 16,
        ),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(18),
          border: Border.all(
            color: Colors.black.withOpacity(.05),
          ),
        ),
        child: Row(
          children: [
            Icon(
              Icons.search,
              color: Theme.of(context).colorScheme.primary,
            ),
            const SizedBox(width: 12),
            Text(
              'ابحث عن منتج أو عرض...',
              style: TextStyle(
                color: Colors.grey.shade600,
                fontSize: 15,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _HeroCard extends StatelessWidget {
  final VoidCallback onTap;

  const _HeroCard({
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      borderRadius: BorderRadius.circular(28),
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(28),
          gradient: const LinearGradient(
            begin: Alignment.topRight,
            end: Alignment.bottomLeft,
            colors: [
              Color(0xFF0F766E),
              Color(0xFF134E4A),
            ],
          ),
        ),
        child: Row(
          children: [
            const Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'لقطة الديرة',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 25,
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'عروض التصفية السريعة بأسعار خاصة',
                    style: TextStyle(
                      color: Colors.white70,
                      fontSize: 15,
                    ),
                  ),
                ],
              ),
            ),
            Container(
              width: 58,
              height: 58,
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(.15),
                shape: BoxShape.circle,
              ),
              child: const Icon(
                Icons.arrow_forward,
                color: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _HomeActionCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _HomeActionCard({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final primary = Theme.of(context).colorScheme.primary;

    return Card(
      child: InkWell(
        borderRadius: BorderRadius.circular(22),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(17),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                width: 46,
                height: 46,
                decoration: BoxDecoration(
                  color: primary.withOpacity(.10),
                  borderRadius: BorderRadius.circular(15),
                ),
                child: Icon(
                  icon,
                  color: primary,
                ),
              ),
              const Spacer(),
              Text(
                title,
                style: const TextStyle(
                  fontWeight: FontWeight.w800,
                  fontSize: 17,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                subtitle,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(
                  color: Colors.grey.shade600,
                  fontSize: 12,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _CategoryTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _CategoryTile({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final primary = Theme.of(context).colorScheme.primary;

    return Card(
      child: InkWell(
        borderRadius: BorderRadius.circular(20),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                width: 52,
                height: 52,
                decoration: BoxDecoration(
                  color: primary.withOpacity(.10),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Icon(
                  icon,
                  color: primary,
                ),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      subtitle,
                      style: TextStyle(
                        color: Colors.grey.shade600,
                      ),
                    ),
                  ],
                ),
              ),
              const Icon(Icons.arrow_forward_ios, size: 17),
            ],
          ),
        ),
      ),
    );
  }
}

class _LargeAction extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _LargeAction({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        borderRadius: BorderRadius.circular(22),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(18),
          child: Row(
            children: [
              CircleAvatar(
                radius: 27,
                backgroundColor:
                    Theme.of(context).colorScheme.primary.withOpacity(.10),
                child: Icon(
                  icon,
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),
              const SizedBox(width: 15),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    const SizedBox(height: 5),
                    Text(
                      subtitle,
                      style: TextStyle(
                        color: Colors.grey.shade600,
                      ),
                    ),
                  ],
                ),
              ),
              const Icon(Icons.arrow_forward_ios, size: 18),
            ],
          ),
        ),
      ),
    );
  }
}

class _ProductCard extends StatelessWidget {
  final String name;
  final String subtitle;
  final String price;
  final IconData icon;

  const _ProductCard({
    required this.name,
    required this.subtitle,
    required this.price,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Container(
              width: 68,
              height: 68,
              decoration: BoxDecoration(
                color: Theme.of(context)
                    .colorScheme
                    .primary
                    .withOpacity(.08),
                borderRadius: BorderRadius.circular(18),
              ),
              child: Icon(
                icon,
                size: 32,
                color: Theme.of(context).colorScheme.primary,
              ),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    name,
                    style: const TextStyle(
                      fontWeight: FontWeight.w800,
                      fontSize: 17,
                    ),
                  ),
                  const SizedBox(height: 5),
                  Text(
                    subtitle,
                    style: TextStyle(
                      color: Colors.grey.shade600,
                    ),
                  ),
                  const SizedBox(height: 7),
                  Text(
                    price,
                    style: TextStyle(
                      fontWeight: FontWeight.w700,
                      color: Theme.of(context).colorScheme.primary,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _OfferCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _OfferCard({
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        borderRadius: BorderRadius.circular(22),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(18),
          child: Row(
            children: [
              const CircleAvatar(
                radius: 27,
                child: Icon(Icons.local_offer),
              ),
              const SizedBox(width: 15),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontWeight: FontWeight.w800,
                        fontSize: 17,
                      ),
                    ),
                    const SizedBox(height: 5),
                    Text(subtitle),
                  ],
                ),
              ),
              const Icon(Icons.arrow_forward_ios, size: 17),
            ],
          ),
        ),
      ),
    );
  }
}

class _InfoTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String value;

  const _InfoTile({
    required this.icon,
    required this.title,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        contentPadding: const EdgeInsets.all(12),
        leading: CircleAvatar(
          child: Icon(icon),
        ),
        title: Text(
          title,
          style: const TextStyle(
            fontWeight: FontWeight.w800,
          ),
        ),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 5),
          child: Text(value),
        ),
      ),
    );
  }
}
