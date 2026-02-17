import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/models.dart';

class AuthProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  String? _token;
  bool get isAuthenticated => _token != null;

  Future<void> login(String email, String password) async {
    try {
      final data = await _apiService.login(email, password);
      _token = data['access_token'];
      notifyListeners();
    } catch (e) {
      rethrow;
    }
  }

  Future<void> register(String email, String password) async {
    try {
      await _apiService.register(email, password);
    } catch (e) {
      rethrow;
    }
  }

  void logout() {
    _token = null;
    notifyListeners();
  }
}
