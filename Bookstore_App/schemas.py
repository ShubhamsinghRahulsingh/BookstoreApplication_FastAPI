from pydantic import BaseModel, EmailStr


class User(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: EmailStr
    phone_number: int
    location: str
    password: str
    is_super_user: bool = False

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    user_name: str
    email: EmailStr
    phone_number: int
    location: str

    class Config:
        orm_mode = True
