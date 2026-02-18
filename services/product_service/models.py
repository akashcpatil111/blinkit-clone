from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class Product(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    price: float
    category: str
    image_url: str
    description: Optional[str] = None
    quantity: Optional[str] = None
    availability: bool = True

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Milk",
                "price": 2.5,
                "category": "Dairy",
                "image_url": "http://example.com/milk.jpg",
                "description": "Fresh milk",
                "quantity": "1L",
                "availability": True
            }
        }
