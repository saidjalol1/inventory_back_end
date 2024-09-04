from fastapi import APIRouter, HTTPException
from typing import List
import ver_models
import models
from dependency.dependencies import super_user, admin_user, user, database_dep
import ver_models.expance
from sqlalchemy import desc


app = APIRouter(
    prefix="/expance",
    tags = ["Expance"]
)


@app.get("/expances", response_model=List[ver_models.expance.Expance])
def read_expances(db = database_dep):
    expances = db.query(models.Expances).order_by(desc(models.Expances.id)).all()
    return expances


@app.post("/expance/add")
def create_expance(expance:ver_models.expance.ExpanceCreate, db = database_dep, us= admin_user):
    db_expance = models.Expances(**expance.model_dump())
    db.add(db_expance)
    db.commit()
    db.refresh(db_expance)
    return {"message":"success"}


@app.delete("/expances/{expance_id}")
def delete_expance(expance_id: int, db = database_dep, us = admin_user):
    db_expance = db.query(models.Expances).filter(models.Expances.id == expance_id).first()
    if db_expance is None:
        raise HTTPException(status_code=404, detail="Expance not found")
    db.delete(db_expance)
    db.commit()
    return {"detail": "Expance deleted"}


@app.patch("/expances/{expance_id}", response_model=ver_models.expance.Expance)
def update_expance(expance_id: int, expance_update:ver_models.expance.ExpanceBase, db = database_dep):
    db_expance = db.query(models.Expances).filter(models.Expances.id == expance_id).first()
    if db_expance is None:
        raise HTTPException(status_code=404, detail="Expance not found")
    
    update_data = expance_update.model_dump(exclude_unset=True)  # Exclude fields not provided in the request
    
    for key, value in update_data.items():
        setattr(db_expance, key, value)
    
    db.commit()
    db.refresh(db_expance)
    return db_expance

    


@app.post("/money_transactions")
def create_money_transaction(money_transaction: ver_models.expance.MoneyTransactionCreate, db = database_dep):
    db_money_transaction = models.MoneyTransactions(**money_transaction.model_dump())
    db.add(db_money_transaction)
    db.commit()
    db.refresh(db_money_transaction)
    return db_money_transaction