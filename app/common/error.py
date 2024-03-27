class BizException(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message


class Error:
    def __init__(self):
        self.message = None
        self.code = None

    def to_dict(self):
        return {
            "message": self.message,
            "code": self.code
        }
