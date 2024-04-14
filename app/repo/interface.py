from typing import Optional

from app.repo.po import ModelContextPO, ProjectPO


class ModelRepo(object):
    def __init__(self, repo_name) -> None:
        self._repo = repo_name

    def init(self) -> None:
        pass

    def get_model_by_name(self, project_id, model_name) -> Optional[ModelContextPO]:
        pass

    def create_model(self, model_ctx: ModelContextPO) -> None:
        pass


class ProjectRepo(object):
    def __init__(self, repo_name) -> None:
        self._repo = repo_name

    def init(self) -> None:
        pass

    def get_project_by_project_id(self, project_id) -> Optional[ProjectPO]:
        pass

    def create_project(self, project: ProjectPO) -> None:
        pass
