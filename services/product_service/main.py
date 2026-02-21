from fastapi import FastAPI, HTTPException
from .database import db
from .models import Product
from typing import List, Optional

app = FastAPI()

from fastapi.responses import RedirectResponse

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/products", response_model=List[Product])
async def get_products(category: Optional[str] = None, q: Optional[str] = None):
    query = {}
    if category:
        query["category"] = category
    if q:
        query["name"] = {"$regex": q, "$options": "i"}
        
    products = await db.products.find(query).to_list(100)
    return products

@app.get("/categories", response_model=List[str])
async def get_categories():
    categories = await db.products.distinct("category")
    return categories

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db.products.find_one({"_id": product_id})
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")
