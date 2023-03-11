from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .main import app
from .database import Base, get_db
import pytest

Client = TestClient(app)

database_url = "postgresql+psycopg2://postgres:783049@localhost:5432/pytest_demo"

# Create the SQLAlchemy engine for testing
engine = create_engine(database_url)

# Create a SessionLocal class for testing
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):

    # Dependency override
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture()
def user_data(client):
    response = client.post("/user/register",
                           json={"first_name": "Manish",
                                 "last_name": "Singh",
                                 "user_name": "manish",
                                 "email": "manish@gmail.com",
                                 "location": "MBD",
                                 "phone_number": 7656445678,
                                 "password": "manish",
                                 "is_super_user": "true"
                                 },
                           )
    response = client.post("/user/log_in",
                           json={"user_name": "manish",
                                 "password": "manish"}
                           )
    return response


@pytest.fixture()
def book_data(client):
    response = client.post("/book/addBook", json={"id": 1,
                                                  "author": "Nirmala",
                                                  "title": "Rahasiya",
                                                  "price": 350,
                                                  "quantity": 2})
    return response


@pytest.fixture()
def cart_data(client):
    response = client.post("/cart/add_cart", json={"id": 1,
                                                    "user_id": 1,
                                                    "book_id": 1,
                                                    "quantity": 1},
                           )
    return response


def test_register_user(client):
    response = client.post("/user/register",
                           json={"first_name": "Manish",
                                "last_name": "Singh",
                                "user_name": "manish",
                                "email": "manish@gmail.com",
                                "location": "MBD",
                                "phone_number": 7656445678,
                                "password": "manish",
                                "is_super_user": "true"
                             },
                           )
    assert response.status_code == 200
    assert response.json() == {"user_name": "manish",
                                "email": "manish@gmail.com",
                                "phone_number": 7656445678,
                                "location": "MBD",
                                }


def test_user_login(user_data):
    response = user_data
    assert response.status_code == 200
    assert response.json() == {"message": "Login Successfully", "status": 202, "data": {}}


def test_user_logout(user_data, client):
    response = client.get("/user/log_out")
    assert response.status_code == 200
    assert response.json() == {"message": "Logout Successfully", "status": 200, "data": {}}


def test_add_book(user_data, book_data, client):
    response = book_data
    assert response.status_code == 200
    assert response.json().get("message") == "Book Added"


def test_retrieve_books(user_data, book_data, client):
    response = client.get("/book/retrieve_books")
    assert response.status_code == 200


def test_update_book(user_data, book_data, client):
    response = client.put("/book/update_book?id=1", json={"id": 1,
                                                    "author": "Nirmala",
                                                    "title": "Rahasiya",
                                                    "price": 450,
                                                    "quantity": 2},
                          )
    assert response.status_code == 200
    assert response.json().get("message") == "Book Details Updated"


def test_delete_book(user_data, book_data, client):
    response = client.delete("/book/delete_book?id=1")
    assert response.status_code == 200
    assert response.json() == {"delete status": "success"}


def test_add_to_cart(user_data, book_data, cart_data, client):
    response = cart_data
    assert response.status_code == 200
    assert response.json().get("message") == "Cart Added"


def test_retrieve_cart(user_data, book_data, cart_data, client):
    response = client.get("/cart/retrieve_cart")
    assert response.status_code == 200


def test_update_cart(user_data, book_data, cart_data, client):
    response = client.put("/cart/update_cart?cart_id=1", json={
                                                    "book_id": 1,
                                                    "quantity": 2},
                          )
    assert response.status_code == 200
    assert response.json().get("message") == "Cart Updated"


def test_delete_cart(user_data, book_data, cart_data, client):
    response = client.delete("/cart/delete_cart?id=1")
    assert response.status_code == 200
    assert response.json() == {"delete status": "success"}


def test_place_order(user_data, book_data, cart_data, client):
    response = client.post("/order/place_order/", json={"cart_id": 1})
    assert response.status_code == 201
    assert response.json().get("message") == "Order placed"
