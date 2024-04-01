import unittest
from unittest.mock import Mock

from pymongo import MongoClient

from app.service.model_domain.metadata.model import ModelName
from app.service.tenant.tenant import DatabaseInfo
from context import MongoDbContext


class TestMongoDbContext(unittest.TestCase):
    def setUp(self):
        self.database_info = Mock(spec=DatabaseInfo)
        self.database_info.get_db_url.return_value = "mongodb://localhost:27017/"
        self.database_info.get_db_name.return_value = "test_db"

        self.model_name = Mock(spec=ModelName)
        self.model_name.collection_name.return_value = "test_collection"

        self.mongo_db_context = MongoDbContext(self.database_info, self.model_name)

    def test_create_client(self):
        client = self.mongo_db_context.create_client()
        self.assertIsInstance(client, MongoClient)

    def test_database_name(self):
        db_name = self.mongo_db_context.database_name()
        self.assertEqual(db_name, "test_db")

    def test_table_name(self):
        table_name = self.mongo_db_context.table_name()
        self.assertEqual(table_name, "test_collection")


if __name__ == '__main__':
    unittest.main()
