from uuid import uuid4

from tests.utils import mock_load, assert_code, assert_data, assert_message


def test_create_user_successful(client):
    """
    Test for creating an user

    AC:
        - Response has status code 201
        - Created user must be equal to expected value
    """
    from api.schemas.user import UserBase

    data = mock_load("user")
    response = client.post("api/users", json=data)

    assert_code(response, 201)
    assert_data(UserBase, response, data)


def test_create_user_failed_duplicate(client):
    """
    Test for creating a duplicate user

    AC:
        - Get an HTTP error with status code 400
        - Get an HTTP error with message "user already exists"
    """
    data = mock_load("user")

    _ = client.post("api/users", json=data)
    response = client.post("api/users", json=data)

    assert_code(response, 400)
    assert_message(response, "user already exists")


def test_get_all_users(client, mock_create_user):
    """
    Test for getting all users

    AC:
        - Response has status code 200
        - Users must be the same as expected value
    """
    from api.schemas.user import UserBase

    data = mock_load("user")
    response = client.get("api/users")

    assert_code(response, 200)
    assert_data(UserBase, response, data)


def test_get_user_by_id_successful(client, mock_create_user):
    """
    Test for getting an user by its id

    AC:
        - Response has status code 200
        - User must be the same as the expected value
    """
    from api.schemas.user import UserBase

    data = mock_load("user")

    user_id = mock_create_user["id"]
    response = client.get(f"api/users/{user_id}")

    assert_code(response, 200)
    assert_data(UserBase, response, data)


def test_get_user_by_id_failed(client):
    """
    Test for querying a user that doesn't exist

    AC:
        - Get an HTTP error with status code 404
        - Get an HTTP error with message "user not found"
    """
    user_id = uuid4()
    response = client.get(f"api/users/{user_id}")

    assert_code(response, 404)
    assert_message(response, "user not found")


def test_update_user_successful(client, mock_create_user):
    """
    Test for updating an user

    AC:
        - Response has status code 201
        - Updated user must be equal to expected value
    """
    from api.schemas.user import UserBase

    data = mock_load("user")

    user_id = mock_create_user["id"]

    new_username = "new_username"
    data["username"] = new_username

    response = client.patch(f"api/users/{user_id}", json={"username": new_username})

    assert_code(response, 200)
    assert_data(UserBase, response, data)


def test_update_user_failed(client):
    """
    Test for updating an user that doesn't exist

    AC:
        - Get an HTTP error with status code 404
        - Get an HTTP error with message "user not found"
    """
    user_id = uuid4()
    response = client.patch(f"api/users/{user_id}", json={"username": ""})

    assert_code(response, 404)
    assert_message(response, "user not found")


def test_delete_user_successful(client, mock_create_user):
    """
    Test for deleting an user

    AC:
        - Response has status code 200
        - User is deleted from db
    """
    data = mock_load("user")

    user_id = mock_create_user["id"]
    response = client.delete(f"api/users/{user_id}")
    get_response = client.get(f"api/users/{user_id}")

    assert_code(response, 200)
    assert_code(get_response, 404)


def test_delete_user_failed(client):
    """
    Test for deleting an user that doesn't exist

    AC:
        - Get an HTTP error with status code 404
        - Get an HTTP error with message "user not found"
    """
    user_id = uuid4()
    response = client.delete(f"api/users/{user_id}")

    assert_code(response, 404)
    assert_message(response, "user not found")
