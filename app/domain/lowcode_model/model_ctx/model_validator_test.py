import unittest
from app.domain.lowcode_model.model_ctx.column import SchemaColumn, ColumnType, ColumnFormat
from app.domain.lowcode_model.model_ctx.model_validator import ShortTextValidator, ColumnValidatorFactory, \
    LongTextValidator


class TestColumnValidators(unittest.TestCase):

    def setUp(self):
        self.factory = ColumnValidatorFactory()

    def create_column(self, field, type, format_v, max_length):
        return SchemaColumn(key=field, json_val={"type": type, "maxLength": max_length, "format": format_v.value})

    def test_short_text_validator(self):
        validator = self.factory.create_validator(ColumnFormat.SHORT_TEXT)
        self.assertIsInstance(validator, ShortTextValidator)

        column = self.create_column("test", "string", ColumnFormat.SHORT_TEXT, 256)
        is_valid, msg = validator.validate_and_fill(column)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")

        column = self.create_column("test", "number", ColumnFormat.SHORT_TEXT, 256)
        is_valid, msg = validator.validate_and_fill(column)
        self.assertFalse(is_valid)
        self.assertEqual(msg, f"{ColumnFormat.SHORT_TEXT.value} must be a string type")

        column = self.create_column("test", "string", ColumnFormat.SHORT_TEXT, None)
        is_valid, msg = validator.validate_and_fill(column)
        self.assertTrue(is_valid)

        column = self.create_column("test", "string", ColumnFormat.SHORT_TEXT, 512)
        is_valid, msg = validator.validate_and_fill(column)
        self.assertFalse(is_valid)
        self.assertEqual(msg, f"{ColumnFormat.SHORT_TEXT.value} maxLength must be <= 256")

    def test_long_text_validator(self):
        validator = self.factory.create_validator(ColumnFormat.LONG_TEXT)
        self.assertIsInstance(validator, LongTextValidator)

        column = SchemaColumn(key="test", json_val={
            "type": "string",
            "format": "xLongText",
            "maxLength": 64 * 1024
        })
        is_valid, msg = validator.validate_and_fill(column)
        print(msg)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")

        column = SchemaColumn(key="test", json_val={
            "type": "number",
            "format": "xLongText",
            "maxLength": 64 * 1024
        })
        is_valid, msg = validator.validate_and_fill(column)
        self.assertFalse(is_valid)
        self.assertEqual(msg, f"{ColumnFormat.LONG_TEXT.value} must be a string type")

        column = SchemaColumn(key="test", json_val={
            "type": "string",
            "format": "xLongText",
            "maxLength": None
        })
        is_valid, msg = validator.validate_and_fill(column)
        self.assertTrue(is_valid)

        column = SchemaColumn(key="test", json_val={
            "type": "string",
            "format": "xLongText",
            "maxLength": 64 * 1024 + 1
        })
        is_valid, msg = validator.validate_and_fill(column)
        self.assertFalse(is_valid)
        self.assertEqual(msg, f"{ColumnFormat.LONG_TEXT.value} maxLength must be <= 65536")


if __name__ == '__main__':
    unittest.main()
