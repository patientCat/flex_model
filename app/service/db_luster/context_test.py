import unittest
from unittest.mock import Mock

from pymongo import MongoClient

from app.service.model_domain.metadata.model import ModelNameCtx
from app.service.tenant.tenant import DatabaseInfo
from context import MongoDbContext


class TestMongoDbContext(unittest.TestCase):
    def setUp(self):
        self.database_info:DatabaseInfo = Mock(spec=DatabaseInfo)
        self.database_info.db_url = "mongodb://localhost:27017/"
        self.database_info.database_name = "test_db"

        self.model_name: ModelNameCtx = ModelNameCtx("test_collection")

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
