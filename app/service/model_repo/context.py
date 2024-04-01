from abc import abstractmethod

from pymongo import MongoClient

from app.service.model_domain.metadata.model import ModelName
from app.service.tenant.tenant import DatabaseInfo


class DbContext:
    @abstractmethod
    def database_name(self):
        pass

    @abstractmethod
    def table_name(self):
        pass

    @abstractmethod
    def create_client(self):
        pass


class MongoDbContext(DbContext):
    def __init__(self, database_info : DatabaseInfo, model_name: ModelName):
        super().__init__()
        self._database_info = database_info
        self.model_name = model_name

    def create_client(self):
        return MongoClient(self._database_info.get_db_url())

    def database_name(self):
        return self._database_info.get_db_name()

    def table_name(self):
        return self.model_name.collection_name()
