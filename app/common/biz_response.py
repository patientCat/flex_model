from app.common.bizlogger import LogKey
from app.common.error import Error
from app.common.thread_local_utils import BIZ_CONTEXT


class BizResponse:
    def __init__(self):
        self.status = 200
        self.message = None
        self.header = None
        pass

    @staticmethod
    def success(response) -> "BizResponse":
        resmsg = BizResponse()
        resmsg.message = response
        resmsg.status = 200
        return resmsg

    @staticmethod
    def fail(error: Error) -> "BizResponse":
        resmsg = BizResponse()
        resmsg.message = error
        resmsg.status = 400
        return resmsg

    def dict_msg(self):
        return {
            "RequestId": BIZ_CONTEXT.get_attr(LogKey.request_id),
            "Response": self.message.dict_msg()
        }


def dict_response(cls):
    def dict_msg(self):
        return {key: value for key, value in self.__dict__.items()}

    cls.dict_msg = dict_msg
    return cls
