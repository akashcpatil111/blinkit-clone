import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/models.dart';

class ApiService {
  // Use 10.0.2.2 for Android Emulator, localhost for iOS/Web.
  // In Codespaces, this will be replaced by the forwarded port URL.
  static const String baseUrl = 'http://10.0.2.2'; 
  static const String userServiceUrl = '$baseUrl:8001';
  static const String productServiceUrl = '$baseUrl:8002';
  static const String orderServiceUrl = '$baseUrl:8003';
  static const String deliveryServiceUrl = '$baseUrl:8004';

  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$userServiceUrl/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to login: ${response.body}');
    }
  }

  Future<void> register(String email, String password) async {
    final response = await http.post(
      Uri.parse('$userServiceUrl/register'),
       headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );

    if (response.statusCode != 201) {
      throw Exception('Failed to register: ${response.body}');
    }
  }

  Future<List<Product>> getProducts() async {
    final response = await http.get(Uri.parse('$productServiceUrl/products'));

    if (response.statusCode == 200) {
      List<dynamic> body = jsonDecode(response.body);
      return body.map((dynamic item) => Product.fromJson(item)).toList();
    } else {
      throw Exception('Failed to load products');
    }
  }

  Future<dynamic> createOrder(String userId, List<String> productIds, double total) async {
    final response = await http.post(
      Uri.parse('$orderServiceUrl/order/create'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'user_id': userId,
        'product_ids': productIds,
        'total': total,
      }),
    );

    if (response.statusCode == 201) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to create order');
    }
  }
  
  // Actually fetches from Delivery Service to get the status
  Future<Map<String, dynamic>> getDeliveryStatus(String orderId) async {
     final response = await http.get(Uri.parse('$deliveryServiceUrl/order/$orderId/status'));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load delivery status');
    }
  }
}
