from pydantic import BaseModel

class OrderBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    total_price: float

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int

    class Config:
        orm_mode = True