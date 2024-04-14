from dataclasses import dataclass
from typing import Optional

from app.repo.interface import ProjectRepo


@dataclass
class DatabaseInfo:
    db_url: str
    database_name: str
    user: str
    password: str


class ProjectContext:
    def __init__(self, project_repo: ProjectRepo):
        self.__project_repo = project_repo

    def get_database_info(self, project_id: str) -> Optional[DatabaseInfo]:
        return self.__project_repo.get_project_by_project_id(project_id=project_id)
