from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from crud import CreateObject
from pydantics import places
import models
from database.db_conf import get_db


market_crud = APIRouter(
    prefix="/markets"
)


@market_crud.post("/province/add")
async def province_add(object : places.ProvinceIn, db: Session = Depends(get_db)):
    try:
        obj = models.Province(**object.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj  
    except Exception as e:
        return {"error":"Invalid data"}
    
    
@market_crud.post("/region/add")
async def province_add(object :places.RegionIn, db: Session = Depends(get_db)):
    try:
        obj = models.Region(**object.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj  
    except Exception as e:
        return {"error":"Invalid data"}


@market_crud.post("/market/add")
async def province_add(object :places.MarketIn, db: Session = Depends(get_db)):
    try:
        obj = models.Markets(**object.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj  
    except Exception as e:
        return {"error":"Invalid data"}