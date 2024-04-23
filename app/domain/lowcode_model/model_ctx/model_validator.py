from abc import abstractmethod

from app.domain.lowcode_model.model_ctx.column import SchemaColumn, ColumnType, ColumnFormat


class ColumnValidator:
    @abstractmethod
    def validate(self, column: SchemaColumn) -> (bool, str):
        pass


class ShortTextValidator(ColumnValidator):
    def validate(self, column: SchemaColumn) -> (bool, str):
        if column.format != ColumnFormat.SHORT_TEXT.value:
            return False, f"format {column.format} must be {ColumnFormat.SHORT_TEXT.value}"
        if column.type != ColumnType.STRING:
            return False, f"{column.format} must be a string type"
        json_val = column.json_val
        print(json_val)
        max_length: int = json_val.get("maxLength")
        if max_length is None:
            return False, f"{column.format} maxLength must be defined"
        max_limit = 256
        if max_length > max_limit:
            return False, f"{column.format} maxLength must be <= {max_limit}"
        return True, ""


class LongTextValidator(ColumnValidator):
    def validate(self, column: SchemaColumn):
        if column.format != ColumnFormat.LONG_TEXT.value:
            return False, f"format {column.format} must be LONG_TEXT"
        if column.type != ColumnType.STRING:
            return False, f"{column.format} must be a string type"
        json_val = column.json_val
        max_length: int = json_val.get("maxLength")
        if max_length is None:
            return False, f"{column.format} maxLength must be defined"
        max_limit = 64 * 1024
        if max_length > max_limit:
            return False, f"{column.format} maxLength must be <= {max_limit}"
        return True, ""


class ColumnValidatorFactory:
    def __init__(self):
        self.__validator_dict = {
            ColumnFormat.SHORT_TEXT: ShortTextValidator(),
            ColumnFormat.LONG_TEXT: LongTextValidator(),
        }

    def create_validator(self, column_format: ColumnFormat):
        return self.__validator_dict.get(column_format)
