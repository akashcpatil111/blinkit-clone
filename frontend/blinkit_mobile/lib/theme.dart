import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  static const Color primary = Color(0xFFF9F506); // #f9f506
  static const Color backgroundLight = Color(0xFFF8F8F5); // #f8f8f5
  static const Color backgroundDark = Color(0xFF23220F); // #23220f (Not used in this iteration)
  static const Color textMain = Color(0xFF181811); // #181811
  static const Color textMuted = Color(0xFF8C8B5F); // #8c8b5f
  static const Color neutralSoft = Color(0xFFE5E5DF); // #e5e5df

  static ThemeData get lightTheme {
    return ThemeData(
      primaryColor: primary,
      scaffoldBackgroundColor: backgroundLight,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primary,
        primary: primary,
        background: backgroundLight,
        surface: Colors.white,
      ),
      useMaterial3: true,
      textTheme: GoogleFonts.plusJakartaSansTextTheme().apply(
        bodyColor: textMain,
        displayColor: textMain,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent, // Transparent for custom headers
        elevation: 0,
        titleTextStyle: TextStyle(
          color: textMain,
          fontWeight: FontWeight.bold,
          fontSize: 20,
        ),
        iconTheme: IconThemeData(color: textMain),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primary,
          foregroundColor: textMain,
          textStyle: const TextStyle(fontWeight: FontWeight.bold),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16), // Rounded Corners
          ),
          elevation: 0,
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.white,
        contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(30), // Pill shape for inputs
          borderSide: BorderSide.none,
        ),
        hintStyle: const TextStyle(color: textMuted),
      ),
    );
  }
}
