from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from bson import ObjectId

class OrderStatus(str, Enum):
    PLACED = "PLACED"
    PACKED = "PACKED"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Order(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    user_id: str
    product_ids: List[str]
    total: float
    status: OrderStatus = OrderStatus.PLACED

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "user_id_here",
                "product_ids": ["prod_1", "prod_2"],
                "total": 50.5,
                "status": "PLACED"
            }
        }
