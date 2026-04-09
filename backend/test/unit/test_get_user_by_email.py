import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController

class TestGetUserByEmail:
    
    @pytest.fixture
    def mockeddao():
        mockedDAO = mock.MagicMock()
        mockedDAO.find.return_value = [{"id": 1, "name": "Jane", "email": "jane@jane.com"}, {"id": 2, "name": "Jane2", "email": "jane@jane.com"}, {"id": 3, "name": "Tarzan", "email": "tarzan@tarzan.com"}]
        mockedUserController = UserController(mockedDAO)

        return mockedUserController

    @pytest.mark.unit
    @pytest.mark.parametrize("email, res", [
        ("@jane.com", ValueError),
        ("jane@jane", ValueError),
        ("tarzan@jane.com", None),
        ("tarzan@tarzan.com", {"id": 3, "name": "Tarzan", "email": "tarzan@tarzan.com"}),
        ("jane@jane.com", {"id": 1, "name": "Jane", "email": "jane@jane.com"})
    ])
