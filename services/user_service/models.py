from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from bson import ObjectId

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "India"
    is_default: bool = False

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str
    addresses: List[Address] = []

class UserResponse(UserBase):
    id: str = Field(..., alias="_id")
    addresses: List[Address] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
