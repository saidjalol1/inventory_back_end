from fastapi import APIRouter
from typing import List
from ver_models import places
import models
from dependency.dependencies import super_user, admin_user, user, database_dep

market_crud = APIRouter(
    prefix="/markets",
    tags = ["Markets"]
)


@market_crud.get("/province/get", response_model=List[places.ProvinceOut])
async def province_add(db = database_dep):
    try:
        obj = db.query(models.Province).all()
        return obj  
    except Exception as e:
        return {"error":e}
    
    
@market_crud.get("/regions/get/{id}", response_model=List[places.RegionOut])
async def regions_get(id:int,db = database_dep):
    try:
        obj = db.query(models.Region).filter(models.Region.province_id == id)
        return obj  
    except Exception as e:
        return {"error":e}
    

@market_crud.get("/region/get/{id}", response_model=places.RegionOut)
async def regions(id:int,db = database_dep):
    try:
        obj = db.query(models.Region).filter(models.Region.id == id).first()
        return obj  
    except Exception as e:
        return {"error":e}
    
    
@market_crud.post("/region/add")
async def province_add(object :places.RegionIn, db = database_dep, us = admin_user):
    try:
        obj = models.Region(**object.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj  
    except Exception as e:
        return {"error":"Oldin qo'shilgan"}


# @market_crud.get("/markets/get/{id}", response_model=places.RegionOut)
# async def regions(id:int,db = database_dep):
#     try:
#         obj = db.query(models.Region).filter(models.Region.id == id).first()
#         return obj  
#     except Exception as e:
#         return {"error":e}


@market_crud.post("/market/add")
async def province_add(object :places.MarketIn, db = database_dep, us = admin_user ):
    try:
        obj = models.Markets(**object.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj  
    except Exception as e:
        return {"error":"Oldin qo'shilgan"}
    
    
# @market_crud.post("/province/add")
# async def province_add(object : places.Province, db = database_dep):
#     try:
#         obj = models.Province(**object.model_dump())
#         db.add(obj)
#         db.commit()
#         db.refresh(obj)
#         return obj  
#     except Exception as e:
#         return {"error":e}