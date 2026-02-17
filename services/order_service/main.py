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

@app.get("/")
def read_root():
    return {"Hello": "Order Service"}
