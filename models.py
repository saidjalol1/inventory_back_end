from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date, DateTime
from sqlalchemy.orm import relationship

from database.db_conf import Base, current_time


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
    

class QrCode(Base):
    __tablename__ = "codes"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True)
    qr_code_image = Column(String, unique=True)
    
    
