from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import auth.auth_main
from crud import CreateObject
from pydantics import places, user_models
import models
from database import db_conf
import auth

super_user = Depends(auth.auth_main.is_super_user)
admin_user : user_models.User = Depends(auth.auth_main.is_admin)
user : user_models.User = Depends(auth.auth_main.is_admin)

market_crud = APIRouter(
    prefix="/markets",
    tags = ["Markets"]
)


# @market_crud.post("/province/add")
# async def province_add(object : places.Province, db: Session = Depends(db_conf.get_db)):
#     try:
#         obj = models.Province(**object.model_dump())
#         db.add(obj)
#         db.commit()
#         db.refresh(obj)
#         return obj  
#     except Exception as e:
#         return {"error":e}

@market_crud.get("/province/get", response_model=List[places.ProvinceOut])
async def province_add(db: Session = Depends(db_conf.get_db)):
    try:
        obj = db.query(models.Province).all()
        return obj  
    except Exception as e:
        return {"error":e}
    
    
@market_crud.get("/regions/get/{id}", response_model=List[places.RegionOut])
async def regions_get(id:int,db: Session = Depends(db_conf.get_db)):
    try:
        obj = db.query(models.Region).filter(models.Region.province_id == id)
        return obj  
    except Exception as e:
        return {"error":e}
    
@market_crud.post("/region/add")
async def province_add(object :places.RegionIn, db: Session = Depends(db_conf.get_db), us = admin_user):
    try:
        obj = models.Region(**object.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj  
    except Exception as e:
        return {"error":"Oldin qo'shilgan"}


@market_crud.post("/market/add")
async def province_add(object :places.MarketIn, db: Session = Depends(db_conf.get_db), us = admin_user ):
    try:
        obj = models.Markets(**object.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj  
    except Exception as e:
        return {"error":"Oldin qo'shilgan"}