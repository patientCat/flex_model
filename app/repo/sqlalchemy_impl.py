import json
import logging
from datetime import datetime
from typing import Optional, List, Callable

from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, create_engine
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.repo.interface import ProjectRepo, ModelRepo
from app.repo.po import ModelPO, ProjectPO

# 创建基类
Base = declarative_base()

Db_Path = 'sqlite:///database.db'
Engine = create_engine(Db_Path, echo=True)

# 配置日志记录器
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


def copy_value(from_cls, to_cls):
    for k, v in from_cls.__dict__.items():
        setattr(to_cls, k, v)


class _ProjectPO(Base, ProjectPO):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    project_id = Column(String)
    db_type = Column(String)
    connection_info = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ConnectionInfoHolder:
    def __init__(self, connection_info: str):
        self.info_map = json.loads(connection_info)

    def get_db_url(self):
        return self.info_map.get('db_url')


class _ModelPO(Base, ModelPO):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    # namespace 用来逻辑隔离
    namespace = Column(String, default="default")
    project_id = Column(String)
    schema = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('project_id', 'model_name', name='unique_project_id_name'),
    )

    def __str__(self):
        return f'_ModelPO(__dict__={self.__dict__})'

    def __repr__(self):
        return self.__str__()


def call_on_session(*, engine, func: Callable):
    SessionFactory = sessionmaker(bind=engine)
    session = SessionFactory()
    rtn = func(session)
    session.close()
    return rtn


class SqlModelRepo(ModelRepo):
    def __init__(self):
        super().__init__("sql")
        self.engine = None

    def init(self) -> None:
        self.engine = Engine
        Base.metadata.create_all(self.engine)

    def get_model_by_name(self, project_id, model_name) -> Optional[ModelPO]:
        def func(session: Session):
            model = (session.query(_ModelPO)
                     .filter(and_(_ModelPO.project_id == project_id, _ModelPO.model_name == model_name))
                     .first())
            return model

        return call_on_session(engine=self.engine, func=func)

    def get_model_list_page(self, project_id, page_num, page_size) -> List[ModelPO]:
        def func(session: Session):
            session_query = session.query(_ModelPO).filter(_ModelPO.project_id == project_id)
            paginated_query = session_query.limit(page_size).offset((page_num - 1) * page_size)
            model_list = paginated_query.all()
            return model_list

        return call_on_session(engine=self.engine, func=func)

    def create_model(self, model_ctx: ModelPO) -> None:
        def func(session: Session):
            _model_ctx: _ModelPO = _ModelPO()
            copy_value(model_ctx, _model_ctx)
            session.add(_model_ctx)
            session.commit()

        return call_on_session(engine=self.engine, func=func)

    def delete_model(self, project_id, model_name):
        def func(session: Session):
            user_to_delete = session.query(_ModelPO).filter(
                and_(_ModelPO.model_name == model_name, _ModelPO.project_id == project_id)).first()
            if user_to_delete:
                session.delete(user_to_delete)
                session.commit()

        return call_on_session(engine=self.engine, func=func)


class SqlProjectRepo(ProjectRepo):
    def __init__(self):
        super().__init__("sql")
        self.engine = None

    def init(self) -> None:
        self.engine = Engine
        Base.metadata.create_all(self.engine)

    def get_project_by_project_id(self, project_id) -> Optional[ProjectPO]:
        def func(session: Session):
            project = (session.query(_ProjectPO)
                       .filter(_ProjectPO.project_id == project_id)
                       .first())
            return project

        return call_on_session(engine=self.engine, func=func)

    def create_project(self, project: ProjectPO) -> None:
        def func(session: Session):
            _project = _ProjectPO()
            copy_value(project, _project)
            session.add(_project)
            session.commit()

        return call_on_session(engine=self.engine, func=func)
