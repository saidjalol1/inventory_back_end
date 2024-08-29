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