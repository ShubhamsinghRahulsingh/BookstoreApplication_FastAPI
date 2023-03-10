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

# Create a Base class
#Base.metadata.create_all(bind=engine)


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










