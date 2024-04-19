import unittest

from app.common.error import BizException
from field import ColumnFormat, ColumnType, SchemaColumn


class TestSchemaColumn(unittest.TestCase):

    def test_name(self):
        column = SchemaColumn("test_key", {})
        self.assertEqual(column.name, "test_key")

    def test_format(self):
        column = SchemaColumn("test_key", {"format": "xShortText"})
        self.assertEqual(column.format, ColumnFormat.SHORT_TEXT)

        column = SchemaColumn("test_key", {"format": "xLongText"})
        self.assertEqual(column.format, ColumnFormat.LONG_TEXT)

        column = SchemaColumn("test_key", {"format": "xNumber"})
        self.assertEqual(column.format, ColumnFormat.NUMBER)

        column = SchemaColumn("test_key", {"format": "xJson"})
        self.assertEqual(column.format, ColumnFormat.JSON)

        column = SchemaColumn("test_key", {"format": "xManyToOne"})
        self.assertEqual(column.format, ColumnFormat.MANY_TO_ONE)

        column = SchemaColumn("test_key", {"format": "xOneToMany"})
        self.assertEqual(column.format, ColumnFormat.ONE_TO_MANY)

        column = SchemaColumn("test_key", {"format": "xManyToMany"})
        self.assertEqual(column.format, ColumnFormat.MANY_TO_MANY)
        # Add more tests for other formats

    def test_not_exist_format(self):
        column = SchemaColumn("test_key", {"format": "x-unknown"})
        with self.assertRaises(BizException):
            print(column.format)

    def test_type(self):
        column = SchemaColumn("test_key", {"type": "number"})
        self.assertEqual(column.type, ColumnType.NUMBER)

        column = SchemaColumn("test_key", {"type": "string"})
        self.assertEqual(column.type, ColumnType.STRING)

        column = SchemaColumn("test_key", {"type": "boolean"})
        self.assertEqual(column.type, ColumnType.BOOL)

        column = SchemaColumn("test_key", {"type": "object"})
        self.assertEqual(column.type, ColumnType.OBJECT)

        column = SchemaColumn("test_key", {"type": "array"})
        self.assertEqual(column.type, ColumnType.ARRAY)
        # Add more tests for other types

    def test_is_relation(self):
        column = SchemaColumn("test_key", {"type": "number", "format": "xOneToMany"})
        self.assertTrue(column.is_relation())


if __name__ == '__main__':
    unittest.main()
