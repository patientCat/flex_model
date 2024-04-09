import unittest

from app.common.error import BizException, ErrorCode
from app.service.model_domain.metadata.model import ModelContext
from app.service.tenant.tenant import DatabaseInfo
from .context import TestContextHolder


class TestTestContextHolder(unittest.TestCase):

    def setUp(self):
        self.test_context_holder = TestContextHolder()

    def test_model_context(self):
        model_context = self.test_context_holder.get_model_context(tenant_id, )
        self.assertIsInstance(model_context, ModelContext)
        self.assertEqual(model_context.model_name.name, TestContextHolder.example_schema.get("x-model-name"))

    def test_database_info(self):
        model_context = self.test_context_holder.get_model_context(tenant_id, )
        database_info = self.test_context_holder.get_database_info(tenantId, model_context)
        self.assertIsInstance(database_info, DatabaseInfo)
        self.assertEqual(database_info.database_name, model_context.database_identity.database_name)

    def test_database_info_not_exist(self):
        with self.assertRaises(BizException) as context:
            self.test_context_holder.get_database_info(tenantId, ModelContext.create_from_schema({}))
        self.assertEqual(context.exception.code, ErrorCode.InternalError)

if __name__ == '__main__':
    unittest.main()