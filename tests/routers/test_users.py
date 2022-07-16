import pytest
from uuid import uuid4
from copy import deepcopy

from tests.routers.base import RouteTest
from tests.utils import assert_code, assert_data, assert_message
from api.models.user import User
from api.controllers import user as user_crud
from api.schemas.user import UserBase, UserCreate


class TestUserRouters(RouteTest):
    model = User
    model_id = str(uuid4())
    crud = user_crud
    create_schema = UserCreate

    data = "user"

    @pytest.fixture
    def mock_get_by_username(self, monkeypatch):
        def mock_crud_get_by_username(session, username):
            if username == self.instance.username:
                return self.instance
            else:
                return None

        monkeypatch.setattr(self.crud, "get_by_username", mock_crud_get_by_username)

    @pytest.fixture
    def mock_create_user(self, monkeypatch, mock_create, mock_get_by_username):
        return mock_create

    def test_create_user_successful(self, client, mock_create):
        """
        Test for creating an user
        Uses mock_create because `get_by_username` has to return None

        AC:
            - Response has status code 201
            - Created user must be equal to expected value
        """
        response = client.post("api/users", json=self.data)

        assert_code(response, 201)
        assert_data(UserBase, response, self.data)

    def test_create_user_failed_duplicate(self, client, mock_create_user):
        """
        Test for creating a duplicate user

        AC:
            - Get an HTTP error with status code 400
            - Get an HTTP error with message "user already exists"
        """
        response = client.post("api/users", json=self.data)

        assert_code(response, 400)
        assert_message(response, "user already exists")

    def test_get_all_users(self, client, mock_all):
        """
        Test for getting all users

        AC:
            - Response has status code 200
            - Users must be the same as expected value
        """
        response = client.get("api/users")

        assert_code(response, 200)
        assert_data(UserBase, response, self.data)

    def test_get_user_by_id_successful(self, client, mock_get_by_id):
        """
        Test for getting an user by its id

        AC:
            - Response has status code 200
            - User must be the same as the expected value
        """
        response = client.get(f"api/users/{self.model_id}")

        assert_code(response, 200)
        assert_data(UserBase, response, self.data)

    def test_get_user_by_id_failed(self, client, mock_get_by_id):
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

    def test_update_user_successful(self, client, mock_update):
        """
        Test for updating an user

        AC:
            - Response has status code 201
            - Updated user must be equal to expected value
        """
        data = deepcopy(self.data)

        new_username = "new_username"
        data["username"] = new_username

        response = client.patch(
            f"api/users/{self.model_id}", json={"username": new_username}
        )

        assert_code(response, 200)
        assert_data(UserBase, response, data)

    def test_update_user_failed(self, client, mock_update):
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

    def test_delete_user_successful(self, client, mock_delete):
        """
        Test for deleting an user

        AC:
            - Response has status code 200
            - User is deleted from db
        """
        response = client.delete(f"api/users/{self.model_id}")

        assert_code(response, 200)

    def test_delete_user_failed(self, client, mock_delete):
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
