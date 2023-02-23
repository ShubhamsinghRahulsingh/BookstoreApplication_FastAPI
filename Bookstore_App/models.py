from sqlalchemy import (
    Column,
    String,
    Integer,
    BigInteger,
    Boolean,
    ForeignKey
   )
from Bookstore_App.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    user_name = Column(String, unique=True)
    email = Column(String, unique=True)
    phone_number = Column(BigInteger)
    location = Column(String)
    password = Column(String)
    is_super_user = Column(Boolean, default=False)


class Book(Base):
    __tablename__ = "book"

    id = Column(BigInteger, primary_key=True, index=True)
    author = Column(String(250))
    title = Column(String(250))
    price = Column(Integer)
    quantity = Column(Integer)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
