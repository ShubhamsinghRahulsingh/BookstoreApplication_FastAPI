from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/user', response_model=schemas.ShowUser)
def register_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = crud.add_user(user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
