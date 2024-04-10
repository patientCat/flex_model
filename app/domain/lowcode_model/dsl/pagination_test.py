from .find_option import PaginationFactory

import unittest
from app.common.error import BizException, ErrorCode


class TestPaginationFactory(unittest.TestCase):
    def setUp(self):
        self.factory = PaginationFactory()

    def test_create_pagination_with_valid_params(self):
        param_dict = {"limit": 5, "offset": 10}
        pagination = self.factory.create_pagination(param_dict)
        self.assertEqual(pagination.limit, 5)
        self.assertEqual(pagination.offset, 10)

    def test_create_pagination_with_invalid_limit(self):
        param_dict = {"limit": -5, "offset": 10}
        with self.assertRaises(BizException) as context:
            self.factory.create_pagination(param_dict)
        self.assertEqual(context.exception.code, ErrorCode.InvalidParameter)
        self.assertEqual(context.exception.message, PaginationFactory.ERROR_MESSAGE_INVALID_LIMIT)

    def test_create_pagination_with_invalid_offset(self):
        param_dict = {"limit": 5, "offset": -10}
        with self.assertRaises(BizException) as context:
            self.factory.create_pagination(param_dict)
        self.assertEqual(context.exception.code, ErrorCode.InvalidParameter)
        self.assertEqual(context.exception.message, PaginationFactory.ERROR_MESSAGE_INVALID_OFFSET)

    def test_create_pagination_with_default_values(self):
        param_dict = {}
        pagination = self.factory.create_pagination(param_dict)
        self.assertEqual(pagination.limit, 10)
        self.assertEqual(pagination.offset, 0)

    def test_create_pagination_default_values(self):
        pagination = self.factory._create_pagination(None, None)
        self.assertEqual(pagination.limit, 10)
        self.assertEqual(pagination.offset, 0)

    def test_create_pagination_custom_values(self):
        pagination = self.factory._create_pagination(5, 20)
        self.assertEqual(pagination.limit, 5)
        self.assertEqual(pagination.offset, 20)

    def test_create_pagination_invalid_limit(self):
        with self.assertRaises(BizException) as context:
            self.factory._create_pagination(-1, 10)
        self.assertEqual(context.exception.code, ErrorCode.InvalidParameter)
        self.assertEqual(context.exception.message, PaginationFactory.ERROR_MESSAGE_INVALID_LIMIT)

    def test_create_pagination_invalid_offset(self):
        with self.assertRaises(BizException) as context:
            self.factory._create_pagination(10, -1)
        self.assertEqual(context.exception.code, ErrorCode.InvalidParameter)
        self.assertEqual(context.exception.message, PaginationFactory.ERROR_MESSAGE_INVALID_OFFSET)


if __name__ == '__main__':
    unittest.main()
