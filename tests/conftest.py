import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import app
from app.core.security import hash_password
from app.db.base import Base
from app.db.session import engine
from app.models import User


@pytest.fixture
def client():
    return TestClient(app)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@pytest.fixture
def db():
    # Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# @pytest.fixture
# def test_db_session():
#     engine = create_engine("sqlite:///:memory:")
#     Base.metadata.create_all(engine)
#     SessionLocal = sessionmaker(bind=engine)
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# @pytest.fixture
# def create_test_user(test_db_session):
#     db = test_db_session
#     user = User(
#         username="original",
#         email="original@test.com",
#         password=hash_password("123456")
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user