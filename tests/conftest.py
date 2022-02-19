import os
import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import start_app
import api.common.settings as settings
from api.common.database import db_session, Base

engine = create_engine(os.environ.get("TEST_DATABASE_URL"))
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def assert_code(response, code):
    """Helper for simplifying response code assertion"""
    assert response.status_code == code


def assert_data(schema, response, data, use_list=False):
    """Helper for simplifying response data assertion"""
    if use_list:
        assert schema(**response.json()["data"][0]).dict() == schema(**data).dict()
    else:
        assert schema(**response.json()["data"]).dict() == schema(**data).dict()


def assert_message(response, message):
    assert response.json()["message"] == message


def mock_load(mock_file):
    """Helper for simplifying mock loading"""
    return json.load(open(f"tests/mock/{mock_file}.json"))


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


@pytest.fixture
def mock_user():
    from api.models.user import User

    data = json.load(open("tests/mock/users/user.json"))
    mocked_user = User(**data)

    # Un-hash password for validation
    mocked_user.password = data["password"]

    return mocked_user


@pytest.fixture
def mock_users(mock_user):
    del mock_user._sa_instance_state

    return [mock_user]


@pytest.fixture
def mock_get_all_users(mock_db_session, mock_users):
    mock_db_session.query.all.return_value = [vars(user) for user in mock_users]

    return mock_db_session
