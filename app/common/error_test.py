import unittest

from app.common.error import *


class TestErrorCode(unittest.TestCase):
    def test_error_code(self):
        self.assertEqual(ErrorCode.InternalError.value, "InternalError")
        self.assertEqual(ErrorCode.InvalidParameter.value, "InvalidParameter")


class TestBizException(unittest.TestCase):
    def test_biz_exception(self):
        try:
            raise BizException(ErrorCode.InternalError, "An internal error occurred")
        except BizException as e:
            self.assertEqual(e.code, ErrorCode.InternalError.value)
            self.assertEqual(e.message, "An internal error occurred")

    def test_replace_holder(self):
        msg = replace_placeholders('{0}, {1}', 'hello', 'world')
        print(msg)

    def test_ez_error_code_exception(self):
        try:
            raise BizException(ezcode=EzErrorCodeEnum.InvalidKeyNotFound, arg_list=["hello", "world"])
        except BizException as e:
            print(e.message)
            print(e.code)
            self.assertTrue(e.code == ErrorCode.InvalidParameter.value)


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
