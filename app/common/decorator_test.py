import unittest

from app.common.decorator import readable


class TestToString(unittest.TestCase):

    def test_to_string(self):
        @readable
        class TestClass:
            def __init__(self, a, b):
                self.a = a
                self.b = b

        test_obj = TestClass(1, "autotest")
        print(test_obj)

        @readable
        class TestClass2:
            def __init__(self, a, b):
                self.a = a
                self.b = b

        test_obj2 = TestClass2(1, TestClass(1, 2))
        print(test_obj2)


if __name__ == '__main__':
    unittest.main()
