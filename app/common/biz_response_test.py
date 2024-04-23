import unittest

from app.common.bizlogger import LogKey
from app.common.error import Error, ErrorCode
from app.common.param import test_response
from app.common.thread_local_utils import BIZ_CONTEXT
from biz_response import BizResponse


class TestBizResponse(unittest.TestCase):
    def setUp(self) -> None:
        BIZ_CONTEXT.set_attr(LogKey.request_id, "request_id")

    def test_success(self):
        message = test_response.TestResponse(name="John Doe", age=10)
        res = BizResponse.success(message)
        self.assertEqual(res.status, 200)
        self.assertEqual(res.message, message)

    def test_fail(self):
        error = Error("Error message", ErrorCode.InvalidParameter.value)
        res = BizResponse.fail(error)
        self.assertEqual(res.status, 400)
        self.assertEqual(res.message, error)
        print(res.dict_msg())
        self.assertTrue('Response' in res.dict_msg())

    def test_dict_msg(self):
        response = test_response.TestResponse(name="John Doe", age=10)
        res = BizResponse.success(response)
        self.assertEqual(res.status, 200)
        print(res.dict_msg())
        self.assertTrue('Response' in res.dict_msg())


if __name__ == "__main__":
    unittest.main()
