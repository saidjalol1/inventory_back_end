from datetime import timedelta
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm


from ver_models import user_models
from auth import auth_main, token
from dependency.dependencies import database_dep


from routes import super_user_routes, markets_crud, qr_code
app = FastAPI()
app.include_router(super_user_routes.super)
app.include_router(markets_crud.market_crud)
app.include_router(qr_code.code_path)
app.mount("/static", StaticFiles(directory="static"), name="static")


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
        return {"access_token": created_token, "token_type": "bearer",}
    except Exception as e:
        print(e)
        return {"error":str(e)}
    # Return the exception message as a string
    