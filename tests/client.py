import os

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import start_app
from app.database import db_session, Base

engine = create_engine(os.environ.get("TEST_DATABASE_URL"))
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def mock_app()->FastAPI:
    Base.metadata.create_all(engine)
    app = start_app()
    yield app
    Base.metadata.drop_all(engine)


def mock_db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


def test_db_session():
    try:
        yield mock_db_session
    finally:
        pass


app = mock_app()
app.dependency_overrides[db_session] = test_db_session

client = TestClient(app)
