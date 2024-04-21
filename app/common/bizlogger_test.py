import threading
import unittest

from app.common.bizlogger import LOGGER, init_logger
from app.common.thread_local_utils import BIZ_CONTEXT


class TestBizLogger(unittest.TestCase):
    def setUp(self):
        init_logger()

    def test_bizlogger(self):

        def worker():
            BIZ_CONTEXT.set_attr("request_id", "123")
            LOGGER.info("Hello, world!", extra={"n1221ame": "app", "level": "info"})
            # 预期request_id = 123

        def worker2():
            LOGGER.info("Hello, world!", extra={"n1221ame": "app", "level": "info"})
            # 预期request_id = ""

        threading.Thread(target=worker).start()
        threading.Thread(target=worker2).start()

    def test_log_json(self):
        LOGGER.info("hello %s", "world")