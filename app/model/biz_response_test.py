import unittest
from app.common.error import Error, ErrorCode
from app.model.param import find
from biz_response import BizResponse, dict_response


class TestBizResponse(unittest.TestCase):

    def test_success(self):
        message = "Successful operation"
        res = BizResponse.success(message)
        self.assertEqual(res.status, 200)
        self.assertEqual(res.message, message)

    def test_fail(self):
        error = Error("Error message", ErrorCode.InvalidParameter.value)
        res = BizResponse.fail(error)
        self.assertEqual(res.status, 400)
        self.assertEqual(res.message, error)

    def test_dict_msg(self):
        response = find.FindOneResponse(record={'x': 1}, total=10)
        res = BizResponse.success(response)
        res_dict = res.dict_msg()
        self.assertEqual(res.status, 200)


if __name__ == "__main__":
    unittest.main()
