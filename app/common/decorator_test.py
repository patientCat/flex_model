import unittest

from app.common.decorator import to_string


class TestToString(unittest.TestCase):

    def test_to_string(self):
        @to_string
        class TestClass:
            def __init__(self, a, b):
                self.a = a
                self.b = b

        test_obj = TestClass(1, "test")
        print(test_obj)

        @to_string
        class TestClass2:
            def __init__(self, a, b):
                self.a = a
                self.b = b

        test_obj2 = TestClass2(1, TestClass(1, 2))
        print(test_obj2)


if __name__ == '__main__':
    unittest.main()
