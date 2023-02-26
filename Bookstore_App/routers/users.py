from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, Request, status
import hashlib
from Bookstore_App import models, schemas, database, utils

routers = APIRouter(tags=["User"])


@routers.post('/register', response_model=schemas.ShowUser)
def register_user(user: schemas.User, db: Session = Depends(database.get_db)):
    hashed_password = hashlib.md5(user.password.encode('utf-8')).hexdigest()
    new_user = models.User(first_name=user.first_name,
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


@routers.post('/log_in')
def user_login(details: schemas.UserLogin, response: Response, db: Session = Depends(database.get_db)):
    data = db.query(models.User).filter_by(user_name=details.dict().get("user_name")).one_or_none()
    if data:
        input_password = hashlib.md5(details.password.encode('utf-8')).hexdigest()
        if input_password == data.password:
            utils.add_cookies(data.auth_payload, response)
            return {"message": "Login Successfully", "status": 202, "data": {}}
        else:
            return {"message": "Wrong Password", "status": 406, "data": {}}
    response.status_code = status.HTTP_406_NOT_ACCEPTABLE
    return {"message": "Invalid Credentials", "status": 406, "data": {}}


@routers.delete('/log_out')
def user_logout(request: Request, response: Response):
    utils.del_cookies(request, response)
    return {"message": "Logout Successfully", "status": 200, "data": {}}

