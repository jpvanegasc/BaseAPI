from tests.utils import mock_load, assert_code, assert_data, assert_message

def test_successful_user_flow(client):
    """
    Test for user's CRUD
    """
    from api.schemas.user import UserBase

    data= mock_load("user")

    # Create
    response = client.post("api/users", json=data)
    user_id = response.json()["data"]["id"]

    assert_code(response, 201)
    assert_data(UserBase, response, data)

    # Read many
    response = client.get("api/users")

    assert_code(response, 200)
    assert_data(UserBase, response, data)

    # Read one
    response = client.get(f"api/users/{user_id}")

    assert_code(response, 200)
    assert_data(UserBase, response, data)

    # Update
    new_username = "new_username"
    data["username"] = new_username

    response = client.patch(f"api/users/{user_id}", json={"username": new_username})

    assert_code(response, 200)
    assert_data(UserBase, response, data)

    # Delete
    response = client.delete(f"api/users/{user_id}")
    get_response = client.get(f"api/users/{user_id}")

    assert_code(response, 200)
    assert_code(get_response, 404)
