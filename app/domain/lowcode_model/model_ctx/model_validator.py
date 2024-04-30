from abc import abstractmethod

from app.domain.lowcode_model.model_ctx.column import SchemaColumn, ColumnType, ColumnFormat, RelationInfo


class ColumnValidator:
    def validate_and_fill(self, column: SchemaColumn) -> (bool, str):
        right_format: ColumnFormat = self.get_right_format()
        if column.column_format != right_format:
            return False, f"format {column.column_format.value} must be {right_format.value}"
        return self.do_validate_and_fill(column, right_format)

    @abstractmethod
    def do_validate_and_fill(self, column: SchemaColumn, curr_format: ColumnFormat) -> (bool, str):
        pass

    @abstractmethod
    def get_right_format(self) -> ColumnFormat:
        pass


class ShortTextValidator(ColumnValidator):
    def get_right_format(self) -> ColumnFormat:
        return ColumnFormat.SHORT_TEXT

    def do_validate_and_fill(self, column: SchemaColumn, curr_format: ColumnFormat) -> (bool, str):
        if column.column_type != ColumnType.STRING:
            return False, f"{curr_format.value} must be a string type"
        max_length: int = column.get_attr("maxLength")
        max_limit = 256
        if max_length is not None:
            if max_length > max_limit:
                return False, f"{curr_format.value} maxLength must be <= {max_limit}"
        else:
            column.set_attr("maxLength", max_limit)
        return True, ""


class LongTextValidator(ColumnValidator):
    def get_right_format(self) -> ColumnFormat:
        return ColumnFormat.LONG_TEXT

    def do_validate_and_fill(self, column: SchemaColumn, curr_format: ColumnFormat) -> (bool, str):
        if column.column_type != ColumnType.STRING:
            return False, f"{curr_format.value} must be a string type"
        max_length: int = column.get_attr("maxLength")
        max_limit = 64 * 1024
        if max_length is not None:
            if max_length > max_limit:
                return False, f"{curr_format.value} maxLength must be <= {max_limit}"
        else:
            column.set_attr("maxLength", max_limit)
        return True, ""


class NumberValidator(ColumnValidator):
    def get_right_format(self) -> ColumnFormat:
        return ColumnFormat.NUMBER

    def do_validate_and_fill(self, column: SchemaColumn, curr_format: ColumnFormat):
        if column.column_type != ColumnType.NUMBER:
            return False, f"{curr_format.value} must be a number type"
        return True, ""


class TimestampValidator(ColumnValidator):
    def get_right_format(self) -> ColumnFormat:
        return ColumnFormat.TIMESTAMP

    def do_validate_and_fill(self, column: SchemaColumn, curr_format: ColumnFormat):
        if column.column_type != ColumnType.NUMBER:
            return False, f"{curr_format.value} must be a number type"
        minimum: int = column.get_attr("minimum")
        min_limit = 0
        if minimum is not None:
            if minimum < min_limit:
                return False, f"{curr_format.value} must be greater than {min_limit}"
        else:
            column.set_attr("minimum", min_limit)
        return True, ""


class EmailValidator(ColumnValidator):
    def get_right_format(self) -> ColumnFormat:
        return ColumnFormat.EMAIL

    def do_validate_and_fill(self, column: SchemaColumn, curr_format: ColumnFormat):
        if column.column_type != ColumnType.STRING:
            return False, f"{curr_format.value} must be a string type"
        return True, ""


def check_relation(relation: RelationInfo, curr_format: ColumnFormat):
    if relation is None:
        return False, f"{curr_format.value} must has 'xRelation' attr"
    if "field" not in relation:
        return False, f"{curr_format.value} 'xRelation' must have 'field' attr"
    if "relatedField" not in relation:
        return False, f"{curr_format.value} 'xRelation' must have 'relatedField' attr"
    if "relatedModelName" not in relation:
        return False, f"{curr_format.value} 'xRelation' must have 'relatedModelName' attr"
    return True, ""


class ManyToOneValidator(ColumnValidator):
    def get_right_format(self) -> ColumnFormat:
        return ColumnFormat.MANY_TO_ONE

    def do_validate_and_fill(self, column: SchemaColumn, curr_format: ColumnFormat):
        if column.column_type != ColumnType.OBJECT:
            return False, f"{curr_format.value} must be a object type"
        relation: RelationInfo = column.get_relation()
        is_ok, err = check_relation(relation, curr_format)
        if is_ok is False:
            return False, err
        return True, ""


class OneToManyValidator(ColumnValidator):
    def get_right_format(self) -> ColumnFormat:
        return ColumnFormat.ONE_TO_MANY

    def do_validate_and_fill(self, column: SchemaColumn, curr_format: ColumnFormat):
        if column.column_type != ColumnType.OBJECT:
            return False, f"{curr_format.value} must be a object type"
        relation: RelationInfo = column.get_relation()
        is_ok, err = check_relation(relation, curr_format)
        if is_ok is False:
            return False, err
        return True, ""


class ColumnValidatorFactory:
    def __init__(self):
        self.__validator_dict = {
            ColumnFormat.SHORT_TEXT: ShortTextValidator(),
            ColumnFormat.LONG_TEXT: LongTextValidator(),
            ColumnFormat.NUMBER: NumberValidator(),
            ColumnFormat.TIMESTAMP: TimestampValidator(),
            ColumnFormat.MANY_TO_ONE: ManyToOneValidator(),
            ColumnFormat.ONE_TO_MANY: OneToManyValidator(),
            ColumnFormat.EMAIL: EmailValidator(),
        }

    def create_validator(self, column_format: ColumnFormat):
        return self.__validator_dict.get(column_format)
