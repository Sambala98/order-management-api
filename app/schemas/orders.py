from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=1, max_length=200)
    item_name: str = Field(min_length=1, max_length=200)
    quantity: int = Field(ge=1, le=100000)


class OrderOut(BaseModel):
    id: int
    customer_name: str
    item_name: str
    quantity: int

    class Config:
        from_attributes = True