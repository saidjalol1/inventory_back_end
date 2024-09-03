from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    base_price: Optional[int] = 0
    sale_price: Optional[int] = 0
    qr_code_id: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
