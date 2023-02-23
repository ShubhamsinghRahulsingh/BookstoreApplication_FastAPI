from sqlalchemy.orm import Session
import hashlib
from . import models, schemas


def add_user(user: schemas.User):
    hashed_password = hashlib.md5(user.password.encode('utf-8')).hexdigest()
    db_user = models.User( first_name=user.first_name,
                           last_name=user.last_name,
                           user_name=user.user_name,
                           email=user.email,
                           location=user.location,
                           phone_number=user.phone_number,
                           password=hashed_password,
                           is_super_user=user.is_super_user
                           )
    return db_user
