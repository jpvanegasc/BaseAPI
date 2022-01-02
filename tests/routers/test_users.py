import json
from uuid import uuid4


def test_create_user_successful(client):
    """
    Test for creating an user

    Expected Behavior:
        - Creates an user

    AC:
        - Response has status code 201
        - Created user must be equal to expected value
    """
    from api.schemas.user import UserBase

    data = json.load(open("tests/mock/users/user.json"))
    response = client.post("api/users", json=data)

    assert response.status_code == 201
    assert UserBase(**response.json()["data"]) == UserBase(**data).dict()


def test_create_user_failed_duplicate(client):
    """
    Test for creating a duplicate user

    Expected behavior:
        - Raises an HTTP error

    AC:
        - Get an HTTP error with status code 400
        - Get an HTTP error with message "user already exists"
    """
    data = json.load(open("tests/mock/users/user.json"))

    _ = client.post("api/users", json=data)
    response = client.post("api/users", json=data)

    assert response.status_code == 400
    assert response.json()["message"] == "user already exists"


def test_get_all_users(client):
    """
    Test for getting all users

    Expected Behavior:
        - Return a list with users

    AC:
        - Response has status code 200
        - Users must be the same as expected value
    """
    from api.schemas.user import UserBase

    data = json.load(open("tests/mock/users/user.json"))

    _ = client.post("api/users", json=data)
    response = client.get("api/users")

    assert response.status_code == 200
    assert UserBase(**response.json()["data"][0]).dict() == UserBase(**data).dict()


def test_get_user_by_id_successful(client):
    """
    Test for getting an user by its id

    Expected Behavior:
        - Return a valid user

    AC:
        - Response has status code 200
        - User must be the same as the expected value
    """
    from api.schemas.user import UserBase

    data = json.load(open("tests/mock/users/user.json"))

    user = client.post("api/users", json=data)
    response = client.get(f"api/users/{user.json()['data']['id']}")

    assert response.status_code == 200
    assert UserBase(**response.json()["data"]) == UserBase(**data).dict()


def test_get_user_by_id_failed(client):
    """
    Test for querying a user that doesn't exist

    Expected Behavior:
        - Raises an HTTP error

    AC:
        - Get an HTTP error with status code 404
        - Get an HTTP error with message "user not found"
    """
    user_id = uuid4()
    response = client.get(f"api/users/{user_id}")

    assert response.status_code == 404
    assert response.json()["message"] == "user not found"


def test_update_user_successful(client):
    """
    Test for updating an user

    Expected Behavior:
        - Edits an user

    AC:
        - Response has status code 201
        - Updated user must be equal to expected value
    """
    from api.schemas.user import UserBase

    data = json.load(open("tests/mock/users/user.json"))

    user = client.post("api/users", json=data)

    new_username = "new_username"
    data["username"] = new_username

    response = client.patch(
        f"api/users/{user.json()['data']['id']}", json={"username": new_username}
    )

    assert response.status_code == 200
    assert UserBase(**response.json()["data"]) == UserBase(**data).dict()


def test_update_user_failed(client):
    """
    Test for updating an user that doesn't exist

    Expected Behavior:
        - Raises an HTTP error

    AC:
        - Get an HTTP error with status code 404
        - Get an HTTP error with message "user not found"
    """
    user_id = uuid4()
    response = client.patch(f"api/users/{user_id}", json={"username": ""})

    assert response.status_code == 404
    assert response.json()["message"] == "user not found"


def test_delete_user_successful(client):
    """
    Test for deleting an user

    Expected Behavior:
        - Deletes an user

    AC:
        - Response has status code 200
        - User is deleted from db
    """
    data = json.load(open("tests/mock/users/user.json"))

    user = client.post("api/users", json=data)
    user_id = user.json()["data"]["id"]
    response = client.delete(f"api/users/{user_id}")

    assert response.status_code == 200
    assert client.get(f"api/users/{user_id}").status_code == 404


def test_delete_user_failed(client):
    """
    Test for deleting an user that doesn't exist

    Expected Behavior:
        - Raises an HTTP error

    AC:
        - Get an HTTP error with status code 404
        - Get an HTTP error with message "user not found"
    """
    user_id = uuid4()
    response = client.delete(f"api/users/{user_id}")

    assert response.status_code == 404
    assert response.json()["message"] == "user not found"
