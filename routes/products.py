from fastapi import APIRouter, HTTPException
from typing import List
from ver_models import product_m
import models
from dependency.dependencies import admin_user, database_dep
from sqlalchemy import desc
app = APIRouter(
    tags=["Products"]
)

@app.get("/products", response_model=List[product_m.ProductOut])
def read_products(db = database_dep):
    products = db.query(models.Product).order_by(desc(models.Product.id)).all()
    return products


@app.get("/products/{product_id}", response_model = product_m.ProductOut)
def read_product(product_id: int, db = database_dep):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.post("/products/add", response_model=product_m.ProductOut)
def create_product(product:product_m.ProductCreate, db = database_dep):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/products/update/{product_id}", response_model=product_m.ProductOut)
def update_product(product_id: int, product:product_m.ProductUpdate, db = database_dep):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for var, value in vars(product).items():
        if value is not None:
            setattr(db_product, var, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/products/delete/{product_id}", response_model=product_m.ProductOut)
def delete_product(product_id: int, db = database_dep):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return db_product
