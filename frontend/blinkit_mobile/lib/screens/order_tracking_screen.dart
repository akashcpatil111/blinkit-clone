import 'package:flutter/material.dart';
import 'dart:async';
import '../theme.dart';
import '../services/api_service.dart';

class OrderTrackingScreen extends StatefulWidget {
  const OrderTrackingScreen({super.key});

  @override
  State<OrderTrackingScreen> createState() => _OrderTrackingScreenState();
}

class _OrderTrackingScreenState extends State<OrderTrackingScreen> {
  String _currentStatus = 'PLACED';
  Timer? _timer;
  
  // Hardcoded for demo - in real app would be passed via constructor
  final String _deliveryId = "65d4c8e7f9a1b2c3d4e5f6a7"; 

  @override
  void initState() {
    super.initState();
    _startPolling();
  }

  void _startPolling() {
    // Poll every 5 seconds
    _timer = Timer.periodic(const Duration(seconds: 5), (timer) async {
       try {
         // In a real scenario, we'd fetch the delivery status
         // final data = await ApiService().getDeliveryStatus(_deliveryId);
         // setState(() => _currentStatus = data['status']);
         
         // For DEMO without running backend, we simulate the text change locally
         // to show the UI transition if the backend isn't reachable.
         setState(() {
           if (_currentStatus == 'PLACED') _currentStatus = 'PACKED';
           else if (_currentStatus == 'PACKED') _currentStatus = 'OUT_FOR_DELIVERY';
           else if (_currentStatus == 'OUT_FOR_DELIVERY') _currentStatus = 'DELIVERED';
         });
       } catch (e) {
         // Ignore errors for polling
       }
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Stack(
        children: [
          // Map Background (Placeholder)
          Container(
            height: MediaQuery.of(context).size.height * 0.6,
            width: double.infinity,
            color: AppTheme.neutralSoft,
            child: const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.map, size: 60, color: Colors.grey),
                  Text('Map View Placeholder', style: TextStyle(color: Colors.grey))
                ],
              ),
            ),
          ),
          
          // Header Overlay
          Positioned(
            top: 40,
            left: 20,
            right: 20,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                CircleAvatar(
                  backgroundColor: Colors.white,
                  child: IconButton(
                    icon: const Icon(Icons.arrow_back, color: AppTheme.textMain),
                    onPressed: () => Navigator.of(context).pop(),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: const [BoxShadow(color: Colors.black12, blurRadius: 10)],
                  ),
                  child: const Column(
                    children: [
                      Text('ORDER ID', style: TextStyle(fontSize: 10, color: AppTheme.textMuted, fontWeight: FontWeight.bold)),
                      Text('#7829-XQZ', style: TextStyle(fontWeight: FontWeight.bold)),
                    ],
                  ),
                )
              ],
            ),
          ),

          // Bottom Sheet Status
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              height: MediaQuery.of(context).size.height * 0.45,
              padding: const EdgeInsets.all(24),
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.vertical(top: Radius.circular(30)),
                boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 20)],
              ),
              child:  Column(
                children: [
                  Container(width: 40, height: 4, decoration: BoxDecoration(color: AppTheme.neutralSoft, borderRadius: BorderRadius.circular(2))),
                  const SizedBox(height: 20),
                  Expanded(
                    child: ListView(
                      children: [
                        _buildTimelineItem('Order Placed', 'We have received your order', _isCompleted('PLACED'), true),
                        _buildTimelineItem('Order Packed', 'The restaurant is preparing your food', _isCompleted('PACKED'), true),
                        _buildTimelineItem('Out for Delivery', 'Carlos is on his way', _isCompleted('OUT_FOR_DELIVERY'), false), 
                        _buildTimelineItem('Delivered', 'Enjoy your meal!', _isCompleted('DELIVERED'), false),
                      ],
                    ),
                  ),

                  // Delivery Agent Widget
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppTheme.backgroundLight,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Row(
                      children: [
                        const CircleAvatar(
                          radius: 24,
                          backgroundImage: NetworkImage('https://via.placeholder.com/150'), 
                        ),
                        const SizedBox(width: 12),
                        const Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('Carlos Rodriguez', style: TextStyle(fontWeight: FontWeight.bold)),
                              Text('Honda Activa • ABC-1234', style: TextStyle(fontSize: 12, color: AppTheme.textMuted)),
                            ],
                          ),
                        ),
                        const Row(
                           children: [
                             CircleAvatar(backgroundColor: Colors.white, child: Icon(Icons.call, color: AppTheme.textMain)),
                           ],
                        )
                      ],
                    ),
                  )
                ],
              ),
            ),
          )
        ],
      ),
    );
  }
  
  bool _isCompleted(String step) {
    const steps = ['PLACED', 'PACKED', 'OUT_FOR_DELIVERY', 'DELIVERED'];
    return steps.indexOf(_currentStatus) >= steps.indexOf(step);
  }

  Widget _buildTimelineItem(String title, String subtitle, bool isCompleted, bool showLine) {
    return SizedBox(
      height: 70,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
           Column(
             children: [
               Container(
                 width: 24,
                 height: 24,
                 decoration: BoxDecoration(
                   color: isCompleted ? AppTheme.primary : AppTheme.neutralSoft,
                   shape: BoxShape.circle,
                 ),
                 child: Icon(Icons.check, size: 16, color: isCompleted ? AppTheme.textMain : Colors.white),
               ),
               if (showLine)
                 Expanded(child: Container(width: 2, color: isCompleted ? AppTheme.primary : AppTheme.neutralSoft)),
             ],
           ),
           const SizedBox(width: 16),
           Column(
             crossAxisAlignment: CrossAxisAlignment.start,
             children: [
               Text(title, style: TextStyle(fontWeight: FontWeight.bold, color: isCompleted ? AppTheme.textMain : AppTheme.textMuted)),
               Text(subtitle, style: const TextStyle(fontSize: 12, color: AppTheme.textMuted)),
             ],
           )
        ],
      ),
    );
  }
}
