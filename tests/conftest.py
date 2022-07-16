import os
import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import start_app
from api.common.database import db_session, Base

engine = create_engine(os.environ.get("TEST_DATABASE_URL"))
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def mock_app():
    Base.metadata.create_all(engine)
    app = start_app()
    yield app
    Base.metadata.drop_all(engine)


@pytest.fixture
def mock_db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(mock_app, mock_db_session):
    def test_db_session():
        try:
            yield mock_db_session
        finally:
            pass

    mock_app.dependency_overrides[db_session] = test_db_session

    with TestClient(mock_app) as client:
        yield client
