from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    brand: str | None = None
    article_number: str | None = None
    price: float

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True