from typing import Annotated
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.db_conf import get_db
from models import User
from .password import pwd_context
from jose import JWTError, jwt
from decouple import config

JWT_SECRET = config("secret")
ALGORITH = config("algorithm")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def get_user(username,db: Session ):
    user = db.query(User).filter(User.username == username).first()
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        payload  = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITH])
        username = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            return {"error":"Bu nom ostidagi foydalanuvchi topilmadi!!!"}
        user = get_user(username, db)
        return user
    except JWTError:
        return {"error":"Parol yoki Foydalanuvchi nomi xato"}
    
    
def is_super_user(username,db):
    user = db.query(User).filter(User.username == username).first()
    if user.is_super_user:
        return True
    else:
        return False
    
def is_admin(username,db):
    user = db.query(User).filter(User.username == username).first()
    if user.is_admin:
        return True
    else:
        return False