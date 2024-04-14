from app.repo.interface import ModelRepo, ProjectRepo
from app.repo.sqlalchemy_impl import SqlModelRepo, SqlProjectRepo

MODEL_REPO: ModelRepo = SqlModelRepo()
PROJECT_REPO: ProjectRepo = SqlProjectRepo()


def init():
    MODEL_REPO.init()
    PROJECT_REPO.init()
