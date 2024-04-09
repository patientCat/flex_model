from abc import abstractmethod

from pymongo import MongoClient

from app.service.model_domain.metadata.model import ModelNameCtx
from app.service.tenant.tenant import DatabaseInfo


class DbContext:
    @abstractmethod
    def database_name(self) -> str:
        pass

    @abstractmethod
    def col_name(self) -> str:
        pass

    @abstractmethod
    def create_client(self):
        pass


class MongoDbContext(DbContext):
    def __init__(self, database_info: DatabaseInfo, collection_name: str):
        super().__init__()
        self.__database_info:DatabaseInfo = database_info
        self.__collection_name = collection_name

    def create_client(self):
        return MongoClient(self.__database_info.db_url)

    def database_name(self):
        return self.__database_info.database_name

    def col_name(self):
        return self.__collection_name
