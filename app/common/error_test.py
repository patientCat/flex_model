import unittest
from enum import Enum

from app.common.error import ErrorCode, BizException, Error


class TestErrorCode(unittest.TestCase):
    def test_error_code(self):
        self.assertEqual(ErrorCode.InternalError.value, "InternalError")
        self.assertEqual(ErrorCode.InvalidParameter.value, "InvalidParameter")


class TestBizException(unittest.TestCase):
    def test_biz_exception(self):
        try:
            raise BizException(ErrorCode.InternalError, "An internal error occurred")
        except BizException as e:
            self.assertEqual(e.code, ErrorCode.InternalError)
            self.assertEqual(e.message, "An internal error occurred")


class TestError(unittest.TestCase):
    def test_error(self):
        error = Error("Invalid parameter", "InvalidParameter")
        self.assertEqual(error.message, "Invalid parameter")
        self.assertEqual(error.code, "InvalidParameter")
        self.assertEqual(error.dict_msg(), {
            "Error": {
                "Message": "Invalid parameter",
                "Code": "InvalidParameter"
            }
        })


if __name__ == '__main__':
    unittest.main()
