import json

import pydantic
import requests


def assert_code(response: requests.Response, code: int):
    """Helper for simplifying response code assertion"""
    assert response.status_code == code


def assert_data(schema: pydantic.BaseModel, response: requests.Response, data: dict):
    """Helper for simplifying response data assertion"""
    response = response.json()["data"]
    if isinstance(response, list):
        response = response[0]

    assert schema(**response).dict() == schema(**data).dict()


def assert_message(response: requests.Response, message: str):
    assert response.json()["message"] == message


def mock_load(mock_file: str):
    """Helper for simplifying mock loading"""
    return json.load(open(f"tests/mock/{mock_file}.json"))
