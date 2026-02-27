from pydantic import BaseModel, Field
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=1, max_length=200)
    item_name: str = Field(min_length=1, max_length=200)
    quantity: int = Field(ge=1, le=100000)


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderOut(BaseModel):
    id: int
    customer_name: str
    item_name: str
    quantity: int
    status: OrderStatus  

    class Config:
        from_attributes = True