from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date, DateTime
from sqlalchemy.orm import relationship
from database.db_conf import Base, current_time
from sqlalchemy import desc

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_super_user = Column(Boolean, default=False)
    admin_id = Column(Integer, ForeignKey("users.id"))
    admin = relationship("User", remote_side=[id], backref="subordinates")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', is_admin={self.is_admin}, is_super_user={self.is_super_user})>"
    

class Province(Base):
    __tablename__ = "provinces"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    regions = relationship("Region", back_populates="province")
    

class Region(Base):
    __tablename__ = "regions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    province_id = Column(Integer, ForeignKey("provinces.id"))
    
    province = relationship("Province", back_populates="regions")
    markets = relationship("Markets", back_populates="region")
    
    
class Markets(Base):
    __tablename__ = "markets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"))
    region = relationship("Region", back_populates="markets")
    sales = relationship("Sale", back_populates="shop")


class QrCode(Base):
    __tablename__ = "codes"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True)
    qr_code_image = Column(String, unique=True)
    
    
    
    
class Expances(Base):
    __tablename__ = "expances"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    amount = Column(Integer, nullable=True)
    date_added = Column(Date)
    
    __table_args__ = (
        {'order_by': [desc('date_added')]},
    )
    

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    base_price = Column(Integer, default=0)
    sale_price = Column(Integer, default=0)
    amount = Column(Integer, default=0)
    qr_code_id = Column(String(250), nullable=False)

    sales = relationship("SaleItems", back_populates="product")
    

    __table_args__ = (
        {'order_by': [desc('id')]},
    )
    
    def __str__(self):
        return self.name


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    transaction_type = Column(String(250), nullable=False)
    amount = Column(Integer, nullable=False)
    date = Column(Date, default=current_time)

    product = relationship("Product")

    __table_args__ = (
        {'order_by': [desc('id')]},
    )
    
    def __str__(self):
        return f"{self.product.name} - {self.transaction_type} - {self.amount} on {self.date}"


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, index=True)
    payment = Column(Integer, default=0)
    debt = Column(Integer, default=0)
    date_added = Column(Date, nullable=False)
    shop_id = Column(Integer, ForeignKey('markets.id'), nullable=False)

    shop = relationship("Markets", back_populates="sales")
    items = relationship("SaleItems", back_populates="sale")

    __table_args__ = (
        {'order_by': [desc('date_added')]},
    )
    
    def get_amount(self):
        return sum([item.get_amount() for item in self.items])

    def __str__(self):
        return f"{self.date_added} - sale - {self.id}"


class SaleItems(Base):
    __tablename__ = 'sale_items'

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, default=0)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    sale_id = Column(Integer, ForeignKey('sales.id'), nullable=False)

    product = relationship("Product", back_populates="sales")
    sale = relationship("Sale", back_populates="items")

    
    __table_args__ = (
        {'order_by': [desc('id')]},
    )
    
    
    def get_income(self):
        profit = self.product.sale_price - self.product.base_price
        return profit * self.quantity

    def get_amount(self):
        overall = self.product.sale_price * self.quantity
        return max(overall, 0)

    def __str__(self):
        return f"{self.product.name} - {self.id}"


class MoneyTransactions(Base):
    __tablename__ = 'money_transactions'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, default=0)
    date = Column(Date, nullable=False)

    __table_args__ = (
        {'order_by': [desc('id')]},
    )
    
    def __str__(self):
        return str(self.amount)


class Payments(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, default=0)
    date = Column(Date, nullable=False)

    __table_args__ = (
        {'order_by': [desc('id')]},
    )
    
    def __str__(self):
        return str(self.amount)
    
