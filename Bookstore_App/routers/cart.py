from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, status
from ..models import Cart, Book
from ..schemas import CartValidator, CartUpdate
from ..database import get_db
from ..utils import verify_user, get_user_id, logger

routers = APIRouter(tags=["Cart"])


@routers.post('/add_cart')
def add_to_cart(cart: CartValidator, response: Response, user: bool = Depends(verify_user), db: Session = Depends(get_db)):
    book_data = db.query(Book).filter(Book.id == cart.book_id).first()
    overall_price = book_data.price * cart.quantity
    try:
        if not user:
            raise Exception("User not authorized")
        new_cart = Cart(id=cart.id,
                               total_price=overall_price,
                               book_id=cart.book_id,
                               user_id=cart.user_id
                             )
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        return {"message": "Cart Added", "status": 201, "data": new_cart}
    except Exception as ex:
        logger.exception(ex.args[0])
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"message": ex.args[0], "status": 406, "data": {}}


@routers.get('/retrieve_cart')
def retrieve_cart(userid: int = Depends(get_user_id), user: bool = Depends(verify_user),
                  db: Session = Depends(get_db)):
    if user:
        data = db.query(Cart).filter(Cart.user_id == userid).all()
        books = []
        values = db.query(Book).join(Cart).all()
        for x in range(len(data)):
            for y in range(len(values)):
                if values[y].id == data[x].book_id:
                    author = values[y].author
                    title = values[y].title
                    total_price = data[x].total_price
                    cart_id = data[x].id
                    book_id = values[y].id
                    books.append({"author": author, "title": title, "total_price": total_price,
                                  "book_id": book_id, "cart_id": cart_id})
        return books
    return {"message": "User not authorized", "status": 404, "data": {}}


@routers.put('/update_cart')
def update_cart(cart_id: int, response: Response,  cart: CartUpdate, userid: int = Depends(get_user_id),
                user: bool = Depends(verify_user),
                db: Session = Depends(get_db)):
    book_data = db.query(Book).filter(Book.id == cart.book_id).first()
    overall_price = book_data.price * cart.quantity
    try:
        if not user:
            raise Exception("User not authorized")
        cart_data = db.query(Cart).filter(Cart.id == cart_id).first()
        cart_data.id = cart_id,
        cart_data.total_price = overall_price,
        cart_data.book_id = cart.book_id,
        cart_data.user_id = userid
        db.add(cart_data)
        db.commit()
        db.refresh(cart_data)
        return {"message": "Cart Updated", "status": 201, "data": cart_data}
    except Exception as ex:
        logger.exception(ex.args[0])
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"message": ex.args[0], "status": 406, "data": {}}


@routers.delete("/delete_cart")
def delete_cart(id: int, response: Response, user: bool = Depends(verify_user),
                db: Session = Depends(get_db)):
    try:
        if not user:
            raise Exception("User not authorized")
        value = db.query(Cart).filter(Cart.id == id).first()
        if value:
            db.query(Cart).filter(Cart.id == id).delete()
            db.commit()
            return {"delete status": "success"}
        else:
            return {"message": "Particular Cart Id not found"}
    except Exception as ex:
        logger.exception(ex.args[0])
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"message": ex.args[0], "status": 406, "data": {}}

