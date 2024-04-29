from abc import abstractmethod
from dataclasses import dataclass

from pymongo import MongoClient

from app.domain.project_ctx.project import DatabaseInfo


### 数据库标识上下文
@dataclass
class DatabaseIdentity:
    database_name: str
    type: str


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
        self.__database_info: DatabaseInfo = database_info
        self.__collection_name = collection_name

    def create_client(self):
        return MongoClient(
            host=self.__database_info.db_url,
            port=self.__database_info.db_port,
            username=self.__database_info.username,
            password=self.__database_info.password
        )

    def database_name(self):
        return self.__database_info.database_name

    def col_name(self):
        return self.__collection_name
