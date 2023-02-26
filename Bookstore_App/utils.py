from fastapi import HTTPException, Request
import cryptocode
import json
from Bookstore_App import models


def add_cookies(details, response):
    data_bytes = json.dumps(details)
    encode = cryptocode.encrypt(data_bytes, 'secret')
    response.set_cookie(key='auth_cred', value=encode)


def get_cookies(request):
    auth_cred = request.cookies.get('auth_cred')
    if auth_cred:
        return cryptocode.decrypt(auth_cred, 'secret')
    return None


def verify_super_user(request, db):
    decode_cookie = get_cookies(request)
    if decode_cookie:
        user_data = json.loads(decode_cookie)
        data = db.query(models.User).filter_by(**user_data).one_or_none()
        if data.is_super_user:
            return True
        raise HTTPException(detail='User not authorized', status_code=404)
    raise HTTPException(detail='User is not Logged In', status_code=404)


def verify_user(request: Request):
    decode_cookie = get_cookies(request)
    if decode_cookie:
        return True
    raise HTTPException(detail='User not authorized', status_code=404)