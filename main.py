from datetime import timedelta, date
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import desc

import my_util_functions
from auth import auth_main, token
import my_util_functions.stattistika
import ver_models
from ver_models import user_models
from dependency.dependencies import database_dep
from routes import super_user_routes, markets_crud, qr_code, expance, products, tranzactions, sale
import models
import ver_models.expance

app = FastAPI()
app.include_router(sale.app)
app.include_router(expance.app)
app.include_router(qr_code.code_path)
app.include_router(products.app)
app.include_router(tranzactions.app)
app.include_router(super_user_routes.super)
app.include_router(markets_crud.market_crud)
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/statistics")
async def welcome(db = database_dep):
    data = {
        "sales":my_util_functions.stattistika.sales(db)["revenue"],
        "income":my_util_functions.stattistika.sales(db)["income"],
        "most_shop": my_util_functions.stattistika.get_most_buying_shop(db),
        "most_product": my_util_functions.stattistika.get_most_bought_product(db),
        "sales_chart": my_util_functions.stattistika.get_sales_by_month(db),
        "balance" : my_util_functions.stattistika.calculate_total_price(db),
        "moneys": my_util_functions.stattistika.moneys(db),
    }
    return data


@app.post("/token")
async def login(user_token : user_models.UserLogin ,database = database_dep):
    try:
        user = auth_main.authenticate_user(user_token.username,user_token.hashed_password, database)
        print(user)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Could not validated the User")
        created_token = token.create_access_token(user.username, user.id, timedelta(minutes=1000))
        return {"access_token": created_token, "token_type": "bearer",}
    except Exception as e:
        print(e)
        return {"error":str(e)}
    # Return the exception message as a string
    