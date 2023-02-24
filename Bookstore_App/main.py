from fastapi import FastAPI
from Bookstore_App.routers import users

app = FastAPI()

app.include_router(users.routers, prefix='/user')



