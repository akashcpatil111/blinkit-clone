import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/models.dart';
import '../providers/cart_provider.dart';
import '../theme.dart';

class ProductDetailScreen extends StatelessWidget {
  final Product product;

  const ProductDetailScreen({super.key, required this.product});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundLight,
      body: Stack(
        children: [
          // Hero Image
          SizedBox(
            height: MediaQuery.of(context).size.height * 0.5,
            width: double.infinity,
            child: Image.network(
              product.imageUrl,
              fit: BoxFit.cover,
              errorBuilder: (ctx, _, __) => Container(color: AppTheme.neutralSoft),
            ),
          ),
          
          // Navigation Overlay
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
                const Row(
                  children: [
                    CircleAvatar(backgroundColor: Colors.white, child: Icon(Icons.share, color: AppTheme.textMain)),
                    SizedBox(width: 10),
                    CircleAvatar(backgroundColor: Colors.white, child: Icon(Icons.favorite_border, color: AppTheme.textMain)),
                  ],
                )
              ],
            ),
          ),

          // Content Sheet
          DraggableScrollableSheet(
            initialChildSize: 0.55,
            minChildSize: 0.55,
            maxChildSize: 0.9,
            builder: (context, scrollController) {
              return Container(
                decoration: const BoxDecoration(
                  color: AppTheme.backgroundLight,
                  borderRadius: BorderRadius.vertical(top: Radius.circular(30)),
                  boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 20, offset: Offset(0, -5))],
                ),
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 30),
                  child: ListView(
                    controller: scrollController,
                    children: [
                      Text(product.name, style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: AppTheme.textMain)),
                      const SizedBox(height: 10),
                      Row(
                        children: [
                          Text('\$${product.price}', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AppTheme.textMain)),
                          const SizedBox(width: 10),
                          Text('\$${(product.price * 1.2).toStringAsFixed(2)}', style: const TextStyle(fontSize: 18, decoration: TextDecoration.lineThrough, color: AppTheme.textMuted)),
                          const SizedBox(width: 10),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                            decoration: BoxDecoration(color: AppTheme.primary.withOpacity(0.2), borderRadius: BorderRadius.circular(20)),
                            child: const Text('20% OFF', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 10, color: AppTheme.textMain)),
                          )
                        ],
                      ),
                      const SizedBox(height: 20),
                      Divider(color: AppTheme.neutralSoft.withOpacity(0.5)),
                      const SizedBox(height: 20),
                      const Text('Product Details', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 10),
                      const Text(
                        'Fresh and high-quality product sourced directly from the best farms. Enjoy the natural taste and nutrition in every bite.',
                        style: TextStyle(color: AppTheme.textMuted, height: 1.5),
                      ),
                      const SizedBox(height: 30),
                      const Text('Quantity', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 10),
                      Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(4),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(30),
                              border: Border.all(color: AppTheme.neutralSoft),
                            ),
                            child: Row(
                              children: [
                                IconButton(icon: const Icon(Icons.remove), onPressed: () {}),
                                const Text('1', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                                IconButton(icon: const Icon(Icons.add), onPressed: () {}),
                              ],
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 100), // Spacing for bottom button
                    ],
                  ),
                ),
              );
            },
          ),

          // Bottom CTA
          Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            child: Container(
              padding: const EdgeInsets.all(24),
              decoration: const BoxDecoration(
                color: Colors.white,
                border: Border(top: BorderSide(color: AppTheme.neutralSoft)),
              ),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      border: Border.all(color: AppTheme.primary, width: 2),
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: const Icon(Icons.shopping_bag_outlined, color: AppTheme.primary),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: ElevatedButton(
                      onPressed: () {
                        Provider.of<CartProvider>(context, listen: false).addItem(product);
                        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Added to Cart!')));
                      },
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                      ),
                      child: const Text('ADD TO CART', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
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
}
