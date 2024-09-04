from fastapi import APIRouter
from ver_models import user_models
from auth import auth_main , password

import models
from dependency.dependencies import super_user, admin_user, user, database_dep

super = APIRouter(
    prefix="/admin",
    tags=["Super User Routes"]
)

@super.post("/create_super_user")
async def create_super_user(user: user_models.CreateSuperUser,database=database_dep, a=super_user):
   try:
        create_user = models.User(**user.model_dump())
        create_user.hashed_password = password.pwd_context.hash(user.hashed_password)
        database.add(create_user)
        database.commit()
        database.refresh(create_user)
        return {"data":create_user}
   except Exception as e:
       return {"error":e}
    
    
@super.post("/create_admin")
async def create_admin(user: user_models.CreateAdmin,database=database_dep,a=super_user):
 
        if auth_main.is_super_user(a.username, database):
            create_user = models.User(**user.model_dump())
            create_user.hashed_password = password.pwd_context.hash(user.hashed_password)
            database.add(create_user)
            database.commit()
            database.refresh(create_user)
            return {"data":create_user}
        else:
            return {"error":"Un authorized"}

    
    
@super.post("/create_user")
async def create_admin(user: user_models.CreateUser,database=database_dep, a= admin_user):
    try:
        create_user = models.User(**user.model_dump())
        create_user.hashed_password = password.pwd_context.hash(user.hashed_password)
        database.add(create_user)
        database.commit()
        database.refresh(create_user)
        return {"data":create_user}
    except Exception as e:
        return {"error":e}
    
    