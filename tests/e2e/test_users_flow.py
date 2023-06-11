from uuid import uuid4

from tests.utils import mock_load, assert_code, assert_data, assert_message
from tests.client import client


def test_successful_user_flow():
    """
    Test for user's CRUD
    """
    from app.schemas.user import UserBase

    data = mock_load("user")

    # Create
    response = client.post("api/users", json=data)
    user_id = response.json()["data"]["id"]

    assert_code(response, 201)
    assert_data(UserBase, response, data)

    # Create duplicate
    response = client.post("api/users", json=data)

    assert_code(response, 400)
    assert_message(response, "user already exists")

    # Read many
    response = client.get("api/users")

    assert_code(response, 200)
    assert_data(UserBase, response, data)

    # Read one
    response = client.get(f"api/users/{user_id}")

    assert_code(response, 200)
    assert_data(UserBase, response, data)

    # Read one - not found
    response = client.get(f"api/users/{uuid4()}")

    assert_code(response, 404)
    assert_message(response, "user not found")

    # # Update
    # new_username = "new_username"
    # data["username"] = new_username

    # response = client.patch(f"api/users/{user_id}", json={"username": new_username})

    # assert_code(response, 200)
    # assert_data(UserBase, response, data)

    # # Update - not found
    # response = client.patch(f"api/users/{uuid4()}", json={"username": ""})

    # assert_code(response, 404)
    # assert_message(response, "user not found")

    # Delete
    response = client.delete(f"api/users/{user_id}")
    get_response = client.get(f"api/users/{user_id}")

    assert_code(response, 200)
    assert_code(get_response, 404)

    # Delete - not found
    response = client.delete(f"api/users/{uuid4()}")

    assert_code(response, 404)
