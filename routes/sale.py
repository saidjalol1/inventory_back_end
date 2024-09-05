from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import joinedload
from typing import List
import models
from ver_models import sale
from dependency.dependencies import database_dep, admin_user
from sqlalchemy import desc
from my_util_functions.stattistika import calculate_total_amount_for_product
# Create the FastAPI instance
app = APIRouter(
    tags = ["Sotuvlar"]
)

# Create a sale with sale items
@app.post("/sales", )
def create_sale(sale: sale.SaleOut, db = database_dep):
    
    db_sale = models.Sale(
        payment=sale.payment,
        debt=sale.debt,
        date_added=sale.date_added,
        shop_id=sale.shop_id,
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    for item in sale.items:
        pr = db.query(models.Product).filter(models.Product.qr_code_id == item.product_id).first()
        total_amount = calculate_total_amount_for_product(db, pr.id)
        
        error_messages = []
        
        if total_amount < item.quantity:
            error_messages.append(f"{pr.name} {total_amount} ta mavjud holos")
            continue
        
        db_sale_item = models.SaleItems(
            quantity=item.quantity,
            product_id=pr.id,
            sale_id=db_sale.id
        )
        db.add(db_sale_item)
        db.commit()

        tr = models.Transaction(
            product_id = pr.id,
            amount = item.quantity,
            transaction_type = "remove"
        )
        db.add(tr)
        db.commit()
    
    db.commit()
    db.refresh(db_sale)
    
    sale_data = db_sale
    sale_data.amount = db_sale.get_amount()
    sale_data.debt = db_sale.get_amount()
    
    db.commit()
    db.refresh(db_sale)
    if error_messages:
        return {"error":error_messages}
    else:
        return {"message":"Barchasi Qo'shildi"}

# Get all sales
@app.get("/sales", response_model=List[sale.Sale])
def read_sales(db = database_dep):
    sales = db.query(models.Sale).order_by(desc(models.Sale.id)).all()
    sales_with_amount = []
    for sale in sales:
        sale_data = sale
        sale_data.amount = sale.get_amount()  # Calculate the total amount
        sales_with_amount.append(sale_data)
        
    return sales_with_amount

@app.get("/debts", response_model=List[sale.Sale])
def read_sales(skip: int = 0, limit: int = 10, db = database_dep):
    sales = db.query(models.Sale).order_by(desc(models.Sale.id)).filter(models.Sale.debt > 0)
    sales = db.query(models.Sale).order_by(desc(models.Sale.id)).all()
    sales_with_amount = []
    for sale in sales:
        sale_data = sale
        sale_data.amount = sale.get_amount()  # Calculate the total amount
        sales_with_amount.append(sale_data)
        
    return sales_with_amount

# Get a specific sale by ID
@app.get("/sales/{sale_id}", response_model=sale.Sale)
def read_sale(sale_id: int, db = database_dep):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).options(joinedload(models.Sale.items)).first()
    
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    sale_data = sale
    sale_data.amount = sale.get_amount()
    return sale_data

# Update a sale
@app.put("/sales/{sale_id}")
def update_sale(sale_id: int, sale: sale.SaleUpdate, db = database_dep):
    db_sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    db_sale.payment += sale.payment
    db.commit()
    db.refresh(db_sale)
    
    db_sale.debt = db_sale.get_amount() - db_sale.payment
    db.commit()
    db.refresh(db_sale)
    print(db_sale.get_amount())
    print(db_sale.payment)
    
    return {"message":"success"}

# Delete a sale
@app.delete("/sales/{sale_id}")
def delete_sale(sale_id: int, db = database_dep):
    db_sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    db.query(models.SaleItems).filter(models.SaleItems.sale_id == sale_id).delete()
    db.delete(db_sale)
    db.commit()
    return {"message": "Sale deleted successfully"}

# Get all sales
@app.get("/sales/market/{id}", response_model=List[sale.Sale])
def read_sales(id:int,db = database_dep):
    sales = db.query(models.Sale).order_by(desc(models.Sale.id)).filter(models.Sale.shop_id == id).order_by(desc(models.Sale.id)).all()
    sales_with_amount = []
    for sale in sales:
        sale_data = sale
        sale_data.amount = sale.get_amount()  # Calculate the total amount
        sales_with_amount.append(sale_data)
        
    return sales_with_amount