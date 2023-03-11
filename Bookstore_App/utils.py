from fastapi import HTTPException, Request, Depends
from datetime import datetime
from sqlalchemy.orm import Session
import cryptocode
import json
from .models import User, Cart
from .schemas import PlaceOrder
from .database import get_db
import logging


logging.basicConfig(filename='book_store.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)


def add_cookies(details, response):
    data_bytes = json.dumps(details)
    encode = cryptocode.encrypt(data_bytes, 'secret')
    response.set_cookie(key='auth_cred', value=encode)


def get_cookies(request):
    auth_cred = request.cookies.get('auth_cred')
    if auth_cred:
        return cryptocode.decrypt(auth_cred, 'secret')
    return None


def del_cookies(request, response):
    auth_cred = request.cookies.get('auth_cred')
    if auth_cred:
        response.delete_cookie('auth_cred')
        return {"message": "Logout Successfully", "status": 200, "data": {}}
    raise HTTPException(detail='User is not Logged In', status_code=404)


def verify_super_user(request: Request, db: Session = Depends(get_db)):
    decode_cookie = get_cookies(request)
    if decode_cookie:
        user_data = json.loads(decode_cookie)
        data = db.query(User).filter_by(**user_data).one_or_none()
        if data.is_super_user:
            return True
        raise HTTPException(detail='User not authorized', status_code=404)
    raise HTTPException(detail='User is not Logged In', status_code=404)


def verify_user(request: Request):
    decode_cookie = get_cookies(request)
    if decode_cookie:
        return True
    raise HTTPException(detail='User not authorized', status_code=404)


def get_user_id(request: Request, db: Session = Depends(get_db)):
    decode_cookie = get_cookies(request)
    if decode_cookie:
        user_data = json.loads(decode_cookie)
        data = db.query(User).filter_by(**user_data).one_or_none()
        userid = data.id
        return userid
    raise HTTPException(detail='User is not Logged In', status_code=404)


def place_order_books(order: PlaceOrder, request: Request, db: Session = Depends(get_db),
                      userid: int = Depends(get_user_id)):
    verify = verify_user(request)
    if verify:
        user = db.query(User).filter(User.id == userid).first()
        order_values = {"UserName": user.first_name, "User_Id": userid, "Location": user.location,
                        "DateTime": datetime.utcnow()}
        if order.cart_id:
            data = db.query(Cart).filter(Cart.id == order.cart_id).first()
            order_values.update({"Total_amount": data.total_price, "Book_id": data.book_id})
            return order_values
        total_amount = 0
        books = []
        cart_data = db.query(Cart).filter(Cart.user_id == userid).all()
        for x in range(len(cart_data)):
            total_amount += cart_data[x].total_price
            books.append(cart_data[x].book_id)
        order_values.update({"Total_amount": total_amount, "Books_Id": books})
        return order_values
    raise HTTPException(detail='User is not Logged In', status_code=404)

