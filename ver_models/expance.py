from pydantic import BaseModel
from typing import Optional
from datetime import date

class ExpanceBase(BaseModel):
    name: str
    amount: int
    date_added: date

class ExpanceCreate(ExpanceBase):
    pass

class Expance(ExpanceBase):
    id: int

    class Config:
        from_attributes = True
        

class MoneyTransactionBase(BaseModel):
    amount: int
    date: date

class MoneyTransactionCreate(MoneyTransactionBase):
    pass

class MoneyTransactionResponse(MoneyTransactionBase):
    id: int

    class Config:
        from_attributes = True
