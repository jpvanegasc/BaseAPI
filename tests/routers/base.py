import pytest
from copy import deepcopy

from tests.utils import mock_load


class UndefinedModelError(Exception):
    pass


class UndefinedCrudError(Exception):
    pass


class UndefinedSchemaError(Exception):
    pass


class RouteTest:
    model = None
    model_id = None
    crud = None
    create_schema = None

    data = None

    @pytest.fixture
    def set_up(self):
        if not self.model:
            raise UndefinedModelError(f"model for test '{type(self).__name__}' not set")

        if not self.crud:
            raise UndefinedCrudError(f"crud for test '{type(self).__name__}' not set")

        if not self.create_schema:
            raise UndefinedSchemaError(
                f"create model for test '{type(self).__name__}' not set"
            )

        if not self.model_id:
            self.model_id = "1"

        self.data = mock_load(self.data)
        validated_data = self.create_schema(**self.data).dict()
        self.instance = self.model(id=self.model_id, **validated_data)

    @pytest.fixture
    def client(self, client, set_up):
        """
        Given that pytest won't test classes with init,
        validation has to be done in a fixture
        """
        yield client

    @pytest.fixture
    def mock_all(self, monkeypatch):
        def mock_crud_all(session):
            return [self.instance]

        monkeypatch.setattr(self.crud, "all", mock_crud_all)

    @pytest.fixture
    def mock_get_by_id(self, monkeypatch):
        def mock_crud_by_id(session, id):
            if id == self.model_id:
                return self.instance
            else:
                return None

        monkeypatch.setattr(self.crud, "get_by_id", mock_crud_by_id)

    @pytest.fixture
    def mock_update(self, monkeypatch, mock_get_by_id):
        def mock_crud_update(session, id, data):
            if id == self.model_id:
                updated_instance = deepcopy(self.instance)
                for attr, val in data.items():
                    setattr(updated_instance, attr, val)
                return updated_instance
            else:
                return None

        monkeypatch.setattr(self.crud, "update", mock_crud_update)

    @pytest.fixture
    def mock_create(self, monkeypatch, mock_get_by_id):
        def mock_crud_create(session, data):
            return self.instance

        monkeypatch.setattr(self.crud, "create", mock_crud_create)

    @pytest.fixture
    def mock_delete(self, monkeypatch, mock_get_by_id):
        def mock_crud_delete(session, id):
            if id == self.model_id:
                return True
            else:
                return False

        monkeypatch.setattr(self.crud, "delete", mock_crud_delete)
