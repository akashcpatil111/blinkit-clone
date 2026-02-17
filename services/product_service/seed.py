import asyncio
import os
import motor.motor_asyncio

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.blinkit_commerce

sample_products = [
    {"name": "Milk", "price": 2.5, "category": "Dairy", "image_url": "https://example.com/milk.jpg"},
    {"name": "Bread", "price": 1.5, "category": "Bakery", "image_url": "https://example.com/bread.jpg"},
    {"name": "Eggs", "price": 3.0, "category": "Dairy", "image_url": "https://example.com/eggs.jpg"},
    {"name": "Butter", "price": 4.0, "category": "Dairy", "image_url": "https://example.com/butter.jpg"},
    {"name": "Cheese", "price": 5.0, "category": "Dairy", "image_url": "https://example.com/cheese.jpg"},
    {"name": "Apples", "price": 2.0, "category": "Fruits", "image_url": "https://example.com/apples.jpg"},
    {"name": "Bananas", "price": 1.2, "category": "Fruits", "image_url": "https://example.com/bananas.jpg"},
    {"name": "Tomatoes", "price": 1.8, "category": "Vegetables", "image_url": "https://example.com/tomatoes.jpg"},
    {"name": "Potatoes", "price": 1.0, "category": "Vegetables", "image_url": "https://example.com/potatoes.jpg"},
    {"name": "Onions", "price": 1.1, "category": "Vegetables", "image_url": "https://example.com/onions.jpg"},
]

async def seed_products():
    await db.products.delete_many({})
    result = await db.products.insert_many(sample_products)
    print(f"Inserted {len(result.inserted_ids)} products")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(seed_products())
