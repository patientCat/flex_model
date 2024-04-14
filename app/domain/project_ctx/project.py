from dataclasses import dataclass
from typing import Optional

from app.repo.interface import ProjectRepo


class DatabaseInfo:
    def __init__(self, db_url: str, db_name: str, user: str, password: str):
        self.__db_url: str = db_url
        self.database_name: str = db_name
        self.user: str = user
        self.password: str = password

    @property
    def db_url(self) -> str:
        return self.db_url


class ProjectContext:
    def __init__(self, project_repo: ProjectRepo):
        self.__project_repo = project_repo

    def get_database_info(self, project_id: str) -> Optional[DatabaseInfo]:
        return self.__project_repo.get_project_by_project_id(project_id=project_id)
