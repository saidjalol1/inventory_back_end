from pydantic import BaseModel
from typing import Optional
from datetime import date
from .product_m import ProductOut

class TransactionCreate(BaseModel):
    qr_code_id : str
    amount: int


class TransactionOut(BaseModel):
    id: int
    product_id : int
    product : ProductOut
    transaction_type: str
    amount: int
    date : date
    
    class Config:
        orm_mode = True