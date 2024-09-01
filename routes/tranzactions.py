from fastapi import APIRouter, HTTPException
from typing import List
import ver_models
import models
from dependency.dependencies import admin_user, database_dep
import ver_models.expance
import ver_models.tranzactions
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
app = APIRouter(
    tags = ["Tranzactions"]
)

@app.get("/store")
def store(db = database_dep):
    transactions = db.query(models.Transaction).filter(models.Transaction.amount > 0).options(joinedload(models.Transaction.product)).order_by(desc(models.Transaction.id)).all()
    response = []
    product_data_map = {}

    for transaction in transactions:
        product_id = transaction.product_id
        if product_id not in product_data_map:
            # Initialize data for a new product
            product_data_map[product_id] = {
                "id": transaction.id,
                "product_id": product_id,
                "name": transaction.product.name,
                "sale_price": transaction.product.sale_price,
                "base_price": transaction.product.base_price,
                "quantity": 0,
                "overall_price": 0
            }
        
        # Update the quantity based on transaction type
        if transaction.transaction_type == "add":
            product_data_map[product_id]["quantity"] += transaction.amount
        elif transaction.transaction_type == "remove":
            product_data_map[product_id]["quantity"] -= transaction.amount
    
    # Calculate the overall price after all transactions have been processed
    for product_data in product_data_map.values():
        product_data["overall_price"] = product_data["base_price"] * product_data["quantity"]
        response.append(product_data)

    return response

@app.get("/tranzactions", response_model=List[ver_models.tranzactions.TransactionOut])
def read_transactions(db = database_dep):
    transactions = db.query(models.Transaction).order_by(desc(models.Transaction.id)).all()
    return transactions

@app.post("/tranzactions/add")
def create_transaction(transaction: ver_models.tranzactions.TransactionCreate, db = database_dep):
    _product_ = db.query(models.Product).filter(models.Product.qr_code_id == transaction.qr_code_id).first()
    if _product_ :
        db_transaction = models.Transaction(
            amount = transaction.amount,
            transaction_type = "add",
            product_id = _product_.id
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
    else:
        return {"error": "Mahsulot Topilmadi"}
    return {"error":"Qo'shildi"}