import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/auth_provider.dart';
import 'providers/cart_provider.dart';
import 'theme.dart';
import 'screens/order_tracking_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => CartProvider()),
      ],
      child: MaterialApp(
        title: 'Blinkit Clone',
        theme: AppTheme.lightTheme,
        home: const LoginScreen(),
        routes: {
          '/home': (ctx) => const HomeScreen(),
          '/tracking': (ctx) => const OrderTrackingScreen(),
        },
      ),
    );
  }
}
