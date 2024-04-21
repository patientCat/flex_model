import threading
import unittest
from typing import Any

from app.common.thread_local_utils import BIZ_CONTEXT


class TestThreadLocalContext(unittest.TestCase):
    def test_get_context(self):
        context = BIZ_CONTEXT.get_context()
        self.assertIsInstance(context, dict)

    def test_get_attr(self):
        BIZ_CONTEXT.set_attr("test_attr", "test_value")
        attr_value = BIZ_CONTEXT.get_attr("test_attr")
        self.assertEqual(attr_value, "test_value")

    def test_get_attr_and_set(self):
        attr_value = BIZ_CONTEXT.get_attr_and_set("test_attr2", "test_value2")
        self.assertEqual(attr_value, "test_value2")
        attr_value = BIZ_CONTEXT.get_attr("test_attr2")
        self.assertEqual(attr_value, "test_value2")

    def test_set_attr(self):
        BIZ_CONTEXT.set_attr("test_attr3", "test_value3")
        attr_value = BIZ_CONTEXT.get_attr("test_attr3")
        self.assertEqual(attr_value, "test_value3")

    def test_thread_local(self):
        def set_and_get_in_thread(attr: str, value: Any, result: list):
            BIZ_CONTEXT.set_attr(attr, value)
            result.append(BIZ_CONTEXT.get_attr(attr))

        result1 = []
        result2 = []
        t1 = threading.Thread(target=set_and_get_in_thread, args=("thread_attr", "value1", result1))
        t2 = threading.Thread(target=set_and_get_in_thread, args=("thread_attr", "value2", result2))

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.assertEqual(result1[0], "value1")
        self.assertEqual(result2[0], "value2")

if __name__ == "__main__":
    unittest.main()