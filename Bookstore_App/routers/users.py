from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, Request, status
import hashlib
from ..models import User
from ..schemas import UserValidator, ShowUser, UserLogin
from ..database import get_db
from ..utils import add_cookies, del_cookies, logger

routers = APIRouter(tags=["User"])


@routers.post('/register', response_model=ShowUser)
def register_user(user: UserValidator, response: Response, db: Session = Depends(get_db)):
    try:
        hashed_password = hashlib.md5(user.password.encode('utf-8')).hexdigest()
        new_user = User(first_name=user.first_name,
                        last_name=user.last_name,
                        user_name=user.user_name,
                        email=user.email,
                        location=user.location,
                        phone_number=user.phone_number,
                        password=hashed_password,
                        is_super_user=user.is_super_user
                        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as ex:
        logger.exception(ex.args[0])
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"message": ex.args[0], "status": 406, "data": {}}


@routers.post('/log_in')
def user_login(details: UserLogin, response: Response, db: Session = Depends(get_db)):
    try:
        data = db.query(User).filter_by(user_name=details.dict().get("user_name")).one_or_none()
        if not data:
            raise Exception("Invalid Credentials")
        input_password = hashlib.md5(details.password.encode('utf-8')).hexdigest()
        if input_password == data.password:
            add_cookies(data.auth_payload, response)
            return {"message": "Login Successfully", "status": 202, "data": {}}
        else:
            return {"message": "Wrong Password", "status": 406, "data": {}}
    except Exception as ex:
        logger.exception(ex.args[0])
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"message": ex.args[0], "status": 406, "data": {}}


@routers.get('/log_out')
def user_logout(request: Request, response: Response):
    del_cookies(request, response)
    return {"message": "Logout Successfully", "status": 200, "data": {}}

