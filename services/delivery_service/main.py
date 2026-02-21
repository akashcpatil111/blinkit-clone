from fastapi import FastAPI, HTTPException
from .database import db
from .models import Delivery, DeliveryStatus
from bson import ObjectId

app = FastAPI()

from fastapi.responses import RedirectResponse

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/deliveries", status_code=201)
async def create_delivery(delivery: Delivery):
    new_delivery = await db.deliveries.insert_one(delivery.dict(by_alias=True))
    created_delivery = await db.deliveries.find_one({"_id": new_delivery.inserted_id})
    return created_delivery

@app.get("/order/{order_id}/status", response_model=Delivery)
async def get_delivery(order_id: str):
    delivery = await db.deliveries.find_one({"order_id": order_id})
    if delivery:
        return delivery
    raise HTTPException(status_code=404, detail="Delivery not found")

@app.post("/order/{order_id}/update-status")
async def update_delivery_status(order_id: str, status: DeliveryStatus):
    result = await db.deliveries.update_one(
        {"order_id": order_id}, {"$set": {"status": status}}
    )
    if result.modified_count == 1:
        return {"msg": "Status updated"}
    raise HTTPException(status_code=404, detail="Delivery not found")

import asyncio
from typing import List

async def simulate_delivery_updates():
    while True:
        # Find all deliveries that are not DELIVERED
        active_deliveries = db.deliveries.find({"status": {"$ne": "DELIVERED"}})
        async for delivery in active_deliveries:
            current_status = delivery["status"]
            next_status = None
            
            if current_status == "PLACED":
                next_status = "PACKED"
            elif current_status == "PACKED":
                next_status = "OUT_FOR_DELIVERY"
            elif current_status == "OUT_FOR_DELIVERY":
                next_status = "DELIVERED"
            
            if next_status:
                await db.deliveries.update_one(
                    {"_id": delivery["_id"]},
                    {"$set": {"status": next_status}}
                )
                print(f"Updated delivery {delivery['_id']} status to {next_status}")
        
        await asyncio.sleep(30)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulate_delivery_updates())
