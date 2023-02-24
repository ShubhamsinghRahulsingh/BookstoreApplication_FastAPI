import cryptocode
import json


def add_cookies(details, response):
    data_bytes = json.dumps(details)
    encode = cryptocode.encrypt(data_bytes, 'secret')
    response.set_cookie(key='auth_cred', value=encode)
    return encode
