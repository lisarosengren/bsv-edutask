from src.util.dao import DAO
import pytest
from unittest.mock import patch
import pymongo


# ändrat i .env = MONGO_URL=mongodb://root:root@localhost:27017


class TestDaoToMongo():

    @pytest.fixture
    def dao(self):
        with patch("src.util.dao.getValidator") as mockValidator:

            mockValidator.return_value = {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": [ "name", "city" ],
                    "properties": {
                        "name": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                        },
                        "city": {
                        "bsonType": "string",
                        "description": "must be a string and is required",
                        "uniqueItems": True
                        },
                        "stupid": {
                            "bsonType": "bool"
                        }
                    }
                }
            }
        
            dao = DAO("test")

            yield dao

            dao.drop()

    @pytest.mark.integration
    def test_dao_to_mongo_missing_property(self, dao):

        with pytest.raises(pymongo.errors.WriteError):
            result = dao.create({"name": "lisa", "stupid": True})
        
        
    
    @pytest.mark.integration
    def test_dao_to_mongo_wrong_bson(self, dao):

        with pytest.raises(pymongo.errors.WriteError):
            result = dao.create({"name": 1234, "city": "Malmö", "stupid": True})

    @pytest.mark.integration
    def test_dao_to_mongo_not_unique(self, dao):

        with pytest.raises(pymongo.errors.WriteError):
            dao.create({"name": "lisa", "city": "Malmö", "stupid": True})
            result = dao.create({"name": "rebecka", "city": "Malmö", "stupid": False})

    @pytest.mark.integration
    def test_dao_to_mongo_valid_input(self, dao):
        
        result = dao.create({"name": "lisa", "city": "Malmö", "stupid": True})

        assert len(result) == 4
        assert result["name"] == "lisa"
        assert result["city"] == "Malmö"
        assert result["stupid"] == True
        assert result["_id"] is not None
        
