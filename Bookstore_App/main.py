from fastapi import FastAPI
from Bookstore_App.routers import users, book, cart

app = FastAPI()

app.include_router(users.routers, prefix='/user')
app.include_router(book.routers, prefix='/book')
app.include_router(cart.routers, prefix='/cart')



