from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int


class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True
