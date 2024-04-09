import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.repo.interface import RepoInterface
from app.repo.po.tenant_po import TenantPO
from app.repo.sqlite_impl import SqlRepoInterface


class TestSqlRepoInterface(unittest.TestCase):
    def setUp(self):
        self.repo = SqlRepoInterface()
        self.repo.init()

    def test_get_tenant_by_tenant_id(self):
        # 创建一个新的租户
        new_tenant = TenantPO()
        new_tenant.tenant_id = "test_tenant"
        new_tenant.connection_info = ""
        self.repo.create_tenant(new_tenant)

        # 使用get_tenant_by_tenant_id方法获取租户
        tenant = self.repo.get_tenant_by_tenant_id("test_tenant")
        print(vars(tenant))

        # 断言租户信息是否正确
        self.assertIsNotNone(tenant)
        self.assertEqual(tenant.tenant_id, "test_tenant")


if __name__ == "__main__":
    unittest.main()
