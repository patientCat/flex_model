import unittest
from app.common.error import Error, ErrorCode
from app.model.param import find, test_response
from biz_response import BizResponse, dict_response


class TestBizResponse(unittest.TestCase):

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
