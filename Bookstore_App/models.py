from sqlalchemy import (
    Column,
    String,
    Integer,
    BigInteger,
    Boolean,
    ForeignKey
   )
from Bookstore_App.database import Base
from sqlalchemy.orm import relationship


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
    cart = relationship("Cart", back_populates="user")

    @property
    def auth_payload(self):
        return {"user_name": self.user_name, "password": self.password}


class Book(Base):
    __tablename__ = "book"

    id = Column(BigInteger, primary_key=True, index=True)
    author = Column(String(250))
    title = Column(String(250))
    price = Column(Integer)
    quantity = Column(Integer)
    cart = relationship("Cart", back_populates="book")


class Cart(Base):
    __tablename__ = "cart"

    id = Column(BigInteger, primary_key=True, index=True)
    total_price = Column(Integer)
    book_id = Column(BigInteger, ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    book = relationship("Book", back_populates="cart")
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="cart")


# class Order(Base):
#     __tablename__ = "order"
#
#     id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
#     total_amount = Column(Integer)
#     user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
#     user = relationship("User", back_populates="cart")
#     cart_id = Column(BigInteger, ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
#     cart = relationship("Cart", back_populates="book")
#     address = Column(String(500))

