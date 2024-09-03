from datetime import date, datetime
import models

from sqlalchemy import func, extract, desc

current = datetime.now()

def sales(db):
    sale_obj = db.query(models.Sale).filter(
        extract('year', models.Sale.date_added) == current.year,
        extract('month', models.Sale.date_added) == current.month   
    ).all()
    responce1 = sum([i.get_amount() for i in sale_obj])
    responce2 = sum([i.get_in() for i in sale_obj])
    return {
        "revenue":responce1,
        "income":responce2,
    }
    

def get_most_bought_product(db_session):
    current_year = datetime.now().year
    current_month = datetime.now().month

    most_bought_product = db_session.query(
        models.SaleItems.product_id,
        func.sum(models.SaleItems.quantity).label('total_quantity')
    ).join(models.Sale).filter(
        extract('year', models.Sale.date_added) == current_year,
        extract('month', models.Sale.date_added) == current_month
    ).group_by(models.SaleItems.product_id).order_by(desc('total_quantity')).first()

    if most_bought_product:
        product = db_session.query(models.Product).get(most_bought_product.product_id)
        return product.name

    return None, 0
    

def get_most_buying_shop(db_session):
    current_year = datetime.now().year
    current_month = datetime.now().month

    most_buying_shop = db_session.query(
        models.Sale.shop_id,
        func.count(models.Sale.id).label('total_sales')
    ).filter(
        extract('year', models.Sale.date_added) == current_year,
        extract('month', models.Sale.date_added) == current_month
    ).group_by(models.Sale.shop_id).order_by(desc('total_sales')).first()

    if most_buying_shop:
        shop = db_session.query(models.Markets).get(most_buying_shop.shop_id)
        return shop.name

    return None, 0

def get_sales_by_month(db):
    current_year = datetime.now().year
    sales_by_month = db.query(
        extract('month', models.Sale.date_added).label('month'),
        func.sum(models.Sale.payment).label('total_sales')
    ).filter(
        extract('year', models.Sale.date_added) == current_year
    ).group_by('month').all()

    # Prepare the response data
    sales_data = [0] * 12  # Initialize a list with 12 zeroes (for 12 months)
    for sale in sales_by_month:
        sales_data[int(sale.month) - 1] = sale.total_sales

    return {"series": [{"name": "Sales", "data": sales_data}]}

def calculate_total_price(db):
  
    total_added = db.query(
        func.sum(models.Transaction.amount * models.Product.base_price)
    ).join(models.Product).filter(models.Transaction.transaction_type == "add").scalar() or 0

   
    total_removed = db.query(
        func.sum(models.Transaction.amount * models.Product.base_price)
    ).join(models.Product).filter(models.Transaction.transaction_type == "remove").scalar() or 0

    total_price = total_added - total_removed
    
    return total_price 

def moneys(db):
    total_money_given = db.query(models.MoneyTransactions).order_by(desc(models.MoneyTransactions.date)).all()
    return total_money_given

