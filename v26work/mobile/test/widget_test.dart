import 'package:flutter_test/flutter_test.dart';
import 'package:wanasa_aldeerah/main.dart';

void main() {
  testWidgets('Wanasa V26 home page loads correctly', (tester) async {
    await tester.pumpWidget(const WanasaApp());

    expect(find.text('وناسة الديرة V25'), findsOneWidget);
    expect(find.text('منصة التجارة والتصفية السريعة'), findsOneWidget);

    expect(find.text('حساب العميل'), findsOneWidget);
    expect(find.text('حساب التاجر'), findsOneWidget);
    expect(find.text('لقطة الديرة'), findsOneWidget);
    expect(find.text('الأغذية الجافة'), findsOneWidget);
    expect(find.text('التجميل والعناية'), findsOneWidget);
  });
}
