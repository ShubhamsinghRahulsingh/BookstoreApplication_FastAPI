from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Response
from ..models import Book
from ..schemas import BookValidator
from ..database import get_db
from ..utils import verify_super_user, verify_user, logger


routers = APIRouter(tags=["Book"])


@routers.post('/addBook')
def add_book(book: BookValidator, response: Response, user: bool = Depends(verify_super_user),
             db: Session = Depends(get_db)):
    try:
        if not user:
            raise Exception("User not authorized")
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
    except Exception as ex:
        logger.exception(ex.args[0])
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"message": ex.args[0], "status": 406, "data": {}}


@routers.get('/retrieve_books')
def retrieve_books(user: bool = Depends(verify_user), db: Session = Depends(get_db)):
    logger.info("Books Retrieved")
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
def delete_book(id: int, response: Response, user: bool = Depends(verify_super_user),
                db: Session = Depends(get_db)):
    if user:
        try:
            value = db.query(Book).filter(Book.id == id).first()
            if value:
                db.query(Book).filter(Book.id == id).delete()
                db.commit()
                return {"delete status": "success"}
            else:
                return {"message": "Particular Book Id not found"}
        except Exception as ex:
            logger.exception(ex.args[0])
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
            return {"message": ex.args[0], "status": 406, "data": {}}
    return {"message": "User not authorized", "status": 404, "data": {}}
