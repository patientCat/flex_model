import json
from dataclasses import dataclass
from typing import Optional

from app.repo.interface import ProjectRepo


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
    def __init__(self, project_repo: ProjectRepo):
        self.__project_repo = project_repo

    def get_database_info(self, project_id: str) -> Optional[DatabaseInfo]:
        project = self.__project_repo.get_project_by_project_id(project_id=project_id)
        conn_json = json.loads(project.connection_info)
        print(f"Connected to database: {conn_json}, connection_info : {project.connection_info}")
        return DatabaseInfo(db_url=conn_json.get("db_url"), database_name=conn_json.get("database_name"))
