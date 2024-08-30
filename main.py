from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

import routes
from pydantics import user_models
from auth import auth_main, token
from database.db_conf import get_db, engine
import routes.markets_crud
import routes.super_user_routes

app = FastAPI()

app.include_router(routes.super_user_routes.super)
app.include_router(routes.markets_crud.market_crud)


database_dep : Session = Depends(get_db)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def welcome():
    return {"data":"welcome"}

@app.post("/token/")
async def login(user_token : user_models.UserLogin ,database = database_dep):
    try:
        user = auth_main.authenticate_user(user_token.username,user_token.hashed_password, database)
        print(user)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Could not validated the User")
        created_token = token.create_access_token(user.username, user.id, timedelta(minutes=1000))
        return {"access_token": created_token, "token_type": "bearer", "is_admin":user.is_admin}
    except Exception as e:
        return {"error": e}
    