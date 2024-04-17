import unittest

from app.repo.po import ModelPO, ProjectPO
from app.repo.sqlalchemy_impl import SqlModelRepo, SqlProjectRepo


class TestModelSqlRepoInterface(unittest.TestCase):
    def setUp(self):
        self.repo = SqlModelRepo()
        self.repo.init()

    def test_get_model(self):
        # 创建一个新的租户
        model_ctx = ModelPO(model_name="autotest")
        model_ctx.model_name = "autotest"
        model_ctx.project_id = "test_project_id"
        model_ctx.namespace = "default"
        self.repo.create_model(model_ctx)

        # 使用get_tenant_by_project_id方法获取租户
        rtn_model = self.repo.get_model_by_name(project_id="test_project_id", model_name="autotest")
        print(vars(rtn_model))

    def test_get_model_list(self):
        model_list = self.repo.get_model_list_page(project_id="test_project_id", page_size=10, page_num=1)
        print(model_list)


class TestProjectSqlRepoInterface(unittest.TestCase):
    def setUp(self):
        self.repo = SqlProjectRepo()
        self.repo.init()

    def test_set_up(self):
        self.setUp()

    def test_create_project(self):
        # 创建一个新的project
        project = ProjectPO()
        project.project_id = "test_project_id1"
        project.connection_info = "default"
        self.repo.create_project(project)

    def test_get_project(self):
        rtn_model1 = self.repo.get_project_by_project_id(project_id="test_project_id1")
        rtn_model2 = self.repo.get_project_by_project_id(project_id="test_project_id2")
        print(vars(rtn_model1))
        print(vars(rtn_model2))

    def test_cls_var(self):
        project1 = ProjectPO(id="1")
        project1.id = "1"
        ProjectPO.id = "1"

        project2 = ProjectPO(id="1")
        project2.id = "2"
        ProjectPO.id = "2"

        print(project1.id)
        print(project2.id)
        print(ProjectPO.id)

if __name__ == "__main__":
    unittest.main()
