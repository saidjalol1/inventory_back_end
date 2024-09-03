from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from .product_m import ProductOut
from .places import MarketOut
# Schema for SaleItems
class SaleItemBase(BaseModel):
    quantity: int
    product_id: int

class SaleItemCreate(SaleItemBase):
    pass

class SaleItem(SaleItemBase):
    id: int
    sale_id: int
    product : ProductOut
    

    class Config:
        from_attributes = True

# Schema for Sale
class SaleBase(BaseModel):
    payment: int
    debt: int
    date_added: date
    shop_id: int
    shop : MarketOut

class SaleCreate(SaleBase):
    items: List[SaleItemCreate]


class SaleCreation(BaseModel):
    payment: int
    debt: int
    date_added: date
    shop_id: int

class SaleOut(SaleCreation):
    items: List[SaleItemCreate]

class Sale(SaleBase):
    id: int
    items: List[SaleItem]
    amount: int
    
    class Config:
        from_attributes = True
        
class SaleUpdate(BaseModel):
    payment : int

    class Config:
        from_attributes = True
