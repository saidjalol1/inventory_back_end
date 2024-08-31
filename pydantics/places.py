from typing import List
from pydantic import BaseModel

class Market(BaseModel):
    name : str

class Province(BaseModel):
    name : str
    
class Region(BaseModel):
    name : str


class MarketOut(Market):
    id: int

class MarketIn(Market):
    region_id : int
    
    
class RegionOut(Region):
    id : int
    province_id : int
    markets : List[MarketOut]
    
    class Config:
        from_attributes = True
        
class RegionIn(BaseModel):
    name : str
    province_id : int


class ProvinceOut(Province):
    id : int
    regions : List[RegionOut]
    
    class Config:
        from_attributes = True
        