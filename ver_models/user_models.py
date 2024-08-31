from datetime import date, datetime
from typing import Union, Optional
from pydantic import BaseModel


class User(BaseModel):
    username : str
    hashed_password : str
    
    class Config:
        from_attributes = True


class CreateSuperUser(User):
    is_super_user : bool
    is_admin : bool
    class Config:
        from_attributes = True


class CreateAdmin(User):
    is_admin : bool
    
    class Config:
        from_attributes = True


class AdminOut(CreateAdmin):
    id: int


class CreateUser(User):
    admin_id : int
    
    class Config:
        from_attributes = True


class UserOut(CreateUser):
    id: int


class UserLogin(User):
    username: str
