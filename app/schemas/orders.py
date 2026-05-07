from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


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
class OrderEventOut(BaseModel):
    id: int
    order_id: int
    changed_by_user_id: int
    old_status: str
    new_status: str
    note: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True