import os

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import start_app
from app.database import db_session, Base

engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def test_db_session():
    try:
        db = TestingSession()
        yield db
    finally:
        db.close()


app = start_app()
app.dependency_overrides[db_session] = test_db_session

client = TestClient(app)
