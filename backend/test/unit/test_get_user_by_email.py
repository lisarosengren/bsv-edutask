import pytest
from unittest.mock import patch
import unittest.mock as mock

from src.controllers.usercontroller import UserController

class TestGetUserByEmail0:

    """ Test class to test the return from get_user_by_email function 
    in the UserController class when the database returns no users. 
    """
    
    @pytest.fixture
    def sut(self):

        mockedDAO = mock.MagicMock()
        mockedDAO.find.return_value = []

        sut = UserController(mockedDAO)

        return sut

    @pytest.mark.unit
    def test_get_user_by_email_None(self, sut):
        with patch("src.controllers.usercontroller.re.fullmatch") as reMock:
            reMock.return_value = True
            result = sut.get_user_by_email("tarzan@jane.com")

            assert result == None


    @pytest.mark.unit
    def test_get_user_by_email_None(self, sut):
        with patch("src.controllers.usercontroller.re.fullmatch") as reMock:
            reMock.return_value = True
            with pytest.raises(ValueError):
                result = sut.get_user_by_email("tarzan@jane.com")
    
class TestGetUserByEmailInvalid:

    """ Test class to test the return from get_user_by_email function 
    in the UserController class when the database returns no users. 
    """
    
    @pytest.fixture
    def sut(self):

        mockedDAO = mock.MagicMock()
        mockedDAO.find.return_value = []

        sut = UserController(mockedDAO)

        return sut   

    @pytest.mark.unit
    def test_incorrectEmail(self, sut):
        with patch("src.controllers.usercontroller.re.fullmatch") as reMock:
            reMock.return_value = False
            # Test if incorrect email raises an ValueError.
            with pytest.raises(ValueError):
                result = sut.get_user_by_email("janejane.com")


class TestGetUserByEmail1:

    """ Test class to test the return from get_user_by_email function 
    in the UserController class when the database returns one users. 
    """
    
    @pytest.fixture
    def sut(self):

        mockedDAO = mock.MagicMock()
        mockedDAO.find.return_value = [{"id": 3, "name": "Tarzan", "email": "tarzan@tarzan.com"}]
        sut = UserController(mockedDAO)

        return sut

    @pytest.mark.unit
    def test_get_user_by_email1(self, sut):
        with patch("src.controllers.usercontroller.re.fullmatch") as reMock:
            reMock.return_value = True
            result = sut.get_user_by_email("tarzan@tarzan.com")

            assert result == {"id": 3, "name": "Tarzan", "email": "tarzan@tarzan.com"}

class TestGetUserByEmail2:

    """ Test class to test the return from get_user_by_email function 
    in the UserController class when the database returns two users. 
    """
    
    @pytest.fixture
    def sut(self):

        mockedDAO = mock.MagicMock()
        mockedDAO.find.return_value = [{"id": 1, "name": "Jane", "email": "jane@jane.com"}, {"id": 2, "name": "Jane2", "email": "jane@jane.com"}]
        sut = UserController(mockedDAO)

        return sut

    @pytest.mark.unit
    def test_get_user_by_email2_obj(self, sut):
        with patch("src.controllers.usercontroller.re.fullmatch") as reMock:
            reMock.return_value = True
            result = sut.get_user_by_email("jane@jane.com")

            assert result == {"id": 1, "name": "Jane", "email": "jane@jane.com"}

    @pytest.mark.unit
    def test_get_user_by_email2_print(self, sut, capsys):
        with patch("src.controllers.usercontroller.re.fullmatch") as reMock:
            reMock.return_value = True
            result = sut.get_user_by_email("jane@jane.com")
            captured = capsys.readouterr()
            assert len(captured.out) > 0

class TestGetUserByEmailException:

    """ Test class to test the return from get_user_by_email function 
    in the UserController class when the database returns an exception. 
    """
    
    @pytest.fixture
    def sut(self):

        mockedDAO = mock.MagicMock()
        mockedDAO.find.return_value = Exception
        sut = UserController(mockedDAO)

        return sut

    @pytest.mark.unit
    def test_get_user_by_email_database_error(self, sut):
        with patch("src.controllers.usercontroller.re.fullmatch") as reMock:
            reMock.return_value = True
            with pytest.raises(Exception):
                result = sut.get_user_by_email("jane@jane.com")
