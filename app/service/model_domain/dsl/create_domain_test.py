import unittest
from unittest.mock import Mock

from app.common.error import BizException, ErrorCode
from app.service.model_domain.metadata.model import ModelContext
from app.service.model_domain.dsl.create_domain import CreateDomainFactory, CreateDomain, CreateManyDomain


class TestCreateDomainFactory(unittest.TestCase):
    def setUp(self):
        self.model_context = Mock(ModelContext)
        self.create_domain_factory = CreateDomainFactory(self.model_context)

    def test_create_domain(self):
        test_data = {"foo": "bar"}
        test_dict = {"data": test_data}
        result = self.create_domain_factory.create_domain(test_dict)
        self.assertIsInstance(result, CreateDomain)
        self.assertEqual(result.data, test_data)

    def test_create_domain_none_param(self):
        with self.assertRaises(BizException) as context:
            self.create_domain_factory.create_domain(None)
        self.assertEqual(context.exception.code, ErrorCode.InvalidParameter)

    def test_create_domain_missing_key(self):
        test_dict = {}
        with self.assertRaises(BizException) as context:
            self.create_domain_factory.create_domain(test_dict)
        self.assertEqual(context.exception.code, ErrorCode.InvalidParameter)

    def test_create_many_domain(self):
        test_data_list = [{"foo": "bar"}]
        test_dict = {"datalist": test_data_list}
        result = self.create_domain_factory.create_many_domain(test_dict)
        self.assertIsInstance(result, CreateManyDomain)
        self.assertEqual(result.datalist, test_data_list)

    def test_create_many_domain_none_param(self):
        with self.assertRaises(BizException) as context:
            self.create_domain_factory.create_many_domain(None)
        self.assertEqual(context.exception.code, ErrorCode.InvalidParameter)

    def test_create_many_domain_missing_key(self):
        test_dict = {}
        with self.assertRaises(BizException) as context:
            self.create_domain_factory.create_many_domain(test_dict)
        self.assertEqual(context.exception.code, ErrorCode.InvalidParameter)


if __name__ == "__main__":
    unittest.main()
