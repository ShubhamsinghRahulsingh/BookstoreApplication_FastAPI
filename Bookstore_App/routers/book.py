from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from ..models import Book
from ..schemas import BookValidator
from ..database import get_db
from ..utils import verify_super_user, verify_user

routers = APIRouter(tags=["Book"])


@routers.post('/addBook')
def add_book(book: BookValidator, user: bool = Depends(verify_super_user), db: Session = Depends(get_db)):
    if user:
        new_book = Book(id=book.id,
                        author=book.author,
                        title=book.title,
                        price=book.price,
                        quantity=book.quantity
                        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return {"message": "Book Added", "status": 201, "data": book.dict()}
    return {"message": "User not authorized", "status": 404, "data": {}}


@routers.get('/retrieve_books')
def retrieve_books(user: bool = Depends(verify_user), db: Session = Depends(get_db)):
    if user:
        book_data = db.query(Book).all()
        return book_data


@routers.put('/update_book')
def update_book(id: int, book: BookValidator, user: bool = Depends(verify_super_user),
                db: Session = Depends(get_db)):
    if user:
        new_data = db.query(Book).filter(Book.id == id).first()
        new_data.id = book.id,
        new_data.author = book.author,
        new_data.title = book.title,
        new_data.price = book.price,
        new_data.quantity = book.quantity

        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return {"message": "Book Details Updated", "status": 201, "data": book.dict()}
    return {"message": "User not authorized", "status": 404, "data": {}}


@routers.delete("/delete_book")
def delete_book(id: int, user: bool = Depends(verify_super_user),
                db: Session = Depends(get_db)):
    if user:
        try:
            db.query(Book).filter(Book.id == id).delete()
            db.commit()
        except Exception as e:
            raise Exception(e)
        return {"delete status": "success"}
    return {"message": "User not authorized", "status": 404, "data": {}}
