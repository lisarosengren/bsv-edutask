import pytest
import unittest.mock as mock
from unittest.mock import patch

from src.controllers.usercontroller import UserController

class TestUserController:

    """ Test class to test the return from get_user_by_email function 
    in the USerController class. 
    """

    mockedusercontroller = mock.MagicMock()
    mockedusercontroller.get.return_value = {'age': age}
    mockedsut = ValidationHelper(usercontroller=mockedusercontroller)

    @pytest.fixture
    # @patch('src.controllers.usercontroller.Controller', autospec=True)
    # @patch('src.controllers.usercontroller.DAO', autospec=True)
    def sut(self, mockedDAO, mockedcontroller):
        mockedusercontroller = mock.MagicMock()
        mockedsut = ValidationHelper(usercontroller=mockedusercontroller)
        mockedDAO = None
        mockedcontroller.return_value = mock.MagicMock()
        sut = UserController(mockedcontroller)
        return sut

    @pytest.mark.unit
    def test_existingEmail(self, sut):
        # Test if email connected to one user returns an object.
        result = sut.get_user_by_email('user@okey.com')
        assert isinstance(result, object)

    @pytest.mark.unit
    def test_existingManyEmail(self, sut):
        # Test if email connected to many user returns an object.
        result = sut.get_user_by_email('usermany@okey.com')
        assert isinstance(result, object)

    @pytest.mark.unit
    def test_notExistingEmail(self, sut):
        # Test if email not connected to a user returns None.
        result = sut.get_user_by_email('notuser@okey.com')
        assert result == None

    @pytest.mark.unit
    def test_incorrectEmail(self, sut):
        # Test if incorrect email raises an ValueError.
        with pytest.raises(ValueError):
            result = sut.get_user_by_email('invalidemail.com')