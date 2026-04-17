import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController

class TestGetUserByEmail0:
    
    @pytest.fixture
    def sut(self):
        mockedDAO = mock.MagicMock()
        mockedDAO.find.return_value = []
        sut = UserController(mockedDAO)

        return sut

    @pytest.mark.unit
    def test_get_user_by_email_None(self, sut):

        result = sut.get_user_by_email("tarzan@jane.com")

        assert result == None


    @pytest.mark.unit
    def test_get_user_by_email_None(self, sut):

        result = sut.get_user_by_email("tarzan@jane.com")

        assert result == ValueError

    @pytest.mark.parametrize("email",["jane@jane", "@jane.com", "janejane.com"])
    @pytest.mark.unit
    def test_incorrectEmail(self, sut, email):
        # Test if incorrect email raises an ValueError.
        with pytest.raises(ValueError):
            result = sut.get_user_by_email(email)


class TestGetUserByEmail1:
    
    @pytest.fixture
    def sut(self):
        mockedDAO = mock.MagicMock()
        mockedDAO.find.return_value = [{"id": 3, "name": "Tarzan", "email": "tarzan@tarzan.com"}]
        sut = UserController(mockedDAO)

        return sut

    @pytest.mark.unit
    def test_get_user_by_email1(self, sut):

        result = sut.get_user_by_email("tarzan@tarzan.com")

        assert result == {"id": 3, "name": "Tarzan", "email": "tarzan@tarzan.com"}

class TestGetUserByEmail2:
    
    @pytest.fixture
    def sut(self):
        mockedDAO = mock.MagicMock()
        mockedDAO.find.return_value = [{"id": 1, "name": "Jane", "email": "jane@jane.com"}, {"id": 2, "name": "Jane2", "email": "jane@jane.com"}]
        sut = UserController(mockedDAO)

        return sut

    @pytest.mark.unit
    def test_get_user_by_email2_obj(self, sut):

        result = sut.get_user_by_email("jane@jane.com")

        assert result == {"id": 1, "name": "Jane", "email": "jane@jane.com"}

    @pytest.mark.unit
    def test_get_user_by_email2_print(self, sut):

        result = sut.get_user_by_email("jane@jane.com")

        assert result == {"id": 1, "name": "Jane", "email": "jane@jane.com"}

class TestGetUserByEmailException:
    
    @pytest.fixture
    def sut(self):
        mockedDAO = mock.MagicMock()
        mockedDAO.find.return_value = Exception
        sut = UserController(mockedDAO)

        return sut

    @pytest.mark.unit
    def test_get_user_by_email_database_error(self, sut):
       
        with pytest.raises(Exception):
            result = sut.get_user_by_email("jane@jane.com")