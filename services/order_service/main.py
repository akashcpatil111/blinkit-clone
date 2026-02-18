from fastapi import FastAPI, HTTPException
from typing import List
from .database import db
from .models import Order
from bson import ObjectId

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/orders", status_code=201)
async def create_order(order: Order):
    new_order = await db.orders.insert_one(order.dict(by_alias=True))
    created_order = await db.orders.find_one({"_id": new_order.inserted_id})
    return created_order

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    order = await db.orders.find_one({"_id": ObjectId(order_id)})
    if order:
        return order
    raise HTTPException(status_code=404, detail="Order not found")

# --- Cart APIs (Compliance) ---
# Note: The Flutter app uses client-side state for the cart (Provider), 
# but these APIs are implemented to strictly meet the backend assignment requirements.

class CartItem(BaseModel):
    user_id: str
    product_id: str
    quantity: int

@app.post("/cart/add")
async def add_to_cart(item: CartItem):
    # Upsert item in "carts" collection
    await db.carts.update_one(
        {"user_id": item.user_id, "product_id": item.product_id},
        {"$inc": {"quantity": item.quantity}},
        upsert=True
    )
    return {"msg": "Item added to cart"}

@app.post("/cart/remove")
async def remove_from_cart(item: CartItem):
    await db.carts.delete_one({"user_id": item.user_id, "product_id": item.product_id})
    return {"msg": "Item removed from cart"}

@app.get("/cart/{user_id}")
async def get_cart(user_id: str):
    cursor = db.carts.find({"user_id": user_id})
    cart_items = await cursor.to_list(length=100)
    return cart_items

@app.get("/")
def read_root():
    return {"Hello": "Order Service"}
