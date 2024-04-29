from typing import Optional

from app.common.bizlogger import LOGGER
from app.repo.interface import DatabaseInstanceRepo


class DatabaseInfo:
    def __init__(self, *, host: str, port: int, database_name: str, user: str, password: str):
        self.host: str = host
        self.port: int = port
        self.database_name: str = database_name
        self.username: str = user
        self.password: str = password

    def to_json(self):
        return {
            "host": self.host,
            "port": self.port,
            "database_name": self.database_name,
            "username": self.username,
            "password": self.password
        }


class ProjectContext:
    def __init__(self, db_instance_repo: DatabaseInstanceRepo):
        self.__db_instance_repo = db_instance_repo

    def get_database_info(self, project_id: str) -> Optional[DatabaseInfo]:
        db_instance = self.__db_instance_repo.get_db_instance_by_project_id(project_id=project_id)
        LOGGER.debug(f"Connected to database: {db_instance}")
        return DatabaseInfo(host=db_instance.host,
                            database_name=db_instance.db_name,
                            user=db_instance.username,
                            port=db_instance.port,
                            password=db_instance.password)
