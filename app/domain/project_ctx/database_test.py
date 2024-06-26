import unittest
from unittest.mock import Mock

from pymongo import MongoClient

from app.domain.lowcode_model.model_ctx.model import ModelNameContext
from app.domain.project_ctx.project import DatabaseInfo
from database import MongoDbContext


class TestMongoDbContext(unittest.TestCase):
    def setUp(self):
        self.database_info:DatabaseInfo = Mock(spec=DatabaseInfo)
        self.database_info.db_url = "mongodb://localhost:27017/"
        self.database_info.database_name = "test_db"

        self.model_name: ModelNameContext = ModelNameContext("test_collection")

        self.mongo_db_context = MongoDbContext(self.database_info, self.model_name.collection_name)

    def test_create_client(self):
        client = self.mongo_db_context.create_client()
        self.assertIsInstance(client, MongoClient)

    def test_database_name(self):
        db_name = self.mongo_db_context.database_name()
        self.assertEqual(db_name, "test_db")

    def test_table_name(self):
        table_name = self.mongo_db_context.col_name()
        self.assertEqual(table_name, "test_collection")


if __name__ == '__main__':
    unittest.main()
