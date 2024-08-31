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
        orm_mode = True