from fastapi import FastAPI, HTTPException
from .database import db
from .models import Delivery, DeliveryStatus
from bson import ObjectId

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/deliveries", status_code=201)
async def create_delivery(delivery: Delivery):
    new_delivery = await db.deliveries.insert_one(delivery.dict(by_alias=True))
    created_delivery = await db.deliveries.find_one({"_id": new_delivery.inserted_id})
    return created_delivery

@app.get("/deliveries/{delivery_id}", response_model=Delivery)
async def get_delivery(delivery_id: str):
    delivery = await db.deliveries.find_one({"_id": ObjectId(delivery_id)})
    if delivery:
        return delivery
    raise HTTPException(status_code=404, detail="Delivery not found")

@app.put("/deliveries/{delivery_id}/status")
async def update_delivery_status(delivery_id: str, status: DeliveryStatus):
    result = await db.deliveries.update_one(
        {"_id": ObjectId(delivery_id)}, {"$set": {"status": status}}
    )
    if result.modified_count == 1:
        return {"msg": "Status updated"}
    raise HTTPException(status_code=404, detail="Delivery not found")
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
            
            if current_status == "PENDING":
                next_status = "ASSIGNED"
            elif current_status == "ASSIGNED":
                next_status = "PICKED_UP"
            elif current_status == "PICKED_UP":
                next_status = "DELIVERED"
            
            if next_status:
                await db.deliveries.update_one(
                    {"_id": delivery["_id"]},
                    {"$set": {"status": next_status}}
                )
                print(f"Updated delivery {delivery['_id']} text to {next_status}")
        
        await asyncio.sleep(30)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulate_delivery_updates())
