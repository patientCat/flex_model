import json
from dataclasses import dataclass
from typing import Optional

from app.common.bizlogger import LOGGER
from app.repo.interface import DatabaseInstanceRepo


class DatabaseInfo:
    def __init__(self, db_url: str, database_name: str, user: str = None, password: str = None):
        self.db_url: str = db_url
        self.database_name: str = database_name
        self.user: str = user
        self.password: str = password

    def to_json(self):
        return {
            "db_url": self.db_url,
            "database_name": self.database_name,
            "user": self.user,
            "password": self.password
        }


class ProjectContext:
    def __init__(self, db_instance_repo: DatabaseInstanceRepo):
        self.__db_instance_repo = db_instance_repo

    def get_database_info(self, project_id: str) -> Optional[DatabaseInfo]:
        db_instance = self.__db_instance_repo.get_db_instance_by_project_id(project_id=project_id)
        LOGGER.debug(f"Connected to database: {db_instance}")
        return DatabaseInfo(db_url=db_instance.db_url, database_name=db_instance.db_name)
