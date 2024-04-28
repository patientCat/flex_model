from app.repo.interface import ModelRepo, DatabaseInstanceRepo
from app.repo.sqlalchemy_impl import SqlModelRepo, SqlDatabaseInstanceRepo

MODEL_REPO: ModelRepo = SqlModelRepo()
db_instance_repo: DatabaseInstanceRepo = SqlDatabaseInstanceRepo()


def init():
    MODEL_REPO.init()
    db_instance_repo.init()
